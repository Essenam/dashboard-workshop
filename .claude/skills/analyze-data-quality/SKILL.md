---
name: analyze-data-quality
description: Use this when a participant wants to turn a dataset into a working data quality check, from picking dimensions through a scorecard dashboard built on stored, non-sensitive results.
---

# Analyze data quality

This skill walks through building a data quality check from scratch: agree what to
measure, look at the real data before writing any rule, write the rules as plain code,
run them over everything, record what each finding actually means, and build a dashboard
from the results. Work through the steps in order and check in with the person after
each one before moving to the next.

## 1. Agree on the dimensions

Read `docs/data-quality-dimensions.md` together with the person. Ask which of the eight
dimensions apply to their data, and whether their organization already uses a different
name for one of them. Not every dimension applies to every dataset: if uniqueness is
meaningless for this data, drop it. Write down the short list you land on before moving
on.

## 2. Profile the data first

Before writing a single rule, look at what the data actually contains:

- the list of columns and what each one is supposed to mean
- the data type of each column
- the total row count
- the null rate for each column
- the range of values for numeric and date columns, and the distinct values for coded
  or categorical columns

This step exists so that rules are written against the data as it really is, not against
what the documentation claims or what someone assumes. A column that is supposed to
never be empty, but is empty a third of the time, changes what you write next.

## 3. Write the rules as code

Write the rules in one file, one rule per entry. Each rule needs:

- an id, such as `CMP-01`, made of a short dimension prefix and a number
- a name
- the dimension it belongs to
- a severity
- the test, in one plain sentence a non-coder can read and agree with
- why it matters to someone who uses this data
- the SQL predicate that is true for a row that fails the rule

Writing the predicate as "true when the row fails" rather than "true when the row
passes" keeps every rule readable the same way: run the predicate, and the rows it
returns are the problem rows.

## 4. Run every rule over the whole dataset

Run each rule over every row, never a sample. A sample can hide a problem that only
shows up in one slice of the data. For each rule, store only:

- the count and rate of failing rows
- a small number of example failing rows, enough to see the shape of the problem

Do not store the full set of failing rows, and never store the raw dataset itself.
Storing counts, rates and a few examples is what lets these results be committed to a
repository while the underlying data stays out of it entirely.

**Example rows must never contain personal data.** Before storing an example row, strip
or mask any field that identifies a specific person, such as a name, an address, an
email, or an account number. If a rule cannot be explained without showing a personal
field, describe the example in words instead of storing the row.

## 5. Record what each finding actually means

A failing rule is not automatically a defect. For each finding, decide which of these it
is:

- a **defect**: the data is simply wrong and should be fixed at the source
- a **business rule** the check did not know about: the data is correct, and the rule
  needs to be adjusted to account for it
- a **documentation gap**: the data and the rule disagree because the written
  specification never said what actually happens

Write this decision down next to the rule. It is what turns a list of red numbers into
something a team can act on.

## 6. Build the dashboard from the stored results

Build the dashboard from the stored counts and examples only, never from the raw data.
A useful shape:

- headline numbers: total rows checked, total rules, overall pass rate
- a scorecard broken down by dimension, so a viewer can see at a glance which dimension
  is weakest
- a card per rule, showing the plain sentence describing the test, the count and rate,
  one masked example, and the SQL predicate for anyone who wants to verify it

## 7. Re-run as new data arrives

Data quality is not a one time check. Re-run the same rules against each new batch of
data as it arrives, and watch how the rates move over time. A rate that suddenly jumps
is usually more interesting than a rate that stays high but steady, because it points to
something that just changed upstream.
