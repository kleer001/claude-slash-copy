# CLAUDE.md — claude-slash-copy

A Claude Code plugin: four skills that check public-facing copy, plus the three
reader agents `copy:desk` spawns.

## Layout

```
.claude-plugin/plugin.json        plugin identity
.claude-plugin/marketplace.json   marketplace entry; lists the four skills in canonical order
agents/reader-{insider,outsider,skeptic}.md
skills/{honest,plain,humanize,desk}/SKILL.md
skills/plain/detect.py            jargon candidate detector
skills/plain/terms.md             house term list, parsed by detect.py
skills/humanize/check.py          length, reading grade, banned constructions
skills/humanize/banned.md         ban rules, parsed by check.py
skills/humanize/tells.md          the AI-writing tell catalog
```

## Constraints that are easy to break

**The chain block is duplicated verbatim in all four SKILL.md files.** This is
deliberate: skills load independently, and a skill that had to read a sibling
file to learn its own position would pay a read hop for it. The cost is that the
four copies must stay byte-identical. Change one, change all four, and verify:

```sh
for f in skills/*/SKILL.md; do
  awk '/^## The chain$/{p=1} p{print} /each stands alone\.$/{if(p)exit}' "$f" | md5sum
done   # four identical hashes
```

**Paths to bundled files use `${CLAUDE_PLUGIN_ROOT}`.** A hardcoded home
directory works on one machine and breaks for everyone who installs the plugin.
This applies to any path a skill hands to a subagent or prints as a command.

**Project-override paths are relative and stay relative.** `check.py` and
`detect.py` walk up from the file being checked looking for
`.claude/skills/copy/humanize/banned.md` and `.claude/skills/copy/plain/terms.md`.
Both scripts resolve their own house list via `Path(__file__).parent`, so neither
needs to know where the plugin lives.

**Rules live in the data files, not in the scripts.** Editing `banned.md`
retunes the linter with no code change; section headers route the parse, so
renaming a header silently drops its entries. Same for `terms.md`.

**No references to private or machine-local resources.** This plugin is
installed by people who have neither. Anything a reader cannot follow is either
inlined or cut.

## Testing

Both scripts are standard-library Python 3 and run directly:

```sh
skills/humanize/check.py --budget 200 path/to/copy.md   # exits 1 on hard failure
skills/plain/detect.py --audience "who" path/to/copy.md
```

`detect.py` reads `/usr/share/dict/american-english` (or british-english, or
words). Without one its dictionary signal goes quiet; the other four signals are
unaffected.

## Adding a tell

`tells.md` requires a real observed instance — a draft, a published page, a
quoted example from a study. A shape you can imagine a model producing is not a
tell. Record provenance and capture date, append with the next free ID, and
never reuse an ID. When a better-stated tell replaces an old one, mark the old
`superseded by TNNN` and leave it in place.

## Conventions

Commits: `type(scope): short description`, body explains why. Scope is the skill
name where the change is local to one (`fix(humanize): ...`), `copy` where it
spans the plugin.
