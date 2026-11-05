"""Sheet renderer for the north-facing set (north up, road on the north side)."""
import os
from collections import Counter
from layouts_n import *
from PIL import Image

NAMES_G = {"GA": "Open shop, store/pantry and staff toilet at rear",
           "GB": "Open shop, owner cabin with attached toilet at rear",
           "GC": "Open shop, store and pantry, staff toilet, rear service door"}
NAMES_F = {"A": "Front Bedroom 2 (with toilet), Master Bedroom at rear (with toilet)",
           "D": "Front Master Bedroom (with toilet), Bedroom 2 at rear (with toilet)"}
S_IN = 0.21
GAP = 15.0
RED = "#B03030"


def segs_along(fl, axis, scan, lim):
    step, out, cur, start = 0.02, [], None, 0.0
    for i in range(int(lim / step) + 1):
        v = min(i * step, lim - 1e-6)
        x, y = (scan, v) if axis == "y" else (v, scan)
        if axis == "y" and v >= DFP:
            c = "yard"
        elif axis == "x" and False:
            c = "yard"
        else:
            r = fl.room_at(x, y)
            c = r.name if r else "wall"
        if c != cur:
            if cur is not None:
                out.append((start, v, cur))
            start, cur = v, c
    out.append((start, lim, cur))
    return out


def chain(ax, T, fl, axis, scan, draw, label, fs=7.5):
    lim = D if axis == "y" else W
    segs = segs_along(fl, axis, scan, lim)
    P = (lambda t: T(draw, t)) if axis == "y" else (lambda t: T(t, draw))
    for (a, b, nm) in segs:
        for t in (a, b):
            p = P(t)
            q = (p[0] - 0.4, p[1]) if axis == "y" else (p[0], p[1] - 0.4)
            q2 = (p[0] + 0.4, p[1]) if axis == "y" else (p[0], p[1] + 0.4)
            ax.plot([q[0], q2[0]], [q[1], q2[1]], color="#222", lw=0.6, zorder=9)
        p1, p2 = P(a), P(b)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#222", lw=0.6, zorder=9)
        ln = b - a
        if nm == "wall" or ln < 1.0:
            continue
        m = P((a + b) / 2)
        txt = fi(ln) if nm != "yard" else "5'-0\" yard"
        if axis == "y":
            ax.text(m[0] - 0.7, m[1], txt, rotation=90, ha="right", va="center", fontsize=fs, zorder=9)
        else:
            ax.text(m[0], m[1] - 0.7, txt, ha="center", va="top", fontsize=fs, zorder=9)
    # section line on the plan
    if axis == "y":
        p, q = T(scan, 0), T(scan, DFP)
        ax.text(*P(-1.6), label, ha="center", va="center", fontsize=fs + 1, fontweight="bold", color=RED, zorder=9)
    else:
        p, q = T(0, scan), T(W, scan)
        ax.text(*P(-1.6) if False else (T(-1.6, draw)), label, ha="center", va="center", fontsize=fs + 1, fontweight="bold", color=RED, zorder=9)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=RED, lw=0.5, ls=(0, (1, 2)), zorder=9)


def fi2(v):
    return fi(v)


def room_rows(fl):
    rows = []
    for r in fl.rooms:
        if r.kind in ("court", "terrace", "mumty", "void", "passage") and r.name not in ("Passage",):
            continue
        xs = [q[0] for q in r.rects] + [q[2] for q in r.rects]
        ys = [q[1] for q in r.rects] + [q[3] for q in r.rects]
        w, l = max(xs) - min(xs), max(ys) - min(ys)
        if len(r.rects) == 1:
            rows.append(f"{r.name}: {fi(w)} x {fi(l)} = {r.area():.0f} sq ft")
        else:
            rows.append(f"{r.name}: L-shape {fi(w)} x {fi(l)} overall = {r.area():.0f} sq ft")
    return rows


