"""Generates the Heritage (mono) pages in this folder and the Agency pages in ./agency.
Run: python3 build.py     (artifact mode: python3 build.py --flat OUTDIR BRAND)"""
import sys, os, re

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

def gauge():
    return '''<div class="gauge" aria-live="polite">
  <div class="row mono"><span>Threshold</span><span><b data-bind="reserved"></b> of <span data-bind="threshold"></span> units reserved</span></div>
  <div class="bar-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-label="Progress toward production threshold"><span></span></div>
  <div class="count" data-countdown aria-label="Time remaining"><div><b>--</b><span>Days</span></div><div><b>--</b><span>Hrs</span></div><div><b>--</b><span>Min</span></div><div><b>--</b><span>Sec</span></div></div>
  <p class="foot mono">Closes <span data-bind="ends"></span></p>
  <p class="foot mono" data-closed hidden>Campaign closed.</p>
</div>'''

TERMS = '''<dl class="terms">
  <div><dt>Threshold</dt><dd><span data-bind="threshold"></span> units. Production starts only if met.</dd></div>
  <div><dt>Deadline</dt><dd><span data-bind="ends"></span>. Fixed. Not extended.</dd></div>
  <div><dt>Payment</dt><dd>Charged at order.</dd></div>
  <div><dt>Refund</dt><dd>Full refund to everyone if the threshold is not met by the deadline.</dd></div>
  <div><dt>Shipping</dt><dd data-bind="ship"></dd></div>
</dl>'''

