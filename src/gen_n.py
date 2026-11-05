import json, os
from render_n import *

cands = [tuple(x) for x in json.load(open("cands_n.json"))]
by = {}
for g, typ, pj, t, pts, mx in cands:
    by.setdefault((g, typ, pj), (pts, mx))
keys = sorted(by, key=lambda k: (-by[k][0], k))
out = "docs/north"
os.makedirs(out, exist_ok=True)
meta = []
for i, k in enumerate(keys, 1):
    t = 1 + (i % 2)
    p = build_n(k[0], (k[1], k[2]), t)
    errs = geo_checks(p)
    bad, pts, mx, det = vastu(p, "N", True)
    assert not errs and not bad
    name = f"plan-n{i:02d}"
    render_n(p, i, dict(det=det, pts=pts, mx=mx), errs, f"{out}/{name}")
    im = Image.open(f"{out}/{name}.webp")
    im.resize((900, int(900 * im.height / im.width))).save(f"{out}/{name}-thumb.webp", quality=75, method=6)
    g, f = p["floors"][0], p["floors"][1]
    meta.append(dict(n=i, file=f"north/{name}.webp", thumb=f"north/{name}-thumb.webp", ground=NAMES_G[k[0]],
                     first=NAMES_F[k[1]] + (", with pooja" if k[2] else ""), terrace="Tank, solar, clothes drying" if t == 1 else "Tank, solar, garden / tulsi seating",
                     score=f"{pts}/{mx}", commercial=round(carpet(g)), residential=round(carpet(f)),
                     size=os.path.getsize(f"{out}/{name}.webp") // 1024))
    print(i, k, t, pts, mx, flush=True)
json.dump(meta, open("docs/plans_north.json", "w"), indent=1)
