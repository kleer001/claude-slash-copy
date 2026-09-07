#!/usr/bin/env python3
"""Mechanical jargon detector for plain-copy.

Finds candidate terms a named audience may not parse. It does not decide what to
do with them -- necessity is a judgement the skill method makes, and the same
word is required vocabulary for one reader and a wall for another.

Self-review is the one method known to fail here: fluency with a subject reads
to the writer as the subject being simple, so a writer cannot see their own
jargon. This script is the outside reader.

Signals, strongest first:
  1. Acronym used with no expansion anywhere before it.
  2. Word absent from the system dictionary -- high precision for domain terms
     and proper nouns, poor recall (it misses "culvert", "proponent").
  3. Word listed as a domain term by the project's terms.md.
  4. Definite reference ("the X") to something never introduced, where X is
     already a candidate by 2 or 3. Ungated, this signal is mostly noise.
  5. A hyphenated or repeated multi-word term of art.
  6. An ordinary word carrying a technical meaning the document never states --
     high use with no definition anywhere, or a definition that arrives after
     first use. This is the signal the dictionary cannot give: "pass", "reader"
     and "wave" are all ordinary English and all opaque as terms.

Decisions live in terms.md beside this script, and in the project's own
`.claude/skills/plain-copy/terms.md`. A term recorded as fine for an audience
stops being reported, so a second run on the same project is quieter than the
first. That accumulation is the point.

Usage:
  ./detect.py --audience "discipline lead" path/to/copy.md
  ./detect.py --audience "general public" --all path/to/copy.md   # include tables
"""
import argparse
import re
import sys
from pathlib import Path

DICTS = [Path("/usr/share/dict/american-english"), Path("/usr/share/dict/british-english"),
         Path("/usr/share/dict/words")]
HOUSE_TERMS = Path(__file__).parent / "terms.md"
PROJECT_REL = Path(".claude") / "skills" / "plain-copy" / "terms.md"


def project_terms(target):
    """Nearest terms.md at or above the file being checked.

    Resolving this from the working directory instead silently drops every
    recorded decision whenever the script is run from anywhere else, and the
    only symptom is a report that got louder.
    """
    d = Path(target).resolve().parent
    for base in [d, *d.parents]:
        cand = base / PROJECT_REL
        if cand.exists():
            return cand
    return None

# Words that look like domain terms to a dictionary but carry no load.
IGNORE = {
    "http", "https", "com", "org", "www", "md", "py", "json", "html", "csv",
    "todo", "eg", "ie", "etc", "vs",
}


def load_terms(path):
    """Parse a terms.md into {section: {term: note}}. Sections are ## headers."""
    out = {}
    if not path or not path.exists():
        return out
    section = None
    for line in path.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            section = h.group(1).strip().lower()
            out[section] = {}
            continue
        if section is None or not line.strip().startswith("-"):
            continue
        body = line.strip().lstrip("-").strip()
        if not body:
            continue
        term, _, note = body.partition(":")
        out[section][term.strip().lower()] = note.strip()
    return out


def merge_terms(target):
    """Project file overlays the house file. Project decisions win."""
    house = load_terms(HOUSE_TERMS)
    found = project_terms(target)
    for sec, items in load_terms(found).items():
        house.setdefault(sec, {}).update(items)
    return house, found


def load_dictionary():
    """Every dictionary on the box. American-only flags every British spelling."""
    vocab = set()
    for d in DICTS:
        if d.exists():
            vocab |= {w.strip().lower() for w in d.read_text(
                encoding="utf-8", errors="replace").splitlines() if w.strip()}
    return vocab or None


# Ordinary morphology a base dictionary does not carry. Strip before deciding a
# word is domain vocabulary, or "searchable" and "unsorted" read as jargon.
PREFIXES = ("un", "re", "under", "over", "non", "pre", "post", "mis", "de")
SUFFIXES = ("s", "es", "ed", "ing", "er", "ers", "est", "ly", "able", "ible",
            "ness", "less", "ful", "ise", "ize", "ised", "ized")


def known(w, vocab):
    """True when w is the dictionary's, or a plain inflection of something in it."""
    if w in vocab:
        return True
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            stem = w[: -len(suf)]
            if stem in vocab or stem + "e" in vocab or (
                    stem and stem[-1] == stem[-2:-1] and stem[:-1] in vocab):
                return True
    for pre in PREFIXES:
        if w.startswith(pre) and len(w) - len(pre) >= 4:
            rest = w[len(pre):].lstrip("-")
            if rest in vocab or known(rest, vocab):
                return True
    if "-" in w:
        return all(known(part, vocab) for part in w.split("-") if len(part) > 2)
    return False


