#!/usr/bin/env python3
"""craft_lint: detect template monoculture and disclaimer stuffing in a corpus of markdown articles.
exit 0 clean | 1 violations | 2 bad arguments or unreadable file | 3 corpus too small to measure (never a pass)
Counts markdown files except README/CHANGELOG/CONTRIBUTING/LICENSE and anything under hidden, node_modules or vendor folders. The first "##" heading outside a code fence is
the article's opening structure; articles with no "##" heading cannot be compared and are reported separately (too few comparable articles is exit 3)."""
import argparse, collections, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("dir"); ap.add_argument("--min-corpus", type=int, default=5)
ap.add_argument("--max-share", type=float, default=0.4, help="max share of articles starting with the same first H2")
ap.add_argument("--disclaimer", action="append", default=[], help="phrase counted per article")
ap.add_argument("--max-disclaimers", type=int, default=2)
a = ap.parse_args()
if a.min_corpus < 1: print("--min-corpus must be at least 1: an empty corpus proves nothing"); sys.exit(2)
if not os.path.isdir(a.dir): print(f"not a directory: {a.dir}"); sys.exit(2)
SKIP_DIRS = {"node_modules", "vendor", "dist", "build"}; SKIP_FILES = {"readme.md", "changelog.md", "contributing.md", "license.md", "code_of_conduct.md"}
files = []
for d, dirs, fs in os.walk(a.dir):
    dirs[:] = [x for x in dirs if not x.startswith(".") and x not in SKIP_DIRS]
    files += [os.path.join(d, f) for f in fs if f.endswith((".md", ".mdx")) and f.lower() not in SKIP_FILES]
first, bad, no_h2 = collections.Counter(), [], 0
def first_h2(t):
    fence = False
    for line in t.split("\n"):
        if line.lstrip().startswith(("```", "~~~")): fence = not fence; continue
        if not fence and re.match(r"^##\s+\S", line): return re.sub(r"^##\s+", "", line).strip().lower()
    return None
for f in files:
    try: t = open(f, encoding="utf-8").read().replace("\r\n", "\n")
    except (OSError, UnicodeError) as e: print(f"cannot read {f}: {type(e).__name__}"); sys.exit(2)
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    h = first_h2(t)
    if h: first[h] += 1
    else: no_h2 += 1
    for p in a.disclaimer:
        n = t.lower().count(p.lower())
        if n > a.max_disclaimers: bad.append(f"{f}: '{p}' appears {n}x (max {a.max_disclaimers})")
comparable = sum(first.values())
if comparable < a.min_corpus:
    print(f"UNMEASURED: {comparable} article(s) with a '##' heading ({no_h2} without one) < {a.min_corpus}; monoculture cannot be judged"); sys.exit(3)
h, n = first.most_common(1)[0]
if n / comparable > a.max_share:
    bad.append(f"monoculture: {n}/{comparable} articles ({n/comparable:.0%}) open with the same H2 '{h}' (max {a.max_share:.0%})")
print("\n".join(bad) if bad else f"clean ({comparable} comparable articles" + (f", {no_h2} without a '##' heading not compared" if no_h2 else "") + ")")
sys.exit(1 if bad else 0)
