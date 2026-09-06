# Machine tells — catalog

The live list of things that mark copy as machine-written. `SKILL.md` holds the
method; this file holds the evidence. Loading this file is step one of the tell
pass.

**This file is append-only.** New tells go at the end with the next free ID. A
tell that turns out to be wrong, or that a better-stated tell replaces, is marked
`superseded` in place — never deleted. IDs are permanent so a note elsewhere that
cites `T007` still resolves years later.

**Every record carries provenance.** An unsourced tell is taste. A record needs a
short verbatim excerpt or a concrete example, where it was observed, and the date
it was captured. `Observed` is a URL, a publication, or `observed in own drafts` —
and `own drafts` is only honest when a real draft actually did it. A tell with no
observed instance does not go in this file.

**Division of labour with `banned.md`.** `banned.md` is the machine-checkable
lexicon: literal words and regexes that `check.py` parses and matches. This file
is the catalog of shapes, some of which no regex can catch. A tell that reduces to
a word or a pattern gets its record here *and* its line in `banned.md`; the record
says which.

**Fields**

| Field | Meaning |
|---|---|
| `Rank` | Reader weight. `professor-ranked N` = position in the ranked features of the MDPI study. `structural` = a habit the measured signature exposes, unranked. |
| `Signal` | What the tell is, in one or two sentences. |
| `Example` | A verbatim excerpt, or a pattern schema marked `(pattern)`. |
| `Observed` | Where it was seen. URL, publication, or `observed in own drafts`. |
| `Captured` | Date the record entered this catalog. |
| `Caught by` | `check.py`, `banned.md`, `read aloud`, or `judgment`. |
| `Status` | `active`, `delegated` (another skill owns it), or `superseded by TNNN`. |

Records with `Captured: 2026-07-31` are the catalog's founding set — the date this
skill's tell list is first attested in the record.

---

### T001 — Invented facts and sources

- **Rank:** professor-ranked 1
- **Signal:** A stated fact, number, or attribution that no primary source
  supports. The single strongest reader signal of machine authorship, and the one
  that costs the most when an expert reader catches it.
- **Example:** (pattern) any count, date, spec, or named external reference in the
  copy that the git history, issue tracker, or code does not settle.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2
- **Captured:** 2026-07-31
- **Caught by:** judgment — `honest-copy` tests 1, 3, 4, and 6
- **Status:** delegated to `honest-copy`. Listed here so the split between the two
  skills is legible from either side.

### T002 — Fabricated citations

- **Rank:** professor-ranked 2
- **Signal:** A source that does not exist, or a real source that does not say what
  the copy claims it says.
- **Example:** (pattern) a link, paper title, or "according to" clause that cannot
  be opened and read back to the claim it is supporting.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2
- **Captured:** 2026-07-31
- **Caught by:** judgment — `honest-copy`, verified against a primary source
- **Status:** delegated to `honest-copy`.

### T003 — Unnatural polish

- **Rank:** professor-ranked 3
- **Signal:** No contraction, no fragment, no sentence that opens on *And*. Nothing
  wrong anywhere. Uniform correctness reads as nobody — professors rank "no errors
  at all" among the strongest signals of machine authorship.
- **Example:** (pattern) a passage of five or more sentences with zero
  contractions and zero fragments.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2
- **Captured:** 2026-07-31
- **Caught by:** read aloud
- **Status:** active

### T004 — Repetition of shape

- **Rank:** professor-ranked 4
- **Signal:** The same sentence pattern three times running, or every paragraph
  opening on the same construction.
- **Example:** (pattern) three consecutive paragraphs beginning with the same
  first word or the same participial lead-in.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2
- **Captured:** 2026-07-31
- **Caught by:** `check.py` — it flags repeated openings
- **Status:** active

### T005 — Formulaic structure

- **Rank:** professor-ranked 5
- **Signal:** Generic opener, three body beats, summary close that restates the
  opener. Real posts start in the middle and stop when they are done.
- **Example:** (pattern) a closing paragraph whose content is already in the
  opening paragraph.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2
- **Captured:** 2026-07-31
- **Caught by:** judgment
- **Status:** active

### T006 — Complex syntax

