import json, os
from layouts_n4 import *
from render_n import *
from specs_n4 import specs, desc


def render_floor(plan, which, idx, path):
    fl = plan["floors"][which]
    tw, th = 15.4 + 24, D + 22
    fig = plt.figure(figsize=(tw * 0.3, th * 0.3), dpi=130)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, tw)
    ax.set_ylim(0, th)
    ax.set_aspect("equal")
    ax.axis("off")
    ox, oy = 12, 8
    T, _, _ = draw_floor(ax, fl, plan, "N", True, ox, oy, fs=11.5)
    quad = [T(-1.5, -5.2), T(W + 1.5, -5.2), T(W + 1.5, -0.2), T(-1.5, -0.2)]
    ax.add_patch(Polygon(quad, closed=True, fc="#BDBDBD", ec="none", zorder=0.5))
    rc = T(W / 2, -2.7)
    ax.text(rc[0], rc[1], "ROAD (NORTH)", ha="center", va="center", fontsize=11)
    ax.text(ox - 2, th - 4.5, f"PLAN {idx:02d} (no court)  |  {fl.title}", fontsize=14, fontweight="bold", va="center")
    ax.text(ox - 2, th - 7.2, "North-facing, plot 15.4 x 57.6 ft. Clear internal sizes in feet-inches. Walls 9 in outer, 4.5 in inner.",
            fontsize=10, va="center", color="#444")
    north_arrow(ax, ox + W + 9, th - 14, 3.0)
    chain(ax, T, fl, "y", 6.5, -3.6, "A", fs=9.5)
    chain(ax, T, fl, "y", 12.0, W + 3.6, "B", fs=9.5)
    chain(ax, T, fl, "x", 43.5, D + 1.6, "C", fs=9.5)
    chain(ax, T, fl, "x", 47.0, D + 4.0, "D", fs=9.5)
    fig.savefig(path + ".png", dpi=130)
    plt.close(fig)
    Image.open(path + ".png").convert("RGB").save(path + ".webp", quality=82, method=6)
    os.remove(path + ".png")


out = "docs/designs"
meta = json.load(open("docs/designs.json"))
meta = [m for m in meta if not m.get("nc")]
for j, s in enumerate(specs(), 21):
    p = build_nc(s)
    p["desc"] = desc(s)
    p["tag"] = "N"
    errs = geo_checks(p)
    bad, pts, mx, det = vastu(p, "N", True)
    assert not errs and not bad, (j, errs, bad)
    name = f"plan-{j:02d}"
    render_n(p, j, dict(det=det, pts=pts, mx=mx), errs, f"{out}/{name}")
    render_floor(p, 1, j, f"{out}/{name}-first")
    render_floor(p, 0, j, f"{out}/{name}-ground")
    im = Image.open(f"{out}/{name}.webp")
    im.resize((800, int(800 * im.height / im.width))).save(f"{out}/{name}-thumb.webp", quality=72, method=6)
    for suf in ("first", "ground"):
        im2 = Image.open(f"{out}/{name}-{suf}.webp")
        im2.resize((520, int(520 * im2.height / im2.width))).save(f"{out}/{name}-{suf}-thumb.webp", quality=72, method=6)
    g_, f_ = p["floors"][0], p["floors"][1]
    meta.append(dict(n=j, sheet=f"designs/{name}.webp", first=f"designs/{name}-first.webp", ground=f"designs/{name}-ground.webp",
                     thumb=f"designs/{name}-thumb.webp", desc=desc(s).replace("  North is up.", ""),
                     role="Master at rear" if s["role"] == "M" else "Master at front", balcony=bool(s["bal"]), nc=True,
                     score=f"{pts}/{mx}", commercial=round(carpet(g_)), residential=round(carpet(f_)), spec=s))
    print(j, pts, mx, flush=True)
json.dump(meta, open("docs/designs.json", "w"), indent=1)
