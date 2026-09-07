---
name: copy-desk
description: >-
  Turn a dense draft — receipts, numbers, lists, notes-to-self — into one clean
  piece of prose a stranger would read to the end, via a role chain:
  developmental editor, line editor, an isolated reader panel, and a reviser.
  TRIGGER when the user wants a draft made postable or readable, wants notes
  turned into prose, asks to polish or tighten a post, dev blog, essay, release
  write-up or announcement, or hands over a draft that is correct but nobody
  would finish reading.
argument-hint: "[path/to/draft.md] [--panel role,role,role] [--cut-below \"marker\"]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent, Skill
---

# copy-desk

The desk a draft crosses on its way to print. Four roles in sequence, each one
transforming the text and handing it on.

Three sibling skills each ask public copy a single question — `honest-copy` asks
*is this true?*, `humanized-copy` asks *would anyone say this?*, `unpack-jargon`
asks *can this reader parse it?* This one asks **will anyone read it to the end?**
and answers it with a chain rather than an audit.

The chain is the light version of a book-production pipeline, where a draft flows
through role-personas in order. No outline-looper machinery; just the roles.

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

**1. Developmental editor.** Find the single throughline — the one thing the piece
is about — and cut everything that doesn't serve it. Decide the order a *reader*
wants, which is rarely the order the work happened in. Produce a short beat outline
and a title.

**2. Line editor.** Write the piece from that outline in flowing prose.

- **No bullet lists.** If the draft made a point with a list, make it with sentences.
- **Few numbers.** Keep the one or two load-bearing figures that actually punch; drop
  the rest and all methodology. When in doubt, ask the author which numbers stay —
  they usually have a specific contrast in mind.
- **Timestamps sparingly.** Keep only the few that set real pace; cut the rest to
  plain phrasing.
- Run the `unpack-jargon` skill over the result — gloss or cut every internal term.
- Keep the author's voice. Match the register of the draft; do not add hype.

**3. Reader panel.** Three readers, spawned **concurrently as separate subagents**
with the `Agent` tool, each handed the full line-edited draft in its prompt.

The isolation is the point: each reader must see the draft and nothing else — not
the other readers' reactions, not the earlier stages, not the scaffolding. Three
reactions that could see each other would converge into one, and the panel would be
worth no more than a single pass. Never simulate the panel inline in the main thread.

Name the roles for the subject at hand with `--panel`. The default triptych:

| Role | Reads as | Flags |
|---|---|---|
| **insider** | someone who works in the subject | hand-waving, claims that skip a step |
| **outsider** | interested, no background | jargon, density, the paragraph they bounce off |
| **skeptic** | allergic to being sold to | the moment it reads like an ad or a victory lap |

Rename them to fit — a music post might want *producer, listener, crate-digger*; a
short story *genre reader, cold reader, editor*. Keep three, keep them distinct, and
keep at least one who does not already care about the subject.

If the repository defines matching reader agents under `.claude/agents/`, use those
definitions rather than improvising: a codified reader is sharper than an ad-hoc one.

Each reader returns four things: where they skimmed or got lost, what read as
hand-waving or jargon, what they would cut, and the one line that earned their trust.

**4. Reviser.** Fold the panel's notes into a final draft. Where two readers flag the
same spot, fix it. Where they disagree, side with the outsider on clarity and the
skeptic on tone.

**5. Honesty gate.** Run the `honest-copy` skill on the result and apply its fixes.
A piece that now reads well can still claim more than it earned.

## Output

Write the clean piece beside the draft as `<draft-stem>.post.md`, leaving the
original untouched as the working source of record. Show the post, name the file,
and remind the author it is a draft for them to review and publish themselves.
