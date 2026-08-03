"""gitroast CLI — roasts your git commit history."""

import argparse
import os
import subprocess
import sys

from .roasts import analyze, format_report

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_commit_messages(path, limit=None, author=None):
    cmd = ["git", "-C", path, "log", "--pretty=format:%s"]
    if limit:
        cmd += ["-n", str(limit)]
    if author:
        cmd += ["--author", author]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("Error: git is not installed or not on PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    return [line for line in result.stdout.split("\n") if line.strip()]


def get_repo_name(path):
    try:
        result = subprocess.run(
            ["git", "-C", path, "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        )
        url = result.stdout.strip()
        name = url.rstrip("/").split("/")[-1]
        return name.removesuffix(".git")
    except subprocess.CalledProcessError:
        return os.path.basename(os.path.abspath(path))


def main():
    parser = argparse.ArgumentParser(
        prog="gitroast",
        description="Roasts your git commit history. Run at your own risk.",
    )
    parser.add_argument("path", nargs="?", default=".", help="Path to git repo (default: current directory)")
    parser.add_argument("-n", "--limit", type=int, default=200, help="Number of recent commits to analyze (default: 200)")
    parser.add_argument("--author", default=None, help="Only roast commits by this author")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    args = parser.parse_args()

    if not os.path.isdir(os.path.join(args.path, ".git")):
        print(f"Error: '{args.path}' is not a git repository.", file=sys.stderr)
        sys.exit(1)

    messages = get_commit_messages(args.path, limit=args.limit, author=args.author)

    if not messages:
        print("No commits found. Can't roast an empty repo. (Yet.)")
        sys.exit(0)

    repo_name = get_repo_name(args.path)
    score, roasts, stats = analyze(messages)
    report = format_report(repo_name, len(messages), score, roasts, stats)

    if args.no_color:
        import re
        report = re.sub(r"\033\[[0-9;]*m", "", report)

    print(report)


if __name__ == "__main__":
    main()
