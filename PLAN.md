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

## Who it is for

Name one real person, not "users". Then work backwards from what they are trying to do.
The `jobs-quote-ux` skill is the standard for this section.

- **The person:** the COO of a ride-hail operation in New York City, who runs day-to-day
  operations. (First imagined as a retail COO; the workshop data is NYC ride-hail trips, so the
  role moved to fit it. The same design can later carry real retail data.)
- **What they are trying to do:** "Show me what is going on, where the pain points are, and
  where my attention is needed. Then let me drill down into the detail."
- **How often they look:** three times a day. They also want alerts when a number crosses a
  threshold they set, so they do not have to keep checking.
- **What they do today instead:** spreadsheets and emails.

## The questions it answers

Three to five questions. If a chart does not answer one of these, it does not belong.

| # | Question the person asks | How they will know the answer at a glance |
|---|---|---|
| 1 | Are trips and revenue on track? | Trips and rider fares for the latest day, week and month, each with the change from the period before |
| 2 | Where and when are riders waiting too long? | Typical wait from request to pickup, with the zones and hours past my threshold ranked first; click a zone for its detail |
| 3 | Are drivers getting a fair share of what riders pay? | Driver pay as a share of the fare, by company, with the trend over the year |
| 4 | Where does something look wrong today? | An attention list: anything past a threshold (volume drop, long waits, pay share, bad data), with the reason |
| 5 | Can I trust these numbers? | One data quality score per check, with the failing rows a click away |

The data runs September 2025 to August 2026, so "today" means the latest day in the data.

## Data quality checks

Pick the dimensions that matter from the framework you use. If you have none, tell Claude to
use the data quality dimensions in the DAMA-DMBOK. The `/analyze-data-quality` skill walks
through this step.

| Dimension | The rule, in plain words | Where it shows on the dashboard |
|---|---|---|
| Completeness | Key fields are filled in: zones, times, fare, driver pay, driver arrival time | Score tile, failing rows a click away |
| Validity | Values are possible: no negative fares or miles, zones exist in the lookup, dropoff after pickup | Score tile, failing rows a click away |
| Accuracy | Values are believable: speed under about 80 mph, no zero-mile trips with big fares, pay not far above fare | Score tile, failing rows a click away |
| Consistency | Fields agree: trip time matches dropoff minus pickup; request, arrival and pickup run in order | Score tile, failing rows a click away |
| Timeliness | Each month's file holds only that month's trips | Score tile, failing rows a click away |
| Uniqueness | No trip appears twice (rows identical in every field) | Score tile, failing rows a click away |

Framework: DAMA-DMBOK dimensions. The exact rules are written after profiling the data. Each
check's score also shows beside the numbers it affects (for example, wait times beside the
time checks).

## What is on screen

Four pages, each answering named questions. "Today" is the latest day in the data.

- **Today** (questions 1 and 4). Headline tiles: trips, rider fares, typical wait, driver pay
  share, each against the same day last week, with the week and month beside it. Below them
  the attention list: everything past a threshold, worst first, with the reason and a link to
  the detail. Then the daily trend for the year. A slim strip shows the data quality score.
- **Wait times** (question 2). Zones ranked by typical wait, those past the threshold first.
  A day by hour grid shows when waits run long. Choosing a zone drills down to its weekly trend
  and its hours.
- **Driver pay** (question 3). Driver pay share by company, month by month, with the share of
  trips where pay was above what the rider paid (rule ACC-04) beside it.
- **Data quality** (question 5). Headline: rows checked, rules, overall pass rate. A score per
  DMBOK dimension. A card per rule: the plain test, count and rate, the trend by month, an
  example row, what the finding means, and the SQL.

Thresholds (long wait, volume drop, pay share, data quality) live in one settings file and
can be adjusted on the Today page. Alerts that reach the COO when a threshold is crossed are a
separate scheduled job, planned after the dashboard works.

## Success criteria

