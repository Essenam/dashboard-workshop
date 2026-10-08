---
title: Wait times
---

```js
// Pinned to the tested versions, so a rebuild never pulls a different release.
import * as d3 from "npm:d3@7.9.0";
import * as Plot from "npm:@observablehq/plot@0.6.17";
import {html} from "npm:htl@1.0.0";
import {fmt, loadThresholds, token, icon} from "./components/ui.js";

const zoneWeek = await FileAttachment("data/zone_week.csv").csv({typed: true});
const zoneHour = await FileAttachment("data/zone_hour.csv").csv({typed: true});
const weekHour = await FileAttachment("data/week_hour.csv").csv({typed: true});
const zones = await FileAttachment("data/zones.csv").csv({typed: true});
const daily = await FileAttachment("data/daily.csv").csv({typed: true});

const zoneName = new Map(zones.map((z) => [z.zone, z.name]));
const zoneBorough = new Map(zones.map((z) => [z.zone, z.borough]));
const th = loadThresholds();
const DAY = 86400000;

// Judge zones on the last four complete weeks, so one odd day does not decide the ranking.
const lastDay = d3.max(daily, (d) => +d.date);
const fullWeeks = [...new Set(zoneWeek.map((d) => +d.week))].filter((t) => t + 6 * DAY <= lastDay).sort((a, b) => a - b);
const recent = new Set(fullWeeks.slice(-4));
const ranked = d3.rollups(zoneWeek.filter((d) => recent.has(+d.week) && d.zone < 264), (v) => {
  const trips = d3.sum(v, (d) => d.trips);
  return {
    trips,
    wait: d3.sum(v, (d) => d.wait_median * d.trips) / trips,
    p90: d3.sum(v, (d) => d.wait_p90 * d.trips) / trips,
    longShare: d3.sum(v, (d) => d.long_wait_share * d.trips) / trips
  };
}, (d) => d.zone)
  .map(([zone, v]) => ({zone, name: zoneName.get(zone), borough: zoneBorough.get(zone), ...v}))
  .filter((d) => d.trips >= 2000)
  .sort((a, b) => b.wait - a.wait);
const unknownTrips = d3.sum(zoneWeek.filter((d) => recent.has(+d.week) && d.zone >= 264), (d) => d.trips);
const allTrips = d3.sum(zoneWeek.filter((d) => recent.has(+d.week)), (d) => d.trips);
const over = ranked.filter((d) => d.wait > th.waitMinutes);
const maxWait = d3.max(ranked, (d) => d.p90);
const startZone = Number(new URLSearchParams(location.search).get("zone")) || ranked[0].zone;
```

<div class="page-head">
  <div>
    <p class="eyebrow">Question 2</p>
    <h1>Where and when riders wait too long</h1>
    <p class="lede">Wait is the time from booking the ride to being picked up. Zones are ranked over the last four complete weeks.</p>
  </div>
  <span class="as-of">${over.length} of ${ranked.length} zones above ${th.waitMinutes} min</span>
</div>

<div class="grid grid-2-1">
  <div class="card">
    <h2>Zones by typical wait</h2>
    <p class="sub">Pickup zones with at least 2,000 trips in four weeks, longest wait first. A red edge marks a zone past your threshold. Choose a zone to drill in.</p>

```js
const search = view(Inputs.search(ranked, {placeholder: "Find a zone or borough", columns: ["name", "borough"], label: "Search"}));
```

```js
const pick = Mutable(startZone);
const choose = (z) => { pick.value = z; document.getElementById("drill")?.scrollIntoView({behavior: "smooth", block: "start"}); };
```

```js
const shown = search.slice(0, 15);
display(html`<div class="table-wrap"><table class="ranked">
  <thead><tr><th>Zone</th><th class="num">Typical wait</th><th class="hide-sm" style="width:28%"></th><th class="num hide-sm">1 in 10 waits over</th><th class="num">Trips</th></tr></thead>
  <tbody>${shown.map((d) => html`<tr class="${d.wait > th.waitMinutes ? "over" : ""}">
    <td><button class="linklike" onclick=${() => choose(d.zone)}>${d.name}</button><div class="muted">${d.borough}</div></td>
    <td class="num">${fmt.minutes(d.wait)}</td>
    <td class="hide-sm"><div class="bar ${d.wait > th.waitMinutes ? "over" : ""}"><span style="width:${(100 * d.wait) / maxWait}%"></span></div></td>
    <td class="num hide-sm">${fmt.minutes(d.p90)}</td>
    <td class="num">${fmt.compact(d.trips)}</td>
  </tr>`)}</tbody>
