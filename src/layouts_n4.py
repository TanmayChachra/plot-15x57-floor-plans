"""North set v4: NO open court. The centre is built over (hall + passage lit by closed skylights
in the terrace slab). The only open void is a small services duct between common washroom and kitchen."""
from layouts_n3 import *
import layouts_n3 as V3

DUCT2 = (8.65, 29.5, X1, 32.8)            # 6'-0" x 3'-4" = 19.8 sq ft
WC2 = (8.65, 24.8, X1, 29.125)            # common washroom 6'-0" x 4'-4"
KIT2 = KIT
SK1 = (6.0, 11.0, 13.0, 20.5)             # hall skylight on terrace
SK2 = (5.0, 26.5, 7.9, 38.0)              # passage skylight
T1CL = (10.65, 41.55, X1, 45.475)         # master closet (was duct slot)

LIV_NC = {
    "L1": ([bx((4.95, 10.0, 6.95, 13.4), "SOFA"), bx((10.2, 9.5, 14.4, 10.4), "TV UNIT"), bx((9.4, 17.0, 13.6, 20.4), "DINING 6"),
            bx((13.9, 12.0, 14.65, 13.8), "P", "#FFF0B8")], (9.4, 14.2)),
    "L2": ([bx((5.2, 9.9, 9.6, 12.9), "DINING 6"), bx((4.95, 15.0, 5.75, 18.4), "TV"), bx((9.8, 16.6, 14.4, 19.0), "SOFA"),
            bx((13.9, 9.4, 14.65, 11.2), "P", "#FFF0B8")], (10.0, 14.2)),
    "L3": ([bx((10.2, 9.4, 14.4, 11.6), "SOFA"), bx((5.2, 15.6, 9.6, 18.8), "DINING 6"), bx((4.95, 9.4, 5.75, 12.4), "TV"),
            bx((13.9, 12.4, 14.65, 14.2), "P", "#FFF0B8"), bx((5.0, 22.2, 6.2, 24.2), "SHOE")], (10.0, 13.6)),
}


