---
title: Today
---

```js
// Pinned to the tested versions, so a rebuild never pulls a different release.
import * as d3 from "npm:d3@7.9.0";
import * as Plot from "npm:@observablehq/plot@0.6.17";
import {html} from "npm:htl@1.0.0";
import {fmt, delta, badge, icon, loadThresholds, saveThresholds, DEFAULT_THRESHOLDS, token, monthText} from "./components/ui.js";

const daily = await FileAttachment("data/daily.csv").csv({typed: true});
const zoneWeek = await FileAttachment("data/zone_week.csv").csv({typed: true});
const zones = await FileAttachment("data/zones.csv").csv({typed: true});
const payMonth = (await FileAttachment("data/pay_month.csv").csv({typed: true})).map((d) => ({...d, month: monthText(d.month)}));
const dq = await FileAttachment("data/dq_rules.json").json();
const dqMonthly = (await FileAttachment("data/dq_monthly.csv").csv({typed: true})).map((d) => ({...d, month: monthText(d.month)}));

const zoneName = new Map(zones.map((z) => [z.zone, `${z.name}, ${z.borough}`]));
const DAY = 86400000;

// Citywide totals per day, both companies together. The typical wait is the trip-weighted
// average of each company's median.
const days = d3.rollups(daily, (v) => {
  const waitTrips = d3.sum(v, (d) => d.wait_trips);
  return {
    trips: d3.sum(v, (d) => d.trips),
    fares: d3.sum(v, (d) => d.fares),
    pay: d3.sum(v, (d) => d.driver_pay),
    wait: d3.sum(v, (d) => d.wait_median * d.wait_trips) / waitTrips
  };
}, (d) => +d.date).map(([t, v]) => ({date: new Date(t), ...v})).sort((a, b) => a.date - b.date);

const byTime = new Map(days.map((d) => [+d.date, d]));
const latest = days.at(-1);
const lastWeekSameDay = byTime.get(+latest.date - 7 * DAY);

function windowTotals(endTime, n) {
  const rows = days.filter((d) => +d.date > endTime - n * DAY && +d.date <= endTime);
  return {trips: d3.sum(rows, (d) => d.trips), fares: d3.sum(rows, (d) => d.fares), pay: d3.sum(rows, (d) => d.pay),
    wait: d3.sum(rows, (d) => d.wait * d.trips) / d3.sum(rows, (d) => d.trips)};
}
const w = windowTotals(+latest.date, 7), wPrev = windowTotals(+latest.date - 7 * DAY, 7);
const m = windowTotals(+latest.date, 28), mPrev = windowTotals(+latest.date - 28 * DAY, 28);
```

<div class="page-head">
  <div>
    <p class="eyebrow">Ride-hail operations · New York City</p>
    <h1>Today at a glance</h1>
    <p class="lede">What happened on the latest day in the data, where your attention is needed, and how far to trust it.</p>
  </div>
  <span class="as-of">Latest day: ${fmt.longDay(latest.date)}</span>
</div>

```js
function tile(label, value, now, before, {higherIsBetter = true, week, month, fmtFn}) {
  return html`<div class="card kpi">
    <div class="label">${label}</div>
    <div class="value">${value}</div>
    <div class="context">
      <span>${delta(now, before, {higherIsBetter})} vs. same day last week</span>
    </div>
    <div class="context" style="margin-top:6px">
      <span>7 days: ${fmtFn(week[0])} ${delta(week[0], week[1], {higherIsBetter})}</span>
      <span>28 days: ${fmtFn(month[0])} ${delta(month[0], month[1], {higherIsBetter})}</span>
    </div>
  </div>`;
}
const share = (x) => x.pay / x.fares;
```

<div class="grid grid-cols-4">
  ${tile("Trips", fmt.compact(latest.trips), latest.trips, lastWeekSameDay?.trips, {week: [w.trips, wPrev.trips], month: [m.trips, mPrev.trips], fmtFn: fmt.compact})}
  ${tile("Rider fares", fmt.money(latest.fares), latest.fares, lastWeekSameDay?.fares, {week: [w.fares, wPrev.fares], month: [m.fares, mPrev.fares], fmtFn: fmt.money})}
  ${tile("Typical wait", fmt.minutes(latest.wait), latest.wait, lastWeekSameDay?.wait, {higherIsBetter: false, week: [w.wait, wPrev.wait], month: [m.wait, mPrev.wait], fmtFn: fmt.minutes})}
  ${tile("Driver pay share", fmt.pct(share(latest)), share(latest), share(lastWeekSameDay), {week: [share(w), share(wPrev)], month: [share(m), share(mPrev)], fmtFn: (x) => fmt.pct(x)})}
