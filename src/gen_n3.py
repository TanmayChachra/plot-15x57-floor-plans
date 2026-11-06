import json, os
from layouts_n3 import *
from render_n import *
from specs_n3 import specs, desc


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
    ax.text(ox - 2, th - 4.5, f"PLAN {idx:02d}  |  {fl.title}", fontsize=14, fontweight="bold", va="center")
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
os.makedirs(out, exist_ok=True)
meta = []
for i, s in enumerate(specs(), 1):
    p = build_v3(s)
    p["desc"] = desc(s)
    p["tag"] = "N"
    errs = geo_checks(p)
    bad, pts, mx, det = vastu(p, "N", True)
    assert not errs and not bad, (i, errs, bad)
    name = f"plan-{i:02d}"
    render_n(p, i, dict(det=det, pts=pts, mx=mx), errs, f"{out}/{name}")
    render_floor(p, 1, i, f"{out}/{name}-first")
    render_floor(p, 0, i, f"{out}/{name}-ground")
    im = Image.open(f"{out}/{name}.webp")
    im.resize((800, int(800 * im.height / im.width))).save(f"{out}/{name}-thumb.webp", quality=72, method=6)
    g_, f_ = p["floors"][0], p["floors"][1]
    meta.append(dict(n=i, sheet=f"designs/{name}.webp", first=f"designs/{name}-first.webp", ground=f"designs/{name}-ground.webp",
                     thumb=f"designs/{name}-thumb.webp", desc=desc(s).replace("  North is up.", ""),
                     role="Master at rear" if s["role"] == "M" else "Master at front", balcony=bool(s["bal"]),
                     score=f"{pts}/{mx}", commercial=round(carpet(g_)), residential=round(carpet(f_)),
                     spec=s))
    print(i, pts, mx, flush=True)
json.dump(meta, open("docs/designs.json", "w"), indent=1)