def first_nc(role="M", balcony=False, kit="K1", liv="L1", hinge="a", bedset=1):
    hb = {"a": "b", "b": "a"}[hinge]
    stair = Room("Staircase", "stair", [(SX0, YO1 + TW, SX1, YF2)], label="")
    ex = [("flight", SX0, SX1, YF1 - 11 * TREAD_IN / 12, YF1, 11, "DN"), ("flight", SX0, SX1, YL, YF2, 17, "UP")]
    fk, fn = ("bed", "Bedroom 2") if role == "M" else ("master", "Master Bedroom")
    rk, rn = ("master", "Master Bedroom") if role == "M" else ("bed", "Bedroom 2")
    wins, rooms = [], [stair]
    doors = [door("V", (SX1 + PX0) / 2, 19.1, 3.0, 1, hinge)]
    if balcony:
        r1, r2 = (X0, Y0, 8.125, YO1), (8.125, 4.375, X1, YO1)
        front = Room(fn, fk, [r1, r2], label=fn + "\n(with balcony)\n87 sq ft", lp=(10.4, 6.5))
        front.nodim = True
        bal = Room("Balcony", "balcony", [(8.5, Y0, X1, 4.0)], label="BALCONY\n6'-2\" x 3'-3\"", lp=(11.6, 2.4))
        bal.nodim = True
        rooms += [front, bal]
        doors += [door("H", 4.1875, 10.2, 3.0, 1, kind="fdoor")]
        wins += [win("H", EW / 2, 1.3, 5.2), win("H", EW / 2, 9.2, 4.6, 3.5)]
        furn = [bx((2.3, 1.6, 7.3, 8.1), "BED"), bx((13.3, 5.0, 14.5, 8.4), "W")]
    else:
        front = Room(fn, fk, [(X0, Y0, X1, YO1)], label=fn, lp=(5.9, 4.6))
        rooms += [front]
        wins += [win("H", EW / 2, 2.0, 6.0), win("H", EW / 2, 10.0, 3.0)]
        if bedset == 1:
            furn = [bx((9.4, 1.4, 14.4, 7.9), "BED"), bx((0.95, 3.0, 2.75, 7.6), "WARD")]
        else:
            furn = [bx((2.1, 1.4, 7.1, 7.9), "BED"), bx((12.6, 2.6, 14.45, 7.4), "WARD")]
            front.lp = (10.6, 4.6)
    doors += [door("H", (YO1 + YO1 + TW) / 2, 5.5, 2.75, -1, hinge)]
    lf, llp = LIV_NC[liv]
    hall = Room("Living + Dining", "hall2", [(PX0, YO1 + TW, X1, YH1 + 0.0)],
                label="LIVING + DINING\n10'-0\" x 15'-4\"\n154 sq ft", lp=llp)
    hall.nodim = True
    cw = Room("Common Washroom", "guest", [WC2], label="COMMON\nWASHROOM", lp=(11.7, 26.9))
    ps = Room("Passage", "passage", [PS], label="PASSAGE", lp=(6.4, 40.0))
    duct = Room("Duct", "duct", [DUCT2], label="DUCT", lp=(11.65, 31.15))
    kt = Room("Kitchen", "kitchen", [KIT2], label="KITCHEN", lp=KITCHENS[kit][1])
    master = Room(rn, rk, [(X0, 41.55, 10.275, Y1), (X0, YF2 + TW, SX1, 41.55)],
                  label=rn.upper() + "\n9'-6\" x 10'-4\" + nook\n115 sq ft", lp=(6.3, 50.6))
    master.nodim = True
    t1 = Room("Attached Toilet", "toilet", [T1R], label="Attached\nToilet")
    cl = Room("Closet", "store", [T1CL], label="CLOSET")
    rooms += [hall, cw, duct, ps, kt, master, t1, cl]
    doors += [door("H", 24.6125, 4.9, 3.0, 1, kind="arch"), door("V", 8.4625, 25.5, 2.5, 1, hinge),
              door("V", 8.4625, 34.0, 2.75, 1, hb), door("H", 41.3625, 5.4, 2.75, 1, hb),
              door("V", 10.4625, 47.2, 2.5, 1, hinge), door("V", 10.4625, 42.3, 2.4, 1, hb)]
    wins += [win("H", 29.3125, 10.0, 2.0, 1.5), win("H", 32.9875, 10.0, 3.0, 3.0),
             win("H", DFP - EW / 2, 3.0, 6.0), win("H", DFP - EW / 2, 11.5, 2.5, 1.5)]
    ex += furn + lf + KITCHENS[kit][0]
    ex += [bx((0.95, 37.5, 3.1, 41.3), "WARD")]
    if bedset == 1:
        ex += [bx((3.6, 44.4, 10.0, 49.2), "BED"), bx((0.95, 43.0, 2.9, 48.0), "WARD")]
    else:
        ex += [bx((1.1, 44.4, 7.5, 49.2), "BED"), bx((8.0, 43.4, 10.0, 48.6), "WARD")]
    ex += [bx((8.95, 25.1, 10.4, 27.0), "WC"), bx((12.9, 27.8, 14.4, 28.9), "WB"), bx((12.0, 25.1, 14.4, 26.9), "SHR", "#E3F1F8"),
           bx((10.8, 46.2, 12.1, 48.0), "WC"), bx((13.2, 49.6, 14.4, 50.8), "WB"),
           bx((10.9, 42.0, 11.5, 45.2), "", "#E8DCC4"), ("box", SK1, "none", "#2a8ab8", ""), ("box", SK2, "none", "#2a8ab8", "")]
    fl = Floor("F", "FIRST FLOOR (RESIDENTIAL, 2 BEDROOMS)", rooms, doors, wins, ex)
    fl.sky = {"Living + Dining": 0.5 * (SK1[2] - SK1[0]) * (SK1[3] - SK1[1])}
    return fl