</table></div>`);
display(html`<p class="small muted">Showing ${shown.length} of ${search.length}.${unknownTrips / allTrips >= 0.001 ? ` ${fmt.pct(unknownTrips / allTrips)} of trips have an unknown pickup zone (check CMP-01) and cannot be ranked.` : ""}</p>`);
```

  </div>
  <div class="card">
    <h2>When waits run long</h2>
    <p class="sub">Citywide typical wait by day and hour, last four weeks. Darker is longer.</p>

```js
const dows = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
display(resize((width) => Plot.plot({
  width, height: 330, marginLeft: 36, marginBottom: 32, padding: 0.08,
  x: {label: "Hour of day", tickFormat: (h) => (h % 6 === 0 ? `${h}:00` : "")},
  y: {label: null, tickFormat: (d) => dows[d - 1], domain: [1, 2, 3, 4, 5, 6, 7]},
  color: {type: "linear", range: [token("--color-seq-low"), token("--color-seq-high")], label: "Typical wait (min)", legend: true},
  marks: [
    Plot.cell(weekHour, {x: "hour", y: "dow", fill: "wait_median", inset: 0.5, rx: 2}),
    Plot.tip(weekHour, Plot.pointer({x: "hour", y: "dow", title: (d) => `${dows[d.dow - 1]} ${d.hour}:00\nTypical wait ${fmt.minutes(d.wait_median)}\n${fmt.whole(d.trips)} trips`}))
  ]
})));
```

  </div>
</div>

```js
const z = pick;
const zw = zoneWeek.filter((d) => d.zone === z).filter((d) => +d.week + 6 * DAY <= lastDay);
const zh = zoneHour.filter((d) => d.zone === z);
const row = ranked.find((d) => d.zone === z);
```

<div id="drill" class="card" style="margin-top: 16px">
  <p class="eyebrow">Drill-down</p>
  <h2>${zoneName.get(z)}, ${zoneBorough.get(z)}</h2>
  <p class="sub">${row ? html`Typical wait ${fmt.minutes(row.wait)} over four weeks, ${fmt.pct(row.longShare)} of riders waited over 15 minutes, ${fmt.whole(row.trips)} trips.` : "Fewer than 2,000 trips in four weeks, so not ranked."}</p>
  <div class="grid grid-cols-2">
    <div>
      <h3 class="small muted" style="margin:0">Typical wait by week</h3>

```js
display(resize((width) => Plot.plot({
  width, height: 220, marginLeft: 40,
  x: {type: "utc", label: null},
  y: {grid: true, label: "min", zero: true},
  marks: [
    Plot.ruleY([th.waitMinutes], {stroke: token("--color-error"), strokeDasharray: "4 3"}),
    Plot.text([th.waitMinutes], {y: (d) => d, frameAnchor: "right", dy: -7, text: () => "your threshold", fill: token("--color-error"), fontSize: 11}),
    Plot.areaY(zw, {x: "week", y1: "wait_median", y2: "wait_p90", fill: token("--color-accent"), fillOpacity: 0.12}),
    Plot.lineY(zw, {x: "week", y: "wait_median", stroke: token("--color-accent"), strokeWidth: 2}),
    Plot.tip(zw, Plot.pointerX({x: "week", y: "wait_median", title: (d) => `Week of ${fmt.day(d.week)}\nTypical wait ${fmt.minutes(d.wait_median)}\n1 in 10 over ${fmt.minutes(d.wait_p90)}\n${fmt.whole(d.trips)} trips`}))
  ]
})));
```

<p class="small muted">The line is the typical wait; the band reaches up to the wait 1 in 10 riders exceed.</p>
    </div>
    <div>
      <h3 class="small muted" style="margin:0">Typical wait by hour of day, last four weeks</h3>

```js
display(resize((width) => Plot.plot({
  width, height: 220, marginLeft: 40,
  x: {label: "Hour of day", tickFormat: (h) => (h % 3 === 0 ? `${h}` : "")},
  y: {grid: true, label: "min", zero: true},
  marks: [
    Plot.barY(zh, {x: "hour", y: "wait_median", fill: (d) => (d.wait_median > th.waitMinutes ? token("--color-error") : token("--color-accent")), rx: 3, insetLeft: 1, insetRight: 1}),
    Plot.ruleY([0], {stroke: token("--color-border")}),
    Plot.tip(zh, Plot.pointerX({x: "hour", y: "wait_median", title: (d) => `${d.hour}:00\nTypical wait ${fmt.minutes(d.wait_median)}\n${fmt.whole(d.trips)} trips`}))
  ]
})));
```

<p class="small muted">Red bars are hours past your ${th.waitMinutes} minute threshold.</p>
    </div>
  </div>
</div>
