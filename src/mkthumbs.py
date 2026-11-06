import glob, os
from PIL import Image
for p in sorted(glob.glob("docs/designs/plan-*-first.webp") + glob.glob("docs/designs/plan-*-ground.webp")):
    im = Image.open(p)
    w = 520
    im.resize((w, int(w * im.height / im.width))).save(p.replace(".webp", "-thumb.webp"), quality=72, method=6)
print(len(glob.glob("docs/designs/*-thumb.webp")), "thumbs;", sum(os.path.getsize(f) for f in glob.glob("docs/designs/*")) // 1024, "KB total")