def ground_nc(kind, shut="S1", fix="F1"):
    fl = V3.ground_v3(kind, shut, fix)
    # replace duct slot by a locker, add the service shaft inside the shop
    for r in fl.rooms:
        if r.name == "Duct":
            r.name, r.kind, r.label = "Locker", "store", "LOCKER"
        if r.name == "Shop":
            A, B = r.rects[0], r.rects[1]
            r.rects = [A, (X0, YF1 + TW, X1, 29.125), (X0, 29.125, 8.275, 33.175), (X0, 33.175, X1, 41.175)]
            r.lp = (9.0, 24.0)
    fl.rooms.append(Room("Duct", "duct", [DUCT2], label="SERVICE SHAFT", lp=(11.65, 31.15)))
    fl.doors = [d for d in fl.doors] + [door("V", 8.4625, 30.0, 2.0, 1, kind="service")]
    fl.wins = [w for w in fl.wins if not (w["o"] == "H" and abs(w["c"] - 45.6625) < 0.01)]
    fl.extra = [e for e in fl.extra if not (e[0] == "box" and rect_overlap(e[1], (8.2, 29.0, X1, 33.4)))]
    return fl


def terrace_nc(var):
    tr = Room("Open Terrace", "terrace", [(TW, TW, W - TW, DFP - TW)], label="", lp=None)
    mum = Room("Mumty", "mumty", [MUM], label="MUMTY", lp=(2.5, 33.0))
    duct = Room("Duct", "court", [DUCT2], label="DUCT\n(open)", lp=(11.65, 31.15))
    ex = [("wall", MUM), ("wall", DUCT2), ("wall", SK1), ("wall", SK2),
          ("box", SK1, "#CFE9F5", "#2a8ab8", "SKYLIGHT\nhall\n7'-0\" x 9'-6\""), ("box", SK2, "#CFE9F5", "#2a8ab8", "SKYLIGHT\npassage"),
          ("text", 10.0, 24.0, "OPEN TERRACE", 9)]
    used = [MUM, DUCT2, SK1, SK2, (4.5, 10.5, 14.7, 21.0)]
    tk = L._pick("tank", "N", True, used)
    used.append(tk[1])
    ex.append(("box", tk[1], "#B9D7F0", "#2a6a9a", "OVERHEAD TANK 1000 L"))
    sol = L._pick("solar", "N", True, used)
    if sol:
        used.append(sol[1])
        ex.append(("box", sol[1], "#F4D77A", "#8a6d00", "SOLAR PV ZONE"))
    if var == 2:
        g = L._pick("garden", "N", True, used)
        if g:
            ex.append(("box", g[1], "#CFE6B8", "#4a7a2a", "GARDEN / TULSI\nSEATING"))
    elif var == 3:
        ex.append(bx((5.6, 1.6, 14.3, 7.4), "PERGOLA + SEATING 8'-9\" x 5'-9\"", "#E7F0D8"))
    elif var == 4:
        ex.append(("wall", (0.9, 3.0, 5.4, 9.2)))
        ex.append(bx((0.9, 3.0, 5.4, 9.2), "TERRACE\nSTORE + WASH\n4'-6\" x 6'-2\"", "#E8DCC4"))
    else:
        ex.append(("box", (0.9, 22.0, 4.3, 25.0), "#F2EBDD", "#8a8a8a", "CLOTHES\nDRYING"))
    for (x, y) in ((1.2, 1.2), (14.2, 1.2), (1.2, 51.4), (14.2, 51.4)):
        ex.append(("box", (x - 0.25, y - 0.25, x + 0.25, y + 0.25), "#FFFFFF", "#333", ""))
    doors = [dict(door("V", (SX1 + TW / 2), 36.6, 3.0, 1), gap=(SX1, PX0))]
    fl = Floor("T", "TERRACE (SECOND FLOOR LEVEL)", [tr, duct, mum], doors, [], ex)
    fl.zones, fl.tank = {"tank": tk[2]}, tk
    return fl


def build_nc(spec):
    g = ground_nc(spec["g"], spec["shut"], spec["fix"])
    f = first_nc(spec["role"], spec["bal"], spec["kit"], spec["liv"], spec["hinge"], spec["bedset"])
    t = terrace_nc(spec["t"])
    return dict(floors=[g, f, t], g=(spec["g"], False), f=("NC", False), t=spec["t"], spec=spec, nc=True,
                duct_txt="Size 6'-0\" x 3'-4\" = 19.8 sq ft (1.84 sq m), open to sky at the terrace")
