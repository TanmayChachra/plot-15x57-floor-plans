"""North set v3: many real variations on the same constrained frame.
Fixed by the plot: stair spine (west), court + passage, kitchen-duct-toilet stack (east rear), common WC off the hall.
Varied: bedroom roles, front balcony, kitchen type, living layout, court feature, door hinges,
shop rear (4 types), shutter style, shop fittings, terrace (4 types)."""
from layouts_n import *
import layouts_n as N
import layouts as L

COLORS["balcony"] = "#E3EEC8"
FIX = "#8a8a8a"
LIGHT = "#F0F0F0"


def bx(r, label="", fc=LIGHT):
    return ("box", r, fc, FIX, label)


# ---------------------------------------------------------------- first floor
KITCHENS = {
    "K1": ([bx((12.65, 33.55, 14.45, 40.9)), bx((9.0, 39.6, 12.4, 41.0), "SINK")], (10.3, 36.9), "straight platform"),
    "K2": ([bx((12.65, 33.55, 14.45, 41.0)), bx((9.0, 39.3, 12.65, 41.0), "SINK"), bx((10.9, 33.6, 12.5, 35.4), "FRIDGE")],
            (10.4, 37.4), "L-shaped platform"),
    "K3": ([bx((12.65, 33.55, 14.45, 40.9)), bx((12.65, 36.2, 14.45, 38.2), "SINK"), bx((8.8, 37.3, 10.3, 40.8), "SHELF"),
            bx((10.8, 33.6, 12.4, 35.2), "FRIDGE")], (10.9, 38.6), "parallel platform"),
}
LIVINGS = {
    "L1": ([bx((4.95, 10.0, 6.95, 13.4), "SOFA"), bx((10.2, 9.5, 14.4, 10.4), "TV UNIT"), bx((9.4, 14.6, 13.4, 17.6), "DINING"),
            bx((13.9, 11.0, 14.65, 12.8), "P", "#FFF0B8")], (10.6, 12.4)),
    "L2": ([bx((5.2, 9.9, 9.2, 12.9), "DINING"), bx((4.95, 13.6, 5.75, 16.4), "TV"), bx((10.2, 15.4, 14.4, 17.8), "SOFA"),
            bx((13.9, 9.4, 14.65, 11.2), "P", "#FFF0B8")], (9.7, 14.2)),
    "L3": ([bx((10.2, 9.4, 14.4, 11.6), "SOFA"), bx((5.2, 14.4, 9.2, 17.4), "DINING"), bx((4.95, 9.4, 5.75, 12.2), "TV"),
            bx((13.9, 12.4, 14.65, 14.2), "P", "#FFF0B8"), bx((5.0, 22.2, 6.2, 24.2), "SHOE")], (9.0, 12.9)),
}
COURTS = {
    "C1": [bx((10.9, 25.3, 12.5, 26.9), "TULSI", "#FFF0B8")],
    "C2": [bx((9.0, 25.2, 9.9, 26.1), "", "#B7D99B"), bx((13.7, 31.6, 14.5, 32.5), "", "#B7D99B"), bx((11.0, 26.2, 12.6, 27.6), "WATER", "#CFE3F5")],
    "C3": [bx((13.6, 25.2, 14.5, 32.4), "JAALI BENCH", "#E8DCC4")],
}


