"""Layout modules (canonical frame, stair on the left). Each returns a Floor."""
from engine import *

FX = lambda x: W - x                      # flip across the plot centre line


def _fr(r, flip):                         # flip a rect
    return (FX(r[2]), r[1], FX(r[0]), r[3]) if flip else tuple(r)


def _fd(d, flip):                         # flip a door/window dict (V walls swap side, hinge)
    if not flip:
        return d
    d = dict(d)
    if d["o"] == "H":
        d["a"] = FX(d["a"] + d["w"])
        d["hinge"] = {"a": "b", "b": "a"}.get(d.get("hinge", "a"))
    else:
        d["c"] = FX(d["c"])
        d["side"] = -d["side"]
    return d


def _fw(w, flip):
    if not flip:
        return w
    w = dict(w)
    if w["o"] == "H":
        w["a"] = FX(w["a"] + w["w"])
    else:
        w["c"] = FX(w["c"])
    return w


SHAFT_G = (SX0, Y0, SX1, YF1)
LOB_LABEL_Y = (Y0 + YS0) / 2
SHUTTER = door("H", EW / 2, 5.15, 9.0, 1, kind="shutter")
STAIR_DOOR = door("H", EW / 2, 1.0, 3.0, 1)


def _stairG():
    r = Room("Staircase", "stair", [SHAFT_G], label="STAIR\nLOBBY", lp=(2.5, 2.3))
    ex = [("flight", SX0, SX1, YS0, YF1, 17, "UP"),
          ("line", (SX0, YS0), (SX1, YS0), "#444", 1.0, "-"),
          ]
    return r, ex


def ground(kind, flip=False):
    st, ex = _stairG()
    A = (PX0, Y0, X1, YF1 + TW)
    doors = [SHUTTER, STAIR_DOOR]
    wins = []
    rooms = [st]
    if kind == "G1":          # open showroom, store + toilet at rear
        Ys = 43.0
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, Ys)], label="SHOP / SHOWROOM", lp=(9.5, 28))
        store = Room("Store", "store", [_fr((X0, Ys + TW, 10.275, Y1), flip)])
        wc = Room("Toilet", "toilet", [_fr((10.65, Ys + TW, X1, Y1), flip)])
        rooms += [shop, store, wc]
        doors += [_fd(door("H", Ys + TW / 2, 2.5, 3.0, 1), flip), _fd(door("H", Ys + TW / 2, 11.1, 2.5, 1), flip),
                  _fd(door("H", DFP - EW / 2, 2.0, 3.0, -1, kind="door"), flip)]
        wins += [_fw(win("H", DFP - EW / 2, 11.6, 2.5, 1.5), flip), _fw(win("H", DFP - EW / 2, 6.0, 3.0, 3.0), flip)]
    elif kind == "G1C":       # toilet at rear centre, stores both sides
        Ys = 43.0
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, Ys)], label="SHOP / SHOWROOM", lp=(9.5, 28))
        s1 = Room("Store", "store", [(X0, Ys + TW, 5.4, Y1)])
        wc = Room("Toilet", "toilet", [(5.775, Ys + TW, 9.775, Y1)])
        s2 = Room("Pantry", "store", [(10.15, Ys + TW, X1, Y1)])
        rooms += [shop, s1, wc, s2]
        doors += [door("H", Ys + TW / 2, 1.7, 3.0, 1), door("H", Ys + TW / 2, 6.3, 2.5, 1),
                  door("H", Ys + TW / 2, 10.9, 3.0, 1), door("H", DFP - EW / 2, 1.9, 3.0, -1)]
        wins += [win("H", DFP - EW / 2, 6.7, 2.5, 1.5), win("H", DFP - EW / 2, 11.0, 2.5, 3.0)]
    elif kind == "G2":        # shop + cabin + store + toilet
        Ys = 36.0
        C = (9.375, Ys, X1, 45.475)
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, Ys), _fr(C, flip)], label="SHOP", lp=(8.0, 26))
        shop.rects = [A, (X0, YF1 + TW, X1, Ys), _fr(C, flip)]
        store = Room("Store", "store", [_fr((X0, Ys + TW, 9.0, 39.625), flip)])
        cabin = Room("Cabin / Office", "cabin", [_fr((X0, 40.0, 9.0, Y1), flip)], label="Cabin / Office")
        wc = Room("Toilet", "toilet", [_fr((9.375, 45.85, X1, Y1), flip)])
        rooms += [shop, store, cabin, wc]
        doors += [_fd(door("H", Ys + TW / 2, 2.0, 3.0, 1), flip), _fd(door("V", 9.1875, 42.0, 3.0, -1), flip),
                  _fd(door("H", 45.6625, 10.5, 2.5, 1), flip)]
        wins += [_fw(win("H", DFP - EW / 2, 2.5, 5.0, 4.0), flip), _fw(win("H", DFP - EW / 2, 10.8, 2.5, 1.5), flip)]
    elif kind == "G3":        # showroom + godown + toilet, rear service door
        Ys = 31.0
        shop = Room("Showroom", "shop", [A, (X0, YF1 + TW, X1, Ys)], label="SHOWROOM", lp=(9.5, 22))
        god = Room("Godown", "godown", [(X0, Ys + TW, X1, 45.475), _fr((X0, 45.475, 10.275, Y1), flip)], label="GODOWN / WORK AREA",
                   lp=(7.7, 38))
        god.rects = [(X0, Ys + TW, X1, 45.475), _fr((X0, 45.475, 10.275, Y1), flip)]
        wc = Room("Toilet", "toilet", [_fr((10.65, 45.85, X1, Y1), flip)])
        rooms += [shop, god, wc]
        doors += [door("H", Ys + TW / 2, 5.0, 4.0, 1), _fd(door("H", 45.6625, 11.1, 2.5, 1), flip),
                  _fd(door("H", DFP - EW / 2, 2.5, 3.5, -1), flip)]
        wins += [_fw(win("H", DFP - EW / 2, 5.5, 3.5, 3.0), flip), _fw(win("H", DFP - EW / 2, 11.6, 2.5, 1.5), flip)]
        # godown part under flip: toilet door must sit on the flipped wall
        if flip:
            doors[-2] = _fd(door("H", 45.6625, 11.1, 2.5, 1), True)
    return Floor("G", "GROUND FLOOR (COMMERCIAL)", rooms, doors, wins, ex)