def build(page, brand, pre, switch=None, flat=False):
    agency = brand == "agency"
    logo_head = pre + "images/" + ("logo-agency" if agency else "logo-black") + ".webp"
    logo_foot = pre + "images/logo-white.webp"
    titles = {"index": "Don & Doff Co. — Spacewear", "product": "The Pressure-Line — Pre-order · Don & Doff Co.", "about": "The Name — Don & Doff Co."}
    desc = {"index": "Spacewear built around donning and doffing. Suit up. Reach orbit. Repeat.", "product": "Threshold pre-order. 50 units to start production. Full refund if the threshold is not met.", "about": "Donning and doffing: the two bookends of every mission."}
    nav = lambda n: ' aria-current="page"' if n == page else ""
    head = f'''<!doctype html>
<html lang="en" data-brand="{brand}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titles[page]}</title>
<meta name="description" content="{desc[page]}">
<meta name="theme-color" content="{'#0b3d91' if agency else '#0a0a0a'}">
<link rel="icon" href="{pre}favicon.png" type="image/png">
{FONTS}
<link rel="stylesheet" href="{pre}styles.css">
</head>
<body>
'''
    header = f'''<header class="top">
<div class="strip mono">Threshold pre-order · <b data-bind="reserved">0</b> of <b data-bind="threshold">50</b> reserved · Closes <span data-bind="ends"></span></div>
<div class="bar"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Don &amp; Doff Co. home"><img src="{logo_head}" alt=""><span>Don &amp; Doff Co.</span></a>
  <nav aria-label="Primary"><a href="product.html"{nav('product')}>Flagship</a><a href="about.html"{nav('about')}>The name</a><a class="opt" data-bind="ig" data-keep href="https://instagram.com/donanddoffco" rel="noopener">Instagram</a></nav>
  <a class="btn sm" href="product.html">Reserve</a>
</div></div>
</header>
<main>
'''
    sw = ''
    if switch:
        sw = f'<span>Colourway: <a href="{switch[0]}">{switch[1]}</a></span>'
    footer = f'''</main>
<footer><div class="wrap">
  <div class="grid">
    <img src="{logo_foot}" alt="Don &amp; Doff Co. crest">
    <p class="motto">Ad astra<br>eleganter</p>
    <div class="links"><a href="product.html">Flagship pre-order</a><a href="about.html">The name</a><a data-bind="ig" href="https://instagram.com/donanddoffco" rel="noopener">@donanddoffco</a></div>
  </div>
  <div class="fine mono"><span>&copy; Don &amp; Doff Co.</span><span>Pre-orders are refunded in full if the threshold is not met.</span>{sw}</div>
</div></footer>
<script src="{pre}script.js"></script>
</body>
</html>
'''
    P = pre + "images/"
    if page == "index":
        body = f'''
<section class="hero"><div class="wrap grid">
  <div>
    <p class="mono eyebrow">Flagship 001 · Pre-order open</p>
    <h1><span>Suit up.</span><span>Reach orbit.</span><span>Repeat.</span></h1>
    <p class="lead">Spacewear built around the two bookends of every mission: putting the suit on, and taking it off.</p>
    <div class="cta"><a class="btn" href="product.html">Reserve · $99</a><a class="btn line" href="about.html">The name</a></div>
  </div>
  <figure class="stage"><img src="{P}pl-front.webp" alt="Black zip hoodie with white chevron panels across the chest and stripes down the sleeves"><span class="tag mono">001</span><figcaption class="mono"><span>The Pressure-Line</span><span>$99</span></figcaption></figure>
</div></section>

<div class="ticker" aria-hidden="true"><div class="track">
  {''.join('<span>Don</span><i>/</i><span>Reach orbit</span><i>/</i><span>Doff</span><i>/</i><span>Repeat</span><i>/</i>' for _ in range(6))}
</div></div>

<section><div class="wrap">
  <p class="mono mute">Why the name</p>
  <h2 style="margin-top:12px;max-width:14em">Two words. Every mission starts and ends with them.</h2>
  <div class="defs">
    <div><p class="mono ipa">verb · /dɒn/</p><h3>Don</h3><p>To put on the suit. The first act of every mission.</p></div>
    <div><p class="mono ipa">verb · /dɒf/</p><h3>Doff</h3><p>To take it off. The last.</p></div>
  </div>
  <p class="src mono">NASA technical vocabulary since Gemini. Safety-critical today.</p>
</div></section>

<section class="on-band"><div class="wrap campaign">
  <div>
    <p class="mono">Flagship 001 · Threshold pre-order</p>
    <h2>The Pressure-Line</h2>
    <p>Made only if 50 are ordered. Charged at order. Refunded in full to everyone if the threshold is not met by the deadline.</p>
    <a class="btn" href="product.html">Reserve · $99</a>
  </div>
  <div>{gauge()}{TERMS}</div>
</div></section>

<section><div class="wrap">
  <div class="head-row"><h2>In the field</h2><a class="btn line sm" data-bind="ig" data-keep href="https://instagram.com/donanddoffco" rel="noopener">Follow @donanddoffco</a></div>
  <div class="look">
    <figure class="a"><img src="{P}pl-model.webp" alt="Model in the black and white zip hoodie with black joggers" loading="lazy"><figcaption class="mono">Worn</figcaption></figure>
    <figure class="b"><img src="{P}trio.webp" alt="Three spacesuit-inspired hoodies with visors against a moon surface" loading="lazy" style="object-position:50% 30%"><figcaption class="mono">Concept · Kit</figcaption></figure>
    <figure class="c"><img src="{P}suit.webp" alt="Black and white pressure suit before a rocket and moon" loading="lazy"><figcaption class="mono">Concept · Suit</figcaption></figure>
    <figure class="d"><img src="{P}hoodie-visor.jpg" alt="Hooded jacket with a visor and panelled seam lines" loading="lazy"><figcaption class="mono">Concept · Visor</figcaption></figure>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <p class="mono mute">Procedure</p>
  <div class="steps">
    <div><p class="mono">Mid-1960s</p><h3>Gemini</h3><p>The terms enter NASA's technical vocabulary.</p></div>
    <div><p class="mono">1960s–70s</p><h3>Apollo</h3><p>Drilled into procedure. Steps, checks, a crew to confirm.</p></div>
    <div><p class="mono">Now</p><h3>NASA standard</h3><p>Donning and doffing is still treated as a safety-critical task.</p></div>
  </div>
  <p style="margin-top:36px"><a class="btn line" href="about.html">Read the full entry</a></p>
</div></section>
'''
    elif page == "product":
        imgs = [("pl-front.webp","Front of the black zip hoodie with white chevron panels"),("pl-back.webp","Back with a white chevron across the shoulders"),("pl-model.webp","Worn with black joggers"),("trio.webp","Concept: three visor hoodies"),("hoodie-visor.jpg","Concept: hooded jacket with visor")]
        th = ''.join(f'<button type="button" data-src="{P}{a}" data-alt="{b}" aria-pressed="{"true" if i==0 else "false"}" aria-label="View image {i+1}"><img src="{P}{a}" alt=""></button>' for i,(a,b) in enumerate(imgs))
        sizes = ''.join(f'<span><input type="radio" name="size" id="s-{s}" value="{s}"><label for="s-{s}">{s}</label></span>' for s in ["S","M","L","XL","2XL"])
        body = f'''
<section style="padding-top:clamp(28px,4vw,56px)"><div class="wrap pdp">
  <div class="gallery">
    <div class="main"><img id="main-img" src="{P}{imgs[0][0]}" alt="{imgs[0][1]}"></div>
    <div class="thumbs">{th}</div>
    <p class="note">Product renders and concept imagery. Final print placement and colourway are confirmed with the printer before production.</p>
  </div>
  <div>
    <p class="mono mute">Flagship 001 · Threshold pre-order</p>
    <h1 style="font-size:clamp(2.3rem,5.6vw,4rem);margin-top:12px">The Pressure-Line</h1>
    <p class="price">$99</p>
    <p>White panels cross the chest and run down the sleeves, as seams do on a pressure suit. It remembers the suit without pretending to be one.</p>
    {gauge()}
    <form id="reserve" novalidate>
      <p class="mono">Size</p>
      <div class="sizes" role="radiogroup" aria-label="Size">{sizes}</div>
      <button class="btn" type="submit" style="width:100%;justify-content:center">Reserve · $99</button>
      <p class="status" role="status"></p>
    </form>
    <p class="mono" style="margin-top:34px">Campaign terms</p>
    {TERMS}
    <ul class="spec">
      <li>White chevron panels across chest and back, stripes down the sleeves</li>
      <li>Premium blank, printed (DTG / DTF)</li>
      <li>Produced in Toronto</li>
      <li>One production run. No restock promised.</li>
    </ul>
  </div>
</div></section>
'''
    else:
        body = f'''
<section style="padding-bottom:clamp(32px,5vw,56px)"><div class="wrap">
  <p class="mono mute">Why the name</p>
  <h1 style="margin-top:14px">Don &amp;<br>Doff</h1>
  <p style="margin-top:28px;font-size:1.3rem;color:var(--mute)">Every mission has two bookends. Putting the suit on. Taking it off.</p>
</div></section>
<div class="wrap"><div class="hero-img"><img src="{P}suit.webp" alt="Black and white pressure suit before a rocket and moon" style="object-position:50% 35%"></div></div>
<section><div class="wrap">
  <div class="era"><p class="when">Mid-<br>1960s</p><div><p class="mono mute">Gemini</p><h3>Donning enters the vocabulary</h3><p>The term appears in NASA's technical language during the Gemini program. A suit is not worn. It is donned.</p></div></div>
  <div class="era"><p class="when">Apollo</p><div><p class="mono mute">Procedure</p><h3>Drilled into routine</h3><p>Apollo made it routine. Donning and doffing became steps with order, checks and a crew to confirm them.</p></div></div>
  <div class="era" style="border-bottom:3px solid var(--ink)"><p class="when">Today</p><div><p class="mono mute">NASA standard</p><h3>Safety-critical</h3><p>Donning and doffing is still official NASA vocabulary. It is treated as a safety-critical task.</p></div></div>
</div></section>
<section class="on-band"><div class="wrap">
  <p class="pull">We outfit the bookends.<br><em>Ad astra</em> eleganter.</p>
  <p class="mute" style="margin-top:24px">Don &amp; Doff Co. makes spacewear in that spirit: spare, ordered, built to be worn on departure and return.</p>
  <p style="margin-top:32px"><a class="btn" href="product.html">Reserve the flagship</a></p>
</div></section>
'''
    return head + header + body + footer

def artifact_form(html):
    html = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>', '', html)
    html = re.sub(r'<meta charset[^>]*>\s*<meta name="viewport"[^>]*>\s*', '', html)
    html = html.replace('</head>\n<body>', '<style>body{margin:0}</style>').replace('</body>\n</html>', '')
    return html

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) > 1 and sys.argv[1] == "--flat":
        out, brand = sys.argv[2], sys.argv[3]
        os.makedirs(out, exist_ok=True)
        for p in ("index", "product", "about"):
            h = build(p, brand, "")
            open(os.path.join(out, p + ".html"), "w").write(artifact_form(h) if p == "index" else h)
    else:
        os.makedirs(os.path.join(here, "agency"), exist_ok=True)
        for p in ("index", "product", "about"):
            open(os.path.join(here, p + ".html"), "w").write(build(p, "mono", "", ("agency/index.html", "Agency")))
            open(os.path.join(here, "agency", p + ".html"), "w").write(build(p, "agency", "../", ("../index.html", "Heritage")))
