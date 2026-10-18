#!/usr/bin/env python3
"""Manuscript fingerprint: frontmatter (minus volatile keys, in its ORIGINAL order) + normalized body. usage: fingerprint.py make|check post.md receipt.json
exit 0 receipt written / text matches | 1 DRIFT or no receipt | 2 bad usage or unreadable file.
The receipt is a plain hash file, not a signature: whoever can edit the post can also run `make` again, so keep receipts where only the reviewer can write."""
import hashlib, json, re, sys
IGNORE = {"status", "approved", "updated", "draft"}

def fp(path):
    t = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", t, flags=re.S)
    fm, body = (m.group(1), m.group(2)) if m else ("", t)
    keep = [l for l in fm.split("\n") if l.split(":")[0].strip() not in IGNORE]
    # no sorting: reordering list items or lines is an edit
    norm = "\n".join(x.rstrip() for x in keep if x.strip()) + "\n--\n" + re.sub(r"[ \t]+\n", "\n", body).strip()
    return hashlib.sha256(norm.encode()).hexdigest()

if len(sys.argv) != 4 or sys.argv[1] not in ("make", "check"): print(__doc__); sys.exit(2)
cmd, post, rec = sys.argv[1:]
try: open(post, encoding="utf-8").close()
except (OSError, UnicodeError) as e: print(f"cannot read {post}: {type(e).__name__}"); sys.exit(2)
if cmd == "make":
    json.dump({"fingerprint": fp(post)}, open(rec, "w")); print("receipt written"); sys.exit(0)
try: want = json.load(open(rec))["fingerprint"]
except Exception: print("no receipt - unreviewed text cannot be published"); sys.exit(1)
if fp(post) != want: print("DRIFT: text differs from the reviewed version - re-review required"); sys.exit(1)
print("fingerprint matches"); sys.exit(0)
