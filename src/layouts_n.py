"""North-facing set: road on the 15.4 ft north side, 2 bedrooms on the first floor,
a services duct (open to sky) between kitchen and toilet running ground to terrace."""
from layouts import *
import layouts as L

DUCT = (10.65, 41.55, X1, 45.475)          # 4'-0" x 3'-11"
T1R = (10.65, 45.85, X1, Y1)               # toilet below duct, 4'-0" x 6'-0"
KIT = (8.65, 33.175, X1, 41.175)
NFACE, NMIR = "N", True


def ground_n(kind):
    st, ex = L._stairG()
    A = (PX0, Y0, X1, YF1 + TW)
    doors = [L.SHUTTER, L.STAIR_DOOR]
    wins = [win("H", DFP - EW / 2, 11.5, 2.5, 1.5), win("H", 45.6625, 11.3, 2.0, 1.5)]
    duct = Room("Duct", "duct", [DUCT], label="DUCT")
    wc = Room("Toilet", "toilet", [T1R])
    rooms = [st]
    if kind == "GA":                       # open shop, store + staff toilet through store
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, 41.175)], label="SHOP / SHOWROOM", lp=(9.5, 30))
        store = Room("Store", "store", [(X0, 41.55, 10.275, Y1)], label="Store / Pantry")
        rooms += [shop, store, duct, wc]
        doors += [door("H", 41.3625, 2.5, 3.5, 1), door("V", 10.4625, 47.2, 2.5, 1),
                  door("V", 10.4625, 42.3, 2.0, 1, kind="service"), door("H", DFP - EW / 2, 2.0, 3.0, -1)]
        wins += [win("H", DFP - EW / 2, 5.5, 3.0, 3.0)]
    elif kind == "GB":                     # open shop, owner cabin with attached toilet
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, 41.175)], label="SHOP / SHOWROOM", lp=(9.5, 30))
        cab = Room("Cabin", "cabin", [(X0, 41.55, 10.275, Y1)], label="Cabin / Office")
        rooms += [shop, cab, duct, wc]
        doors += [door("H", 41.3625, 2.5, 3.0, 1), door("V", 10.4625, 47.2, 2.5, 1),
                  door("V", 10.4625, 42.3, 2.0, 1, kind="service")]
        wins += [win("H", DFP - EW / 2, 2.5, 5.0, 4.0)]
    elif kind == "GC":                     # shop with two stores, rear service door
        shop = Room("Shop", "shop", [A, (X0, YF1 + TW, X1, 41.175)], label="SHOP / SHOWROOM", lp=(9.5, 30))
        s1 = Room("Store", "store", [(X0, 41.55, 5.4, Y1)], label="Store")
        s2 = Room("Pantry", "store", [(5.775, 41.55, 10.275, Y1)], label="Pantry")
        rooms += [shop, s1, s2, duct, wc]
        doors += [door("H", 41.3625, 1.7, 3.0, 1), door("H", 41.3625, 6.3, 3.0, 1), door("V", 10.4625, 47.2, 2.5, 1),
                  door("V", 10.4625, 42.3, 2.0, 1, kind="service"), door("H", DFP - EW / 2, 1.9, 3.0, -1)]
        wins += [win("H", DFP - EW / 2, 6.7, 2.5, 3.0)]
    return Floor("G", "GROUND FLOOR (COMMERCIAL)", rooms, doors, wins, ex)


def first_n(typ, pooja):
    stair = Room("Staircase", "stair", [(SX0, YO1 + TW, SX1, YF2)], label="")
    ex = [("flight", SX0, SX1, YF1 - 11 * TREAD_IN / 12, YF1, 11, "DN"), ("flight", SX0, SX1, YL, YF2, 17, "UP")]
    doors = [door("V", (SX1 + PX0) / 2, 19.1, 3.0, 1)]
    wins = []
    rooms = [stair]
    f = True
    fk, fn, tn = ("bed", "Bedroom 2", "Toilet 2") if typ == "A" else ("master", "Master Bedroom", "Master Toilet")
    rk, rn, rt = ("master", "Master Bedroom", "Master Toilet") if typ == "A" else ("bed", "Bedroom 2", "Toilet 2")
    B2 = (PX0, YO1, X1, 12.9)
    front = Room(fn, fk, [L._fr((X0, Y0, 10.275, YO1), f), L._fr((10.275, 7.125, X1, YO1), f), B2], label=fn, lp=(7.7, 5.0))
    t2 = Room(tn, "toilet", [L._fr((10.65, Y0, X1, 6.75), f)])
    doors += [L._fd(door("H", 6.9375, 11.0, 2.5, -1), f), door("H", 13.0875, 5.5, 2.75, -1)]
    wins += [L._fw(win("H", EW / 2, 1.5, 6.0), f), L._fw(win("H", EW / 2, 11.5, 2.5, 1.5), f)]
    rooms += [front, t2]
    if pooja:
        hall = Room("Hall", "hall", [(PX0, 16.15, X1, YH1), (PX0, YH0, 11.275, 16.15)], label="LIVING + DINING", lp=(9.0, 20.5))
        pj = Room("Pooja", "pooja", [(11.65, YH0, X1, 15.775)], label="Pooja")
        rooms += [pj]
        doors += [door("V", 11.4625, 13.35, 2.4, 1, kind="arch")]
    else:
        hall = Room("Hall", "hall", [(PX0, YH0, X1, YH1)], label="LIVING + DINING", lp=(9.6, 18.5))
    court = Room("Court", "court", [CT], label="COURT\n(open to sky)", lp=(11.65, 28.8))
    ps = Room("Passage", "passage", [PS], label="PASSAGE", lp=(6.4, 30))
    kit = Room("Kitchen", "kitchen", [KIT], label="KITCHEN")
    duct = Room("Duct", "duct", [DUCT], label="DUCT")
    rear = Room(rn, rk, [(X0, 41.55, 10.275, Y1), (X0, YF2 + TW, SX1, 41.55)], label=rn, lp=(6.0, 47.5))
    t1 = Room(rt, "toilet", [T1R])
    rooms += [hall, court, ps, kit, duct, rear, t1]
    doors += [door("H", 24.6125, 10.0, 3.5, -1, kind="fdoor"), door("H", 24.6125, 4.9, 3.0, 1, kind="arch"),
              door("V", 8.4625, 34.0, 2.75, 1), door("H", 41.3625, 5.4, 2.75, 1), door("V", 10.4625, 47.2, 2.5, 1)]
    wins += [win("H", 32.9875, 10.0, 3.0), win("V", 8.4625, 26.0, 3.0), win("H", 41.3625, 11.0, 3.0, 3.0),
             win("H", 45.6625, 11.3, 2.0, 1.5), win("H", DFP - EW / 2, 3.0, 6.0), win("H", DFP - EW / 2, 11.5, 2.5, 1.5)]
    return Floor("F", "FIRST FLOOR (RESIDENTIAL, 2 BEDROOMS)", rooms, doors, wins, ex)


def terrace_n(var):
    t = L.terrace(var, NFACE, NMIR)
    # replace the duct as another void with parapet ring; keep tank off it
    t.rooms.insert(2, Room("Duct", "court", [DUCT], label="DUCT\n(open)", lp=(12.65, 43.5)))
    t.extra.insert(0, ("wall", DUCT))
    return t


def build_n(g, f, t):
    fl = [ground_n(g), first_n(*f), terrace_n(t)]
    return dict(floors=fl, g=(g, False), f=f, t=t)
