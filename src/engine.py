"""Geometry, checks and drawing for the 15.4 x 57.6 ft plot plans.
Canonical frame: x = 0..W across the front (left as seen from the street), y = 0..D from the road inwards.
All numbers are feet. Walls are the gaps between room rectangles (poche method)."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

W, D = 15.4, 57.6
EW, TW = 0.75, 0.375                 # external (9 in) and internal (4.5 in) walls
REAR = 5.0                           # rear open yard
DFP = D - REAR                       # building depth
X0, X1, Y0, Y1 = EW, W - EW, EW, DFP - EW

# ---- stair (straight flights along the left party wall, starts at the front)
RISER_IN, TREAD_IN, NRISE = 7.0, 10.0, 18      # 18 x 7in = 10'-6" floor to floor
FLOOR_H = NRISE * RISER_IN / 12
SLAB = 5 / 12
LOBBY = 3.85
S_FL = (NRISE - 1) * TREAD_IN / 12             # run of one flight (17 treads)
S_LAND = 3.5
YS0 = Y0 + LOBBY                               # first riser
YF1 = YS0 + S_FL                               # top of flight 1 (first floor level)
YL = YF1 + S_LAND                              # end of landing
YF2 = YL + S_FL                                # top of flight 2 (terrace level)
HEAD = 7.2
OPEN = (FLOOR_H - SLAB - HEAD) / (RISER_IN / TREAD_IN)   # run before headroom is lost
YO1, YO2 = YS0 + OPEN, YL + OPEN               # slab openings start
SX0, SX1 = X0, 4.25                            # stair clear x
PX0 = SX1 + TW                                 # strip starts (4.625)


def fi(v):
    i = round(v * 12)
    return f"{i // 12}'-{i % 12}\""


COLORS = dict(guest="#CDE7F1", hall2="#F9EBC8", duct="#FFFFFF", shop="#F7E6C4", store="#E8DCC4", toilet="#CDE7F1", wc="#CDE7F1", cabin="#E9DDF0", godown="#E8DCC4",
              living="#FBF2D5", dining="#F9EBC8", hall="#F9EBC8", kitchen="#FFDDC9", bed="#DDE7F6", master="#D3E0F5",
              pooja="#FFEFAE", stair="#E4E4E4", court="#CFE6B8", passage="#F3F3F3", terrace="#ECE4D6", mumty="#E4E4E4",
              tank="#B9D7F0", solar="#F4D77A", garden="#CFE6B8", utility="#E8DCC4", void="#FFFFFF")
HAB = {"living", "dining", "hall", "hall2", "bed", "master", "cabin"}


class Room:
    def __init__(s, name, kind, rects, label=None, lp=None):
        s.name, s.kind, s.rects, s.label, s.lp = name, kind, [tuple(r) for r in rects], name if label is None else label, lp

    def area(s):
        return sum((r[2] - r[0]) * (r[3] - r[1]) for r in s.rects)

    def centroid(s):
        a = s.area()
        return (sum((r[0] + r[2]) / 2 * (r[2] - r[0]) * (r[3] - r[1]) for r in s.rects) / a,
                sum((r[1] + r[3]) / 2 * (r[2] - r[0]) * (r[3] - r[1]) for r in s.rects) / a)

    def minwidth(s):
        return max(min(r[2] - r[0], r[3] - r[1]) for r in s.rects)

    def has(s, x, y):
        return any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for r in s.rects)


class Floor:
    def __init__(s, code, title, rooms, doors=(), wins=(), extra=(), notes=()):
        s.code, s.title, s.rooms = code, title, list(rooms)
        s.doors, s.wins, s.extra, s.notes = list(doors), list(wins), list(extra), list(notes)
        s.solid = code != "T"

    def room_at(s, x, y):
        for r in s.rooms:
            if r.has(x, y):
                return r
        return None


def door(o, c, a, w, side, hinge="a", kind="door"):
    return dict(o=o, c=c, a=a, w=w, side=side, hinge=hinge, kind=kind)


def win(o, c, a, w, h=4.0, kind="win"):
    return dict(o=o, c=c, a=a, w=w, h=h, kind=kind)


def _span(fl, o, c, m):
    """wall gap [p0,p1] around line c at along-position m"""
    def inside(t):
        x, y = (t, m) if o == "V" else (m, t)
        return fl.room_at(x, y) is not None
    lim = W if o == "V" else DFP
    st = 0.01
    p0 = c
    while p0 > 0 and not inside(p0 - st):
        p0 -= st
    p1 = c
    while p1 < lim and not inside(p1 + st):
        p1 += st
    return max(p0, 0.0), min(p1, lim)


def side_rooms(fl, d):
    o = d["o"]
    m = d["a"] + d["w"] / 2
    p0, p1 = d.get("gap") or _span(fl, o, d["c"], m)
    def probe(t):
        x, y = (t, m) if o == "V" else (m, t)
        r = fl.room_at(x, y)
        if r:
            return r
        if o == "H" and y < 0:
            return "ROAD"
        if o == "H" and y > DFP:
            return "YARD"
        if o == "V" and (x < 0 or x > W):
            return "NEIGHBOUR"
        return None
    return probe(p0 - 0.05), probe(p1 + 0.05), (p0, p1)


# ------------------------------------------------------------------ orientation
def tf(facing, mirror):
    def f(x, y):
        if mirror:
            x = W - x
        return {"E": (D - y, x), "N": (W - x, D - y), "W": (y, W - x), "S": (x, y)}[facing]
    return f


def zone(facing, mirror, x, y):
    e, n = tf(facing, mirror)(x, y)
    ew, ns = (D, W) if facing in "EW" else (W, D)
    c = 0 if e < ew / 3 else (1 if e < 2 * ew / 3 else 2)
    r = 0 if n < ns / 3 else (1 if n < 2 * ns / 3 else 2)
    return [["SW", "S", "SE"], ["W", "C", "E"], ["NW", "N", "NE"]][r][c]


VASTU = {  # kind -> (ideal, acceptable, forbidden); anything else is a compromise (0 points)
    "toilet": ({"NW", "W"}, {"S"}, {"NE", "C", "E", "SW"}), "wc": ({"NW", "W"}, {"S"}, {"NE", "C", "E", "SW"}),
    "kitchen": ({"SE"}, {"NW"}, {"NE", "SW", "C"}),
    "master": ({"SW"}, {"S", "W", "NW"}, {"NE", "SE", "C"}),
    "bed": ({"W", "NW"}, {"SW", "S", "N", "E"}, {"NE", "C"}),
    "living": ({"N", "NE", "E"}, {"NW", "W"}, {"C"}),
    "hall": ({"W", "E", "N"}, {"NW", "NE", "SE"}, set()),
    "hall2": ({"W", "E", "N"}, {"NW", "NE", "SE"}, set()),
    "guest": ({"NW", "W"}, {"S"}, {"NE", "C", "SW"}),
    "stair": ({"S", "W", "SW"}, {"NW", "SE"}, {"NE", "C", "N", "E"}),
    "dining": ({"W", "E"}, {"N", "NW", "SE", "S"}, {"C"}),
    "pooja": ({"NE"}, {"N", "E"}, {"S", "SW", "SE", "C"}),
    "cabin": ({"SW", "S", "W"}, {"NW"}, {"NE", "C"}),
    "store": ({"SW", "W"}, {"S", "NW"}, {"NE", "C"}),
    "godown": ({"SW", "W", "S"}, {"NW"}, {"NE", "C"}),
}
ENTRY_OK = {"E": {"E", "NE"}, "N": {"N", "NE"}, "W": {"W", "NW"}, "S": {"S", "SE"}}


def vastu(plan, facing, mirror):
    """returns (forbidden_list, points, max_points, details)"""
    bad, pts, mx, det = [], 0, 0, []
    for fl in plan["floors"]:
        for r in fl.rooms:
            if r.kind not in VASTU:
                continue
            ideal, ok, no = VASTU[r.kind]
            z = zone(facing, mirror, *r.centroid())
            mx += 2
            if z in ideal:
                pts += 2
                lv = "ideal"
            elif z in ok:
                pts += 1
                lv = "acceptable"
            elif z in no:
                bad.append(f"{fl.code}:{r.name} in {z}")
                lv = "AVOID"
            else:
                lv = "compromise"
            det.append((fl.code, r.name, z, lv))
    g = plan["floors"][0]
    for d in g.doors:
        if d["kind"] == "shutter":
            z = zone(facing, mirror, d["a"] + d["w"] / 2, 0.1)
            mx += 2
            if z in ENTRY_OK[facing]:
                pts += 2
                det.append(("G", "Shop entrance", z, "ideal"))
            else:
                bad.append(f"shop entrance in {z}")
                det.append(("G", "Shop entrance", z, "AVOID"))
    t = plan["floors"][-1]
    if hasattr(t, "tank"):
        z = t.tank[2]
        mx += 2
        lv = "ideal" if z in ("SW", "W", "S") else ("acceptable" if z in ("NW", "SE") else "AVOID")
        pts += {"ideal": 2, "acceptable": 1}.get(lv, 0)
        if lv == "AVOID":
            bad.append(f"T:tank in {z}")
        det.append(("T", "Overhead tank", z, lv))
    return bad, pts, mx, det


# ------------------------------------------------------------------ checks
def rect_overlap(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]) > 1e-6 and min(a[3], b[3]) - max(a[1], b[1]) > 1e-6


def geo_checks(plan):
    errs, info = [], []
    for fl in plan["floors"]:
        if fl.code == "T":
            continue
        rs = [(r, q) for r in fl.rooms for q in r.rects]
        for i, (r, a) in enumerate(rs):
            if a[0] < X0 - 1e-6 or a[2] > X1 + 1e-6 or a[1] < Y0 - 1e-6 or a[3] > Y1 + 1e-6:
                errs.append(f"{fl.code}:{r.name} outside walls {a}")
            for r2, b in rs[i + 1:]:
                if r2 is r:
                    continue
                if rect_overlap(a, b):
                    errs.append(f"{fl.code}:{r.name} overlaps {r2.name}")
                else:
                    gx = max(b[0] - a[2], a[0] - b[2])
                    gy = max(b[1] - a[3], a[1] - b[3])
                    if (gx < TW - 1e-3 and gy < -1e-6) or (gy < TW - 1e-3 and gx < -1e-6):
                        if min(a[3], b[3]) - max(a[1], b[1]) > 1e-6 or min(a[2], b[2]) - max(a[0], b[0]) > 1e-6:
                            errs.append(f"{fl.code}:{r.name}/{r2.name} wall thinner than 4.5in")
        for r in fl.rooms:
            a = r.area()
            mw = r.minwidth()
            if r.kind in ("master", "bed", "living", "hall", "hall2", "dining", "cabin"):
                lim = 7.87 if r.kind in ("master", "living", "hall", "hall2") else (6.5 if r.kind == "dining" else 7.0)
                if mw < lim - 1e-6:
                    errs.append(f"{fl.code}:{r.name} width {mw:.2f} < {lim} ft")
                if a < (100 if r.kind == "master" else 80):
                    errs.append(f"{fl.code}:{r.name} area {a:.0f} < 80")
            if r.kind == "kitchen" and (a < 48 - 0.5 or mw < 5.9):
                errs.append(f"{fl.code}:{r.name} kitchen {a:.0f} sqft / {mw:.1f} ft too small")
            if r.kind == "toilet" and (a < 23.5 or mw < 3.94):
                errs.append(f"{fl.code}:{r.name} toilet {a:.0f} sqft / {mw:.2f} ft too small")
            if r.kind == "guest" and (a < 17 or mw < 3.3):
                errs.append(f"{fl.code}:{r.name} guest wc {a:.0f} sqft / {mw:.2f} ft too small")
            if r.kind == "wc" and (a < 11.8 or mw < 2.95):
                errs.append(f"{fl.code}:{r.name} wc too small")
            if r.kind == "passage" and mw < 3.0:
                errs.append(f"{fl.code}:{r.name} passage {mw:.2f} < 3 ft")
        # doors
        graph = {}
        for d in fl.doors:
            A, B, _ = side_rooms(fl, d)
            if A is None or B is None:
                errs.append(f"{fl.code}: door at {d['o']}{d['c']:.2f},{d['a']:.2f} not on a wall")
                continue
            if d["w"] < (2.0 if d["kind"] in ("service", "fdoor") else 2.4):
                errs.append(f"{fl.code}: door too narrow {d['w']}")
            na = A if isinstance(A, str) else A.name
            nb = B if isinstance(B, str) else B.name
            graph.setdefault(na, set()).add(nb)
            graph.setdefault(nb, set()).add(na)
        start = "ROAD" if fl.code == "G" else ("Staircase" if fl.code == "F" else "Mumty")
        seen, st = {start}, [start]
        while st:
            u = st.pop()
            for v in graph.get(u, ()):
                if v not in seen:
                    seen.add(v)
                    st.append(v)
        for r in fl.rooms:
            if r.name not in seen and r.kind not in ("void", "duct"):
                errs.append(f"{fl.code}:{r.name} not reachable by a door")
        # windows / openings
        light = {}
        for w in fl.wins:
            m = w["a"] + w["w"] / 2
            p0, p1 = _span(fl, w["o"], w["c"], m)
            for t in (p0 - 0.05, p1 + 0.05):
                x, y = (t, m) if w["o"] == "V" else (m, t)
                r = fl.room_at(x, y)
                if r is not None:
                    other = (p1 + 0.05) if t == p0 - 0.05 else (p0 - 0.05)
                    ox, oy = (other, m) if w["o"] == "V" else (m, other)
                    o2 = fl.room_at(ox, oy)
                    ok = (o2 is None) or o2.kind in ("court", "duct")
                    if ok:
                        light[r.name] = light.get(r.name, 0) + w["w"] * w["h"]
        for d in fl.doors:
            if d["kind"] in ("fdoor", "shutter"):
                A, B, _ = side_rooms(fl, d)
                for X, Y in ((A, B), (B, A)):
                    if X is not None and not isinstance(X, str) and (isinstance(Y, str) or Y.kind == "court"):
                        light[X.name] = light.get(X.name, 0) + d["w"] * (7.0 if d["kind"] == "shutter" else 6.5)
        for nm_, a_ in getattr(fl, "sky", {}).items():
            light[nm_] = light.get(nm_, 0) + a_
        for r in fl.rooms:
            need = {"master": 1 / 6, "bed": 1 / 6, "living": 1 / 6, "hall": 1 / 8, "hall2": 1 / 10, "guest": 1 / 10, "dining": 1 / 8, "cabin": 1 / 8,
                    "kitchen": 1 / 8, "toilet": 1 / 10, "wc": 1 / 10, "shop": 1 / 10}.get(r.kind)
            if need and light.get(r.name, 0) < need * r.area() - 1e-6:
                errs.append(f"{fl.code}:{r.name} openings {light.get(r.name, 0):.1f} < {need * r.area():.1f} sqft")
    return errs


def stair_info():
    return dict(risers=NRISE, riser_in=RISER_IN, tread_in=TREAD_IN, floor_to_floor_ft=FLOOR_H,
                flight_run_ft=S_FL, width_ft=SX1 - SX0, headroom_ft=HEAD,
                slab_open_from=YO1, pitch_deg=math.degrees(math.atan(RISER_IN / TREAD_IN)))


# ------------------------------------------------------------------ drawing
def _poly(ax, pts, **k):
    ax.add_patch(Polygon(pts, closed=True, **k))


def _rect(T, r):
    return [T(r[0], r[1]), T(r[2], r[1]), T(r[2], r[3]), T(r[0], r[3])]


def draw_floor(ax, fl, plan, facing, mirror, ox, oy, fs=6.5, show_dims=True):
    f = tf(facing, mirror)
    T = lambda x, y: (f(x, y)[0] + ox, f(x, y)[1] + oy)
    ew, ns = (D, W) if facing in "EW" else (W, D)
    # plot boundary + rear yard + road
    _poly(ax, [T(0, 0), T(W, 0), T(W, D), T(0, D)], fc="#FBFBF6", ec="#B03030", lw=0.9, ls=(0, (5, 3)), zorder=1)
    _poly(ax, [T(0, DFP), T(W, DFP), T(W, D), T(0, D)], fc="#E3F0D3", ec="none", zorder=1.1)
    xc, yc = T(W / 2, DFP + REAR / 2)
    ax.text(xc, yc, "REAR OPEN YARD 5'-0\"", ha="center", va="center", fontsize=fs - 1, color="#456", zorder=3,
            rotation=0 if facing in "NS" else 90)
    # building
    if fl.solid:
        _poly(ax, [T(0, 0), T(W, 0), T(W, DFP), T(0, DFP)], fc="#2c2c2c", ec="#111", lw=0.5, zorder=2)
    else:
        _poly(ax, [T(0, 0), T(W, 0), T(W, DFP), T(0, DFP)], fc="#2c2c2c", ec="#111", lw=0.5, zorder=2)
    for r in fl.rooms:
        for q in r.rects:
            _poly(ax, _rect(T, q), fc=COLORS.get(r.kind, "#fff"), ec=COLORS.get(r.kind, "#fff"), lw=0.6, zorder=3)
        if r.kind == "court":
            for q in r.rects:
                _poly(ax, _rect(T, q), fc="none", ec="#6a9a4a", hatch="xx", lw=0, zorder=3.2)
    # openings: windows
    for w in fl.wins:
        m = w["a"] + w["w"] / 2
        p0, p1 = _span(fl, w["o"], w["c"], m)
        a, b = w["a"], w["a"] + w["w"]
        if w["o"] == "V":
            cut = [(p0, a), (p1, a), (p1, b), (p0, b)]
            lines = [((p0, a), (p0, b)), ((p1, a), (p1, b)), (((p0 + p1) / 2, a), ((p0 + p1) / 2, b))]
        else:
            cut = [(a, p0), (b, p0), (b, p1), (a, p1)]
            lines = [((a, p0), (b, p0)), ((a, p1), (b, p1)), ((a, (p0 + p1) / 2), (b, (p0 + p1) / 2))]
        _poly(ax, [T(*c) for c in cut], fc="#F2F9FF", ec="none", zorder=4)
        for (u, v) in lines:
            (x1, y1), (x2, y2) = T(*u), T(*v)
            ax.plot([x1, x2], [y1, y2], color="#1a6aa8", lw=0.7, zorder=4.2)
    # doors
    for d in fl.doors:
        m = d["a"] + d["w"] / 2
        A, B, (p0, p1) = side_rooms(fl, d)
        a, b = d["a"], d["a"] + d["w"]
        if d["o"] == "V":
            cut = [(p0, a), (p1, a), (p1, b), (p0, b)]
        else:
            cut = [(a, p0), (b, p0), (b, p1), (a, p1)]
        floorc = "#F7F2E8"
        _poly(ax, [T(*c) for c in cut], fc=floorc, ec="none", zorder=4)
        if d["kind"] == "arch":
            continue
        if d["kind"] == "shutter":
            for t in (p0, p1):
                pts = [(t, a), (t, b)] if d["o"] == "V" else [(a, t), (b, t)]
                (x1, y1), (x2, y2) = T(*pts[0]), T(*pts[1])
                ax.plot([x1, x2], [y1, y2], color="#C0392B", lw=1.8, zorder=5)
            mid = (p0 + p1) / 2
            pts = [(a, mid), (b, mid)]
            (x1, y1), (x2, y2) = T(*pts[0]), T(*pts[1])
            ax.plot([x1, x2], [y1, y2], color="#C0392B", lw=1.0, ls=(0, (2, 1.5)), zorder=5)
            continue
        c = d["c"]
        sd = d["side"]
        if d["o"] == "V":
            hp = (c, a if d["hinge"] == "a" else b)
            cv = (0, 1 if d["hinge"] == "a" else -1)
            ov = (sd, 0)
        else:
            hp = (a if d["hinge"] == "a" else b, c)
            cv = (1 if d["hinge"] == "a" else -1, 0)
            ov = (0, sd)
        w = d["w"]
        a0, a1 = math.atan2(cv[1], cv[0]), math.atan2(ov[1], ov[0])
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        arc = [T(hp[0] + w * math.cos(a0 + da * i / 14), hp[1] + w * math.sin(a0 + da * i / 14)) for i in range(15)]
        ax.plot([p[0] for p in arc], [p[1] for p in arc], color="#555", lw=0.5, ls=(0, (2, 2)), zorder=5)
        e = T(hp[0] + w * ov[0], hp[1] + w * ov[1])
        h = T(*hp)
        ax.plot([h[0], e[0]], [h[1], e[1]], color="#222", lw=1.0, zorder=5)
        if d["kind"] == "fdoor":
            ax.plot([h[0], e[0]], [h[1], e[1]], color="#1a6aa8", lw=1.6, zorder=5)
    # extras: stair flights, texts, hatches, fixtures
    for ex in fl.extra:
        t = ex[0]
        if t == "flight":                     # ('flight', xa, xb, ya, yb, n, label)
            _, xa, xb, ya, yb, n, lab = ex
            for i in range(n + 1):
                yy = ya + (yb - ya) * i / n
                p, q = T(xa, yy), T(xb, yy)
                ax.plot([p[0], q[0]], [p[1], q[1]], color="#777", lw=0.5, zorder=4.5)
            xm = (xa + xb) / 2
            s, e = (ya + 0.4, yb - 0.4) if lab == "UP" else (yb - 0.4, ya + 0.4)
            p, q = T(xm, s), T(xm, e)
            ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="-|>", color="#222", lw=0.8), zorder=6)
            lp = T(xm, (ya + yb) / 2)
            ax.text(lp[0], lp[1], lab, fontsize=fs - 1, ha="center", va="center", zorder=6, color="#111",
                    bbox=dict(fc="#E4E4E4", ec="none", pad=0.6))
        elif t == "hatch":                    # ('hatch', rect, color)
            _poly(ax, _rect(T, ex[1]), fc="none", ec=ex[2], hatch="///", lw=0, zorder=4.4)
        elif t == "wall":                     # ('wall', clear rect): dark ring 4.5in around a clear rect
            r = ex[1]
            for q in ((r[0] - TW, r[1] - TW, r[2] + TW, r[1]), (r[0] - TW, r[3], r[2] + TW, r[3] + TW),
                      (r[0] - TW, r[1], r[0], r[3]), (r[2], r[1], r[2] + TW, r[3])):
                _poly(ax, _rect(T, q), fc="#2c2c2c", ec="#2c2c2c", lw=0.3, zorder=3.5)
        elif t == "box":                      # ('box', rect, fc, ec, label)
            _poly(ax, _rect(T, ex[1]), fc=ex[2], ec=ex[3], lw=0.7, zorder=4.6)
            if len(ex) > 4 and ex[4]:
                cx, cy = T((ex[1][0] + ex[1][2]) / 2, (ex[1][1] + ex[1][3]) / 2)
                ax.text(cx, cy, ex[4], fontsize=fs - 1.5, ha="center", va="center", zorder=6, linespacing=0.95)
        elif t == "line":                     # ('line', (x1,y1),(x2,y2), color, lw, ls)
            p, q = T(*ex[1]), T(*ex[2])
            ax.plot([p[0], q[0]], [p[1], q[1]], color=ex[3], lw=ex[4], ls=ex[5], zorder=5)
        elif t == "text":                     # ('text', x, y, s, size)
            p = T(ex[1], ex[2])
            ax.text(p[0], p[1], ex[3], fontsize=ex[4], ha="center", va="center", zorder=6, linespacing=0.95)
    # labels
    for r in fl.rooms:
        if r.kind in ("void",) or r.label == "":
            continue
        cx, cy = r.lp if r.lp else r.centroid()
        p = T(cx, cy)
        big = max(r.rects, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
        wd, ln = big[2] - big[0], big[3] - big[1]
        horiz, vert = (ln, wd) if facing in "EW" else (wd, ln)
        if len(r.rects) == 1:
            dims = f"{fi(horiz)} x {fi(vert)}" + (f"\n{r.area():.0f} sq ft" if r.area() >= 30 else "")
        else:
            dims = f"L-shape, {r.area():.0f} sq ft"
        small = min(horiz, vert) < 4.6
        txt = r.label + (f"\n{dims}" if show_dims and not getattr(r, "nodim", False) and r.kind not in ("tank", "court", "stair", "terrace", "mumty") else "")
        ax.text(p[0], p[1], txt, fontsize=fs - (1.2 if small else 0), ha="center", va="center", zorder=7,
                linespacing=1.0, color="#111")
    return T, ew, ns


def north_arrow(ax, x, y, s=2.2):
    ax.annotate("", xy=(x, y + s), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", color="#111", lw=1.4))
    ax.text(x, y + s + 0.3, "N", ha="center", va="bottom", fontsize=11, fontweight="bold")
