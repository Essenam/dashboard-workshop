---
name: ux-heuristics
description: Inspect a screen, flow or dashboard against Jakob Nielsen's ten usability heuristics and report the violations by severity. Use when someone asks for a heuristic evaluation or a usability review, says "run the heuristics", "check this against Nielsen", "what is wrong with this screen", or when the jobs-quote-ux skill needs a systematic pass over a real interface. Needs a rendered interface to look at; with none, it says so and stops.
---

# Usability heuristics

Jakob Nielsen's ten heuristics are the standard checklist for finding usability problems
without running a user test. They are rules of thumb, not laws: each one names a way that
interfaces commonly fail people.

## Where this sits

- **`jobs-quote-ux` comes first.** It names the person and what they are trying to do.
  A heuristic pass with no person in mind produces a list of nitpicks. If nobody has
  named the person yet, do that before anything below.
- **`closed-loop-visual-feedback` supplies the evidence.** Inspect the rendered interface,
  at the size and on the device the person will use. Reading the source is not an
  inspection.
- **`inverse-set-kondo` is the eighth heuristic turned on everything else.** Aesthetic and
  minimalist design, asked of rules, checks, config, and code instead of the screen.

## The ten

Walk them in order, once per screen or per step of a flow.

1. **Visibility of system status.** The person can always tell what is happening. A
   dashboard says how fresh its data is. A filter that is on looks on. A load that takes
   more than a second shows that it is working.
2. **Match between the system and the real world.** It speaks the person's language, in
   the order they think. "Late trips" rather than `dq_flag_3`. Dates the way the audience
   writes them.
3. **User control and freedom.** There is an obvious way back out of anything. Clear all
   filters. Undo. Close the drill-down and land where you were.
4. **Consistency and standards.** The same thing looks and behaves the same everywhere,
   and follows conventions the person already knows. One colour means one thing across
   every chart. Red is not "good" on one tab and "bad" on the next.
5. **Error prevention.** The design makes the mistake hard to make, which beats a good
   error message. A date picker that cannot select an end before the start.
6. **Recognition rather than recall.** Nothing has to be remembered from another screen.
   Chart titles carry the active filters. Legends sit next to what they explain.
7. **Flexibility and efficiency of use.** A newcomer can get through it, and a regular is
   not slowed down by the newcomer's path. Sensible defaults, shareable URLs, the last
   view remembered.
8. **Aesthetic and minimalist design.** Every element on screen competes with the ones
   that matter. Cut the KPI nobody acts on, the gridlines, the third decimal place.
9. **Help users recognize, diagnose and recover from errors.** When it goes wrong, say
   what happened in plain words and what to do next. "No trips match these filters. Clear
   the borough filter?" rather than an empty chart.
10. **Help and documentation.** Best if none is needed. Where it is, it sits at the point
    of need: a one-line definition on the metric, not a manual somewhere else.

## Rating what you find

Give each finding a severity, so the list can be acted on in order:

- **4, blocker:** the person cannot finish the task, or leaves believing something false.
- **3, major:** they finish, but slowly or only after a wrong turn. Fix before sharing.
- **2, minor:** a stumble they recover from alone. Fix when convenient.
- **1, cosmetic:** fix only if time allows.

A wrong number that looks right is always a 4. On a dashboard, being trusted is the task.

## Output

For each finding: the heuristic by number and name, where on the screen it is, what the
person experiences, the severity, and the smallest fix. Order by severity, highest first.

Do not force a finding for every heuristic. Say which ones the screen passes and move on.
If the screen passes all ten, say so plainly and stop.
