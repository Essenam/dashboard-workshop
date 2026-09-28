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
starting point, and adds two more that other frameworks name but DAMA UK does not:
integrity and conformity. Each entry gives a plain definition, the source it is closest
to, and one concrete example of a check. None of these definitions is the only correct
one; the frameworks above word them differently and sometimes disagree about which
dimension a given problem belongs under. Treat the wording here as a reasonable default,
not the final word.

### Completeness

The proportion of data that is actually present, against the amount that should be
there. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: a required field, such as a customer id or an order date, is null.

### Uniqueness

Nothing in the data is recorded more than once. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: the same record, matched on its key fields, appears twice.

### Timeliness

Data represents reality as of the point in time someone actually needs it. Closest to
[DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: a status field has not been updated since the event it should describe
already happened.

### Validity

A value conforms to the format, type and range its definition calls for. Closest to
[DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an amount field holds a negative number where negative is not possible,
or a phone number field holds letters.

### Accuracy

A value correctly describes the real world thing or event it stands for. This is the one
dimension that cannot be checked by looking at the data alone; it needs an outside
reference to compare against. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an address on file does not match a verified postal reference.

### Consistency

Two or more representations of the same thing agree with each other and with a shared
definition. Closest to [DAMA UK, resource page](https://www.dama-uk.org/resources/the-six-primary-dimensions-for-data-quality-assessment).

Example check: an order total stored in one place does not match the sum of its line
items stored elsewhere.

### Integrity

The absence of data value loss or corruption, extended here to cover broken links
between records. Named in DAMA-DMBOK2's nine but not in DAMA UK's six. Closest to
[Van Nederpelt and Black, DAMA NL, DDQ Research Paper](https://dama-nl.org/wp-content/uploads/2020/09/DDQ-Dimensions-of-Data-Quality-Research-Paper-version-1.2-d.d.-3-Sept-2020.pdf).

Example check: a record refers to another record, such as a customer id on an order,
that does not exist anywhere in the customer data.

### Conformity

The representation, syntax and documented meaning of a value match its written
specification. Not a top level name in any of the frameworks above; it groups ideas that
ISO 8000-8 calls syntactic and semantic quality, and that McGilvray calls data
specifications. Closest to [arc42, ISO 8000 standard summary](https://quality.arc42.org/standards/iso-8000).

Example check: a status code appears in the data that is not one of the values the
documentation lists as valid, or a timestamp is recorded with no time zone attached so
its meaning is ambiguous.

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
