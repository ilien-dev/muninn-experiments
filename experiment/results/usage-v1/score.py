import sys,io,json,sqlite3,collections,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
S=json.load(open('label/sup.json',encoding='utf8')); O={(x['p'],x['id']):x for x in json.load(open('label/sup.out.json',encoding='utf8'))}
ARMS=sys.argv[1:] or ['base','new2']
res={}
for arm in ARMS:
    c=collections.Counter()
    for s in S:
        p=s['p']; f=f'rp/{arm}/{p}/.muninn/muninn.db'
        l=O[(p,int(s['id']))]
        st='noproj'
        if os.path.exists(f):
            db=sqlite3.connect(f)
            key=s['old'].split('\n')[0][:70].replace('\\','\\\\').replace('%','\\%').replace('_','\\_')
            rows=db.execute("select invalid,kind from record where body like ? escape '\\' and kind=?",('%'+key+'%',s['kind'])).fetchall()
            st='absent' if not rows else ('active' if any(r[0]==0 for r in rows) else 'retired')
        res[(arm,p,s['id'])]=st
        c[(l['label'],st)]+=1; c[('LOSS' if l['loss'] else 'noloss',st)]+=1
    print(arm,sorted(c.items(),key=str))
d=collections.Counter()
for s in S:
    a,b=res[(ARMS[0],s['p'],s['id'])],res[(ARMS[1],s['p'],s['id'])]
    if a!=b: d[(O[(s['p'],int(s['id']))]['label'],a,b)]+=1
print('changed',sorted(d.items(),key=str))
print('valid',[(s['p'][:3],s['id'],res[(ARMS[0],s['p'],s['id'])],res[(ARMS[1],s['p'],s['id'])]) for s in S if O[(s['p'],int(s['id']))]['label']=='valid'])
for arm in ARMS:
    t=collections.Counter()
    for p in os.listdir('stores'):
        f=f'rp/{arm}/{p}/.muninn/muninn.db'
        if os.path.exists(f):
            db=sqlite3.connect(f)
            for k,i,n in db.execute("select kind,invalid,count(*) from record group by 1,2"): t[f'{k}{i}']+=n
            t['typed_superseded_heir']+=db.execute("select count(*) from record where invalid=1 and invalid_reason='superseded' and invalidated_by is not null and kind!='episode'").fetchone()[0]
            t['typed_superseded_noheir']+=db.execute("select count(*) from record where invalid=1 and invalid_reason='superseded' and invalidated_by is null and kind!='episode'").fetchone()[0]
            t['older_heir']+=db.execute("select count(*) from record r join record h on h.id=r.invalidated_by where r.invalid=1 and h.created_at<r.created_at").fetchone()[0]
            t['corr_by_same_subject']+=db.execute("select count(*) from record r join record h on h.id=r.invalidated_by where r.invalid=1 and r.kind='correction' and h.subject=r.subject").fetchone()[0]
    print(arm,sorted(t.items()))
