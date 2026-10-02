import json, random, sys, collections
rows=[json.loads(l) for l in open(sys.argv[1])]
rows=[r for r in rows if r.get('status') in ('pass','fail')]
arms=['literal','literal-hookboot']
by=collections.defaultdict(dict)   # (task,run) -> arm -> 1/0
tok=collections.defaultdict(list); cost=collections.defaultdict(list); turns=collections.defaultdict(list)
for r in rows:
    by[(r['task'],r['run'])][r['arm']]=1 if r['status']=='pass' else 0
    tok[r['arm']].append(r.get('delivered_tokens',0)); cost[r['arm']].append(r.get('cost_usd',0)); turns[r['arm']].append(r.get('num_turns',0))
tasks=sorted({t for t,_ in by})
print("arm | pass | tokens mean | turns mean | cost mean")
for a in arms:
    v=[by[k][a] for k in by if a in by[k]]
    print(f"{a} | {sum(v)}/{len(v)} ({100*sum(v)/max(1,len(v)):.0f}%) | {sum(tok[a])/max(1,len(tok[a])):.0f} | {sum(turns[a])/max(1,len(turns[a])):.1f} | ${sum(cost[a])/max(1,len(cost[a])):.3f}")
random.seed(7)
def diff(a,b,keys):
    d=[by[k][a]-by[k][b] for k in keys if a in by[k] and b in by[k]]
    return sum(d)/len(d) if d else float('nan')
def ci(a,b):
    keys=list(by); point=diff(a,b,keys)
    bs=[]
    for _ in range(4000):
        ts=[random.choice(tasks) for _ in tasks]          # cluster bootstrap on task
        ks=[k for t in ts for k in keys if k[0]==t]
        bs.append(diff(a,b,ks))
    bs.sort(); return point, bs[int(0.025*len(bs))], bs[int(0.975*len(bs))]
for a,b in [('literal-hookboot','literal')]:
    p,lo,hi=ci(a,b); print(f"{a} − {b}: {p:+.3f} [95% CI {lo:+.3f}, {hi:+.3f}]")
print("\ntask | "+" | ".join(arms))
for t in tasks:
    print(t+" | "+" | ".join(f"{sum(by[(t,r)].get(a,0) for r in range(3) if (t,r) in by)}/{sum(1 for r in range(3) if (t,r) in by and a in by[(t,r)])}" for a in arms))
errs=[l for l in open(sys.argv[1]) if '"status":"error"' in l]; print("\nerrors:",len(errs))