How we will know it is done and right. Each one is something we can check, not a feeling.

- [x] Every question in "The questions it answers" is answered on screen
- [x] The headline numbers match the source (spot-checked against the raw August file: 587,408 trips and
  $15.7M fares on 31 August, Uber pay share 78.2% for August; all match the screen)
- [x] Every check in "Data quality checks" runs and shows its result (17 rules, every row)
- [ ] Looked at on the live dev site, at the size the person will use it, and it is both correct and pleasing
  (checked locally at desktop and phone width, light and dark; waiting on Netlify for the live site)
- [ ] A pass against the ten usability heuristics, with nothing serious left open
- [ ] The security review under "Test and verify" passes
- [ ] The COO confirms the default alert thresholds (7 min wait, 10% day drop, 25% zone drop, 70% pay share, 1% data defect)

## Test and verify

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

## Hardening (from the security review, October 2026)

Before connecting Netlify:

- [x] Pin every library the pages load to the tested version (htl 1.0.0, d3 7.9.0, Plot 0.6.17).
      A clean build ships only those. d3's own parts (d3-array and so on) still follow d3 7.9.0's
      version ranges; small leftover risk, caught by looking at the dev site before promoting.
- [x] Build on Node 24 everywhere (`.nvmrc`, `netlify.toml`, `engines`); Framework pinned to 1.13.4
- [x] Security headers in `netlify.toml`: content security policy, no framing, nosniff,
      referrer and permissions policies. Tested locally: all four pages render under them.
      Recheck in the browser console on the live dev site after the first deploy.
- [x] `.gitignore` covers local Claude settings, stray data files, partial downloads, logs
- [ ] Owner: decide who can open the site, and record it here
- [ ] Owner: GitHub ruleset blocking deletion and force push on `prod` and `dev`; Dependabot
      alerts and secret scanning on
- [ ] Owner: keep the commit email private

Before shipping `prod`: a summary sanity check and manifest, a GitHub check on every push,
download fingerprints in `fetch.py`, deterministic example rows, a written rollback note.

## Items that will require maintenance

Fill this in as you build: anything that will need attention later, such as a key that
expires or a data source that changes. Include a plan for dependencies that will need to be updated.

- **New months of data (connected to TLC).** `uv run python pipeline/fetch.py` asks TLC which
  monthly files exist, without downloading. `--download` fetches only the months missing from
  `data/raw/`, one file at a time (TLC's server blocks parallel or repeated requests), and saves
  each file's download headers beside it. Then `uv run python pipeline/build_summaries.py`
  (about 8 minutes) and commit `data/summaries/`. The dashboard always covers the latest 12
  months in the cache. Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- **Three looks a day and alerts.** TLC publishes monthly, about two months late, so the data
  cannot refresh three times a day. Real alerts need a live operational feed and a scheduled job
  that checks the thresholds and sends a message. Not built yet.
- **Thresholds** are saved per browser, not shared. If the COO's settings should follow them
  between devices, move them into `src/components/ui.js` defaults or a shared store.
- **Rules not reviewed yet.** 12 of 17 rules still say "not reviewed yet". CON-01 jumped from
  1.1% across the year to 3.0% in August 2026 and should be reviewed first.
- **TLC re-uploads files** without notice. The `.headers.json` files record what each looked
  like when fetched; compare before trusting a re-download.
- **Dependencies.** `npm audit` (October 2026): 0 issues in what ships; 6 (1 low, 5 moderate) in
  build and preview tools (esbuild, sprintf-js) that run only on this laptop. The fix needs a
  downgrade of Observable Framework, so do not run `npm audit fix --force`. The esbuild issue
  cannot be reached through `observable preview`, which listens only on this laptop. Recheck
  with `npm audit` monthly. Library versions the pages load are pinned in the `npm:` imports;
  bump them on purpose and look at the dev site before promoting. Python: `uv lock --upgrade` then rerun the pipeline.
