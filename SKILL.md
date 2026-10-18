---
name: ai-content-editorial-contract
description: An operating contract for AI-assisted publishing (blogs, guides, game/tech articles, video scripts from research) that keeps facts, rights and readability under control. Use when an AI drafts content from web sources, when all your articles start to look identical, when summarizing tools misquote sources, when you need an independent reviewer that actually converges, or when a reviewed manuscript must not be silently edited before publishing. Includes a monoculture linter and a manuscript fingerprint gate.
---

# ai-content-editorial-contract

Governance: **AI collects and drafts; a person confirms facts, experience and rights before anything goes public.**
Never describe this as "automated publishing without review". Files, not vibes, hold approval (unapproved drafts stay private).

## Rights rule

*Citing a source is not permission to use it.* Use material you made yourself or whose terms you checked. Use videos
and articles as **research sources** (record timestamps/URLs), never re-publish them. No disclosure boilerplate
stuffed into the body; if you disclose AI involvement, do it once, deliberately.

## Pipeline: research -> brief -> outline -> draft -> independent review -> verify -> human approval -> publish

Design guidance: record a stage receipt (a hash of the report) at each checkpoint, and let going back a stage invalidate all later receipts. The scripts here implement only the manuscript fingerprint and the craft lint below.

### Claims ledger
Every factual sentence is a claim row: statement, source(s), passage anchor, strength (`primary|secondary|inference`),
`critical` flag. Rules that came from real failures:

1. **Verbatim or no quotation marks.** Summarising fetchers (cheap models behind a "fetch URL" tool) mis-transcribed a
   test condition and altered quotes. Re-open the original; ask the fetcher for verbatim text; if unverified, paraphrase
   without quote marks. Snippet-only sources never go into the body.
2. **Never state stronger than the source.** Source: "you can skip it if you do not own the optional adapter". Draft: "unusable
   without the adapter". Put your interpretation in the ledger as `inference` and say "this article's reading is..." in the text.
3. **Do not fake primary evidence.** If you could not open the official source, say so once; use values on which >=2
   independent sources agree; mark them non-critical. Critical+primary only for text you actually saw.
4. **Negative statements are the most dangerous** ("the source doesn't mention X"): grep the full source text first.
5. **"Consensus" needs a count** ("three or more sources"); one or two voices are "sources disagree".
6. **The same host is one source.** Keep your own blocklist of SEO farms, spam and hijacked domains (not provided here).
7. **Ledger vs body drift:** after every body edit, check (with your own script; none is provided here) that anchors/value phrases still occur in the body.
   If a fact changes, go back to research and re-pass; don't fix the prose only.

### Independent review
- Fresh reviewer who did not write it, opens the original sources, and reads as a **zero-prior-knowledge reader**.
  No machine check can judge undefined jargon; this reviewer is the only detector. Authors must not stand in.
- **Put the blocker definition at the top of the reviewer prompt:** blocker = factual error, attribution not in the source,
  statement that misleads, omission that blocks a decision. Taste goes to recommendations. Before this, taste items kept
  reviews from ever converging; after, 1 issue.
- Expect several rejections; each had a real error. Continue the same reviewer for "confirm fix + look for new errors" when
  the fix is local. The last review must re-open sources again if the last edit touched facts.
- Your own "helpful" additions during fixes create the next error. Fixes may only use words that are in the sources.

### Craft: the monoculture problem
Gates that test truth but not readability let an AI stamp dozens of articles with the same first heading and a wall of
disclaimers. The prompt had said "follow existing articles' format". Remove format-copy instructions; keep structural rules in one craft doc.
`scripts/craft_lint.py` flags corpora where one opening heading dominates and caps disclaimer repetition.
Also: do not repeat the same conclusion four times (summary, verdict, "shortest", recap).

### Fingerprint gate
Hash the reviewed manuscript (frontmatter minus status fields + normalized body). The build fails if the published text
differs from the reviewed receipt (frontmatter order is part of the hash: reordering list items is an edit). If you want to allow meaning-neutral metadata edits,
build an explicit, logged amendment path yourself; this script has none. The receipt is not a signature: keep it where only the reviewer can write.

### Process traps
- `test pass != build pass` when tests read a stale build output directory. Run both after changing manuscripts or pipeline code.
- Adding a value to one enum list but not the content schema passes synthetic tests and breaks the real build; add a test
  that the two lists are equal, and grep for every place a new value must be registered.
- Contract version bumps: grep every exact-equality version comparison; use `>=` and keep older gates alive.
- Date comparisons: parse content dates in the site's timezone or the post disappears for hours after midnight.
- Never filter a command's output through `grep` and conclude success; check the stage status explicitly. Define shell
  variables in the same command that uses them.
- Deploy only after the human says so; confirm the rebuilt artifact fingerprint equals the verify receipt.

```bash
python3 scripts/craft_lint.py articles/ --min-corpus 5 --max-share 0.4 --disclaimer "AI generated" --max-disclaimers 2
python3 scripts/fingerprint.py make post.md receipt.json    # after review
python3 scripts/fingerprint.py check post.md receipt.json   # in the build; exit 1 on drift
python3 tests/run.py
```