# ------------------------------------------------------------------ first floor
YH0, YH1 = 13.275, 24.425           # hall band
CT = (8.65, 24.8, X1, 32.8)         # court
PS = (PX0, 24.8, 8.275, 41.175)     # passage


def first(typ="A", side="R", rf=False):
    stair = Room("Staircase", "stair", [(SX0, YO1 + TW, SX1, YF2)], label="", lp=None)
    ex = [("flight", SX0, SX1, YF1 - 11 * TREAD_IN / 12, YF1, 11, "DN"), ("flight", SX0, SX1, YL, YF2, 17, "UP"),
          ("hatch", (SX0, YF1 - 11 * TREAD_IN / 12, SX1, YF1), "#999")]
    ex = [e for e in ex if e[0] != "hatch"]
    doors = [door("V", (SX1 + PX0) / 2, 19.1, 3.0, 1)]
    wins = []
    rooms = [stair]
    B2 = (PX0, YO1, X1, 12.9)
    f = side == "L"
    if typ == "A":
        bed = Room("Bedroom 2", "bed", [_fr((X0, Y0, 10.275, YO1), f), _fr((10.275, 7.125, X1, YO1), f), B2], label="Bedroom 2",
                   lp=(7.7 if not f else 7.7, 5.0))
        t2 = Room("Toilet 2", "toilet", [_fr((10.65, Y0, X1, 6.75), f)])
        rooms += [bed, t2]
        doors += [_fd(door("H", 6.9375, 11.0, 2.5, -1), f), door("H", 13.0875, 5.5, 2.75, -1)]
        wins += [_fw(win("H", EW / 2, 1.5, 6.0), f), _fw(win("H", EW / 2, 11.5, 2.5, 1.5), f)]
        hall = Room("Hall", "hall", [(PX0, YH0, X1, YH1)], label="LIVING + DINING", lp=(9.6, 18.5))
        wc = None
        doors += [door("H", 24.6125, 10.0, 3.5, -1, kind="fdoor")]
    else:
        liv = Room("Living", "living", [(X0, Y0, X1, YO1), B2], label="LIVING + DINING", lp=(8.5, 5.0))
        rooms += [liv]
        wins += [win("H", EW / 2, 1.5, 5.0), win("H", EW / 2, 8.4, 5.0)]
        doors += [door("H", 13.0875, 5.5, 2.75, -1)]
        if side == "R":
            hall = Room("Hall", "dining", [(PX0, YH0, X1, 20.025), (PX0, 20.025, 11.275, YH1)], label="DINING / FOYER", lp=(8.5, 17.0))
            wc = Room("WC", "wc", [(11.65, 20.4, X1, YH1)], label="WC")
            doors += [door("H", 20.2125, 11.9, 2.5, 1), door("H", 24.6125, 8.75, 2.5, -1, kind="fdoor")]
            wins += [win("H", 24.6125, 12.0, 2.0, 1.5)]
        else:
            hall = Room("Hall", "dining", [(PX0, YH0, X1, 20.025), (PX0, 20.025, 8.275, YH1), (12.025, 20.025, X1, YH1)],
                        label="DINING / FOYER", lp=(8.5, 17.0))
            wc = Room("WC", "wc", [(8.65, 20.4, 11.65, YH1)], label="WC")
            doors += [door("H", 20.2125, 8.9, 2.5, 1), door("H", 24.6125, 12.1, 2.5, -1, kind="fdoor")]
            wins += [win("H", 24.6125, 9.0, 2.0, 1.5)]
    rooms.append(hall)
    if wc:
        rooms.append(wc)
    court = Room("Court", "court", [CT], label="COURT\n(open to sky)", lp=(11.65, 28.8))
    ps = Room("Passage", "passage", [PS], label="PASSAGE", lp=(6.4, 30))
    kit = Room("Kitchen", "kitchen", [(8.65, 33.175, X1, 41.175)], label="KITCHEN")
    sto = Room("Store", "store", [(X0, 37.183, SX1, 41.175)], label="Store")
    M = [(X0, 41.55, 10.275, Y1), (10.65, 41.55, X1, 45.475)]
    master = Room("Master Bedroom", "master", [_fr(m, rf) for m in M], label="Master Bedroom", lp=(FX(5.5) if rf else 5.5, 46.7))
    t1 = Room("Master Toilet", "toilet", [_fr((10.65, 45.85, X1, Y1), rf)], label="Toilet")
    rooms += [court, ps, kit, sto, master, t1]
    doors += [door("H", 24.6125, 4.9, 3.0, 1, kind="arch"),
              door("V", 8.4625, 34.0, 2.75, 1), door("V", (SX1 + PX0) / 2, 37.5, 2.5, -1),
              door("H", 41.3625, 5.4, 2.75, 1), _fd(door("V", 10.4625, 47.2, 2.5, 1), rf)]
    wins += [win("H", 32.9875, 10.0, 3.0), win("V", 8.4625, 26.0, 3.0),
             _fw(win("H", DFP - EW / 2, 3.0, 6.0), rf), _fw(win("H", DFP - EW / 2, 11.5, 2.5, 1.5), rf)]
    return Floor("F", "FIRST FLOOR (RESIDENTIAL)", rooms, doors, wins, ex)