def first_v3(role="M", balcony=False, kit="K1", liv="L1", court="C1", hinge="a", bedset=1):
    hb = {"a": "b", "b": "a"}[hinge]
    stair = Room("Staircase", "stair", [(SX0, YO1 + TW, SX1, YF2)], label="")
    ex = [("flight", SX0, SX1, YF1 - 11 * TREAD_IN / 12, YF1, 11, "DN"), ("flight", SX0, SX1, YL, YF2, 17, "UP")]
    fk, fn = ("bed", "Bedroom 2") if role == "M" else ("master", "Master Bedroom")
    rk, rn = ("master", "Master Bedroom") if role == "M" else ("bed", "Bedroom 2")
    wins = []
    doors = [door("V", (SX1 + PX0) / 2, 19.1, 3.0, 1, hinge)]
    rooms = [stair]
    if balcony:
        r1, r2 = (X0, Y0, 8.125, YO1), (8.125, 4.375, X1, YO1)
        front = Room(fn, fk, [r1, r2], label=fn + "\n(with balcony)\n87 sq ft", lp=(10.4, 6.5))
        front.nodim = True
        bal = Room("Balcony", "balcony", [(8.5, Y0, X1, 4.0)], label="BALCONY\n6'-2\" x 3'-3\"", lp=(11.6, 2.4))
        bal.nodim = True
        rooms += [front, bal]
        doors += [door("H", 4.1875, 10.2, 3.0, 1, kind="fdoor"), door("H", (YO1 + YO1 + TW) / 2, 5.5, 2.75, -1, hinge)]
        wins += [win("H", EW / 2, 1.3, 5.2), win("H", EW / 2, 9.2, 4.6, 3.5)]
        furn = [bx((2.3, 1.6, 7.3, 8.1), "BED"), bx((13.3, 5.0, 14.5, 8.4), "W")]
    else:
        front = Room(fn, fk, [(X0, Y0, X1, YO1)], label=fn, lp=(5.9, 4.6))
        rooms += [front]
        doors += [door("H", (YO1 + YO1 + TW) / 2, 5.5, 2.75, -1, hinge)]
        wins += [win("H", EW / 2, 2.0, 6.0), win("H", EW / 2, 10.0, 3.0)]
        if bedset == 1:
            furn = [bx((9.4, 1.4, 14.4, 7.9), "BED"), bx((0.95, 3.0, 2.75, 7.6), "WARD")]
        else:
            furn = [bx((2.1, 1.4, 7.1, 7.9), "BED"), bx((12.6, 2.6, 14.45, 7.4), "WARD")]
            front.lp = (10.6, 4.6)
    H1 = (PX0, YO1 + TW, X1, 18.4)
    H2 = (PX0, 18.4, 10.775, YH1)
    lf, llp = LIVINGS[liv][0], LIVINGS[liv][1]
    hall = Room("Living + Dining", "hall2", [H1, H2], label="LIVING + DINING\n10'-0\" x 9'-4\" (L-shape)\n130 sq ft", lp=llp)
    hall.nodim = True
    cw = Room("Common WC", "guest", [(11.15, 18.775, X1, YH1)], label="COMMON WC", lp=(12.9, 21.6))
    ct = Room("Court", "court", [CT], label="COURT\n(open to sky)", lp=(11.65, 29.9))
    ps = Room("Passage", "passage", [PS], label="PASSAGE", lp=(6.4, 30))
    kt = Room("Kitchen", "kitchen", [KIT], label="KITCHEN", lp=KITCHENS[kit][1])
    duct = Room("Duct", "duct", [DUCT], label="DUCT")
    master = Room(rn, rk, [(X0, 41.55, 10.275, Y1), (X0, YF2 + TW, SX1, 41.55)],
                  label=rn.upper() + "\n9'-6\" x 10'-4\" + nook\n115 sq ft", lp=(6.3, 50.6))
    master.nodim = True
    t1 = Room("Attached Toilet", "toilet", [T1R], label="Attached\nToilet")
    rooms += [hall, cw, ct, ps, kt, duct, master, t1]
    doors += [door("H", 24.6125, 8.7, 2.05, -1, kind="fdoor"), door("H", 24.6125, 4.9, 3.0, 1, kind="arch"),
              door("V", 10.9625, 19.5, 2.4, 1, hinge), door("V", 8.4625, 34.0, 2.75, 1, hb),
              door("H", 41.3625, 5.4, 2.75, 1, hb), door("V", 10.4625, 47.2, 2.5, 1, hinge)]
    wins += [win("H", 24.6125, 11.8, 2.0, 1.5), win("H", 32.9875, 10.0, 3.0), win("V", 8.4625, 26.0, 3.0),
             win("H", 41.3625, 11.0, 3.0, 3.0), win("H", 45.6625, 11.3, 2.0, 1.5),
             win("H", DFP - EW / 2, 3.0, 6.0), win("H", DFP - EW / 2, 11.5, 2.5, 1.5)]
    ex += furn + lf + KITCHENS[kit][0] + COURTS[court]
    ex += [bx((0.95, 37.5, 3.1, 41.3), "WARD")]
    if bedset == 1:
        ex += [bx((3.6, 44.4, 10.0, 49.2), "BED"), bx((0.95, 43.0, 2.9, 48.0), "WARD")]
    else:
        ex += [bx((1.1, 44.4, 7.5, 49.2), "BED"), bx((8.0, 43.4, 10.0, 48.6), "WARD")]
    ex += [bx((13.0, 18.95, 14.4, 20.0), "WC"), bx((13.0, 23.1, 14.4, 24.2), "WB"),
           bx((10.8, 46.2, 12.1, 48.0), "WC"), bx((13.2, 49.6, 14.4, 50.8), "WB")]
    return Floor("F", "FIRST FLOOR (RESIDENTIAL, 2 BEDROOMS)", rooms, doors, wins, ex)