def split_prose(text, keep_all=False):
    """Prose only by default. A table of domain terms is the payload, not a leak."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    lines = []
    for ln in text.splitlines():
        if not keep_all and (ln.lstrip().startswith("|") or re.match(r"^\s*\|?-{3,}", ln)):
            continue
        lines.append(re.sub(r"^#{1,6}\s+", "", ln))
    out = "\n".join(lines)
    out = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", out)     # links to their text
    return out


def acronyms(text):
    """Initialisms with no expansion before first use.

    A gloss counts when the initials of nearby capitalised words match, in
    either order. An adjacent capitalised word that does not match the initials
    is reported as a weak gloss for a human to judge -- "HPAC Pacific" explains
    the code without expanding it.
    """
    hits = {}
    for m in re.finditer(r"\b([A-Z][A-Z0-9]{1,6})\b", text):
        a = m.group(1)
        if a.lower() in IGNORE or a in hits:
            continue
        before = text[:m.start()]
        window = text[max(0, m.start() - 200): m.end() + 200]
        initials = "".join(w[0] for w in re.findall(r"\b([A-Za-z])[a-z]{1,}", window))
        expanded = a.lower() in re.sub(r"[^a-z]", "", initials.lower())
        if re.search(rf"\b{re.escape(a)}\b\s*[=:]\s*\w", window) or \
           re.search(rf"\({re.escape(a)}\)", before):
            expanded = True
        tail = re.sub(r"[`*_]", "", text[m.end(): m.end() + 40])
        weak = bool(re.match(r"[\s,]+[A-Z][a-z]+", tail))
        if not expanded:
            hits[a] = ("weak gloss nearby" if weak else "no expansion")
    return hits


def rare_words(text, vocab, domain, seen_acronyms):
    """Words no dictionary holds, or the project has named as domain vocabulary."""
    hits = {}
    lowered = {a.lower() for a in seen_acronyms}
    for m in re.finditer(r"\b([a-z][a-z'-]{3,})\b", text.lower()):
        w = m.group(1).strip("-'")
        if w in hits or w in IGNORE or len(w) < 4 or w in lowered:
            continue
        if w in domain:
            hits[w] = "listed as a domain term"
        elif vocab is not None and not known(w, vocab):
            hits[w] = "no dictionary holds it"
    return hits


def dangling_definites(text, candidates):
    """'the X' where X was never introduced and is already a candidate."""
    hits = {}
    for m in re.finditer(r"\bthe ([a-z][a-z-]{3,})\b", text.lower()):
        n = m.group(1)
        if n in hits or n not in candidates:
            continue
        before = text[:m.start()].lower()
        introduced = re.search(
            rf"\b(?:a|an|one|each|every|our|this) {re.escape(n)}\b"
            rf"|{re.escape(n)}\s+(?:is|are|means)\b"
            rf"|call (?:it|them|this) the {re.escape(n)}", before)
        if not introduced:
            hits[n] = "definite reference, never introduced"
    return hits


# Function words. A frequency signal without these is a list of "the" and "of".
STOP = set("""a an the and or but nor for so yet of in on at to from by with without
into onto over under above below between among through during before after since until
is are was were be been being am do does did done has have had having will would shall
should can could may might must this that these those it its it's they them their there
here what which who whom whose when where why how all any both each few more most other
some such no not only own same than too very just also then once about against
one two three four five six seven eight nine ten first second next last
you your we our us i me my he she his her him
if while because as up down out off again further once every either neither
per via across within upon whether though although however therefore thus hence
document documents value values page pages column columns row rows file files
run runs read reads write writes name names number numbers text list lists
work works case cases part parts side sides thing things way ways time times
does not don't cannot""".split())

# Constructions that introduce a term. "**pass** --" is the markdown definition shape.
def _defined_at(word, text):
    w = re.escape(word)
    pats = [rf"\*\*{w}s?\*\*[^\n]{{0,4}}(?:—|--|:|,| is | are | means )",
            rf"\b(?:an?|the|one) {w}\b[^.\n]{{0,20}}?\b(?:is|are|means)\b",
            rf"\b{w}s?\b\s*(?:—|--)\s*[a-z]",
            rf"\b{w}s?\b[^.\n]{{0,10}}\bmeaning\b",
            rf"\bcall (?:it|them|this) (?:a |the )?{w}\b",
            rf"\b{w}s?\b\s*\([a-z][^)]{{8,}}\)"]
    for pat in pats:
        m = re.search(pat, text, re.I)
        if m:
            return m.start()
    return None