# ------------------------------------------------------------------ terrace
MUM = (SX0, 25.9, SX1, 39.7)
CAND = {
    "tank": [(1.0, 46.4, 5.5, 50.9), (9.9, 46.4, 14.4, 50.9), (1.0, 1.0, 5.5, 5.5), (9.9, 1.0, 14.4, 5.5),
             (5.6, 46.4, 10.1, 50.9), (9.9, 34.6, 14.4, 39.1), (5.2, 14.0, 9.7, 18.5)],
    "garden": [(9.9, 1.0, 14.4, 7.0), (1.0, 1.0, 6.0, 7.0), (9.9, 44.9, 14.4, 50.9), (1.0, 44.9, 6.0, 50.9),
               (9.9, 34.6, 14.4, 40.6), (5.2, 12.5, 14.4, 17.5)],
    "solar": [(5.2, 41.0, 14.4, 45.0), (5.2, 8.0, 14.4, 12.0), (5.2, 14.0, 14.4, 18.0), (1.0, 8.0, 5.2, 16.0)],
}


def _pick(kind, facing, mirror, used):
    best = None
    for c in CAND[kind]:
        if any(rect_overlap(c, u) for u in used):
            continue
        z = zone(facing, mirror, (c[0] + c[2]) / 2, (c[1] + c[3]) / 2)
        sc = {"tank": {"SW": 5, "W": 4, "S": 4, "NW": 2, "SE": 2},
              "garden": {"NE": 5, "N": 4, "E": 4, "NW": 1, "SE": 1},
              "solar": {"S": 5, "SW": 4, "SE": 4, "W": 2, "E": 2}}[kind].get(z, 0)
        if best is None or sc > best[0]:
            best = (sc, c, z)
    return best


