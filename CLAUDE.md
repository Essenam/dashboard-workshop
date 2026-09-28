# Workshop dashboard: instructions for Claude

This repo is a participant's copy of an Exagrow workshop starter. The person you are working
with may never have written code. They steer; you build. Follow every rule below.

## How to work with this person

- Explain what you are about to do in one or two plain sentences before you do it, and what
  you did afterwards. No jargon without a short definition the first time it appears.
- Keep changes small: one visible step at a time, so they can see the dashboard grow and so
  any mistake is easy to undo.
- When something fails, say what failed in plain words and what you will try next.
- Never do anything that costs money or changes an account setting without asking first.

## Writing style: no em dashes

Never use em dashes. Not in chat, code comments, commit messages, page text, chart labels or
documentation. An en dash or a doubled hyphen is not a substitute. Rewrite the sentence with
a full stop, colon, semicolon, comma or parentheses instead. If you find an em dash in a file
you touch, fix it in the same edit.

Why: language models reach for em dashes far more often than people do, so a page full of
them reads as machine written. Ordinary punctuation reads more professionally.

## Branches: `dev` and `prod`

This project has two branches, and each one is a live website:

- **`dev`** is where all work happens. Its site is the test copy.
- **`prod`** is the real, shared site. It only ever receives work that already ran on `dev`.

**First-time setup.** If the repo has no `prod` branch yet, create it from `dev` and push it:

```bash
git checkout dev
git branch prod dev
git push -u origin dev
git push -u origin prod
```

**Every change:**

1. Work on `dev`. No pull requests and no feature branches: commit straight to `dev`.
2. Commit after every change that works, with a short message saying what changed.
3. **Push after every commit**, immediately: `git push origin dev`. The push is the backup.
   Work that exists only on this laptop can be lost; work on GitHub cannot.
4. Read the push output. If it did not say the branch moved, it did not push; fix it before
   doing anything else. Never use `git push -q`, which hides failures.
5. Never force push, and never rewrite history that has been pushed.

**Promoting to `prod`** happens only when the person says so, in so many words ("ship it to
prod", "promote", "publish the real site"). Then:

```bash
git checkout prod
git merge --ff-only dev
git push origin prod
git checkout dev
```

If the fast-forward fails, stop and explain; never merge or reset `prod` to force it. Never
commit to `prod` directly.

## Secrets

API keys, tokens and passwords are secrets. Treat every one like a password.

- **Locally** a secret lives in `.env`, which git ignores. Copy `.env.example` to `.env` and
  have the person paste the value in themselves. Do not ask them to paste it into chat, and
  never print it, log it, or echo it back.
- **On a hosting service** it lives in that service's environment variable settings, set by
  the person in its dashboard.
- **Never in code, never in git, never in the browser.** Anything shipped to the browser can
  be read by anyone who opens the page, so a secret is only ever used by code that runs on a
  server.
- Before every commit, check `git status` and the diff for anything that looks like a secret.
  If one is ever committed or pushed, stop, tell the person plainly, and help them create a
  new one and revoke the old one. Removing it from the latest commit is not enough.
