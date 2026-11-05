import json, shutil, os
m = json.load(open('docs/plans_north.json'))
if os.path.exists('docs/index.html') and not os.path.exists('docs/other-facings.html'):
    shutil.copy('docs/index.html', 'docs/other-facings.html')
cards = ''
for x in m:
    cards += f'''<a class="card" href="{x['file']}"><img loading="lazy" src="{x['thumb']}" alt="Plan N-{x['n']:02d}"><div class="b"><b>Plan N-{x['n']:02d}</b> <span class="t">2 BHK, north-facing</span><br>Shop {x['commercial']} sq ft | home {x['residential']} sq ft | vastu {x['score']}<br><small>Ground: {x['ground']}<br>First: {x['first']}<br>Terrace: {x['terrace']}</small></div></a>
'''
html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>North-facing 2 bedroom plans, plot 15.4 x 57.6 ft, shop + home + terrace</title>
<style>
body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#f6f4ef;color:#222}
header{padding:24px 20px;background:#2b2b2b;color:#fff}h1{margin:0 0 6px;font-size:22px}header p{margin:0;opacity:.85;max-width:950px}a.l{color:#ffd37a}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:16px;padding:20px}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden;color:inherit;text-decoration:none}.card img{width:100%;display:block;border-bottom:1px solid #ddd}
.b{padding:10px 12px}.t{font-size:12px;padding:2px 8px;border-radius:10px;background:#e8e0cc}small{color:#555}
section{padding:0 20px 30px;max-width:950px}li{margin:4px 0}
</style></head><body>
<header><h1>12 north-facing plans: plot 15.4 ft x 57.6 ft, road on the 15.4 ft north side</h1>
<p>Ground floor shop, first floor 2 bedroom home, terrace on the second floor. Stair starts at the front with its own door. A services duct (open to sky) sits between the kitchen and the toilet and runs ground to terrace for pipes and electrical risers. Every room carries its clear size in feet-inches, with dimension chains and door and window schedules on each sheet. Click a card for the full sheet. <a class="l" href="other-facings.html">First set (East, North, South, West, before the 2 bedroom and duct update)</a></p></header>
<main>
''' + cards + '''</main>
<section><h2>Read this first</h2><ul>
<li>Plans differ in the shop rear (store and pantry, owner cabin, two stores), which bedroom is at the front, and a pooja niche. Terrace alternates between two versions.</li>
<li>Living and dining is a compact 100 to 112 sq ft hall on a 15 ft frontage. Both bedrooms are 115 to 125 sq ft with attached toilets.</li>
<li>Vastu: no room is in a forbidden zone. The kitchen sits in the east third, a compromise, because the duct, kitchen and toilet stack had to stay together. Scores are on each sheet.</li>
<li>Assumed: road in front, party walls on both sides, 5 ft rear yard. Confirm setbacks, plinth, court and duct sizes with local bylaws, an architect and a structural engineer.</li>
<li>Every plan passed a script check (no overlaps, wall thickness, doors to every room, room sizes, window area, stair geometry).</li>
</ul></section></body></html>'''
open('docs/index.html', 'w', encoding='utf-8').write(html)
