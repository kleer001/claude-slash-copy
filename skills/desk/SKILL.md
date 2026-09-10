---
name: desk
description: >-
  Turn a dense draft — receipts, numbers, lists, notes-to-self — into one clean
  piece a stranger would read to the end, or a reference they can find one entry
  in, via a role chain: developmental editor, line editor, an isolated reader
  panel, and a reviser, bracketed by honesty and readability gates. Decides by
  genre whether a passage wants prose or bullets. TRIGGER when the user wants a
  draft made postable or readable, wants notes turned into prose, asks to polish
  or tighten a post, dev blog, essay, release write-up or announcement, asks
  whether something should be prose or a list, or hands over a draft that is
  correct but nobody would finish reading.
argument-hint: "[path/to/draft.md] [--panel role,role,role] [--cut-below \"marker\"]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, Skill
---

# copy:desk

The desk a draft crosses on its way to print. A sequence of roles, each one
transforming the text and handing it on. It is the light version of a
book-production pipeline, where a draft flows through role-personas in order.
No outline-looper machinery; just the roles.

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

This skill is **stage 4**, and it is the only one of the four that writes new
prose rather than correcting existing prose. That is why it carries its own copies
of the other three gates: whatever ran upstream audited a draft this skill is about
to replace.

**You draft. You never publish.** The output is a new file for the author to review.

## Input

The draft at `$ARGUMENTS`, or the newest markdown file in the working directory if
no path is given.

Many drafts carry working scaffolding below a marker — machine receipts, churn
tables, a commit appendix, raw notes. Read **only the narrative above it**. Pass
`--cut-below "<marker>"` to name that line; with no flag, look for a heading that
reads as a receipts or appendix section and confirm with the author before cutting.
Scaffolding never reaches the post.

## The role chain

Run these in order. Each stage receives the previous stage's output.

**0. Honesty gate (opening).** Run the `copy:honest` skill over the narrative before
any editing starts, and cut what it flags. A claim that will not survive the audit is
not worth developing, line-editing, or putting in front of three readers. Skip this
stage only when `copy:honest` ran on this same text immediately upstream.

**1. Developmental editor.** Find the single throughline — the one thing the piece
is about — and cut everything that doesn't serve it. Decide the order a *reader*
wants, which is rarely the order the work happened in. Produce a short beat outline
and a title.

Settle the shape here too, because it governs every stage below. Most drafts are
read start to finish and want prose. Some are consulted rather than read — an index,
a column glossary, a parts manifest, a checklist someone works through — and their
throughline is coverage: the reader needs to find one entry and leave, so a missing
entry is the defect and completeness is not padding. Name which kind the piece is
before outlining it.

**Then name the genre, because it sets the default form.** Prose is the default
everywhere. What genre decides is whether an *enumeration* inside the piece may be
set as a list. An enumeration is a set of parallel items where the reader wants to
find one or check membership — features, platforms, prices, supported formats,
steps, parameters, requirements, options.

| Genre | Enumerations |
|---|---|
| Marketing, store page, release notes | expected — set them as a list |
| Technical doc, reference, runbook | expected — set them as a list |
| Essay, argument, other non-fiction | usually a failure to argue — write the sentences |
| Fiction, story | never — no lists at all |
| Dev blog, announcement | prose, with a list only for a genuine enumeration |

The store page is the case the read-versus-consulted split gets wrong on its own:
it is read start to finish, so that split says prose, and it still wants its
feature list. Genre settles it. An essay is the mirror case — read the same way,
and its lists are almost always three fragments standing in for the sentence that
would have had to connect them.

**2. Line editor.** Write the piece from that outline.

- **Prose by default; enumerations follow the genre named in stage 1.** A list earns
  its place when each entry is a thing the reader might be looking for, and the
  entries do not argue with each other. It fails when it stands in for an argument
  the draft never made — three fragments where a sentence would have been forced to
  say how they connect. Convert that second kind to sentences. In fiction, convert
  both kinds. Hold every surviving entry to the same standard as a sentence: no
  filler entries, no entry that exists only to make the list longer, and **25 words
  maximum** — one claim plus at most one supporting clause. A bullet that has grown
  an explanatory tail has stopped being scannable, which was the only reason to set
  it as a bullet.
- **Few numbers.** Keep the one or two load-bearing figures that actually punch; drop
  the rest and all methodology. When in doubt, ask the author which numbers stay —
  they usually have a specific contrast in mind.
- **Timestamps sparingly.** Keep only the few that set real pace; cut the rest to
  plain phrasing.
- Run the `copy:plain` skill over the result — gloss or cut every internal term.
- Keep the author's voice. Match the register of the draft; do not add hype.

**3. Reader panel.** Three readers, spawned **concurrently as separate subagents**
with the `Agent` tool, each handed the full line-edited draft in its prompt.

The isolation is the point: each reader must see the draft and nothing else — not
the other readers' reactions, not the earlier stages, not the scaffolding. Three
reactions that could see each other would converge into one, and the panel would be
worth no more than a single pass. Never simulate the panel inline in the main thread.

The default triptych are codified agents, not personas to improvise:

| `agentType` | Reads as | Flags |
|---|---|---|
| `reader-insider` | someone who works in the subject | hand-waving, claims that skip a step |
| `reader-outsider` | interested, no background | jargon, density, the paragraph they bounce off |
| `reader-skeptic` | allergic to being sold to | the moment it reads like an ad or a victory lap |

Each is defined with **no tools at all**, so the sandbox holds structurally rather than
by instruction: a reader cannot open the source draft, the receipts, or anything else.
The draft in its prompt is the whole of what it can see.

A project that defines an agent of the same name under its own `.claude/agents/`
overrides the default automatically — project scope outranks plugin scope — so a repo
can sharpen a reader for its own audience without touching this skill.

`--panel role,role,role` names roles for the subject instead: a music post might want
*producer, listener, crate-digger*; a short story *genre reader, cold reader, editor*.
Roles named this way are spawned ad-hoc, still concurrently and still isolated. Keep
three, keep them distinct, and keep at least one who does not already care about the
subject — that is the reader who detects density, and the easiest one to drop by accident.

Each reader returns four things: where they skimmed or got lost, what read as
hand-waving or jargon, what they would cut, and the one line that earned their trust.

**4. Reviser.** Fold the panel's notes into a final draft. Where two readers flag the
same spot, fix it. Where they disagree, side with the outsider on clarity and the
skeptic on tone.

**5. Closing gates.** The tail of the chain, run over the revised piece in this
order. Each one covers text that did not exist when it last ran: stages 2 and 4 both
write new prose, so an upstream pass audited a draft that no longer exists.

1. **`copy:plain`** — the reviser can reintroduce a term the stage-2 pass removed.
2. **`copy:humanize`** — including `check.py` against the surface's word budget. This
   is the last measurement the piece gets, because nothing downstream of this skill
   measures anything. It is what stands between the output and a 40-word bullet.
3. **`copy:honest`** — a piece that now reads well can still claim more than it earned.

Report the `check.py` numbers alongside the output.

## Output

Write the clean piece beside the draft as `<draft-stem>.post.md`, leaving the
original untouched as the working source of record. Show the post, name the file,
and remind the author it is a draft for them to review and publish themselves.
