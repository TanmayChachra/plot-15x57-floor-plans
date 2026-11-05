import json
m = json.load(open('docs/plans.json'))
cards = ''
for x in m:
    cards += f'''<a class="card" data-f="{x['facing']}" href="{x['file']}"><img loading="lazy" src="{x['thumb']}" alt="Plan {x['n']:02d} {x['facing']}-facing floor plans"><div class="b"><b>Plan {x['n']:02d}</b> <span class="t {x['facing']}">{x['facing']}-facing</span><br>{x['bhk']} | shop {x['commercial']} sq ft | home {x['residential']} sq ft<br><small>Ground: {x['ground']}<br>Terrace: {x['terrace']}<br>Vastu score {x['score']}</small></div></a>
'''
html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>20 floor plans, plot 15.4 x 57.6 ft, shop + residence + terrace</title>
<style>
body{font:15px/1.5 system-ui,sans-serif;margin:0;background:#f6f4ef;color:#222}
header{padding:24px 20px;background:#2b2b2b;color:#fff}h1{margin:0 0 6px;font-size:22px}header p{margin:0;opacity:.85;max-width:900px}
nav{padding:14px 20px;display:flex;gap:8px;flex-wrap:wrap}button{border:1px solid #888;background:#fff;padding:6px 14px;border-radius:18px;cursor:pointer;font:inherit}button.on{background:#2b2b2b;color:#fff}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:16px;padding:0 20px 30px}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden;color:inherit;text-decoration:none}.card img{width:100%;display:block;border-bottom:1px solid #ddd}
.b{padding:10px 12px}.t{font-size:12px;padding:2px 8px;border-radius:10px;background:#e8e0cc}small{color:#555}
section{padding:0 20px 30px;max-width:900px}li{margin:4px 0}
</style></head><body>
<header><h1>20 floor plans: plot 15.4 ft x 57.6 ft (887 sq ft)</h1>
<p>Ground floor commercial, first floor residential, terrace at second floor level. Stair starts at the front with its own street door, full width shop front, no parking. Indian courtyard (Brahmasthan) and vastu reading on every plan. Click a card for the full sheet (all three floors, areas, stair data, vastu table, checks).</p></header>
<nav id="n"><button class="on" data-f="all">All 20</button><button data-f="East">East</button><button data-f="North">North</button><button data-f="South">South</button><button data-f="West">West</button></nav>
<main id="g">
''' + cards + '''</main>
<section><h2>Read this first</h2><ul>
<li>The road side was not given, so there are plans for all four facings. Pick the facing of your plot; tell me and I can make more for that facing.</li>
<li>East and North facing reach the best vastu scores. South and West facing have more compromises because the stair and shop entrance take the good corners on a 15 ft frontage.</li>
<li>Assumed: road in front, party walls on both sides, 5 ft rear yard, 9 in outer walls, 4.5 in partitions. Confirm setbacks, plinth and height with your local building bylaws and a licensed architect and structural engineer before building.</li>
<li>Every plan passed a script check: no overlaps, wall thickness, every room reached by a door, room sizes, window area, stair geometry. Source code is in the repository.</li>
</ul></section>
<script>
document.querySelectorAll('#n button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#n button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
document.querySelectorAll('#g .card').forEach(c=>c.style.display=(b.dataset.f=='all'||c.dataset.f==b.dataset.f)?'':'none')})
</script></body></html>'''
open('docs/index.html', 'w', encoding='utf-8').write(html)
open('docs/.nojekyll', 'w').write('')
