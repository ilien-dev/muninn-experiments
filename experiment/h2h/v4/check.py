#!/usr/bin/env python3
"""The mechanical acceptance test v22 registered, as a script so it can be re-run and read.

Ten pairs in order; each `a` names the old value and each `b` names the new one and not the
old; every message at least 25 characters and four words.

`tok` matches on token boundaries. The first version of this check used `in`, and rejected a
valid attempt because "https everywhere, no plaintext exception" contains "plain" — the old
value of that scenario being "plain http". That is the same substring-for-token mistake the
loop 8 oracle carried until it was fixed the same day, found the same way: by a figure that
made no sense.

  check.py <generation_raw_N.json> [...]   -> prints OK or what is wrong with each
"""
import json, re, sys

VALUES = [("gzip", "zstd"), ("LFU", "LRU"), ("bcrypt", "argon2id"), ("openssl", "rustls"),
          ("msgpack", "cbor"), ("async-std", "tokio"), ("calver", "semver"),
          ("GPL-3.0", "Apache-2.0"),
          ("certificate verification disabled in dev builds", None),
          ("plain http", "https")]


def tok(text: str, word: str) -> bool:
    return re.search(r"(?<![0-9a-z])" + re.escape(word.lower()) + r"(?![0-9a-z])",
                     text.lower()) is not None


def pairs_of(path):
    t = json.load(open(path)).get("result", "")
    m = re.search(r"```json\s*(.*?)```", t, re.S) or re.search(r"(\[.*\])", t, re.S)
    return json.loads(m.group(1))


def problems(pairs):
    out = []
    if len(pairs) != len(VALUES):
        out.append(f"{len(pairs)} pairs")
    for n, (p, (old, new)) in enumerate(zip(pairs, VALUES)):
        if p.get("key") != f"p{n}":
            out.append(f"p{n}: key {p.get('key')!r}")
        for half in ("a", "b"):
            v = p.get(half, "")
            if len(v) < 25 or len(v.split()) < 4:
                out.append(f"p{n}.{half}: too short {v!r}")
        ow = old.split()[0]
        if not tok(p.get("a", ""), ow):
            out.append(f"p{n}.a: does not name {ow!r}")
        if new:
            nw = new.split()[0]
            if not tok(p.get("b", ""), nw):
                out.append(f"p{n}.b: does not name {nw!r}")
            if tok(p.get("b", ""), ow):
                out.append(f"p{n}.b: names the old value {ow!r}")
    return out


if __name__ == "__main__":
    for path in sys.argv[1:]:
        try:
            pr = problems(pairs_of(path))
        except Exception as e:
            print(f"{path}: does not parse ({e})")
            continue
        print(f"{path}: {'OK' if not pr else pr}")
