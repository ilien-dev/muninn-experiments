"""Turns the private labelled sets of usage-v4 into `muninn-bench replay` fixtures, under the
private scratch root only, and compares replay's counts with the harness's for one build.

    python -I replay_private.py make                  # writes S/t10/replay_private/{extraction,delivery}.json
    python -I replay_private.py compare <build sha16> # replay output files against counts/<section>_<build>.json

Prints key names and numbers only.
"""
import hashlib, json, os, sys
S = os.environ["MUNINN_USAGE_FIXTURES"].replace("\\", "/")
OUT = S + "/t10/replay_private"
U = S + "/exp/experiment/results/usage-v4"


def split_of(item_id):
    return "design" if hashlib.sha256(("usage-v4:" + item_id).encode()).digest()[0] % 2 == 0 else "heldout"


def rows(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def make():
    os.makedirs(OUT, exist_ok=True)
    # --- extraction: the staged transcripts a_extract.py left, one directory a store
    tx = S + "/work/usage-v4/a_extract/tx_staged"
    P = rows(S + "/out/extract/precision_items.jsonl")
    R = rows(S + "/out/extract/recall_items.jsonl")
    plab = {x["id"]: x["label"] for x in rows(S + "/out/usage-v4/labels/precision.jsonl")}
    rlab = {x["id"]: x for x in rows(S + "/out/usage-v4/labels/recall.jsonl")}
    anchors = {a["id"]: a["anchors"] for a in rows(S + "/out/usage-v4/labels/recall_anchors.jsonl")}
    stores = sorted({p["store"] for p in P} | {r["store"] for r in R})
    fx = {"section": "extraction",
          "transcripts": {st: tx + "/" + st for st in stores if os.path.isdir(tx + "/" + st)},
          "precision": [], "recall": []}
    for p in P:
        k = "%s:%d" % (p["store"], p["id"])
        fx["precision"].append({"id": k, "label": plab[k], "kind": p["kind"], "origin": p["origin"], "project": p["store"],
                                "session": p["session"], "body": p["body"] or "", "object": p["object"] or "",
                                "split": split_of(k)})
    for r in R:
        lab = rlab[r["uid"]]
        item = {"id": r["uid"], "label": lab["label"], "project": r["store"], "session": r["session"], "turn": r["turn"],
                "anchors": anchors.get(r["uid"], []), "split": split_of(r["uid"])}
        if lab.get("kind"):
            item["kind"] = lab["kind"]
        fx["recall"].append(item)
    json.dump(fx, open(OUT + "/extraction.json", "w", encoding="utf-8"))
    print("extraction: stores", len(fx["transcripts"]), "precision", len(fx["precision"]), "recall", len(fx["recall"]))
    # --- delivery: the store copies and the 150 labelled prompts
    D = S + "/out/delivery"
    sample = rows(D + "/sample_prompt.jsonl")
    pairs = {(p["store"], p["session"], p["at"]): p for p in rows(D + "/pairs.jsonl") if p["reason"] == "literal"}
    labels = {}
    for x in rows(S + "/out/usage-v4/labels/delivery.jsonl"):
        labels.setdefault(x["item"], {})[str(x["id"])] = x["label"]
    fx = {"section": "delivery", "stores": {}, "prompts": []}
    for s in sample:
        fx["stores"].setdefault(s["store"], {"db": S + "/stores/%s/muninn.db" % s["store"]})
        fx["prompts"].append({"id": s["item"], "store": s["store"], "at": s["at"],
                              "prompt": pairs[(s["store"], s["session"], s["at"])]["prompt"],
                              "labels": labels.get(s["item"], {}), "split": split_of(s["item"])})
    json.dump(fx, open(OUT + "/delivery.json", "w", encoding="utf-8"))
    print("delivery: stores", len(fx["stores"]), "prompts", len(fx["prompts"]))


def compare(build):
    for section, counts_file, part in (("extraction", "a_extract_%s.json" % build, None),
                                       ("delivery", "c_delivery_%s.json" % build, "c12")):
        harness = json.load(open(U + "/counts/" + counts_file))["splits"]
        for sp in ("all", "design", "heldout"):
            rp = OUT + "/%s_%s_%s.json" % (section, build, sp)
            if not os.path.isfile(rp):
                print(section, sp, "no replay output")
                continue
            mine = json.load(open(rp))["counts"]
            theirs = harness[sp] if part is None else harness[sp][part]
            if part:
                mine = mine[part]
            same, differ, only_theirs = 0, [], []

            def walk(a, b, path):
                nonlocal same
                if isinstance(b, dict):
                    for k, v in b.items():
                        if isinstance(a, dict) and k in a:
                            walk(a[k], v, path + "/" + k)
                        else:
                            only_theirs.append(path + "/" + k)
                elif a == b:
                    same += 1
                else:
                    differ.append("%s replay=%s harness=%s" % (path, json.dumps(a), json.dumps(b)))
            walk(mine, theirs, "")
            print("%-10s %-8s leaves equal %d, differing %d, harness-only %d" % (section, sp, same, len(differ), len(only_theirs)))
            for d in differ:
                print("    differs:", d)
            if sp == "all":
                for k in only_theirs:
                    print("    not covered by replay:", k)


if __name__ == "__main__":
    make() if sys.argv[1] == "make" else compare(sys.argv[2])
