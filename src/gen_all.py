import json, os, sys
from layouts import *
from build import render, carpet, NAMES, FNAMES, FACE
from PIL import Image

cands = [tuple(x) for x in json.load(open("cands.json"))]
by = {}
for fa, mir, g, f, t, pts, mx in cands:
    by.setdefault((fa, bool(mir), tuple(g), tuple(f)), []).append((t, pts, mx))
picked = []
order = {"E": 0, "N": 1, "S": 2, "W": 3}
keys = sorted(by, key=lambda k: (order[k[0]], -by[k][0][1], str(k)))
for i, k in enumerate(keys):
    ts = sorted(by[k])
    t = 1 + (i % 2)
    picked.append((k, t))
# two extra East plans with the other terrace variant
ek = [k for k in keys if k[0] == "E"]
for k in ek[:2]:
    t0 = [t for kk, t in picked if kk == k][0]
    picked.append((k, 3 - t0))
picked.sort(key=lambda p: (order[p[0][0]], p[0][1], str(p[0])))
assert len(picked) == 20, len(picked)
out = "docs/plans"
os.makedirs(out, exist_ok=True)
meta = []
for n, ((fa, mir, g, f), t) in enumerate(picked, 1):
    p = build(g, f, fa, mir, t)
    bad, pts, mx, det = vastu(p, fa, mir)
    errs = geo_checks(p)
    assert not errs and not bad
    name = f"plan-{n:02d}-{FACE[fa].lower()}-facing"
    render(p, fa, mir, f"{out}/{name}", n, dict(det=det, pts=pts, mx=mx), errs)
    im = Image.open(f"{out}/{name}.webp")
    th = im.resize((900, int(900 * im.height / im.width)))
    th.save(f"{out}/{name}-thumb.webp", quality=75, method=6)
    meta.append(dict(n=n, facing=FACE[fa], file=f"plans/{name}.webp", thumb=f"plans/{name}-thumb.webp",
                     ground=NAMES[g[0]], first=FNAMES[f[0]], terrace=("Tank, solar, clothes drying" if t == 1 else "Tank, solar, garden / tulsi seating"),
                     score=f"{pts}/{mx}", commercial=round(carpet(p['floors'][0])), residential=round(carpet(p['floors'][1])),
                     bhk="2 BHK" if f[0] == "A" else "1 BHK + dining",
                     size=os.path.getsize(f"{out}/{name}.webp") // 1024))
    print(n, fa, g, f, t, pts, mx, flush=True)
json.dump(meta, open("docs/plans.json", "w"), indent=1)
