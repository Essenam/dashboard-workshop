# Data quality dimensions

This is a starting list, not a finished one. Copy it into your own project, keep the
dimensions that fit your data, and adapt the rest. The point is not to use exactly these
eight words. It is to write your definitions down once so that two people, checking the
same data on two different days, end up testing the same thing the same way.

## The frameworks these dimensions come from

There is no single industry standard for data quality dimensions. Several organizations
and authors have each published their own list, and the lists disagree with each other
about names, counts and boundaries. The table below is a starting map, not a full survey.

| Framework | What it counts as dimensions | Link |
|---|---|---|
| DAMA UK, "The Six Primary Dimensions for Data Quality Assessment" (2013) | Six: completeness, uniqueness, timeliness, validity, accuracy, consistency. | [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment) |
| DAMA-DMBOK2, Revised Edition (2024) | Nine, the set DAMA states there is general agreement on: accuracy, completeness, consistency, currency, integrity, reasonableness, timeliness, uniqueness, validity. | [DAMA International, DMBOK2 revisions](https://www.damadmbok.org/dmbok2-revisions) |
| DAMA NL, "Dimensions of Data Quality" research (2020) | 60 standardized dimension definitions distilled from nine authoritative sources, each tied to the kind of data it applies to. | [Van Nederpelt and Black, DAMA NL, DDQ Research Paper](https://dama-nl.org/wp-content/uploads/2020/09/DDQ-Dimensions-of-Data-Quality-Research-Paper-version-1.2-d.d.-3-Sept-2020.pdf) |
| ISO/IEC 25012:2008 | 15 characteristics grouped as inherent (accuracy, completeness, consistency, credibility, currentness), both inherent and system dependent (accessibility, compliance, confidentiality, efficiency, precision, traceability, understandability), and system dependent only (availability, portability, recoverability). | [ISO/IEC 25012:2008, preview](https://cdn.standards.iteh.ai/samples/35736/3791c8ca8fd64a7fa4c7b629ec8f8524/ISO-IEC-25012-2008.pdf) |
| ISO 8000-8:2015 | Three, and a conformance model rather than a named list: syntactic quality (does a value match its declared format), semantic quality (does it correctly encode its intended meaning), pragmatic quality (does it fit the purpose of the people using it). | [arc42, ISO 8000 standard summary](https://quality.arc42.org/standards/iso-8000) |
| Danette McGilvray, "Executing Data Quality Projects" | 14 practitioner dimensions, including data specifications, duplication, accuracy, consistency and synchronization, timeliness and availability, and data coverage. | [McGilvray, Data Quality Dimensions excerpt](http://static1.1.sqspcdn.com/static/f/739370/24990045/1401912164197/1) |
| David Loshin, "Data Quality Fundamentals" (2010) | Two branches, presented as a starting point rather than a fixed canon: intrinsic (accuracy, lineage, semantic, structure) and contextual (timeliness, currency, completeness, consistency, identifiability, reasonableness). | [Loshin, Data Quality Fundamentals](https://dama-ny.com/images/meeting/041510/dqprogram.pdf) |

## The eight dimensions this material uses

This list keeps DAMA UK's six as its core, because they are the most widely reused
starting point, and adds two that other frameworks name but DAMA UK does not: integrity
and reasonability. It runs alphabetically, so a reader looking for a dimension finds it
where they expect. Each entry gives a plain definition, the source it is closest to, and
one concrete example of a check. None of these definitions is the only correct one; the
frameworks above word them differently and sometimes disagree about which dimension a
given problem belongs under. Treat the wording here as a reasonable default, not the
final word.

### Accuracy

The degree to which data correctly represents the real world entity or event it
describes, usually checked against an authoritative source. This is the one dimension
that cannot be checked by looking at the data alone. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an address on file does not match a verified postal reference.

### Completeness

Whether all required data is present, at the field, record or dataset level. Closest to
[DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: a required field, such as a customer id or an order date, is null.

### Consistency

Whether data values agree with each other within a record, across records, across
systems and over time. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an order total stored in one place does not match the sum of its line
items stored elsewhere.

### Integrity

Whether relationships and rules hold, such as referential integrity (no orphan records)
and internal coherence. Named in DAMA-DMBOK2's nine but not in DAMA UK's six. Closest to
[Van Nederpelt and Black, DAMA NL, DDQ Research Paper](https://dama-nl.org/wp-content/uploads/2020/09/DDQ-Dimensions-of-Data-Quality-Research-Paper-version-1.2-d.d.-3-Sept-2020.pdf).

Example check: an order refers to a customer id that does not exist in the customer data.

### Reasonability

Whether data patterns meet expectations, for example whether daily transaction volumes
fall within a normal range. Named in DAMA-DMBOK2's nine. Closest to [DAMA International, DMBOK2 revisions](https://www.damadmbok.org/dmbok2-revisions).

Example check: yesterday's order count is a third of every other Tuesday this year, with
no known cause.

### Timeliness

Whether data is available when needed and current enough for its use. This covers the
related ideas of currency (how up to date a value is) and latency (how long it takes to
arrive). Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: the newest record is older than the period the report claims to cover.

### Uniqueness

Whether each real world entity appears only once in the dataset. Also called
deduplication, after the work it usually creates. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: the same record, matched on its key fields, appears twice.

### Validity

Whether values conform to the defined domain, format, type or business rules. Closest to
[DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an amount field holds a negative number where negative is not possible,
or a status code appears that the documentation does not list.

### Adding one of your own

Eight is a starting point, not a boundary. A project that keeps finding problems none of
these names fits should add a dimension and write its definition down with the rest. The
worked example that ships with this workshop adds **conformity**, for whether the
representation and its documentation follow the written specification: a schema that has
drifted from its dictionary, a timestamp with no time zone, a fee amount the
documentation never updated. That idea lives in [arc42, ISO 8000 standard summary](https://quality.arc42.org/standards/iso-8000) as syntactic and semantic
quality, and in McGilvray's list as data specifications, but no framework above makes it
a top level name.

## How to adapt this list

- Drop a dimension you have no way to measure yet. A dimension with no check behind it
  is a heading, not a control. Add it back once you have a way to test it.
- Add a dimension your regulator, your industry or your own data documentation already
  names, even if none of the frameworks above use that word. The frameworks disagree
  with each other on purpose; picking the name your organization already uses is a
  reasonable choice.
- Write the definition down, in plain words, before anyone writes a check against it.
  Two people who each hold the definition in their head will write two different checks.
  One written sentence keeps the checks in agreement with each other.
- Revisit the list occasionally. A dimension nobody has ever found a defect under is
  worth asking about: is it truly clean, or is the check too weak to catch anything.
- Keep the source link next to each definition you adapt. When two people disagree about
  what a check should do, going back to the written definition, and where it came from,
  settles the disagreement faster than arguing from memory.

A team that starts here and adjusts is in a better position than a team that starts from
nothing: the first pass at a definition is the hardest one to write, and this list exists
so no one has to write it alone.