def schedule(fl):
    cd, cw = Counter(), Counter()
    for d in fl.doors:
        if d["kind"] == "arch":
            cd[("opening", round(d["w"], 2))] += 1
        elif d["kind"] == "shutter":
            cd[("rolling shutter", round(d["w"], 2))] += 1
        elif d["kind"] == "fdoor":
            cd[("sliding french door", round(d["w"], 2))] += 1
        elif d["kind"] == "service":
            cd[("duct service door", round(d["w"], 2))] += 1
        else:
            cd[("door", round(d["w"], 2))] += 1
    for w in fl.wins:
        cw[(round(w["w"], 2), round(w["h"], 2))] += 1
    a = "; ".join(f"{n} {fi(w)} {k}" for (k, w), n in sorted(cd.items(), key=lambda z: -z[0][1]))
    b = "; ".join(f"{n} {fi(w)} x {fi(h)}" for (w, h), n in sorted(cw.items(), key=lambda z: -z[0][0]))
    return a, b


def carpet(fl):
    return sum(r.area() for r in fl.rooms if r.kind not in ("stair", "court", "terrace", "mumty", "duct", "void"))


def render_n(plan, idx, vs, errs, path):
    fls = plan["floors"]
    ew, ns = W, D
    pw = 74.0
    tw, th = 8 + 3 * ew + 2 * GAP + 8 + pw, ns + 34
    offs = [(10 + i * (ew + GAP), 14) for i in range(3)]
    px = 10 + 3 * ew + 2 * GAP + 6
    fig = plt.figure(figsize=(tw * S_IN, th * S_IN), dpi=110)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, tw)
    ax.set_ylim(0, th)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(8, th - 3.2, f"PLAN N-{idx:02d}  |  NORTH-FACING, ROAD ON THE 15.4 ft NORTH SIDE  |  PLOT 15.4 ft x 57.6 ft  |  GROUND SHOP, FIRST FLOOR 2 BEDROOM HOME, TERRACE",
            fontsize=13, fontweight="bold", va="center")
    ax.text(8, th - 6.4, f"Ground: {NAMES_G[plan['g'][0]]}.   First: {NAMES_F[plan['f'][0]]}{', with pooja' if plan['f'][1] else ''}.   Services duct (open to sky) between kitchen and toilet.   North is up.",
            fontsize=9, va="center", color="#333")
    ax.text(8, th - 9.0, "All room sizes are clear internal sizes in feet-inches. Walls: 9 in outer, 4.5 in inner. Chains A, B, C, D on each plan (red dotted lines) give clear lengths along that line; segments without a figure are walls.",
            fontsize=8, va="center", color="#555")
    for fl, (ox, oy) in zip(fls, offs):
        T, _, _ = draw_floor(ax, fl, plan, "N", True, ox, oy, fs=8.3)
        quad = [T(-1.5, -5.2), T(W + 1.5, -5.2), T(W + 1.5, -0.2), T(-1.5, -0.2)]
        ax.add_patch(Polygon(quad, closed=True, fc="#BDBDBD", ec="none", zorder=0.5))
        rc = T(W / 2, -2.7)
        ax.text(rc[0], rc[1], "ROAD (NORTH)", ha="center", va="center", fontsize=9, color="#222")
        xs = [T(0, 0)[0], T(W, D)[0]]
        ys = [T(0, 0)[1], T(W, D)[1]]
        bx, ex_, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        ax.text(bx, by1 + 6.4, fl.title, fontsize=11, fontweight="bold", va="bottom")
        north_arrow(ax, ex_ - 2, by1 + 6.2, 2.6)
        chain(ax, T, fl, "y", 6.5, -3.4, "A")
        chain(ax, T, fl, "y", 12.0, W + 3.4, "B")
        chain(ax, T, fl, "x", 43.5, D + 1.4, "C")
        chain(ax, T, fl, "x", 47.0, D + 3.2, "D")
        ax.text((bx + ex_) / 2, by0 - 6.2, "15'-4.8\" (15.4 ft) plot width = 9\" wall + clear + 9\" wall", ha="center", fontsize=8, va="top")
    g, f = fls[0], fls[1]
    L_ = []

    def add(t="", b=False, sz=8.5):
        L_.append((t, b, sz))
    st = stair_info()
    add("AREA STATEMENT", True, 10)
    add("Plot 15.4 x 57.6 ft = 887.0 sq ft (82.4 sq m, 98.6 sq yd)")
    add("Footprint 15.4 x 52.6 ft = 810.0 sq ft per floor (91.3%); rear yard 5'-0\"")
    add(f"Commercial carpet (ground, excl. stair, duct): {carpet(g):.0f} sq ft")
    add(f"Residential carpet (first, excl. stair, court, duct): {carpet(f):.0f} sq ft")
    add("Height: floor to floor 10'-6\", slab 5 in, clear height 10'-1\"")
    add()
    add("ROOM SIZES, GROUND FLOOR (clear)", True, 10)
    for t in room_rows(g):
        add(t)
    add()
    add("ROOM SIZES, FIRST FLOOR (clear)", True, 10)
    for t in room_rows(f):
        add(t)
    add("Court (open to sky): 6'-0\" x 8'-0\" = 48 sq ft")
    add()
    add("SERVICES DUCT (kitchen, toilet, electrical risers)", True, 10)
    add("Size 4'-0\" x 3'-11\" = 15.7 sq ft (1.46 sq m), open to sky at the terrace")
    add("Runs ground to terrace between the kitchen and the toilet.")
    add("Kitchen window and toilet ventilator open into it. It carries")
    add("water supply, waste, soil and vent pipes, gas line, electrical")
    add("conduits and meter risers. Access: ground floor service door")
    add("(2'-0\") and the terrace opening. Floor drain at the base.")
    add("Cover the top with a RCC chhajja and mesh, not a slab.")
    add()
    add("DOOR AND WINDOW SCHEDULE (doors 7'-0\" high)", True, 10)
    for fl_, nm in ((g, "Ground"), (f, "First")):
        a, b = schedule(fl_)
        add(f"{nm} doors: {a}")
        add(f"{nm} windows (w x h): {b}")
    add("Sill 3'-0\" (windows), 6'-0\" (toilet ventilators), lintel 7'-0\".")
    add()
    add("STAIR (starts at the front, own street door)", True, 10)
    add(f"Straight flights on the west party wall, clear width {st['width_ft']:.1f} ft")
    add(f"{st['risers']} risers x {st['riser_in']:.0f} in, tread {st['tread_in']:.0f} in, pitch {st['pitch_deg']:.0f} deg")
    add(f"Headroom {st['headroom_ft']} ft (2.2 m) minimum; riser 178 mm, tread 254 mm")
    add()
    add("VASTU READING (plot thirds, room centroid)", True, 10)
    for fc, nm, z, lv in vs["det"]:
        mark = {"ideal": "+", "acceptable": "~", "compromise": "-", "AVOID": "X"}[lv]
        add(f"[{mark}] {fc}  {nm}: {z} ({lv})")
    add(f"Score {vs['pts']}/{vs['mx']}    + ideal   ~ acceptable   - compromise   X avoid")
    add("Brahmasthan (centre) kept open to sky as the court.")
    add()
    add("CHECKS (run by script)", True, 10)
    add("0 errors" if not errs else f"{len(errs)} errors")
    add("No overlaps, walls >= 4.5 in, every room reached by a door,")
    add("master/living >= 7.9 ft wide, master >= 100 sq ft, 2nd bed 7.0 ft,")
    add("kitchen >= 48 sq ft, toilets >= 24 sq ft and 4 ft wide, openings")
    add(">= 1/6 (bedrooms), 1/8 (hall, kitchen, cabin), 1/10 (toilets, shop).")
    add()
    add("ASSUMPTIONS (confirm with local bylaws and an architect)", True, 10)
    for t in ["Road on the north, party walls east and west, 5 ft rear yard.",
              "9 in outer walls, 4.5 in partitions, 5 in RCC slabs.",
              "Floor level 6 in above road: one step at shutter and stair door.",
              "Terrace: slope 1:100 to outlets (small squares), parapet 3 ft 6 in.",
              "First floor wet areas on sunk waterproofed slab.",
              "Structural frame by a structural engineer. No parking built."]:
        add(t)
    y, col = th - 12, 0
    for t, b, sz in L_:
        step = 0.25 + sz * 0.098
        if y - step < 4:
            y, col = th - 12, col + 1
        ax.text(px + col * (pw / 2 + 1), y, t, fontsize=sz - (0.8 if col == 0 else 0.8), fontweight="bold" if b else "normal", va="top")
        y -= step
    fig.savefig(path + ".png", dpi=110)
    plt.close(fig)
    im = Image.open(path + ".png").convert("RGB")
    im.save(path + ".webp", quality=80, method=6)
    os.remove(path + ".png")
