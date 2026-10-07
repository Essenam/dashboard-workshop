// Shared helpers for every page: formatting, thresholds, colors from the tokens, icons.
import {html} from "npm:htl";

// ---- Thresholds ----------------------------------------------------------------------
// The defaults for what counts as "needs attention". The COO can adjust them on the Today
// page; their choice is remembered in this browser only.
export const DEFAULT_THRESHOLDS = {
  waitMinutes: 7, // a zone's typical (median) wait above this is flagged
  volumeDropPct: 10, // trips or fares down more than this from the same day last week
  zoneDropPct: 25, // a busy zone's trips down more than this from its usual week
  zoneMinTrips: 5000, // only zones with at least this many trips a week are judged on drops
  payShareMin: 70, // driver pay share below this percent is flagged
  dqRatePct: 1 // a data defect rule failing on more than this percent of trips is flagged
};

const KEY = "coo-dashboard-thresholds";

export function loadThresholds() {
  try {
    return {...DEFAULT_THRESHOLDS, ...JSON.parse(localStorage.getItem(KEY) ?? "{}")};
  } catch {
    return {...DEFAULT_THRESHOLDS};
  }
}

export function saveThresholds(value) {
  try {
    localStorage.setItem(KEY, JSON.stringify(value));
  } catch {
    // Private windows can refuse storage; the thresholds still apply for this visit.
  }
}

// ---- Formatting ----------------------------------------------------------------------
const compact = new Intl.NumberFormat("en-US", {notation: "compact", maximumFractionDigits: 1});
const whole = new Intl.NumberFormat("en-US", {maximumFractionDigits: 0});
const money = new Intl.NumberFormat("en-US", {style: "currency", currency: "USD", notation: "compact", maximumFractionDigits: 1});

export const fmt = {
  compact: (n) => compact.format(n),
  whole: (n) => whole.format(n),
  money: (n) => money.format(n),
  minutes: (n) => `${n.toFixed(1)} min`,
  pct: (n, digits = 1) => `${(n * 100).toFixed(digits)}%`,
  rate: (n) => (n === 0 ? "0%" : n < 0.0001 ? "<0.01%" : `${(n * 100).toFixed(n < 0.01 ? 2 : 1)}%`),
  day: (d) => d.toLocaleDateString("en-US", {weekday: "short", month: "short", day: "numeric", timeZone: "UTC"}),
  longDay: (d) => d.toLocaleDateString("en-US", {weekday: "long", month: "long", day: "numeric", year: "numeric", timeZone: "UTC"}),
  month: (m) => new Date(`${m}-01T00:00:00Z`).toLocaleDateString("en-US", {month: "short", year: "numeric", timeZone: "UTC"})
};

// A change pill: arrow plus signed percent, colored by whether the change is good.
// `higherIsBetter` false flips the coloring (for wait times).
export function delta(now, before, {higherIsBetter = true, label = ""} = {}) {
  if (!before) return html`<span class="delta flat">no comparison</span>`;
  const change = now / before - 1;
  const flat = Math.abs(change) < 0.005;
  const good = flat ? null : (change > 0) === higherIsBetter;
  const cls = flat ? "flat" : good ? "good" : "bad";
  const arrow = flat ? "→" : change > 0 ? "▲" : "▼";
  return html`<span class="delta ${cls}" title="${label}">${arrow} ${change > 0 ? "+" : ""}${(change * 100).toFixed(1)}%</span>`;
}

// ---- Colors --------------------------------------------------------------------------
// Charts read colors from the design tokens so light and dark mode stay in step.
export function token(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

export function companyColors() {
  return {domain: ["Uber", "Lyft"], range: [token("--color-series-1"), token("--color-series-2")]};
}

// ---- Icons (Lucide, outline) ---------------------------------------------------------
const paths = {
  "alert-triangle": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
  "alert-circle": '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>',
  "check-circle": '<path d="M21.8 10A10 10 0 1 1 17 3.34"/><path d="m9 11 3 3L22 4"/>',
  "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
  "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
  "sliders": '<line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/>',
  "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>'
};

export function icon(name, size = 16) {
  const el = html`<span aria-hidden="true" style="display:inline-flex"></span>`;
  el.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${paths[name]}</svg>`;
  return el;
}

// A status badge: always icon plus word, never color alone.
export function badge(level) {
  const map = {critical: ["alert-circle", "Act now"], warning: ["alert-triangle", "Watch"], good: ["check-circle", "OK"], info: ["info", "Note"]};
  const [name, word] = map[level];
  return html`<span class="badge is-${level}">${icon(name, 13)} ${word}</span>`;
}

// Typed CSV reading turns "2026-08" into a date; keep months as "YYYY-MM" text so they compare.
export function monthText(value) {
  return value instanceof Date ? value.toISOString().slice(0, 7) : String(value);
}

// A legend for the two companies: swatch plus name, so identity is never color alone.
export function companyLegend() {
  const {domain, range} = companyColors();
  return html`<div class="legend">${domain.map((name, i) => html`<span><span class="swatch" style="background:${range[i]}"></span>${name}</span>`)}</div>`;
}
