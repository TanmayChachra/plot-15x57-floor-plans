from layouts_n4 import *

def specs():
    out = []
    for i in range(8):
        role = "F" if i % 3 == 1 else "M"
        out.append(dict(g=["GA", "GB", "GC", "GE"][i % 4], shut=["S1", "S2", "S3"][i % 3], fix=["F1", "F2", "F3"][(i + i // 3) % 3],
                        role=role, bal=(role == "M" and i % 2 == 0), kit=["K1", "K2", "K3"][(i + 1) % 3], liv=["L1", "L2", "L3"][(i * 2 + i // 3) % 3],
                        hinge="a" if i % 2 == 0 else "b", bedset=1 + (i // 2) % 2, t=(i % 4) + 1, court="C1"))
    return out

def desc(s):
    g = {"GA": "store/pantry and staff toilet", "GB": "owner cabin with attached toilet", "GC": "store, pantry and staff toilet with rear door",
         "GE": "store with loft and staff toilet"}[s["g"]]
    sh = {"S1": "one 9'-0\" shutter", "S2": "two 4'-3\" shutters", "S3": "one 7'-6\" shutter"}[s["shut"]]
    kit = {"K1": "straight", "K2": "L-shaped", "K3": "parallel"}[s["kit"]]
    if s["role"] == "M":
        rooms = "Bedroom 2 at front" + (" with balcony" if s["bal"] else "") + ", Master at rear with attached toilet"
    else:
        rooms = "Master at front (uses the common washroom), Bedroom 2 at rear with attached toilet"
    t = {1: "tank, solar, drying", 2: "tank, solar, garden", 3: "pergola seating, tank, solar", 4: "store + wash room, tank, solar"}[s["t"]]
    return f"NO COURT, skylit hall.  Ground: shop ({sh}), {g}.  First: {rooms}; {kit} kitchen; common washroom off the hall.  Terrace: {t}.  North is up."

if __name__ == "__main__":
    for i, s in enumerate(specs(), 1):
        p = build_nc(s)
        e = geo_checks(p)
        bad, pts, mx, det = vastu(p, "N", True)
        print(i, "ERR" if e else "ok", e[:4], bad, pts, mx)
