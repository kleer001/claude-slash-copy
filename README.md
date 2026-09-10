# copy

Four editing skills for Claude Code that check public-facing copy, each asking a
different question. Run one alone, or all four in order.

| stage | skill | asks | what it does |
|---|---|---|---|
| 1 | `copy:honest` | is this true? | audits every claim against the record — git history, the issue tracker, the code |
| 2 | `copy:plain` | can this reader parse it? | finds the jargon a *named* reader cannot parse, and decides replace-or-gloss for each term |
| 3 | `copy:humanize` | would anyone say this? | cuts to a word budget, strips machine tells, holds a reading-grade ceiling |
| 4 | `copy:desk` | will anyone read it to the end? | runs a draft through an editorial role chain and an isolated reader panel |
| 5 | `copy:honest` | is it *still* true? | the closing gate |

`copy:honest` runs at both ends. At the head it is triage: a claim that won't
survive isn't worth line-editing. At the tail it is the gate — a rewrite for
rhythm turns a hedged claim into a confident one.

Ask for "the copy skills" or "the copy pipeline" to run the whole chain. Name one
skill to run only that one.

## Install

```
/plugin marketplace add kleer001/claude-slash-copy
/plugin install copy@copy
```

## What each one is

**`copy:honest`** — six tests for claims the record does not support: invented
first-person experience, assertions about what the reader has done, unverified
ordinals and superlatives, implied repetition, emotional filler, and claims the
build does not keep across its whole range. Every flag carries evidence: a
file:line, a commit, a command's output. A flag without evidence is an opinion.

**`copy:plain`** — a writer cannot find their own jargon, because knowing a
subject makes it feel simple. This one names an audience first, then runs
`skills/plain/detect.py` to surface five kinds of candidate: undefined
load-bearing terms, unexpanded acronyms, words no dictionary holds, definite
references to things never introduced, and repeated hyphenated coinages.
Decisions are recorded in `terms.md` so the tenth run on a project is quieter
than the first.

**`copy:humanize`** — length is a rule, not a preference: a store description
gets 200 words, a social post 50, a bullet 25. `skills/humanize/check.py`
measures reading grade, mean sentence length, length spread and banned
constructions, and exits non-zero on a hard failure. The tell catalog in
`tells.md` requires a real observed instance for every entry; an imagined
failure mode is not a tell.

**`copy:desk`** — the only skill that writes new prose rather than correcting
existing prose. A developmental editor finds the throughline and names the
genre, a line editor writes from that outline, three reader agents read the
result in isolation, and a reviser folds in their notes. Because it generates
text the upstream passes never saw, it carries its own copies of all three
gates and closes with a measurement.

## Bullets are a genre decision

`copy:desk` decides prose-versus-list by genre, not by taste. Prose is the
default everywhere; genre decides whether an *enumeration* inside the piece may
be set as a list.

| Genre | Enumerations |
|---|---|
| Marketing, store page, release notes | expected — set them as a list |
| Technical doc, reference, runbook | expected — set them as a list |
| Essay, argument, other non-fiction | usually a failure to argue — write the sentences |
| Fiction, story | never |
| Dev blog, announcement | prose, with a list only for a genuine enumeration |

## The reader panel

`copy:desk` spawns three agents concurrently, each handed the draft and nothing
else. Isolation is the point: three reactions that could see each other would
converge into one.

| agent | reads as | flags |
|---|---|---|
| `reader-insider` | someone who works in the subject | hand-waving, claims that skip a step |
| `reader-outsider` | interested, no background | jargon, density, the paragraph they bounce off |
| `reader-skeptic` | allergic to being sold to | the moment it reads like an ad or a victory lap |

Each ships with **no tools at all**, so the sandbox holds structurally rather
than by instruction — a reader cannot open the source draft or the receipts.
`--panel role,role,role` swaps in ad-hoc roles for a different subject. A repo
that defines an agent of the same name under its own `.claude/agents/` overrides
the default.

## Per-project overrides

Two lists take project-local overlays, found by walking up from the file being
checked:

- `.claude/skills/copy/humanize/banned.md` — adds bans; its `## Exceptions`
  spare words the house list would otherwise flag.
- `.claude/skills/copy/plain/terms.md` — domain vocabulary and recorded
  decisions, so the same terms are not re-litigated for every new memo.

A word that is a tell in general copy can be the exact word one audience
searches for; that is what `## Exceptions` is for. Both runs print which project
list was applied, so a spared word is traceable to the file that spared it.

## Layout

```
.claude-plugin/       plugin.json, marketplace.json
agents/               the three reader agents copy:desk spawns
skills/honest/        SKILL.md
skills/plain/         SKILL.md, detect.py, terms.md
skills/humanize/      SKILL.md, check.py, banned.md, tells.md
skills/desk/          SKILL.md
```

## Requirements

Python 3 for the two scripts, both standard library only. `detect.py` reads a
system word list from `/usr/share/dict/`; without one, its dictionary signal
goes quiet and the other four still work.

## License

MIT
