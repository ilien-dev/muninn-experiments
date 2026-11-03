import glob, json, re, sys
sys.argv = ["grid3.py", "x", "x", "x"]
src = open(__file__.replace("rescore3.py", "grid3.py"), encoding="utf8").read()
T = eval(src[src.index("T = [") + 4: src.index("]\nH =") + 1])
W = __file__.replace("rescore3.py", "g3")
res = []
for name, _, _, rx in T:
    for arm in ("off", "on"):
        code = "".join(open(f, encoding="utf8", errors="replace").read()
                       for f in glob.glob(f"{W}/{arm}-{name}/**/*.py", recursive=True))
        res.append({"task": name, "arm": arm, "pass": bool(re.search(rx, code)), "wrote": bool(code)})
print(json.dumps(res))
print("off", sum(r["pass"] for r in res if r["arm"] == "off"), "on", sum(r["pass"] for r in res if r["arm"] == "on"))
