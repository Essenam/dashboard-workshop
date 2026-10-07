---
title: Driver pay
---

```js
import {fmt, loadThresholds, token, companyColors, companyLegend, delta, monthText} from "./components/ui.js";

const payMonth = (await FileAttachment("data/pay_month.csv").csv({typed: true}))
  .map((d) => ({...d, month: monthText(d.month)})).map((d) => ({...d, date: new Date(`${d.month}-01T00:00:00Z`), share: d.driver_pay / d.fares, above: d.pay_above_fare / d.trips}));
const dq = await FileAttachment("data/dq_rules.json").json();
const th = loadThresholds();
const colors = companyColors();
const months = [...new Set(payMonth.map((d) => d.month))].sort();
const last = months.at(-1), prev = months.at(-2), first = months[0];
const get = (company, month) => payMonth.find((d) => d.company === company && d.month === month);
const acc04 = dq.rules.find((r) => r.id === "ACC-04");
```

<div class="page-head">
  <div>
    <p class="eyebrow">Question 3</p>
    <h1>Are drivers getting a fair share?</h1>
    <p class="lede">Driver pay as a share of what riders paid in base fares, month by month, for each company.</p>
  </div>
  <span class="as-of">Latest month: ${fmt.month(last)}</span>
</div>

<div class="grid grid-cols-4">
  ${["Uber", "Lyft"].map((c) => {
    const now = get(c, last), before = get(c, prev), start = get(c, first);
    return html`<div class="card kpi">
      <div class="label"><i style="display:inline-block;width:10px;height:10px;border-radius:3px;background:${c === "Uber" ? colors.range[0] : colors.range[1]};margin-right:6px"></i>${c} pay share</div>
      <div class="value">${fmt.pct(now.share)}</div>
      <div class="context"><span>${delta(now.share, before.share)} vs. ${fmt.month(prev)}</span></div>
      <div class="context" style="margin-top:6px"><span>${fmt.pct(start.share)} in ${fmt.month(first)}</span></div>
    </div>`;
  })}
  ${["Uber", "Lyft"].map((c) => {
    const now = get(c, last), before = get(c, prev);
    return html`<div class="card kpi">
      <div class="label">${c} trips paid above fare</div>
      <div class="value">${fmt.pct(now.above)}</div>
      <div class="context"><span>${delta(now.above, before.above, {higherIsBetter: false})} vs. ${fmt.month(prev)}</span></div>
      <div class="context" style="margin-top:6px"><span>${fmt.compact(now.pay_above_fare)} of ${fmt.compact(now.trips)} trips</span></div>
    </div>`;
  })}
</div>

<div class="grid grid-cols-2">
  <div class="card">
    <h2>Pay share by month</h2>
    <p class="sub">Driver pay divided by rider base fares. The dashed line is your ${th.payShareMin}% threshold.</p>
    ${companyLegend()}

```js
display(resize((width) => Plot.plot({
  width, height: 280, marginLeft: 44, marginRight: 44,
  x: {type: "utc", label: null},
  y: {grid: true, label: null, tickFormat: (d) => `${Math.round(d * 100)}%`, domain: [Math.min(th.payShareMin / 100, d3.min(payMonth, (d) => d.share)) - 0.03, d3.max(payMonth, (d) => d.share) + 0.03]},
  color: colors,
  marks: [
    Plot.ruleY([th.payShareMin / 100], {stroke: token("--color-error"), strokeDasharray: "4 3"}),
    Plot.lineY(payMonth, {x: "date", y: "share", stroke: "company", strokeWidth: 2}),
    Plot.dot(payMonth, {x: "date", y: "share", fill: "company", r: 4, stroke: token("--color-surface"), strokeWidth: 2}),
    Plot.text(payMonth.filter((d) => d.month === last), {x: "date", y: "share", text: "company", dx: 10, textAnchor: "start", fill: token("--color-text"), fontSize: 11}),
    Plot.tip(payMonth, Plot.pointer({x: "date", y: "share", title: (d) => `${d.company}, ${fmt.month(d.month)}\nPay share ${fmt.pct(d.share)}\nDriver pay ${fmt.money(d.driver_pay)}\nRider fares ${fmt.money(d.fares)}`}))
  ]
})));
```

  </div>
  <div class="card">
    <h2>Trips where pay was above what the rider paid</h2>
    <p class="sub">Share of each company's trips where driver pay exceeded fare, tips and tolls (rule ACC-04).</p>
    ${companyLegend()}

```js
display(resize((width) => Plot.plot({
  width, height: 280, marginLeft: 44,
  fx: {label: null, tickFormat: (m) => fmt.month(m).replace(" 20", " '"), padding: 0.25},
  x: {axis: null, domain: colors.domain},
  y: {grid: true, label: null, tickFormat: (d) => `${Math.round(d * 100)}%`},
  color: colors,
  marks: [
    Plot.barY(payMonth, {fx: "month", x: "company", y: "above", fill: "company", rx: 2, insetLeft: 1, insetRight: 1}),
    Plot.ruleY([0], {stroke: token("--color-border")}),
    Plot.tip(payMonth, Plot.pointer({fx: "month", x: "company", y: "above", title: (d) => `${d.company}, ${fmt.month(d.month)}
${fmt.pct(d.above)} of trips
${fmt.whole(d.pay_above_fare)} trips`}))
  ]
})));
```

  </div>
</div>

<div class="card" style="margin-top: 16px">
  <h2>How to read this</h2>
  <p class="small">Pay above what the rider paid is mostly Uber, and it is how the business works rather than a data error: companies top up driver pay on cheap or discounted trips. We reviewed this with the data quality check ACC-04 and recorded it as a business rule.</p>
  <p class="small muted">Pay share leaves out trips with a negative fare (check VAL-01). Tips go to drivers on top of pay and are not in the share.</p>
</div>
