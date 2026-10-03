---
name: closed-loop-visual-feedback
description: Build anything visual by rendering it and actually looking at it, the way the person who uses it will, then iterating until it is both correct and pleasing. Use whenever making or changing something graphical (an SVG or diagram, a dashboard, a web app or page, a static site, a chart, an illustration), and before ever calling such a thing done. Triggers on "draw a diagram", "make an SVG", "build the dashboard", "does this look right", "redraw", "the layout is off", and on any moment you are about to ship a visual you have not seen.
---

# Closed-loop visual feedback

**You cannot tell whether a visual is any good by reading its source. Render it, look at
the image, and iterate. That loop is the work, not a check at the end of it.**

This applies to everything graphical: SVGs and diagrams, dashboards, web apps and pages,
static sites, charts, illustrations. Anywhere a person will look at a result rather than
read a file.

## The two questions

After every render, ask exactly two things.

1. **Is it correct?** Does it say the true thing? Is every label attached to the right
   object, every arrow pointing the right way, every number the real number?
2. **Is it pleasing?** Would you be happy to put your name on it? Nothing overlapping,
   nothing clipped, nothing crowded against an edge, nothing accidentally ugly.

**Iterate until both are 100%.** Not "close enough", not "the structure is right". If
either answer is less than yes, fix it and render again. A visual is one of the few things
where the person will notice the flaw before they notice the content.

## Look at it the way a user will

**At native resolution.** This is the rule that gets skipped and it is the one that costs
most. A thumbnail, a scaled screenshot, a preview pane at 68%: all of them hide exactly
the defects you are looking for. Text overlapping a box by six pixels is invisible at 70%
and glaring at 100%. Export at the real size and read the image.

**At the real size, in the real place, on the real device.** A dashboard is used at the
window size people have, not maximised on your monitor. A page that will be read on a phone
gets looked at narrow. A diagram that will sit on a documentation page gets looked at on
that page, not just as a file.

**On the real background.** Something that reads beautifully on white can vanish on a dark
page. If the destination has a light and a dark mode, see both.

## How many renders, and in what

**That is yours to judge, per task.** Sometimes one look is enough and you are done.
Sometimes the thing renders differently in two places that both matter, and then both
matter and you check both. Decide it deliberately rather than by habit in either direction.

The question to ask is: **who will see this, and through what?** Every answer to that is a
renderer you are responsible for. If a file is served to readers through a browser and also
opened by a colleague in an editing tool, those are two audiences and they do not always
agree. If it only ever appears in one place, one render is the honest amount.

## What "it renders" does not mean

**Valid is not correct.** An SVG can be perfectly well-formed XML and be a black rectangle.
A page can return 200 and be blank. A chart can plot and have the axes swapped. Parsing,
compiling and returning a status code all prove the machine was satisfied; none of them
prove a person would be.

**A failed screenshot is not a pass.** If the render did not happen (the pane was not
compositing, the export errored, the file did not load), you have no signal at all. Do not
reason past it. Get an image or say plainly that you could not.

**Your mental model of the edit is not evidence.** Re-render after every fix. An edit
routinely lands somewhere other than where you pictured it, and two fixes in a row without
a look between them is how a small correction becomes a new defect.

## Working with SVG specifically

**Keep colour and size on the elements.** Presentation attributes (`fill`, `font-size`,
`stroke`) on each element are understood by every renderer. Styling through a `<style>`
block, CSS custom properties or `@media` queries is understood by browsers and by very
little else, so a file that depends on them is a browser-only file. If it will only ever be
seen in a browser that is fine; if anything else will open it, that choice quietly removes
every colour in the drawing.

**Text is the part that breaks.** SVG does not wrap, does not reflow, and does not tell you
when a label runs past the box behind it. Nothing in the file is wrong; it just looks
broken. So after each render, walk the labels: every one inside its shape, none touching a
border, none colliding with its neighbour.

**Estimate text width before you place it.** Roughly, a proportional label is about 0.5 of
its font size per character, a monospace one about 0.6. A 14px label of 30 characters wants
about 210px. Leave real margin rather than fitting exactly, then confirm by looking.

**When a label does not fit, shorten the words first.** Moving the box or shrinking the
font fixes this one collision and pushes the problem somewhere else. Tighter wording fixes
it and usually improves the diagram.

**Export a detail strip when the whole image is too big to judge.** Most renderers can
export a sub-region; use it to inspect a crowded corner at full size rather than squinting
at the whole thing.

## Where this sits

This loop is the evidence for the other two.

- **`jobs-quote-ux`** says who "the person who uses it" is and what they are trying to do.
  "Pleasing" means pleasing to them, so name them before judging.
- **`ux-heuristics`** turns "is it correct, is it pleasing" into a systematic pass over a
  screen. Run it on the render, not the source.

## The habit

Draft, render, look, fix, render again. Say what you actually saw rather than that it
should be fine. When you hand the work over, it should be because you looked at it and it
was right, not because you ran out of edits.