- **Rank:** professor-ranked 6
- **Signal:** Nested subordinate clauses, and nominalizations — a verb wearing a
  noun costume. At full strength it produces a noun-pile appositive nobody would
  say aloud.
- **Example:** "Sixteen levels are the game as designed"
- **Observed:** observed in own drafts — lifted from a source code comment into
  store copy
- **Captured:** 2026-07-31
- **Caught by:** read aloud
- **Status:** active

### T007 — Difficult words

- **Rank:** professor-ranked 7
- **Signal:** Advanced vocabulary standing where a plain word would be more
  precise, not less.
- **Example:** *delve*, *tapestry*, *myriad*, *leverage*, *seamless* — the full
  list is `banned.md` §Word bans.
- **Observed:** https://www.mdpi.com/3042-8130/2/1/2 for the ranking;
  https://plusai.com/blog/the-most-overused-chatgpt-words/ for the vocabulary
- **Captured:** 2026-07-31
- **Caught by:** `banned.md` via `check.py`
- **Status:** active

### T008 — Uniform sentence length

- **Rank:** structural
- **Signal:** Machine drafts cluster at 15–20 words per sentence. Human writing
  varies hard. This is the strongest rhythm tell, and the one a formula can
  actually measure.
- **Example:** (pattern) a paragraph whose sentence lengths all fall inside a
  four-word band.
- **Observed:** https://vrid.ai/blog/signs-of-ai-writing and
  https://www.oliviacal.com/post/ai-writing-tells
- **Captured:** 2026-07-31
- **Caught by:** `check.py` — it measures mean and spread
- **Status:** active

### T009 — Tricolon

- **Rank:** structural
- **Signal:** Ideas grouped in threes, endlessly. One tricolon is rhetoric; every
  list of three is a fingerprint. Use two. Use four. Use seven.
- **Example:** (pattern) three consecutive lists or coordinate series each
  carrying exactly three items.
- **Observed:** https://gptzero.me/news/the-rule-of-three/
- **Captured:** 2026-07-31
- **Caught by:** judgment
- **Status:** active

### T010 — Uniform hedging

- **Rank:** structural
- **Signal:** Everything qualified to the same mild degree. One hedge in a
  paragraph is caution; four is a voice that will not stand behind anything.
- **Example:** *arguably*, *potentially*, *somewhat*, *tends to*, *it could be
  argued* — `banned.md` §Hedges carries the list.
- **Observed:** https://vrid.ai/blog/signs-of-ai-writing
- **Captured:** 2026-07-31
- **Caught by:** `banned.md` via `check.py`, flagged SOFT
- **Status:** active

### T011 — Em-dash asides

- **Rank:** structural
- **Signal:** An em-dash aside carrying work that belongs in a sentence of its own.
  The dash is not the problem; using it to avoid deciding what is the main clause
  is.
- **Example:** (pattern) two or more em-dash asides in one paragraph, each holding
  a full independent clause.
- **Observed:** https://www.oliviacal.com/post/ai-writing-tells
- **Captured:** 2026-07-31
- **Caught by:** read aloud
- **Status:** active

### T012 — Adjective inflation on abstract nouns

- **Rank:** structural
- **Signal:** A weighty adjective propping up a noun that names nothing you can
  point at. The adjective is doing the work the noun failed to do.
- **Example:** *profound impact*, *robust framework*, *transformative experience* —
  the adjectives are in `banned.md` §Word bans.
- **Observed:** https://plusai.com/blog/the-most-overused-chatgpt-words/
- **Captured:** 2026-07-31
- **Caught by:** `banned.md` via `check.py`
- **Status:** active

### T013 — The connector

- **Rank:** structural
- **Signal:** The signature machine connective. It promises a reveal and delivers a
  restatement. Banned outright — there is no sentence it improves.
- **Example:** "It's not just a level editor, it's a way of thinking about levels."
- **Observed:** https://vrid.ai/blog/signs-of-ai-writing
- **Captured:** 2026-07-31
- **Caught by:** `banned.md` §Structural bans — regex
  `\bit'?s not just \w+,? it'?s\b`, with `\bmore than just\b` and `\bnot just\b`
  covering the shorter forms
- **Status:** active

<!-- Append new tells below this line. Next free ID: T014. -->
