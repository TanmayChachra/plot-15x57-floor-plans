import json
from layouts_n import *
res = []
for g in ("GA", "GB", "GC"):
    for typ in "AD":
        for pj in (False, True):
            for t in (1, 2):
                p = build_n(g, (typ, pj), t)
                errs = geo_checks(p)
                bad, pts, mx, det = vastu(p, "N", True)
                print(g, typ, pj, t, "ERR" if errs else "ok", errs[:4], bad, pts, mx)
                if not errs and not bad:
                    res.append((g, typ, pj, t, pts, mx))
json.dump(res, open("cands_n.json", "w"))
print(len(res))
