---
name: inverse-set-kondo
description: Audit a set of rules, workflows, configs, checks or code by notionally emptying it and making every piece earn its way back. Use when something has accumulated and nobody is sure what is still needed, or when someone says "run the inverse-set Kondo", "declutter this", "what can we delete", "audit these rules", "do we still need all of this", "clean up the config". With no target named, it describes the method and stops.
---

# The inverse-set Kondo

**Not "what should we remove". Everything currently in place goes into a box and is
notionally already gone. Then take each piece out, one at a time, and ask whether we
actually want it in the world we are building now.** If nothing about it earns its way
back, it goes in the delete box.

Existing is not a reason to keep. Neither is "it was carefully built", "somebody wrote a
long comment justifying it", or "removing it feels risky". Those are all arguments for
reading it carefully before deciding, not for keeping it.

## If no target was named

Do not pick one yourself. Say what the method is in two or three sentences, ask what set
to audit (a folder of workflows, a ruleset, a config file, a list of data quality checks),
then stop. Everything below applies only when there is a set to audit.

## How to run it

**Enumerate exhaustively first, by reading, not from memory.** List every item in the set
before judging any of them. Read the actual rules, workflow files, config keys or
functions. A Kondo done from recollection audits your recollection.

**Then, for each item, answer three questions in this order:**

1. **What does it assert?** In one sentence, in plain terms. If you cannot say what it
   asserts, that is already a finding.
2. **What breaks without it?** Concretely, naming the failure. "Less safe" is not an
   answer.
3. **Does that thing still matter, and is this still the place to assert it?** Often the
   invariant is real and has moved somewhere better, or is now guaranteed structurally, or
   is asserted twice and only one copy works.

**Sort into three boxes, and say which:**

- **Keep:** with the reason it earned its place, which must not be "it is already there".
- **Change:** it asserts something real in the wrong place, or with the wrong scope, or
  at the wrong time. Say what the new shape is.
- **Delete:** nothing about it survives the three questions. Say what used to justify it
  and why that justification no longer reaches.

**Watch for these four patterns**, because they account for most of what a Kondo finds:

- **A rule that can only be satisfied by a flow nobody uses any more.** It looks like
  enforcement and is a locked door with the key handed out.
- **The same invariant asserted twice**, where one copy is structural and the other is
  checked. Keep the structural one.
- **A check whose failure nobody can see.** It costs runtime and buys nothing.
- **Something whose stated justification is circular**: it exists because of a condition
  that only exists because of it.

## Where this sits

The other skills in this set judge what a person sees. This one judges what has piled up
behind it.

- **`jobs-quote-ux`** asks you to cut a screen to the essential. The Kondo is the same
  question asked of rules, checks, config and code.
- **`ux-heuristics`** names the on-screen version in its eighth heuristic, aesthetic and
  minimalist design.
- **`closed-loop-visual-feedback`** is how to confirm nothing a person relies on went
  missing: after deleting, render the thing and look.

## Output

One table, ordered by box: everything deleted first, because that is the part worth
reading. Columns: the item, what it asserts, the verdict, and the reason. Then a short
count of what the set weighed before and after.

State plainly anything you could not verify and what it would take to settle it. A Kondo
that guesses at one item's purpose has quietly kept or deleted it for no reason.

Propose the deletions; do not carry them out until the person agrees. Deleting is the
one step here that is hard to take back.
