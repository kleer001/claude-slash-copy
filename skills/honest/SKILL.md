---
name: honest
description: >-
  Audit public-facing copy for false, unverifiable, or fabricated claims —
  store pages, READMEs, release notes, announcement posts, dev-blog drafts,
  landing-page pitches, trailer narration. TRIGGER when the user asks to check,
  audit, or honest-check any copy; when writing or reviewing an announcement,
  release note, or dev-blog post; and at the release gate before a store page
  goes live.
argument-hint: "[path/to/copy.md or inline copy]"
allowed-tools: Read, Glob, Grep, Bash
---

## The chain

The four copy skills have one canonical order when they run together:

> `copy:honest` → `copy:plain` → `copy:humanize` → `copy:desk` → `copy:honest`

| stage | skill | asks |
|---|---|---|
| 1 | `copy:honest` | is this true? |
| 2 | `copy:plain` | can this reader parse it? |
| 3 | `copy:humanize` | would anyone say this? |
| 4 | `copy:desk` | will anyone read it to the end? |
| 5 | `copy:honest` | is it *still* true? |

`copy:honest` brackets the chain. At the head, because no one should line-edit a
sentence that is about to be cut for being false. At the tail, because a rewrite
for rhythm turns a hedged claim into a confident one, and an audit only counts
against the wording that actually ships.

The middle three sit in this order because each measures what the next will not
change: `copy:plain` adds words, so `copy:humanize` has to run after it to measure
the length that will ship; `copy:desk` rewrites wholesale, so it runs last and
carries its own copies of the gates.

Run the whole chain when asked for *the copy skills*, *the copy pipeline*, or all
of them. When one skill is named, run only that one — each stands alone.

This skill is **stage 1 and stage 5**. Everything below is the same audit either
way; at stage 5 it is auditing prose the earlier stages wrote.

---

Audit the copy at **$ARGUMENTS** for honesty.

Read the file. Then go line by line through every claim and flag anything that
fails one of these tests.

Verification means the git history, the issue tracker, the origin chat logs, the
code itself, or something the author has explicitly stated. Nothing else counts —
memory does not count.

Run the tests. Do not report that this audit passed without having gone through
the copy claim by claim; a skipped audit reported as clean is the one failure
mode this skill exists to prevent.

---

## The Six Tests

**1. First-person experience claims**
Any sentence starting with "I", "I've", "Every time I", "I got tired of", etc.
Ask: is this verifiably true from the record? If not, flag it. "So I built X" is
fine when X demonstrably exists.

> Bad: "The tool I got tired of rebuilding from scratch"
> Bad: "Every time I needed to fit an image, I'd rebuild the same node chain"
> OK: "Houdini's Resample COP only does Stretch" ← verifiable fact about the software
> OK: "The fairplay test asserts each clue is reachable" + the commit that added it

This covers invented *sentiment* as much as invented events. "My favorite small
thing", "the part I keep turning over", "me pacing around the room" — a stated
preference or feeling the author never expressed is as fabricated as a stated
fact they never lived. Strip every personal reaction you cannot trace to
something they actually said.

**2. Reader-assumption claims**
Flag assertions that the reader has *actually done or experienced* something
specific: "you've written this five times", "you know how painful this is",
"every developer has had to do this."

Do **not** flag hypothetical or illustrative second-person scene-setting that
walks through a workflow as a possibility: "you select a few objects and reach
for the button", "here's a workflow you might run into", "the button you'd reach
for." That is ordinary copy, not a claim about the reader's real history. The
test is whether the sentence asserts the reader's past as fact — not whether it
uses the word "you."

**3. Ordinal and superlative claims**
"First release", "the first of its kind", "most complete", "the only", "fastest",
"the definitive". Verify ordinals against the record (`git log`,
`gh release list`, the commit being described). Flag unsupported superlatives.

**4. Implied repeated personal experience**
Narrative framing like "every time", "I kept having to", "I always ended up"
implies something happened repeatedly. This is fabricated unless the author has
said so. Rephrase as a description of the problem in second or third person, or
attribute it to a specific moment in the record — a dated chat turn, a commit.

**5. Emotional/rhetorical filler**
"which feels right", "that's the way it should be", "finally", "at last", "now
you can stop" — these add sentiment without adding information. Flag and suggest
cutting.

Also reduce extra metaphors. Stock figures like "papercut", "scar tissue",
"tedious dance", "shuffle" hide the actual mechanism — describe the literal
behavior instead. ("Friction" and "pain point" are fine; they're plain industry
terms.)

**6. Claims the build does not keep**
The other five tests catch invented experience. This one catches claims that
were true of the code once, or are true of part of it, and are now doing more
work than the build supports. For every claim about what the software *does*,
open the code that implements it and check the claim across its whole range —
not just the first case.

Two shapes to watch for:

- **True early, false later.** A progression described from its opening steps
  ("each level wears its own surface, brick then stone then steel") when the
  implementation only holds for the authored head and generalizes past it.
  Check the last case, not the first.
- **True when written, outgrown since.** A dial described as always climbing
  ("more choices the deeper you go") when the code caps it early and holds flat
  for the rest of the range. Find the constant; find where it stops moving.

Numbers, counts, dates, real-world references, and named external facts get
verified against a primary source, not against memory. If the copy borrows
credibility from something real — a hardware spec, a historical broadcast, an
instruction set, a call sign — the audience for that copy contains people who
know the real thing better than you do. An invented detail there costs more
than the sentence was worth.

> Bad: "32 levels, each harder than the last" when levels 13+ share one spec
> OK: "32 levels" when `MAX_LEVEL` is 32
> Fix shape: narrow the claim to what the build keeps, or change the build

---

## Estimates and Numbers

Copy often carries estimates — hours spent, team-equivalent effort, LOC,
throughput. These are fine **only** when shown as estimates with their basis,
not asserted as fact:

- State the method ("by a 45-min commit-gap heuristic", "counting chat turns as
  3–5 min bursts"). A number with no method is a flag.
- Use ranges, not false precision. "~11–14 hours", not "12.5 hours".
- Label comparisons as estimates ("roughly", "on the order of"). Flag any
  bare-fact phrasing of a guess ("this would have taken a team 5 months" →
  "a small team would plausibly need months").

---

## Output Format

List each flagged item as:

```
LINE: [quote the sentence]
PROBLEM: [which test it fails and why]
EVIDENCE: [the source, file:line, or command output that settles it]
FIX: [a replacement that says the same thing honestly, or "cut it"]
```

`EVIDENCE` is required for test-6 flags and for any factual dispute — a flag
without it is an opinion, and opinions do not survive an argument with the
person who wrote the copy.

If nothing is flagged, say so explicitly: "No issues found."

After the audit, ask the author which fixes to apply, then edit the file.

---

## When to Run This

Run it on any copy before it reaches an audience: store-page descriptions,
release notes, announcement drafts, dev-blog posts, README feature lists,
landing-page pitches, trailer narration.

At the release gate this audit is mandatory and covers the store page as well
as the repo — the no-fabrication rule runs all the way to the marketing copy.
A claim that survives this audit should be one you would be comfortable having
checked by someone who already knows the subject.

`copy:humanize` is the companion to this skill, not a replacement. That one asks
*would anyone say this*; this one asks *is this true*. Copy ships only when both
pass.

Run this audit at both ends of the chain. At the head it is triage: a claim that
will not survive is not worth line-editing, so cutting it first saves the passes
below it. At the tail it is the gate: a rewrite for rhythm can quietly change a
claim, so a passing audit only counts against the wording that will actually ship.
A head-of-chain pass never substitutes for the tail one.