</div>

```js
// ---- The attention list: everything past a threshold, worst first ----
const th = thresholds;
const items = [];
const add = (level, what, why, href, linkText, score) => items.push({level, what, why, href, linkText, score});

for (const [key, label, fmtFn] of [["trips", "Trips", fmt.compact], ["fares", "Rider fares", fmt.money]]) {
  if (!lastWeekSameDay) break;
  const change = latest[key] / lastWeekSameDay[key] - 1;
  if (change < -th.volumeDropPct / 100) {
    add(change < (-2 * th.volumeDropPct) / 100 ? "critical" : "warning", `${label} down ${fmt.pct(-change)} on the day`,
      `${fmtFn(latest[key])} vs. ${fmtFn(lastWeekSameDay[key])} the same day last week. Threshold: ${th.volumeDropPct}%.`, null, null, 3 + -change);
  }
}
if (latest.wait > th.waitMinutes) {
  add("critical", `Citywide typical wait is ${fmt.minutes(latest.wait)}`, `Above your ${th.waitMinutes} minute threshold.`, "./waits", "See wait times", 4);
}

// Latest complete week (Monday to Sunday) by pickup zone. Unknown zones (264, 265) are left out.
const lastDay = +latest.date;
const fullWeeks = [...new Set(zoneWeek.map((d) => +d.week))].filter((t) => t + 6 * DAY <= lastDay).sort((a, b) => a - b);
const thisWeek = fullWeeks.at(-1);
const priorWeeks = new Set(fullWeeks.slice(-5, -1));
const known = zoneWeek.filter((d) => d.zone < 264);
const weekRows = known.filter((d) => +d.week === thisWeek);
const usual = d3.rollup(known.filter((d) => priorWeeks.has(+d.week)), (v) => d3.mean(v, (d) => d.trips), (d) => d.zone);

weekRows.filter((d) => d.trips >= 500 && d.wait_median > th.waitMinutes)
  .sort((a, b) => b.wait_median - a.wait_median).slice(0, 6)
  .forEach((d) => add(d.wait_median > th.waitMinutes * 1.25 ? "critical" : "warning",
    `Long waits in ${zoneName.get(d.zone)}`,
    `Typical wait ${fmt.minutes(d.wait_median)} last week (1 in 10 riders waited over ${fmt.minutes(d.wait_p90)}), across ${fmt.whole(d.trips)} trips.`,
    `./waits?zone=${d.zone}`, "Drill in", 2 + d.wait_median / th.waitMinutes));

weekRows.map((d) => ({...d, usual: usual.get(d.zone)}))
  .filter((d) => d.usual >= th.zoneMinTrips && d.trips / d.usual - 1 < -th.zoneDropPct / 100)
  .sort((a, b) => a.trips / a.usual - b.trips / b.usual).slice(0, 5)
  .forEach((d) => add("warning", `Fewer trips in ${zoneName.get(d.zone)}`,
    `${fmt.whole(d.trips)} trips last week vs. a usual ${fmt.whole(d.usual)} (down ${fmt.pct(1 - d.trips / d.usual)}).`,
    `./waits?zone=${d.zone}`, "Drill in", 1 + (1 - d.trips / d.usual)));

const lastMonth = d3.max(payMonth, (d) => d.month);
for (const d of payMonth.filter((d) => d.month === lastMonth)) {
  const s = d.driver_pay / d.fares;
  if (s * 100 < th.payShareMin) add("warning", `${d.company} driver pay share is ${fmt.pct(s)}`,
    `In ${fmt.month(lastMonth)}, below your ${th.payShareMin}% threshold.`, "./pay", "See driver pay", 1.5);
}

// Data quality: defects (and unreviewed rules) failing above the threshold in the latest month,
// and any rule whose rate jumped against the months before.
const months = [...new Set(dqMonthly.map((d) => d.month))].sort();
const latestMonth = months.at(-1);
for (const r of dq.rules.filter((r) => !/^(business rule|documentation gap)/.test(r.meaning))) {
  const series = dqMonthly.filter((d) => d.rule === r.id);
  const now = series.find((d) => d.month === latestMonth);
  const rate = now.failing / now.rows;
  const before = d3.mean(series.filter((d) => d.month !== latestMonth), (d) => d.failing / d.rows);
  if (rate * 100 > th.dqRatePct) {
    add("warning", `Data check ${r.id} failing on ${fmt.rate(rate)} of trips`, `${r.name}. ${fmt.month(latestMonth)}, above your ${th.dqRatePct}% threshold.`, `./quality#${r.id}`, "See the check", 1 + rate);
  } else if (now.failing >= 1000 && rate > 2 * before) {
    add("info", `Data check ${r.id} jumped in ${fmt.month(latestMonth)}`, `${r.name}: ${fmt.rate(rate)} of trips vs. ${fmt.rate(before)} on average before.`, `./quality#${r.id}`, "See the check", 0.5);
  }
}
const order = {critical: 0, warning: 1, info: 2};
items.sort((a, b) => order[a.level] - order[b.level] || b.score - a.score);
```

<div class="grid grid-2-1">
  <div class="card">
    <h2>Needs your attention</h2>
    <p class="sub">${items.length ? `${items.length} item${items.length > 1 ? "s" : ""} past your thresholds, worst first. Zones are judged on the week ending ${fmt.day(new Date(thisWeek + 6 * DAY))}.` : "Checked against your thresholds."}</p>
    ${items.length ? html`<ul class="attention">${items.map((d) => html`<li>
      ${badge(d.level)}
      <div><div class="what">${d.what}</div><div class="why">${d.why}</div></div>
      ${d.href ? html`<a class="go" href="${d.href}">${d.linkText} ${icon("arrow-right", 14)}</a>` : html`<span></span>`}
    </li>`)}</ul>` : html`<div class="all-clear">${icon("check-circle", 18)} Nothing is past a threshold.</div>`}
  </div>
  <div class="card">
    <h2>${icon("sliders", 16)} Alert thresholds</h2>
    <p class="sub">Change these and the list updates. Saved in this browser.</p>

```js
const saved = loadThresholds();
const thresholds = view(Inputs.form({
  waitMinutes: Inputs.range([3, 15], {label: "Long wait (min)", step: 0.5, value: saved.waitMinutes}),
  volumeDropPct: Inputs.range([2, 40], {label: "Day drop (%)", step: 1, value: saved.volumeDropPct}),
  zoneDropPct: Inputs.range([5, 60], {label: "Zone drop (%)", step: 1, value: saved.zoneDropPct}),
  zoneMinTrips: Inputs.range([1000, 20000], {label: "Busy zone (trips/wk)", step: 500, value: saved.zoneMinTrips}),
  payShareMin: Inputs.range([50, 90], {label: "Min pay share (%)", step: 1, value: saved.payShareMin}),
  dqRatePct: Inputs.range([0.1, 5], {label: "Data defect (%)", step: 0.1, value: saved.dqRatePct})
}));
```

```js
saveThresholds(thresholds);
const resetButton = Inputs.button("Reset to defaults", {reduce: () => { saveThresholds(DEFAULT_THRESHOLDS); location.reload(); }});
display(resetButton);
```

  </div>
</div>

```js
const passRate = 1 - d3.sum(dq.rules.filter((r) => !/^(business rule|documentation gap)/.test(r.meaning)), (r) => r.failing) / (dq.rows_checked * dq.rules.length);
const waitExcluded = d3.sum(dq.rules.filter((r) => ["CON-02", "CON-03"].includes(r.id)), (r) => r.failing) / dq.rows_checked;
```

<div class="trust">
  ${icon("shield-check", 18)}
  <span><strong>${fmt.pct(passRate, 2)}</strong> of checks pass across <strong>${fmt.compact(dq.rows_checked)}</strong> trips and ${dq.rules.length} rules.</span>
  <span class="muted">Wait times leave out up to ${fmt.pct(waitExcluded)} of trips whose times are out of order.</span>
  <a href="./quality">See data quality ${icon("arrow-right", 13)}</a>
</div>

<div class="card" style="margin-top: 16px">
  <h2>Trips per day</h2>
  <p class="sub">Daily trips across the year, with the 7-day average. Hover for the day.</p>

```js
display(resize((width) => Plot.plot({
  width, height: 280, marginLeft: 48,
  x: {type: "utc", label: null},
  y: {grid: true, label: null, tickFormat: "~s", zero: true},
  marks: [
    Plot.ruleY([0], {stroke: token("--color-border")}),
    Plot.lineY(days, {x: "date", y: "trips", stroke: token("--color-border"), strokeWidth: 1}),
    Plot.lineY(days, Plot.windowY({k: 7, anchor: "end"}, {x: "date", y: "trips", stroke: token("--color-accent"), strokeWidth: 2})),
    Plot.tip(days, Plot.pointerX({x: "date", y: "trips", title: (d) => `${fmt.day(d.date)}\n${fmt.whole(d.trips)} trips\n${fmt.money(d.fares)} fares\nTypical wait ${fmt.minutes(d.wait)}`}))
  ]
})));
```

</div>
