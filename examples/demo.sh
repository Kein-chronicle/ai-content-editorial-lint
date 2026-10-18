#!/usr/bin/env bash
# Shows both tools on small synthetic data. Output is deterministic.
cd "$(dirname "$0")/.."
run() { printf '$ %s\n' "$*"; "$@"; printf '[exit %s]\n\n' "$?"; }
tmp=.demo-tmp; rm -rf "$tmp"; mkdir "$tmp"; trap 'rm -rf "$tmp"' EXIT

echo "# 1. Do all posts open with the same first heading?"
run python3 scripts/craft_lint.py examples/posts-monoculture
run python3 scripts/craft_lint.py examples/posts-varied

echo "# 2. Freeze the approved manuscript, then notice silent edits"
cp examples/draft.md "$tmp/post.md"
run python3 scripts/fingerprint.py make  "$tmp/post.md" "$tmp/receipt.json"
run python3 scripts/fingerprint.py check "$tmp/post.md" "$tmp/receipt.json"
echo "# Someone quietly edits the approved text:  sed 's/approved body/quietly rewritten body/' post.md"
sed -i.bak 's/approved body/quietly rewritten body/' "$tmp/post.md"
run python3 scripts/fingerprint.py check "$tmp/post.md" "$tmp/receipt.json"
