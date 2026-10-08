---
title: Data quality
---

```js
// Pinned to the tested versions, so a rebuild never pulls a different release.
import * as d3 from "npm:d3@7.9.0";
import * as Plot from "npm:@observablehq/plot@0.6.17";
import {html} from "npm:htl@1.0.0";
import {fmt, token, icon, badge, loadThresholds, monthText} from "./components/ui.js";

const dq = await FileAttachment("data/dq_rules.json").json();
const monthly = (await FileAttachment("data/dq_monthly.csv").csv({typed: true}))
  .map((d) => ({...d, month: monthText(d.month)})).map((d) => ({...d, date: new Date(`${d.month}-01T00:00:00Z`), rate: d.failing / d.rows}));
const zones = await FileAttachment("data/zones.csv").csv({typed: true});
const zoneName = new Map(zones.map((z) => [String(z.zone), z.name]));
const th = loadThresholds();

const kind = (r) => r.meaning.split(":")[0];
const counts = (r) => !["business rule", "documentation gap"].includes(kind(r));
const totalChecks = dq.rows_checked * dq.rules.length;
const failingCounted = d3.sum(dq.rules.filter(counts), (r) => r.failing);
const passRate = 1 - failingCounted / totalChecks;
const passing = dq.rules.filter((r) => r.failing === 0).length;
```

<div class="page-head">
  <div>
    <p class="eyebrow">Question 5</p>
    <h1>Can I trust these numbers?</h1>
    <p class="lede">Every rule runs over every trip, not a sample. The records are submitted by the companies; the city does not verify them, so these checks do.</p>
  </div>
  <span class="as-of">DAMA-DMBOK dimensions</span>
</div>

<div class="grid grid-cols-4">
  <div class="card kpi"><div class="label">Trips checked</div><div class="value">${fmt.compact(dq.rows_checked)}</div><div class="context">${fmt.month(d3.min(monthly, (d) => d.month))} to ${fmt.month(d3.max(monthly, (d) => d.month))}, every row</div></div>
  <div class="card kpi"><div class="label">Rules</div><div class="value">${dq.rules.length}</div><div class="context">${passing} with no failures at all</div></div>
  <div class="card kpi"><div class="label">Overall pass rate</div><div class="value">${fmt.pct(passRate, 2)}</div><div class="context">Of all rule checks, counting defects only</div></div>
  <div class="card kpi"><div class="label">Explained, not errors</div><div class="value">${dq.rules.filter((r) => !counts(r)).length}</div><div class="context">Business rules and documentation gaps</div></div>
</div>

## Score by dimension

```js
const dims = dq.dimensions.map((dim) => {
  const rules = dq.rules.filter((r) => r.dimension === dim);
  const failing = d3.sum(rules.filter(counts), (r) => r.failing);
  return {dim, rules, score: 1 - failing / (dq.rows_checked * rules.length)};
});
const level = (score) => (score >= 0.999 ? "good" : score >= 0.99 ? "warning" : "critical");
```

<div class="grid grid-cols-3">
  ${dims.map((d) => html`<a class="card" href="#${d.rules[0].id}" style="text-decoration:none;color:inherit">
    <div style="display:flex;justify-content:space-between;align-items:center"><strong>${d.dim}</strong>${badge(level(d.score))}</div>
    <div class="score" style="margin-top:8px">${fmt.pct(d.score, 2)}</div>
    <div class="small muted">${d.rules.length} rule${d.rules.length > 1 ? "s" : ""}: ${d.rules.map((r) => r.id).join(", ")}</div>
  </a>`)}
</div>

<p class="small muted">A dimension's score is the share of its rule checks that pass. Rules explained as business rules or documentation gaps are shown but do not lower the score. OK means 99.9% or better, Watch 99% or better.</p>

## Every rule

```js
const filter = view(Inputs.radio(["All", "Failing", "Defects", "Explained"], {label: "Show", value: "All"}));
```

```js
const label = {"defect": "Defect", "business rule": "Business rule", "documentation gap": "Documentation gap", "not reviewed yet": "Not reviewed yet"};
const shown = dq.rules.filter((r) =>
  filter === "All" || (filter === "Failing" && r.failing > 0) || (filter === "Defects" && kind(r) === "defect") || (filter === "Explained" && !counts(r)));

function spark(id) {
  const data = monthly.filter((d) => d.rule === id);
  return Plot.plot({
    width: 260, height: 60, margin: 4, marginLeft: 4, marginBottom: 4,
    x: {type: "utc", axis: null}, y: {axis: null, zero: true},
    marks: [
      Plot.areaY(data, {x: "date", y: "rate", fill: token("--color-accent"), fillOpacity: 0.12}),
      Plot.lineY(data, {x: "date", y: "rate", stroke: token("--color-accent"), strokeWidth: 2}),
      Plot.tip(data, Plot.pointerX({x: "date", y: "rate", title: (d) => `${fmt.month(d.month)}\n${fmt.rate(d.rate)} (${fmt.whole(d.failing)} trips)`}))
    ]
  });
}

function example(row) {
  const names = {PULocationID: "Pickup zone", DOLocationID: "Dropoff zone", request_datetime: "Requested", on_scene_datetime: "Driver arrived",
    pickup_datetime: "Picked up", dropoff_datetime: "Dropped off", trip_miles: "Miles", trip_time: "Trip time (s)",
    base_passenger_fare: "Fare", tips: "Tips", tolls: "Tolls", driver_pay: "Driver pay", company: "Company"};
  return html`<div class="example"><dl>${Object.entries(row).map(([k, v]) => html`<dt>${names[k] ?? k}</dt><dd>${k.endsWith("LocationID") ? `${v} ${zoneName.get(v) ?? ""}` : v}</dd>`)}</dl></div>`;
}

display(html`<div class="grid grid-cols-2">${shown.map((r) => html`<div class="card rule-card" id="${r.id}">
  <header>
    <div><div class="rule-id">${r.id} · ${r.dimension} · ${r.severity} severity</div><h3>${r.name}</h3></div>
    ${r.failing === 0 ? badge("good") : !counts(r) ? badge("info") : badge(r.rate * 100 > th.dqRatePct ? "critical" : "warning")}
  </header>
  <p class="test">${r.test}</p>
  <div style="display:flex;gap:24px;align-items:flex-end;flex-wrap:wrap">
    <div><div class="score">${fmt.rate(r.rate)}</div><div class="small muted">${fmt.whole(r.failing)} failing trip${r.failing === 1 ? "" : "s"}</div></div>
    ${r.failing ? html`<div><div class="small muted">By month</div>${spark(r.id)}</div>` : ""}
  </div>
  <div class="meaning"><strong>${label[kind(r)] ?? kind(r)}.</strong> ${r.meaning.includes(":") ? ((t) => t[0].toUpperCase() + t.slice(1))(r.meaning.split(": ").slice(1).join(": ")) : ""}</div>
  <p class="small muted" style="margin:0">Why it matters: ${r.why}</p>
  ${r.examples.length ? html`<details><summary>An example failing trip</summary>${example(r.examples[0])}</details>` : ""}
  <details><summary>The SQL (true when a trip fails)</summary><pre>${r.fails}</pre></details>
</div>`)}</div>`);
```

<p class="small muted">Example trips contain no rider or driver details; the source data holds none. Counts come from <code>pipeline/build_summaries.py</code>, which reads the raw files and stores only counts, rates and a few examples.</p>
