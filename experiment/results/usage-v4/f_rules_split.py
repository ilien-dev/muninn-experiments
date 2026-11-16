"""usage-v4, rule F, rule compiler: the split of `corpora/claude-md/files` in two by file name.

    python -I f_rules_split.py <corpora/claude-md> <out dir>

A file is `design` when the first byte of sha256("usage-v4:" + its file name) is even and
`held-out` when it is odd: the rule the other usage-v4 sets were split by. The names are those
of a public corpus. Three lists are written:

    f_rules_design.txt            the design half
    f_rules_heldout.txt           the held-out half, read only by `muninn-bench rules --holdout`
    f_rules_design_readable.txt   the design half less every file an earlier gate holds out
                                  (holdout.txt, holdout2.txt, holdout-enforce*.txt): what a
                                  person or an agent developing patterns may open
"""
import hashlib
import os
import sys

OLDER = ("holdout.txt", "holdout2.txt", "holdout-enforce.txt", "holdout-enforce2.txt",
         "holdout-enforce3.txt")


def half(name):
    first = hashlib.sha256(("usage-v4:" + name).encode("utf-8")).digest()[0]
    return "design" if first % 2 == 0 else "held-out"


def main():
    corpus, out = sys.argv[1], sys.argv[2]
    names = sorted(os.listdir(os.path.join(corpus, "files")))
    older = set()
    for f in OLDER:
        with open(os.path.join(corpus, f), encoding="utf-8") as fh:
            older |= {line.strip() for line in fh if line.strip()}
    design = [n for n in names if half(n) == "design"]
    held = [n for n in names if half(n) == "held-out"]
    readable = [n for n in design if n not in older]
    os.makedirs(out, exist_ok=True)
    for name, lst in (("f_rules_design.txt", design), ("f_rules_heldout.txt", held),
                      ("f_rules_design_readable.txt", readable)):
        with open(os.path.join(out, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lst) + "\n")
    print(f"{len(names)} files: design {len(design)}, held-out {len(held)}; "
          f"design not in an earlier hold-out list {len(readable)}; "
          f"earlier lists name {len(older)} files, {len([n for n in held if n in older])} of them "
          f"in the held-out half")


if __name__ == "__main__":
    main()
