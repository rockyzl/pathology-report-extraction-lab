"""Dev-only error browser for the rules baseline: python scripts/dev_errors.py <field> wrong|miss [regex]."""
import sys, random, re
from prel import evaluate as E
rep, gold, mem, texts = E.load_all()
dev = mem["dev"]; f=sys.argv[1]; mode=sys.argv[2]; kw=sys.argv[3] if len(sys.argv)>3 else None
pred = E.run_rules(dev, texts)
random.seed(0)
rows=[]
for p in dev:
    g=gold[p][f]; r=pred[p][f]
    if g is None: continue
    if mode=='wrong' and r['status']=='answered' and str(r['value'])!=str(g): rows.append((p,g,r['value'],r['quotes']))
    if mode=='miss' and r['status']!='answered' and kw and re.search(kw,texts[p],re.I): rows.append((p,g,r['status'],[texts[p][max(0,m.start()-80):m.end()+120] for m in list(re.finditer(kw,texts[p],re.I))[:2]]))
print(len(rows))
for x in random.sample(rows,min(8,len(rows))): print(x,'\n')
