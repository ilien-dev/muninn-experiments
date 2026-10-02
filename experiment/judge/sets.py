"""The judge tournament's items: every (earlier, later) pair with its label, split and language.

A pair asks one question: does `later` make `earlier` no longer current? The sets are the ones
already committed, read as they are:

  positive       (a_i, b_i)  a held-out change and the decision it replaces
  neg_cross      (a_j, b_i)  a change against every *other* decision of its group, j != i:
                             the "which one does it replace" question that closed [Z3] and loop 12
  neg_distractor (a_j, c_i)  a later unrelated decision against every decision of its group
  neg_shared     (a, b)      loop 10's pairs: both stay true, and they share words

A group is one set and one style (terse, chatty, Spanish), so a change is only ever asked
against the decisions a store of that style would hold beside it.

Split, fixed before any arm ran: dev (thresholds are fitted here) = loop1, loop12's
dev_phrasings, loop10/pairs.json; test = everything else.
"""
import json
from pathlib import Path

EXP = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

LANG = {"terse": "en", "chatty": "en", "Spanish": "es"}

HELDOUT = [("loop1", "heldout_phrasings.json", "dev"), ("loop12", "dev_phrasings.json", "dev")] + [
    (f"loop{n}", "heldout_phrasings.json", "test") for n in (2, 3, 4, 5, 6, 7, 8, 9, 11)]
SHARED = [("loop10", "pairs.json", "dev"), ("loop10", "pairs2.json", "test"),
          ("loop10", "pairs3.json", "test")]


def _triples(groups, set_name, split):
    out = []
    for (style, lang), rows in groups.items():
        for i, r in enumerate(rows):
            for j, s in enumerate(rows):
                base = {"set": set_name, "split": split, "lang": lang, "group": f"{set_name}/{style}"}
                out.append({**base, "id": f"{s['key']}|{r['key']}|b",
                            "kind": "positive" if i == j else "neg_cross",
                            "label": int(i == j), "a": s["a"], "b": r["b"]})
                out.append({**base, "id": f"{s['key']}|{r['key']}|c", "kind": "neg_distractor",
                            "label": 0, "a": s["a"], "b": r["c"]})
    return out


def items(include_user: bool = True):
    out = []
    for d, f, split in HELDOUT:
        groups = {}
        for r in json.load(open(EXP / d / f)):
            style = r["key"].split("#")[-1]
            groups.setdefault((style, LANG[style]), []).append(r)
        out += _triples(groups, d, split)
    for d, f, split in SHARED:
        for r in json.load(open(EXP / d / f)):
            style = r["key"].split("#")[-1]
            out.append({"set": f"{d}/{f}", "split": split, "lang": LANG[style], "group": f"{d}/{style}",
                        "id": f"{r['key']}|{f}", "kind": "neg_shared", "label": 0,
                        "a": r["a"], "b": r["b"]})
    third = json.load(open(HERE / "third_language.json"))
    groups = {}
    for r in third["triples"]:
        groups.setdefault((r["key"].split("#")[-1], r["lang"]), []).append(r)
    out += _triples(groups, "third", "test")
    for r in third["negatives"]:
        out.append({"set": "third", "split": "test", "lang": r["lang"], "group": f"third/{r['lang']}",
                    "id": f"{r['key']}|third", "kind": "neg_shared", "label": 0, "a": r["a"], "b": r["b"]})
    user = HERE / "user_pairs.json"
    if include_user and user.exists():
        for r in json.load(open(user))["pairs"]:
            out.append({"set": "user", "split": "test", "lang": r["lang"], "group": f"user/{r['lang']}",
                        "id": f"{r['key']}|user", "kind": "positive" if r["label"] else "neg_user",
                        "label": int(r["label"]), "a": r["a"], "b": r["b"]})
    ids = [x["id"] for x in out]
    assert len(ids) == len(set(ids)), "duplicate item id"
    return out


if __name__ == "__main__":
    from collections import Counter
    xs = items()
    print(len(xs))
    for k, v in sorted(Counter((x["split"], x["lang"], x["kind"]) for x in xs).items()):
        print(k, v)


def probe_items():
    """judge-v1b: the 60 probe pairs (user_pairs_v1b.json). One group per language, so A0's
    store holds every earlier message of that language; the pair is its own later message."""
    out = []
    for r in json.load(open(HERE / "user_pairs_v1b.json"))["pairs"]:
        out.append({"set": "v1b", "split": "test", "lang": r["lang"], "group": f"v1b/{r['lang']}",
                    "id": f"{r['key']}|{r['key']}|v1b", "probe": r["probe"],
                    "kind": "positive" if r["label"] else "neg_probe", "label": int(r["label"]),
                    "a": r["a"], "b": r["b"]})
    return out
