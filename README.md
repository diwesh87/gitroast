# 🔥 gitroast

**Roasts your git commit history. Run it. Regret it.**
![demo](demo.gif)

`gitroast` scans your commit messages and roasts you for every `fix`, `wip`,
`final_v2_ACTUALLY`, and unhinged all-caps rage-commit hiding in your history.
Then it gives you a Roast Score and a verdict on what kind of developer you
actually are.

```
🔥 gitroast: my-side-project
Analyzed 143 commits...

  › 'fix' appears 9 times in your history. Ctrl+V is doing your job for you.
  › 'final_v2_ACTUALLY' — 'final' is doing a lot of heavy lifting here, and it's lying.
  › 'WHY WONT THIS DEPLOY' — did the keyboard survive this commit?
  › 'asdf' — a commit message so vague it could apply to literally anything you've ever written.

Roast Score: 62/100
🔥 Repeat Offender
Future archaeologists will find your repo and assume it was written during a fire drill.
```

## Install

```bash
pip install gitroast
```

Or run it without installing:

```bash
pipx run gitroast
```

## Usage

```bash
# Roast the repo you're standing in
gitroast

# Roast a specific repo
gitroast ~/code/some-other-project

# Only look at the last 50 commits
gitroast -n 50

# Only roast one author (find out who's really responsible)
gitroast --author "that one teammate"

# No colors, for the emotionally fragile terminal
gitroast --no-color
```

## What gets roasted

- **Lazy messages** — `fix`, `wip`, `stuff`, `.`, `asdf`, and friends
- **The "final" spiral** — `final`, `final v2`, `final_ACTUALLY_final`
- **Duplicate spam** — the same message copy-pasted across a dozen commits
- **Rage commits** — ALL CAPS, frustration, mild swearing
- **Rambling** — commit messages that are secretly small essays
- **The suspiciously clean** — yes, good commits get (grudging) credit too

## Why

Because `git blame` already tells everyone what you did. This tells them
*how you felt about it.*

## Contributing

PRs adding new roast categories, funnier lines, or language support are
very welcome. Keep it clever, not mean — the goal is "friend who teases
you," not "internet troll."

## License

MIT — do whatever you want with it.

---

To know more about the kind of work I do → [diweshsaxena.com](https://diweshsaxena.com)
