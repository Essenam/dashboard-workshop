// Observable Framework settings. See https://observablehq.com/framework/config
export default {
  title: "Ride-hail operations",
  root: "src",
  style: "style.css",
  pages: [
    {name: "Today", path: "/"},
    {name: "Wait times", path: "/waits"},
    {name: "Driver pay", path: "/pay"},
    {name: "Data quality", path: "/quality"}
  ],
  sidebar: true,
  pager: false,
  search: false,
  toc: false,
  head: '<link rel="icon" href="logo.svg" type="image/svg+xml">',
  footer: "Source: NYC Taxi and Limousine Commission trip record data, September 2025 to August 2026."
};