def load_bearing(text, threshold=8):
    """Ordinary words carrying a technical meaning the document never states.

    The dictionary cannot find these -- "pass", "reader", "wave" are all in it.
    What marks them is weight without introduction: a word an author reaches for
    a dozen times and never defines is load-bearing, and a reader who guesses
    wrong about it guesses wrong for the whole document.
    """
    counts = {}
    first = {}
    for m in re.finditer(r"\b([a-z][a-z-]{2,})\b", text.lower()):
        w = m.group(1)
        if w in STOP or len(w) < 3:
            continue
        # a term of art is a noun; -ed and -ing forms are the verb doing its job
        if w.endswith(("ed", "ing")) and w[:-2] not in ("fe", "se"):
            continue
        counts[w] = counts.get(w, 0) + 1
        first.setdefault(w, m.start())
    out = {}
    for w, n in counts.items():
        if n < threshold:
            continue
        at = _defined_at(w, text)
        if at is None:
            out[w] = (f"used {n} times, never defined", first[w], None)
        elif at > first[w]:
            out[w] = (f"used {n} times, defined after first use", first[w], at)
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def terms_of_art(text):
    """Hyphenated compounds used as a single unit, repeated.

    Repetition is what separates a coined term from an ad-hoc hyphenation. A
    term of art gets reused because the writer needs it again; "under-report"
    is written once and never returns.
    """
    counts = {}
    for m in re.finditer(r"\b([a-z]{2,}-[a-z]{2,}(?:-[a-z]{2,})?)\b", text.lower()):
        counts[m.group(1)] = counts.get(m.group(1), 0) + 1
    return {t: f"used {n} times as one term" for t, n in counts.items()
            if n >= 2 and len(t) > 7}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--audience", required=True,
                    help="who reads this; the necessity test has no answer without it")
    ap.add_argument("--all", action="store_true", help="include tables and lists")
    a = ap.parse_args()

    text = split_prose(Path(a.path).read_text(encoding="utf-8"), a.all)
    vocab = load_dictionary()
    terms, project_file = merge_terms(a.path)

    domain = set(terms.get("domain terms", {}))
    fine = set(terms.get("decided - fine as-is", {}))
    gloss = terms.get("decided - keep and gloss", {})
    replace = terms.get("decided - replace", {})

    ac = acronyms(text)
    rare = rare_words(text, vocab, domain, set(ac))
    dang = dangling_definites(text, set(rare) | domain)
    art = terms_of_art(text)
    heavy = load_bearing(text)

    print(f"{a.path}")
    print(f"  audience: {a.audience}")
    if vocab is None:
        print("  NOTE: no system dictionary; dictionary signal is off")
    if project_file:
        print(f"  decisions: {project_file}")
    else:
        print(f"  NOTE: no {PROJECT_REL} found at or above this file -- "
              "decisions from this run will not be remembered")

    heavy_flat = {}
    for w, (why, fpos, dpos) in heavy.items():
        heavy_flat[w] = (f"{why} (first at line {line_of(text, fpos)}"
                         + (f", defined at line {line_of(text, dpos)})" if dpos else ")"))

    buckets = [
        ("undefined load-bearing terms", heavy_flat),
        ("acronym with no expansion", ac),
        ("candidate domain terms", rare),
        ("undefined definite reference", dang),
        ("terms of art", art),
    ]
    total = decided = 0
    for label, hits in buckets:
        live = {}
        for t, why in sorted(hits.items()):
            key = t.lower()
            if key in fine:
                decided += 1
                continue
            if key in gloss:
                live[t] = f"{why}  -> recorded gloss: {gloss[key]}"
            elif key in replace:
                live[t] = f"{why}  -> recorded replacement: {replace[key]}"
            else:
                live[t] = why
        if not live:
            continue
        print(f"\n  {label} ({len(live)})")
        for t, why in live.items():
            print(f"     {t:26s} {why}")
        total += len(live)

    print(f"\n  {total} to decide, {decided} already settled for this project")
    if total:
        print("  Decide each: replace it, or keep it and gloss it at first use.")
        dest = project_file or PROJECT_REL
        print(f"  Record the decision in {dest} so the next run is quieter.")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
