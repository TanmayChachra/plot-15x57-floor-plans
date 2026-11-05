import os, sys, math
from layouts import *
from PIL import Image

NAMES = {"G1": "Open showroom, store and toilet at rear", "G1C": "Open showroom, central toilet, two stores",
         "G2": "L-shaped shop with cabin, store and toilet", "G3": "Showroom plus godown with rear service door"}
FNAMES = {"A": "2 BHK: front bedroom with toilet, living-dining on light court, kitchen, master bedroom with toilet",
          "B": "1 BHK + dining: front living-dining, dining/foyer with WC on light court, kitchen, master bedroom with toilet"}
FACE = {"E": "East", "N": "North", "W": "West", "S": "South"}
S_IN = 0.21
MUM_AREA = (MUM[2] - MUM[0]) * (MUM[3] - MUM[1])


def carpet(fl, skip=("stair", "court", "terrace", "mumty")):
    return sum(r.area() for r in fl.rooms if r.kind not in skip)


def render(plan, facing, mirror, path, idx, vs, errs):
    fls = plan["floors"]
    ew, ns = (D, W) if facing in "EW" else (W, D)
    gap = 12.0
    pw = 36.0
    if facing in "EW":
        tw, th = ew + 16 + pw, 12 + 3 * (ns + gap) + 4
        offs = [(8, 12 + (2 - i) * (ns + gap)) for i in range(3)]
        px = 8 + ew + 8
    else:
        tw, th = 8 + 3 * ew + 2 * gap + 8 + pw, ns + 26
        offs = [(8 + i * (ew + gap), 10) for i in range(3)]
        px = 8 + 3 * ew + 2 * gap + 6
    fig = plt.figure(figsize=(tw * S_IN, th * S_IN), dpi=125)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, tw)
    ax.set_ylim(0, th)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(8, th - 3.2, f"PLAN {idx:02d}  |  {FACE[facing].upper()}-FACING  |  PLOT 15.4 ft x 57.6 ft (15'-4.8\" x 57'-7.2\")  |  GROUND COMMERCIAL, FIRST FLOOR RESIDENTIAL, TERRACE ON SECOND FLOOR",
            fontsize=13, fontweight="bold", va="center")
    ax.text(8, th - 6.4, f"Ground: {NAMES[plan['g'][0]]}.  First: {FNAMES[plan['f'][0]]}.  North is up. Room sizes are clear internal sizes.",
            fontsize=9, va="center", color="#333")
    for fl, (ox, oy) in zip(fls, offs):
        T, _, _ = draw_floor(ax, fl, plan, facing, mirror, ox, oy, fs=8.3)
        quad = [T(-1.5, -5.2), T(W + 1.5, -5.2), T(W + 1.5, -0.2), T(-1.5, -0.2)]
        ax.add_patch(Polygon(quad, closed=True, fc="#BDBDBD", ec="none", zorder=0.5))
        rc = T(W / 2, -2.7)
        ax.text(rc[0], rc[1], f"ROAD ({FACE[facing][0]})", ha="center", va="center", fontsize=9, color="#222",
                rotation=0 if facing in "NS" else 90)
        xs = [T(0, 0)[0], T(W, D)[0]]
        ys = [T(0, 0)[1], T(W, D)[1]]
        bx, ex_, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        ax.text(bx, by1 + (6.2 if facing == "N" else 1.0), fl.title, fontsize=11, fontweight="bold", va="bottom")
        north_arrow(ax, ex_ - 2, by1 + (6.0 if facing == "N" else 1.0) , 2.6)
        if facing in "EW":
            ax.text((bx + ex_) / 2, by0 - 1.6, "57'-7.2\" plot depth = building 52'-7.2\" + rear yard 5'-0\"", ha="center", fontsize=8)
            ax.text(bx - (6.5 if facing == "W" else 0.8), (by0 + by1) / 2, "15'-4.8\"", rotation=90, ha="right", va="center", fontsize=8)
        else:
            ax.text((bx + ex_) / 2, by0 - (6.5 if facing == "S" else 1.2), "15'-4.8\" plot width", ha="center", fontsize=8, va="top")
            ax.text(bx - 0.8, (by0 + by1) / 2, "57'-7.2\" (building 52'-7.2\" + rear yard 5'-0\")", rotation=90, ha="right", va="center", fontsize=8)
    g, f = fls[0], fls[1]
    lines = []

    def add(t="", b=False, sz=8.5):
        lines.append((t, b, sz))
    st = stair_info()
    add("AREA STATEMENT", True, 10)
    add("Plot 15.4 x 57.6 ft = 887.0 sq ft (82.4 sq m, 98.6 sq yd)")
    add("Footprint 15.4 x 52.6 ft = 810.0 sq ft per floor (91.3%)")
    add(f"Commercial carpet (ground, excl. stair): {carpet(g):.0f} sq ft")
    add(f"Residential carpet (first, excl. stair, court): {carpet(f):.0f} sq ft")
    add(f"Open terrace (excl. mumty, court void): {(DFP - 0.75) * (W - 0.75) - MUM_AREA - 48:.0f} sq ft")
    add()
    add("STAIR (starts at the front with its own street door)", True, 10)
    add(f"Straight flights on the left party wall, clear width {st['width_ft']:.1f} ft")
    add(f"{st['risers']} risers x {st['riser_in']:.0f} in, tread {st['tread_in']:.0f} in, pitch {st['pitch_deg']:.0f} deg")
    add(f"Floor to floor {st['floor_to_floor_ft']:.1f} ft, headroom {st['headroom_ft']} ft (2.2 m) minimum")
    add("Riser 178 mm (limit 190), tread 254 mm (limit 250)")
    add()
    add("VASTU READING (plot thirds, room centroid)", True, 10)
    for fc, nm, z, lv in vs["det"]:
        mark = {"ideal": "+", "acceptable": "~", "compromise": "-", "AVOID": "X"}[lv]
        add(f"[{mark}] {fc}  {nm}: {z} ({lv})")
    add(f"Score {vs['pts']}/{vs['mx']}    + ideal   ~ acceptable   - compromise   X avoid")
    add("Brahmasthan (centre) kept open to sky as a court.")
    add()
    add("CODE AND GEOMETRY CHECKS (run by script)", True, 10)
    add("0 errors" if not errs else f"{len(errs)} errors")
    add("No overlaps, walls >= 4.5 in, every room reached by a door,")
    add("master/living >= 7.9 ft wide, 2nd bed 7.0 ft, kitchen >= 48 sq ft,")
    add("toilets >= 24 sq ft and 4 ft wide, openings >= 1/6 (bed, living),")
    add("1/8 (hall, kitchen, cabin), 1/10 (toilets, shop) of floor area.")
    add()
    add("ASSUMPTIONS (confirm with local bylaws and an architect)", True, 10)
    for t in ["Road at front, party walls both sides, 5 ft rear yard.",
              "9 in outer walls, 4.5 in partitions, 5 in RCC slabs.",
              "Floor level 6 in above road: one step at shutter and stair door.",
              "Terrace: slope 1:100 to outlets (small squares), parapet 3 ft 6 in.",
              "A higher plinth needs a front setback for steps or a ramp.",
              "First floor wet areas on sunk waterproofed slab.",
              "Structural frame by a structural engineer.",
              "No parking built. Shop shutter 9'-0\" wide."]:
        add(t)
    y = th - 10
    for t, b, sz in lines:
        ax.text(px, y, t, fontsize=sz, fontweight="bold" if b else "normal", va="top")
        y -= 0.25 + sz * 0.098
    fig.savefig(path + ".png", dpi=125)
    plt.close(fig)
    im = Image.open(path + ".png").convert("RGB")
    im.save(path + ".webp", quality=80, method=6)
    os.remove(path + ".png")


if __name__ == "__main__":
    fa, mir = sys.argv[1], sys.argv[2] == "1"
    g = (sys.argv[3], sys.argv[4] == "1")
    f = (sys.argv[5], sys.argv[6], sys.argv[7] == "1")
    p = build(g, f, fa, mir, 1)
    bad, pts, mx, det = vastu(p, fa, mir)
    errs = geo_checks(p)
    print("errs", errs, "bad", bad, pts, mx)
    render(p, fa, mir, sys.argv[8], 1, dict(det=det, pts=pts, mx=mx), errs)
