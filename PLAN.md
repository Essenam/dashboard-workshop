# Dashboard plan

This is the plan for your dashboard. Fill it in with Claude **before** any code is written,
one section at a time, in plain words. Keep every answer short: a line or two is plenty.
When something changes, change it here first, then build.

Why bother: a dashboard built without a plan is the "vibecoded" kind. It looks finished, nobody
can say whether it is right, and nobody knows what to fix when it breaks. Ten minutes here saves
an afternoon later.

The order follows the engineering process: requirements, a plan with success criteria, build,
test and verify, then maintain.

---

## 1. Who it is for

Name one real person, not "users". Then work backwards from what they are trying to do.
The `jobs-quote-ux` skill is the standard for this section.

- **The person:** _who opens this dashboard? (role, team)_
- **What they are trying to do:** _in their words, not the system's_
- **How often they look:** _daily, weekly, before a meeting_
- **What they do today instead:** _the spreadsheet, the email, the report someone rebuilds by hand_

## 2. The questions it answers

Three to five questions. If a chart does not answer one of these, it does not belong.

| # | Question the person asks | How they will know the answer at a glance |
|---|---|---|
| 1 | _e.g. Are trips up or down this month?_ | _one number with the change from last month_ |
| 2 | | |
| 3 | | |

## 3. The data

| Source | How we connect | Key needed? | How fresh | Size |
|---|---|---|---|---|
| _e.g. NYC TLC monthly summaries_ | _file, API, database_ | _yes or no_ | _monthly, daily, live_ | _rows or MB_ |

- **Where the key lives:** _locally in `.env` (git ignores it); on the host in an environment
  variable. Never in code, never in git, never in the browser._
- **Sensitive fields:** _names, emails, IDs, anything personal? If yes, say how they stay out of
  the dashboard._
- **Limits:** _rate limits, file size, anything the source will block us for_

## 4. Data quality checks

Pick the dimensions that matter from [`docs/data-quality-dimensions.md`](docs/data-quality-dimensions.md).
The `/analyze-data-quality` skill walks through this step.

| Dimension | The rule, in plain words | Where it shows on the dashboard |
|---|---|---|
| _e.g. Completeness_ | _every trip has a pickup zone_ | _a score tile plus the failing rows in a table_ |
| | | |

## 5. What is on screen

Sketch it in words. Top to bottom, the way the person reads it.

- **Headline numbers (KPIs):** _the two to four numbers that answer the questions above_
- **Charts:** _one line per chart: what it shows, and which question it answers_
- **Drill-down table:** _what a row is, and which columns_
- **Filters:** _date range, category; only the ones the person will use_
- **Style:** _the default in `design-system/`, or your company's own colors and logo_

## 6. Success criteria

How we will know it is done and right. Each one is something we can check, not a feeling.

- [ ] Every question in section 2 is answered on screen
- [ ] The headline numbers match the source (spot-check two of them by hand)
- [ ] Every quality check in section 4 runs and shows its result
- [ ] Looked at on the live dev site, at the size the person will use it, and it is both correct and pleasing
- [ ] A pass against the ten usability heuristics, with nothing serious left open
- [ ] The security review below passes
- [ ] _add your own_

## 7. Build steps

Small steps, each one something you can see change on screen. Commit and push after each one.

1. _e.g. Load the data and show the row count on the page_
2. _e.g. The first headline number_
3. _e.g. The first chart_
4. _e.g. The quality scores_
5. _e.g. The drill-down table_

## 8. Test and verify

- **Look at it.** Open the live dev site and look at every view, the way the person will. Reading
  the code is not checking. The `closed-loop-visual-feedback` skill covers how.
- **Check the numbers.** Compare the headline numbers against the source.
- **Usability.** Run the `ux-heuristics` skill (Nielsen's ten heuristics) and fix anything serious.
- **Security review.** Ask Claude to review the project as an attacker would, then fix what it finds:
  - [ ] No key or password anywhere in the code or the git history
  - [ ] The browser never receives a key; anything that needs one runs on the server side
  - [ ] Nothing personal or sensitive is sent to the page
  - [ ] Dependencies checked for known problems (`npm audit`)
  - [ ] Who can open the dashboard is a decision you made, not an accident

## 9. Ship

- **Dev site (test copy):** _URL_
- **Prod site (the real one):** _URL_
- Work goes to `dev` first. It moves to `prod` only when you say so.

## 10. Maintain

- **Owner:** _who keeps it running_
- **Data refresh:** _how new data arrives, and how often_
- **What breaks first:** _e.g. the source changes a column name, or a key expires_
- **How to undo a bad change:** ask Claude to restore the dashboard to an earlier commit (for
  example, "the one from an hour ago"). Every change is saved on GitHub.

## 11. Decisions and open questions

Write down what you decided and why, so nobody has to decide it twice.

- _2026-10-07: chose X over Y because..._
- **Open:** _anything still undecided_