def terrace(var, facing, mirror):
    tr = Room("Open Terrace", "terrace", [(TW, TW, W - TW, DFP - TW)], label="", lp=None)
    mum = Room("Mumty", "mumty", [MUM], label="MUMTY", lp=(2.5, 33.0))
    court = Room("Court", "court", [CT], label="COURT VOID\n(open to sky)", lp=(11.65, 28.8))
    ring = (CT[0] - TW, CT[1] - TW, CT[2] + TW, CT[3] + TW)
    ex = [("wall", MUM), ("wall", CT),
          ("flight", SX0, SX1, 26.38, YF2, 12, "UP")]
    ex = [e for e in ex if e[0] != "flight"]
    ex.append(("text", 9.5, 22.2, "OPEN TERRACE", 9))
    used = [MUM, CT]
    notes = []
    tk = _pick("tank", facing, mirror, used)
    used.append(tk[1])
    ex.append(("box", tk[1], "#B9D7F0", "#2a6a9a", "OVERHEAD TANK 1000 L"))
    rooms = [mum, tr, court]
    rooms = [tr, court, mum]
    zones = {"tank": tk[2]}
    sol = _pick("solar", facing, mirror, used)
    if sol:
        used.append(sol[1])
        ex.append(("box", sol[1], "#F4D77A", "#8a6d00", "SOLAR PV ZONE"))
        zones["solar"] = sol[2]
    if var == 2:
        g = _pick("garden", facing, mirror, used)
        if g:
            used.append(g[1])
            ex.append(("box", g[1], "#CFE6B8", "#4a7a2a", "GARDEN / TULSI\nSEATING"))
            zones["garden"] = g[2]
    else:
        dr = (5.2, 8.0, 9.2, 12.0)
        if not any(rect_overlap(dr, u) for u in used):
            used.append(dr)
        ex.append(("box", (0.9, 19.0, 4.4, 22.4), "#F2EBDD", "#8a8a8a", "CLOTHES\nDRYING"))
    for (x, y) in ((1.2, 1.2), (14.2, 1.2), (1.2, 51.4), (14.2, 51.4)):
        ex.append(("box", (x - 0.25, y - 0.25, x + 0.25, y + 0.25), "#FFFFFF", "#333", ""))
    doors = [dict(door("V", (SX1 + TW / 2), 36.6, 3.0, 1), gap=(SX1, PX0))]
    fl = Floor("T", "TERRACE (SECOND FLOOR LEVEL)", rooms, doors, [], ex)
    fl.zones = zones
    fl.tank = tk
    return fl


def build(g, f, fa, fm, t):
    """g=(kind,flip) f=(typ,side,rf) t=var"""
    fl = [ground(*g), first(*f)]
    fl.append(terrace(t, fa, fm))
    return dict(floors=fl, g=g, f=f, t=t)
