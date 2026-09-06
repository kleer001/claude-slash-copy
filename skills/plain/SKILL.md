---
name: unpack-jargon
description: Find the terms a named reader can't parse, and decide for each whether to replace it or keep it and explain it. Use before sending a document to someone outside the work — a lead, a client, a stakeholder, a new joiner — and whenever copy is technically correct but lands flat with its audience.
---

# Unpacking jargon

Three skills guard public copy, and each asks a different question:

| | asks |
|---|---|
| `humanized-copy` | would anyone say this? |
| `honest-copy` | is this true? |
| **`unpack-jargon`** | **can this reader parse it?** |

Run this one **first**. Glossing a term adds words and changes content, so
`humanized-copy` should measure what will actually ship. `honest-copy` stays
last, because any rewrite can turn a careful claim into a confident one.

## Why a tool and not a careful re-read

A writer cannot find their own jargon. Knowing a subject well makes thinking
about it feel easy, and that ease gets misread as *the idea is simple*. The
term stops looking like a term. This is why plain-language guidance that tells
writers to audit their own work keeps failing: it asks for the one judgement
expertise destroys.

Every standard's answer is an outside reader. That is what this skill is.

## 1. Name the audience

Do this first and write it down. Without it the rest of the method has no input,
because the same word is required vocabulary for one reader and a wall for
another. `riprap` is correct for a discipline lead and opaque to a project
manager. Neither reading is wrong.

Be specific. "Stakeholders" is not an audience. "The client's environmental lead,
who knows the regulations and has not seen our data" is.

## 2. Detect

```sh
/home/menser/.claude/skills/unpack-jargon/detect.py --audience "<who>" path/to/copy.md
```

Add `--all` to include tables and lists. By default they're skipped — a table of
domain terms is usually the payload the reader wants, not a leak.

The script reports five kinds of candidate:

- **Undefined load-bearing terms.** An ordinary word carrying a technical meaning
  the document never states. Reported when a word is used many times and never
  defined, or defined *after* its first use, with both line numbers. This is the
  signal a dictionary cannot give — `pass`, `reader` and `wave` are all ordinary
  English and all opaque as terms. Read it as a prompt for judgement, not a
  verdict: some hits are ordinary words used ordinarily.

- **Acronyms with no expansion.** The highest-yield signal, and the one writers
  miss most. `weak gloss nearby` means something explanatory sits next to it but
  the letters were never spelled out — judge it yourself.
- **Words no dictionary holds.** High precision for domain vocabulary and proper
  nouns.
- **Definite references to things never introduced.** "The release", "the queue",
  "the framework" — a *the* that assumes the reader already knows. Reported only
  for words that are candidates on other grounds, since ungated it is mostly noise.
- **Terms of art.** Hyphenated compounds used more than once. Repetition is what
  separates a coined term from a one-off hyphenation.

**Definition order is a defect on its own.** A term defined two hundred lines
after its first use is undefined for every reader who reads in order. Fix it by
moving the definition, not by adding a second one.

## 3. Decide each one

The rule, consistent across plain-language law and the technical style guides:

> **If the term isn't necessary, replace it. If it is necessary, keep it and
> define it on first use.**

Necessity means precision that a plain word would lose. Not familiarity, not
house habit, not that the source document used it.

- **Replace** when an everyday word says the same thing. `commence` → `start`.
- **Keep and gloss** when the plain word would be wrong. A riverbank gets
  `riprap`; "rocks on a bank" is a different claim.
- **Pair** for a mixed audience: precise term first, plain words immediately
  after — `bacteria (tiny living cells)`. The reader who knows it skips the
  parenthesis; the reader who doesn't is not sent elsewhere.

## 4. When several terms describe one mechanism, write the introduction

If the report names half a dozen terms that all belong to the same machinery —
the thing that does the work, the unit it works on, the batch, the place it runs
— do not gloss them one at a time. That the document needs six definitions in six
places means it never introduced the mechanism at all.

Write the introduction instead, before anything refers to it, in the order the
reader meets the parts. Six scattered glosses leave a reader assembling the
machine from footnotes; four sentences up front means every later rule has
something to attach to.

This is the one case where the fix is structural. The signal is several terms at
once, not one hard term.

## 5. Gloss in place

Define at first use, in the sentence, in the reader's words. Not a footnote, not
an appendix, not a glossary — anything that makes the reader leave the paragraph
to understand the paragraph has failed.

One or two sentences is usually enough. If a term needs a paragraph, it may be
carrying an idea the document hasn't introduced yet, which is a structure problem
wearing a vocabulary costume.

## 6. Record the decision

Write what you decided into the project's `.claude/skills/unpack-jargon/terms.md`.
Sections are load-bearing — `detect.py` routes on the header text:

```markdown
## Domain terms
- proponent
- offsetting

## Decided - keep and gloss
- riprap: loose rock placed on a bank to stop it eroding

## Decided - replace
- utilise: use

## Decided - fine as-is
- authorization
```

**A term moves through the sections; it does not sit in two.** `Domain terms` is
a discovery list — words the dictionary cannot find, named so the detector will
raise them. Once you have decided what to do with a word, **move it** to
`Decided - keep and gloss`, `Decided - replace`, or `Decided - fine as-is`.

Leaving a decided word in `Domain terms` makes the report louder every run, which
is the opposite of the point. A word under `keep and gloss` is still reported, but
carries its gloss — that is deliberate, and it is the reminder to check the gloss
is still in the document.

Anything under `fine as-is` stops being reported. This is the whole reason to
record: the first run on a project is loud and the tenth is quiet, and the
decisions stop being re-litigated every time somebody writes a memo.

## What this misses

**The dictionary signal has poor recall.** It finds `intertidal` and `riparian`.
It cannot find `culvert`, `proponent` or `offsetting`, which every dictionary
holds and no outsider knows.

The load-bearing check covers part of that gap — an ordinary word used a dozen
times without a definition surfaces whether or not a dictionary knows it. What
neither signal reaches is a domain word used a handful of times: `culvert` in a
document that says it four times is invisible to both.

That remainder is what `## Domain terms` closes, and closing it is manual. Expect
the first pass on a new domain to need a human naming ten or twenty words no
script will guess.

**Dictionaries have holes.** Some ordinary words are simply absent and will
surface as candidates. Record them once under `fine as-is` and move on.

**A frequency signal cannot see a rare term.** The load-bearing check needs a
word used several times before it will speak. A term used twice can be just as
opaque, and nothing here will find it. Raising the sensitivity floods the report
with ordinary words, so the floor stays where it is and this stays a known gap.

**Glossing costs words.** Expect a document to get longer and its reading grade
to barely move. This skill buys comprehension, not brevity — `humanized-copy`
owns length, and it should measure after this pass rather than before.

## Sources

The replace-versus-define rule is common to the US plain-language guidance
(plainlanguage.gov), ISO 24495-1, the GOV.UK content style guide, and the major
technical-writing style guides; all of them defer the decision to audience
knowledge rather than offering a universal answer. The paired-term pattern is
CDC practice for public health communication. The claim that self-review fails
rests on the curse-of-knowledge literature in psychology and behavioural
economics — the finding that knowing something makes it hard to model not
knowing it.
