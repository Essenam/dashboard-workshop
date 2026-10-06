# Workshop dashboard: instructions for Claude

This repo is a participant's copy of an Exagrow workshop starter.

## How to work with this person

- Plan before you build. Before writing any code, fill in [`PLAN.md`](PLAN.md) with the
  person, one section at a time, asking rather than guessing. When the plan changes, update
  `PLAN.md` first. Check the work against its success criteria before calling anything done.

## How this dashboard is built

Use this stack unless the person asks for something else. It is the one the workshop's
reference dashboard uses, so the room can help each other.

- **[Observable Framework](https://observablehq.com/framework/)** builds the site. Pages are
  Markdown files in `src/`, and the result is a plain static site in `dist/`. Charts use
  **Observable Plot**; filters use **Observable Inputs**. Both come with Framework.
- **Python with DuckDB** does the data work, run through **[uv](https://docs.astral.sh/uv/)**.
  Python is for the data pipeline only; the site itself is static.
- **Node.js 20 or newer** is needed. If Node or uv is missing, install it with the person.
- **GitHub** holds the code. **Netlify** hosts it and rebuilds on every push: the `dev`
  branch is the test site and `prod` is the real one.

**How the data flows.** Keep these four steps separate:

1. **Raw data lands in `data/raw/`**, the local cache. It comes from the flash drive or the
   shared folder, or is downloaded once. Git ignores it; never commit it, and never download
   a file that is already there.
2. **The data quality tests run against the row-level files** in the cache, with DuckDB.
   Run every rule over every row, not a sample.
3. **The results are stored as small summary files** in `data/summaries/`: counts, rates, and
   a few example rows per rule. These are committed.
4. **Every page reads the summaries**, through a Framework data loader in `src/data/`. No
   page ever reads the raw rows.

Because the raw files stay in the cache, changing a test means running it again, not
downloading again.

## Look and feel

Follow [`design-system/README.md`](design-system/README.md). Before styling anything, ask
once whether the person has their company's brand guide, colors, fonts, or logo to use in
place of the defaults.

## Writing style: no em dashes

Never use em dashes. Not in chat, code comments, commit messages, page text, chart labels or
documentation. An en dash or a doubled hyphen is not a substitute. Rewrite the sentence with
a full stop, colon, semicolon, comma or parentheses instead. If you find an em dash in a file
you touch, fix it in the same edit.

Why: language models reach for em dashes far more often than people do, so a page full of
them reads as machine written. Ordinary punctuation reads more professionally.

## Branches: `dev` and `prod`

This project has two branches, and each one is a live website:

- **`dev`** is the default branch and where all work happens. Its site is the test copy.
- **`prod`** is the real, shared site. It only ever receives work that already ran on `dev`.

**First-time setup.** If the repo has no `prod` branch yet, create it from `dev` and push it:

```bash
git checkout dev
git branch prod dev
git push -u origin dev
git push -u origin prod
```

**Every change:**

1. Work on `dev`. CRITICAL: DO NOT USE PRs. COMMIT DIRECTLY TO `DEV`. This repo literally only has one person working in it and they are approving what you do by reviewing it as you go. Don't make extra work for them to do PR theater for no one.
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

## Secrets

API keys, tokens and passwords are secrets. Treat every one like a password.

- **Locally** a secret lives in `.env`, which git ignores. Copy `.env.example` to `.env` and
  have the person paste the value in themselves. Do not ask them to paste it into chat, and
  never print it, log it, or echo it back.
- **On a hosting service** it lives in that service's environment variable settings, set by
  the person in its dashboard.
- **Never in code, never in git.**
