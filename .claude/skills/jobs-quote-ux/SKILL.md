---
name: jobs-quote-ux
description: Test a design against the user-experience-first standard, naming the person first and working backward from what they are trying to accomplish to the technology. Use when someone asks whether a flow, screen, dashboard, skill, process or error message is actually any good for the people who use it, or says "apply the Jobs standard", "work backwards from the user", "critique this UX", "is this the right experience", "does this pass". With no target named, it reports the quote and stops.
---

# The user-experience-first standard

Steve Jobs, closing Q&A at Apple's 1997 developer conference:

> "You've got to start with the [user] experience and work backwards to the technology."

He went on to say you cannot start with the technology and then go looking for where to
sell it, and that he had made that mistake more than anyone in the room and had the scar
tissue to prove it.

## If no target was named

Do not ask for one and do not choose one yourself. Report the quote and the context above,
then stop. Everything below applies only when there is something to test.

## How to apply it

**Name the person first, specifically.** Not "the user". A finance analyst upskilling into
dashboards. A VP looking at a number that is wrong. A dashboard owner clearing a queue on
a Tuesday afternoon. The design changes depending on which, so pick.

**Say what they are actually trying to accomplish**, in their words rather than the
system's. A person manages notifications, not webhook config. A person wants the number
to be right again, not a surgical revert.

**Then work backward.** From that need to the interface, from the interface to the
mechanism, and only then to what has to be built. If a step exists because of how the
system is put together rather than because the person needs it, that step is technology
leaking upward.

**Then say where the current design fails the test**, concretely:

- What does it ask the person to know that is really about the implementation? Branches,
  refs, pull requests, versions and promotions are all suspects.
- What does it ask them to decide that the system could decide, or that has only one
  sensible answer?
- Where does it report the mechanism rather than the outcome? "409 conflict" instead of
  "this cannot ship yet, and here is why."
- What is on screen because it was easy to render rather than because it is needed?

**Cut to the essential.** Dumping everything available and calling it complete is the
failure mode this standard exists to prevent. Fewer, better-chosen things beat exhaustive
ones.

## What good looks like

The person accomplishes the thing without learning the system's shape. Where the system's
shape is genuinely unavoidable, it is named in their language and once, not repeatedly.
Every control says what will happen and afterwards says what did.

## Where this sits

This standard is the first of three, and it sets the target for the other two.

- **`ux-heuristics`** is the systematic pass. Once the person and their need are named,
  walk the real screen against Nielsen's ten heuristics to find where it fails them.
- **`closed-loop-visual-feedback`** supplies the evidence. Judge the rendered thing, at the
  size and on the device the person will use, never the source.

## Output

Say what the person needs, what the design currently makes them do instead, and the
smallest change that closes the gap. If the honest answer is that the design already
passes, say so plainly and stop; inventing a critique to fill the template is its own
failure of the standard.
