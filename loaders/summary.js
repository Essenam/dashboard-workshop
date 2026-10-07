// Shared by the data loaders: copy one file from data/summaries/ to standard output.
import {readFileSync} from "node:fs";

export function summary(name) {
  const url = new URL(`../data/summaries/${name}`, import.meta.url);
  process.stdout.write(readFileSync(url));
}
