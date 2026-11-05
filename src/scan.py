import itertools, json
from layouts import *
G=[("G1",False),("G1",True),("G1C",False),("G2",False),("G2",True),("G3",False),("G3",True)]
F=[("A","R",False),("A","R",True),("A","L",False),("A","L",True),("B","R",False),("B","R",True),("B","L",False),("B","L",True)]
res=[]
for fa in "ENWS":
  for mir in (False,True):
    for g in G:
      for f in F:
        for t in (1,2):
          p=build(g,f,fa,mir,t)
          bad,pts,mx,det=vastu(p,fa,mir)
          errs=geo_checks(p)
          if errs or bad: continue
          res.append((fa,mir,g,f,t,pts,mx))
import collections
c=collections.Counter((r[0],r[1]) for r in res); print(c)
print(len(res), max(r[5] for r in res))
json.dump(res,open('cands.json','w'))
