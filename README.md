# ai-content-editorial-lint

**Catch AI-content monoculture across a folder of posts and detect silent edits to an approved manuscript.**

[![test](https://github.com/Kein-chronicle/ai-content-editorial-lint/actions/workflows/test.yml/badge.svg)](https://github.com/Kein-chronicle/ai-content-editorial-lint/actions/workflows/test.yml) ![license](https://img.shields.io/badge/license-MIT-blue.svg) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

## Why

A batch of AI posts tends to open with the same heading and repeat the same disclaimer. `craft_lint.py` measures that across the corpus, and `fingerprint.py` freezes the approved text so an unreviewed edit is noticed before publishing.

## Install

**As a Claude Code skill** (Claude uses it when the task matches the skill description):

```sh
git clone https://github.com/Kein-chronicle/ai-content-editorial-lint.git ~/.claude/skills/ai-content-editorial-contract
```

For a single project, clone into `<project>/.claude/skills/ai-content-editorial-contract` instead, then start a new Claude Code session.

**As plain scripts:**

```sh
git clone https://github.com/Kein-chronicle/ai-content-editorial-lint.git
cd ai-content-editorial-lint
```

**Requires:** Python 3.10+.

## Quick start

Lint two folders and fingerprint a draft:

```console
$ bash examples/demo.sh
# 1. Do all posts open with the same first heading?
$ python3 scripts/craft_lint.py examples/posts-monoculture
monoculture: 6/6 articles (100%) open with the same H2 'quick answer' (max 40%)
[exit 1]

$ python3 scripts/craft_lint.py examples/posts-varied
clean (6 comparable articles)
[exit 0]

# 2. Freeze the approved manuscript, then notice silent edits
$ python3 scripts/fingerprint.py make .demo-tmp/post.md .demo-tmp/receipt.json
receipt written
[exit 0]

$ python3 scripts/fingerprint.py check .demo-tmp/post.md .demo-tmp/receipt.json
fingerprint matches
[exit 0]

# Someone quietly edits the approved text:  sed 's/approved body/quietly rewritten body/' post.md
$ python3 scripts/fingerprint.py check .demo-tmp/post.md .demo-tmp/receipt.json
DRIFT: text differs from the reviewed version - re-review required
[exit 1]
```

The output above is real: it is produced by the files in `examples/`.

## Use it on your own files

```sh
python3 scripts/craft_lint.py ./content/posts --max-share 0.4 --disclaimer "AI generated"
python3 scripts/fingerprint.py make post.md receipt.json
python3 scripts/fingerprint.py check post.md receipt.json
```

Sample inputs for every file format are in `examples/` and `tests/`; the details are in [SKILL.md](SKILL.md).

## What it checks

- `craft_lint.py DIR`: share of articles that start with the same first H2, disclaimer repetition (`--disclaimer`, `--max-disclaimers`), too small a corpus is exit `3` (unmeasured).
- `fingerprint.py make|check post.md receipt.json`: frontmatter minus volatile keys plus the normalized body; a status change is allowed, a body or metadata edit is `DRIFT`.

## Limits

- Structural checks only; it does not judge writing quality.

## Related projects

These solve neighbouring problems; use them when they fit better.

- **Vale**: prose style linter

## More from the same collection

Small, tested tools that grew out of running AI agents and game/app pipelines for months:

- [**llm-document-review-verifier**](https://github.com/Kein-chronicle/llm-document-review-verifier): Let the LLM propose, let code judge: quote verification, number and date parsing, a rule evaluator, and a stable issue ledger for document review.
- [**ai-resume-screening-safeguards**](https://github.com/Kein-chronicle/ai-resume-screening-safeguards): Safeguards for AI-assisted resume screening: lint rubrics for protected attributes, compute career facts in code, flag prompt injection in resumes.

## Development

```sh
python3 tests/run.py
```

The tests include inputs that are supposed to be rejected, so a green run also shows the checks can fail. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).

If this saved you a debugging session, a star helps other people find it. Bug reports and failing test cases are even better.

<sub>Keywords: content, blogging, seo, ai-generated-content, editorial, markdown, linter, claude-skills</sub>