# ---------------------------------------------------------------- ground floor
SHUTTERS = {"S1": [door("H", EW / 2, 5.15, 9.0, 1, kind="shutter")],
            "S2": [door("H", EW / 2, 5.15, 4.3, 1, kind="shutter"), door("H", EW / 2, 9.85, 4.3, 1, kind="shutter")],
            "S3": [door("H", EW / 2, 6.65, 7.5, 1, kind="shutter")]}
SHOPFIX = {
    "F1": [bx((5.0, 5.2, 5.6, 17.5), "", "#E8DCC4"), bx((14.0, 5.2, 14.6, 40.0), "", "#E8DCC4"),
           bx((6.2, 2.0, 11.0, 3.8), "CASH COUNTER 6'-0\" x 2'-0\"", "#F5D9A8")],
    "F2": [bx((6.5, 8.0, 12.5, 12.0), "DISPLAY ISLAND", "#F5D9A8"), bx((6.5, 20.0, 12.5, 24.0), "DISPLAY ISLAND", "#F5D9A8"),
           bx((12.4, 1.9, 14.4, 5.0), "COUNTER", "#F5D9A8"), bx((1.0, 20.0, 1.7, 40.5), "", "#E8DCC4")],
    "F3": [bx((5.0, 12.0, 5.6, 40.0), "", "#E8DCC4"), bx((14.0, 12.0, 14.6, 40.0), "", "#E8DCC4"),
           bx((7.0, 14.0, 13.0, 15.6), "DISPLAY TABLE", "#F5D9A8"), bx((9.0, 2.0, 13.8, 3.6), "COUNTER", "#F5D9A8")],
}


def ground_v3(kind, shut="S1", fix="F1"):
    if kind == "GE":
        fl = N.ground_n("GA")
        for r in fl.rooms:
            if r.name == "Store":
                r.label = "Store + loft\n9'-6\" x 10'-4\"\n98 sq ft"
                r.lp = (5.5, 49.2)
                r.nodim = True
        fl.extra.append(("box", (0.95, 41.9, 10.1, 46.2), "none", "#555", "LOFT above"))
    else:
        fl = N.ground_n(kind)
    fl.doors = [d for d in fl.doors if d["kind"] != "shutter"] + [dict(d) for d in SHUTTERS[shut]]
    fl.extra += SHOPFIX[fix]
    return fl


# ---------------------------------------------------------------- terrace
def terrace_v3(var, facing="N", mirror=True):
    base = N.terrace_n(1 if var in (1, 3, 4) else 2)
    if var == 3:
        base.extra.append(bx((5.6, 1.6, 14.3, 7.4), "PERGOLA + SEATING 8'-9\" x 5'-9\"", "#E7F0D8"))
        for (x, y) in ((5.9, 2.0), (14.0, 2.0), (5.9, 7.0), (14.0, 7.0)):
            base.extra.append(bx((x - 0.15, y - 0.15, x + 0.15, y + 0.15), "", "#555"))
    if var == 4:
        base.extra.append(("wall", (1.0, 8.0, 6.4, 15.6)))
        base.extra.append(bx((1.0, 8.0, 6.4, 15.6), "TERRACE\nSTORE + WASH\n5'-5\" x 7'-7\"", "#E8DCC4"))
    return base


def build_v3(spec):
    g = ground_v3(spec["g"], spec["shut"], spec["fix"])
    f = first_v3(spec["role"], spec["bal"], spec["kit"], spec["liv"], spec["court"], spec["hinge"], spec["bedset"])
    t = terrace_v3(spec["t"])
    return dict(floors=[g, f, t], g=(spec["g"], False), f=("V3", False), t=spec["t"], spec=spec)
