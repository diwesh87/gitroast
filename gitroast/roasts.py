"""Roast logic: detects patterns in commit messages and generates witty commentary."""

import random
import re
from collections import Counter, defaultdict

# ---------- Terminal colors (no external deps) ----------

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"


LAZY_WORDS = {
    "fix", "fixes", "fixed", "fixing", "update", "updates", "updated",
    "change", "changes", "changed", "stuff", "wip", "asdf", "test",
    "testing", "misc", "minor", "small fix", "typo", "oops", "temp",
    "tmp", "cleanup", "clean up", "stuff done", "idk", "whatever",
    "..", "...", ".", "-", "x", "commit", "more changes", "small changes",
}

FINAL_PATTERN = re.compile(r"\bfinal\b", re.IGNORECASE)
FRUSTRATION_WORDS = re.compile(
    r"\b(ugh|why|damn|argh|hate|please|pls|god|omg|wtf|help|kill me|"
    r"i give up|screw it|whatever|seriously|frustrat\w*)\b",
    re.IGNORECASE,
)
SWEAR_ADJACENT = re.compile(r"\b(f+u+c*k*|sh[i1]t|crap|hell)\b", re.IGNORECASE)

LAZY_ROASTS = [
    "'{msg}' — Shakespeare would like a word.",
    "'{msg}'. Groundbreaking. Truly. What did you even change?",
    "'{msg}' — a commit message so vague it could apply to literally anything you've ever written.",
    "'{msg}'. Future you, six months from now, staring at this in `git blame`: 😐",
    "'{msg}' — the commit message equivalent of a shrug emoji.",
    "'{msg}'. Bold of you to assume anyone will remember what this means.",
]

FINAL_ROASTS = [
    "'{msg}' — sir, this is the {count}th 'final'. Nothing about this is final.",
    "'{msg}' — 'final' is doing a lot of heavy lifting here, and it's lying.",
    "'{msg}' — we both know there's a 'final_v2_ACTUALLY' coming.",
]

DUPLICATE_ROASTS = [
    "You used '{msg}' {count} times. Copy-paste is a skill, I guess.",
    "'{msg}' appears {count} times in your history. Ctrl+V is doing your job for you.",
    "{count} commits, all named '{msg}'. Consistency! (Not the good kind.)",
]

FRUSTRATION_ROASTS = [
    "'{msg}' — the emotional damage is visible from here.",
    "'{msg}' — this commit message is a cry for help, and I'm listening.",
    "'{msg}' — you weren't committing code, you were committing a diary entry.",
]

YELLING_ROASTS = [
    "'{msg}' — ALL CAPS. We can feel the rage through the screen.",
    "'{msg}' — did the keyboard survive this commit?",
]

LONG_ROASTS = [
    "A {words}-word commit message. This isn't a commit, it's a memoir.",
    "{words} words in one commit message — somewhere, a PR description is jealous.",
]

GENERIC_PRAISE = [
    "Okay, '{msg}' is actually... fine? Suspicious. Are you feeling alright?",
    "'{msg}' — clear, descriptive, professional. Who are you and what did you do with the real developer?",
]

VERDICTS = [
    (0, 15, "🏆 Certified Clean Coder", "Your commit history is disturbingly professional. Do you even have feelings?"),
    (16, 35, "🙂 Mostly Reasonable Human", "A few slip-ups, but overall you commit like someone who's read a style guide."),
    (36, 60, "😬 Chronically 'fix'-ated", "Your commit history reads like a stress diary. We've all been there."),
    (61, 85, "🔥 Repeat Offender", "Future archaeologists will find your repo and assume it was written during a fire drill."),
    (86, 200, "💀 Certified Chaos Gremlin", "This isn't a commit history, it's a crime scene. 'final_final_v3' should be a war crime."),
]


def is_lazy(msg: str) -> bool:
    norm = msg.strip().lower().rstrip(".")
    return norm in LAZY_WORDS or len(norm) <= 3


def analyze(messages):
    """Takes a list of raw commit message strings, returns (score, roast_lines, stats)."""
    roasts = []
    score = 0
    counts = Counter(m.strip() for m in messages if m.strip())
    stats = defaultdict(int)

    seen_dupe_msgs = set()

    for msg in messages:
        stripped = msg.strip()
        if not stripped:
            continue

        # Duplicates (only roast once per unique duplicated message)
        if counts[stripped] >= 3 and stripped not in seen_dupe_msgs:
            seen_dupe_msgs.add(stripped)
            roasts.append(random.choice(DUPLICATE_ROASTS).format(msg=stripped, count=counts[stripped]))
            score += min(counts[stripped] * 2, 15)
            stats["duplicates"] += 1
            continue
        elif stripped in seen_dupe_msgs:
            continue

        if FINAL_PATTERN.search(stripped):
            roasts.append(random.choice(FINAL_ROASTS).format(msg=stripped, count=stats["final"] + 1))
            score += 6
            stats["final"] += 1
            continue

        if stripped.isupper() and len(stripped) > 4:
            roasts.append(random.choice(YELLING_ROASTS).format(msg=stripped))
            score += 4
            stats["yelling"] += 1
            continue

        if SWEAR_ADJACENT.search(stripped) or FRUSTRATION_WORDS.search(stripped):
            roasts.append(random.choice(FRUSTRATION_ROASTS).format(msg=stripped))
            score += 5
            stats["frustration"] += 1
            continue

        word_count = len(stripped.split())
        if word_count > 25:
            roasts.append(random.choice(LONG_ROASTS).format(words=word_count))
            score += 3
            stats["rambling"] += 1
            continue

        if is_lazy(stripped):
            roasts.append(random.choice(LAZY_ROASTS).format(msg=stripped))
            score += 3
            stats["lazy"] += 1
            continue

        stats["clean"] += 1

    score = min(score, 100)
    return score, roasts, stats


def get_verdict(score):
    for lo, hi, title, desc in VERDICTS:
        if lo <= score <= hi:
            return title, desc
    return VERDICTS[-1][2], VERDICTS[-1][3]


def format_report(repo_name, total_commits, score, roasts, stats):
    lines = []
    lines.append(f"\n{C.BOLD}{C.CYAN}🔥 gitroast: {repo_name}{C.RESET}")
    lines.append(f"{C.DIM}Analyzed {total_commits} commits...{C.RESET}\n")

    if not roasts:
        lines.append(f"{C.GREEN}Nothing to roast. Your commits are suspiciously clean. 🧐{C.RESET}")
    else:
        sample = roasts if len(roasts) <= 12 else random.sample(roasts, 12)
        for r in sample:
            lines.append(f"  {C.YELLOW}›{C.RESET} {r}")

    title, desc = get_verdict(score)
    lines.append(f"\n{C.BOLD}Roast Score: {C.RED}{score}/100{C.RESET}")
    lines.append(f"{C.BOLD}{C.MAGENTA}{title}{C.RESET}")
    lines.append(f"{C.DIM}{desc}{C.RESET}\n")

    return "\n".join(lines)
