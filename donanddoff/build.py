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
  <div><dt>Provenance</dt><dd>Each piece individually numbered. Certificate of authenticity included.</dd></div>
</dl>'''

SYSTEMS = [
 ("Chevron panels","Suit","High-contrast panels read at a distance and show orientation.","Street","Easy to spot in low light and from across the road."),
 ("Reinforced shoulders","Suit","Shoulders and arms take the load and the wear.","Street","Panels where bag straps and friction land."),
 ("Zipped hand pockets","Suit","Tools stay within reach and stay closed.","Street","Phone, keys and card secured, hands free."),
 ("Full-length zip","Suit","Long closures make donning and doffing a procedure.","Street","Open it fully or only to the chest."),
 ("Collar and hood","Suit","Suits seal at the neck.","Street","A high collar and a hood that sits close."),
 ("Cuffs and hem","Suit","Suits seal at wrist and waist.","Street","Ribbed cuffs and hem hold the fit.")]
PINS = [(63,38),(29,21),(66,62),(50,70),(50,13),(32,87)]

def anatomy(P):
    pins = ''.join(f'<button type="button" class="pin" data-i="{i}" style="left:{x}%;top:{y}%" aria-label="{SYSTEMS[i][0]}">{i+1:02d}</button>' for i,(x,y) in enumerate(PINS))
    rows = ''.join(f'''<li data-i="{i}" tabindex="0"><span class="n mono">{i+1:02d}</span><div><h3>{a}</h3><p><b class="mono">Suit</b> {b}</p><p><b class="mono">Earth</b> {d}</p></div></li>''' for i,(a,_,b,_,d) in enumerate(SYSTEMS))
    return f'''<div class="anat">
  <div class="anat-img"><img src="{P}pl-front.webp" alt="Front of the Pressure-Line jacket with numbered callouts">{pins}</div>
  <ol class="anat-list">{rows}</ol>
</div>'''

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
  <div class="fine mono"><span>&copy; Don &amp; Doff Co.</span><span>Independent brand. Not affiliated with, sponsored by, or endorsed by NASA.</span>{sw}</div>
</div></footer>
<script src="{pre}script.js"></script>
</body>
</html>
'''
    P = pre + "images/"
    if page == "index":
        body = f"""
<section class="hero2"><div class="wrap">
  <p class="mono eyebrow">Flagship 001 · Numbered run · Pre-order open</p>
  <h1>Reverse-engineered<br><em>from the suit.</em></h1>
  <div class="hero-row">
    <p class="lead">Spacewear built from the logic of the pressure suit, for everyday life on Earth.</p>
    <div class="cta"><a class="btn" href="product.html">Reserve · $199</a><a class="btn line" href="#suit-logic">See the systems</a></div>
  </div>
</div>
<figure class="bleed"><img src="{P}hero-salt.webp" alt="A person in the black and white Pressure-Line jacket walking across a white salt flat at dawn toward a rocket on its launch pad"><figcaption class="mono wrap"><span>Suit up. Reach orbit. Repeat.</span><span>Ad astra eleganter</span></figcaption></figure>
</section>

<div class="ticker" aria-hidden="true"><div class="track">
  {''.join('<span>Articulation</span><i>/</i><span>Reinforcement</span><i>/</i><span>Storage</span><i>/</i><span>Visibility</span><i>/</i><span>Closure</span><i>/</i>' for _ in range(5))}
</div></div>

<section id="suit-logic"><div class="wrap">
  <div class="head-row"><div><p class="mono mute">Suit logic</p><h2 style="margin-top:12px;max-width:11em">A suit solves problems. We kept the solutions.</h2></div>
  <p class="mute" style="max-width:24em">Six systems from pressure-suit design, carried into a jacket you wear to work. Select a point.</p></div>
  {anatomy(P)}
</div></section>

<section class="split"><figure class="bleed tall"><img src="{P}hangar.webp" alt="A white pressure suit and the Pressure-Line jacket on matching stands in an aerospace hangar" style="object-position:50% 40%"></figure>
<div class="wrap"><p class="pull2">From the hangar<br>to the street.<br><em>Same logic.</em></p></div></section>

<section><div class="wrap day">
  <figure class="stage2"><img src="{P}street.webp" alt="A person in the Pressure-Line jacket sliding a phone into the zip pocket on a bright city street" loading="lazy"></figure>
  <div>
    <p class="mono mute">Mission profile</p>
    <h2 style="margin:12px 0 28px">An ordinary day, run like a mission.</h2>
    <ol class="log">
      <li><span class="mono">06:40</span><div><h3>Don</h3><p>Zip. Hood up.</p></div></li>
      <li><span class="mono">07:15</span><div><h3>Transit</h3><p>Phone, keys and card stowed. Tap the comm to take a call.</p></div></li>
      <li><span class="mono">12:30</span><div><h3>Hold</h3><p>Collar down. Zip to the chest.</p></div></li>
      <li><span class="mono">18:00</span><div><h3>Return</h3><p>Beacon on. Same jacket, different light.</p></div></li>
      <li><span class="mono">22:10</span><div><h3>Doff</h3><p>Hang it up. Repeat.</p></div></li>
    </ol>
  </div>
</div></section>

<section class="mods"><div class="wrap">
  <div class="head-row"><div><p class="mono mute">Modules · Sold separately</p><h2 style="margin-top:12px;max-width:12em">Clip on. Connect.</h2></div>
  <p class="mute" style="max-width:26em">Magnetic modules that clip onto the jacket. A comm badge for calls and audio. A beacon for low light.</p></div>
  <div class="mod-row">
    <figure class="mod-shot"><img src="{P}module-worn.webp" alt="A finger tapping the inch-wide comm badge clipped to the chest of the Pressure-Line jacket" loading="lazy"></figure>
    <article class="mod"><figure><img src="{P}module-comm.webp" alt="Slim one-inch comm badge with titanium rim, engraved orbit rings and touch controls, beside its magnetic backplate" loading="lazy"></figure>
      <div class="mod-head"><div><p class="mono mute">Module 01</p><h3>Comm</h3></div><p class="mod-price">$99</p></div>
      <ul><li>About one inch across. Slim profile.</li><li>Touch controls: play/pause, volume, track skip</li><li>Answer and end calls</li><li>Built-in speaker and microphone</li><li>Bluetooth</li><li>Magnetic clip</li></ul></article>
  </div>
  <div class="mod-row flip">
    <figure class="mod-shot"><img src="{P}module-beacon-worn.webp" alt="The beacon glowing on the chest of the Pressure-Line jacket on a city street at dusk" loading="lazy"></figure>
    <article class="mod"><figure><img src="{P}module-beacon.webp" alt="Slim clip-on light module with a white LED edge and a magnetic backplate" loading="lazy"></figure>
      <div class="mod-head"><div><p class="mono mute">Module 02</p><h3>Beacon</h3></div><p class="mod-price">$49</p></div>
      <ul><li>Clip-on light for low-light transit</li><li>One-button control</li><li>Magnetic clip</li></ul></article>
  </div>
</div></section>

<section class="on-band"><div class="wrap campaign">
  <div>
    <p class="mono">Flagship 001 · Threshold pre-order</p>
    <h2>The Pressure-Line</h2>
    <p>Made only if 50 are ordered. Each piece is numbered and ships with a certificate of authenticity. Charged at order. Refunded in full to everyone if the threshold is not met by the deadline.</p>
    <a class="btn" href="product.html">Reserve · $199</a>
  </div>
  <div>{gauge()}{TERMS}</div>
</div></section>

<section><div class="wrap">
  <div class="head-row"><h2>In the field</h2><a class="btn line sm" data-bind="ig" data-keep href="https://instagram.com/donanddoffco" rel="noopener">Follow @donanddoffco</a></div>
  <div class="look">
    <figure class="a"><img src="{P}pl-model.webp" alt="Model in the black and white zip hoodie with black joggers" loading="lazy"><figcaption class="mono">Worn</figcaption></figure>
    <figure class="b"><img src="{P}detail.webp" alt="Close-up of the white chevron panel, reinforced shoulder and zip" loading="lazy" style="object-position:50% 30%"><figcaption class="mono">Detail</figcaption></figure>
    <figure class="c"><img src="{P}pl-back.webp" alt="Back of the jacket with a white chevron across the shoulders" loading="lazy"><figcaption class="mono">Aft</figcaption></figure>
    <figure class="d"><img src="{P}trio.webp" alt="Concept: three visor hoodies" loading="lazy"><figcaption class="mono">Concept</figcaption></figure>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <p class="mono mute">Why the name</p>
  <h2 style="margin-top:12px;max-width:14em">Two words. Every mission starts and ends with them.</h2>
  <div class="defs">
    <div><p class="mono ipa">verb · /dɒn/</p><h3>Don</h3><p>To put on the suit. The first act of every mission.</p></div>
    <div><p class="mono ipa">verb · /dɒf/</p><h3>Doff</h3><p>To take it off. The last.</p></div>
  </div>
  <p class="src mono">NASA-STD-3001, requirement V2 11001: Suited Donning and Doffing.</p>
  <div class="steps">
    <div><p class="mono">1966</p><h3>Gemini</h3><p>A NASA technical note describes a suit design approach followed to simplify donning and doffing.</p></div>
    <div><p class="mono">2017</p><h3>Next-gen suits</h3><p>Life support budgeted for 8-hour EVAs, plus 2 hours of donning and doffing.</p></div>
    <div><p class="mono">Now</p><h3>V2 11001</h3><p>NASA's human spaceflight standard requires efficient and effective donning and doffing.</p></div>
  </div>
  <p style="margin-top:36px"><a class="btn line" href="about.html">Read the full entry</a></p>
</div></section>
"""
    elif page == "product":
        imgs = [("pl-front.webp","Front of the black zip hoodie with white chevron panels"),("pl-back.webp","Back with a white chevron across the shoulders"),("pl-model.webp","Worn with black joggers"),("detail.webp","Close-up of chevron panel, shoulder and zip"),("street.webp","Worn on a city street")]
        th = ''.join(f'<button type="button" data-src="{P}{a}" data-alt="{b}" aria-pressed="{"true" if i==0 else "false"}" aria-label="View image {i+1}"><img src="{P}{a}" alt=""></button>' for i,(a,b) in enumerate(imgs))
        sizes = ''.join(f'<span><input type="radio" name="size" id="s-{s}" value="{s}"><label for="s-{s}">{s}</label></span>' for s in ["S","M","L","XL","2XL"])
        body = f"""
<section style="padding-top:clamp(28px,4vw,56px)"><div class="wrap pdp">
  <div class="gallery">
    <div class="main"><img id="main-img" src="{P}{imgs[0][0]}" alt="{imgs[0][1]}"></div>
    <div class="thumbs">{th}</div>
    <p class="note">Product renders and campaign imagery. Final print placement and colourway are confirmed with the printer before production.</p>
  </div>
  <div>
    <p class="mono mute">Flagship 001 · Threshold pre-order</p>
    <h1 style="font-size:clamp(2.3rem,5.6vw,4rem);margin-top:12px">The Pressure-Line</h1>
    <p class="price">$199</p>
    <p>Pressure-suit logic for everyday life on Earth. White chevron panels, reinforced shoulders, zipped pockets and a full-length zip, in one jacket.</p>
    {gauge()}
    <form id="reserve" novalidate>
      <p class="mono">Size</p>
      <div class="sizes" role="radiogroup" aria-label="Size">{sizes}</div>
      <button class="btn" type="submit" style="width:100%;justify-content:center">Reserve · $199</button>
      <p class="status" role="status"></p>
    </form>
    <p class="mono" style="margin-top:34px">Campaign terms</p>
    {TERMS}
    <ul class="spec">
      <li>Six suit systems: chevron panels, reinforced shoulders, zipped pockets, full-length zip, collar and hood, cuffs and hem</li>
      <li>Individually numbered, with certificate of authenticity</li>
      <li>Pairs with Don &amp; Doff magnetic modules: Comm ($99) and Beacon ($49), sold separately</li>
      <li>Produced in Toronto</li>
      <li>One production run. No restock promised.</li>
    </ul>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <p class="mono mute">Suit logic</p>
  <h2 style="margin:12px 0 0;max-width:12em">What the suit taught the jacket.</h2>
  {anatomy(P)}
</div></section>
"""
    else:
        body = f"""
<section style="padding-bottom:clamp(32px,5vw,56px)"><div class="wrap">
  <p class="mono mute">About Don &amp; Doff Co.</p>
  <h1 style="margin-top:14px">Don &amp;<br>Doff</h1>
  <p style="margin-top:28px;font-size:1.3rem;color:var(--mute)">Don is the leaving. Doff is the coming back. We named a clothing brand after the whole cycle.</p>
</div></section>
<div class="wrap"><figure class="hero-img"><img src="{P}hangar.webp" alt="A white pressure suit and the Pressure-Line jacket on matching stands in an aerospace hangar"></figure></div>
<section><div class="wrap">
  <div class="era"><p class="when">V2<br>11001</p><div><p class="mono mute">The name</p><h3>Suited Donning and Doffing</h3>
    <p>Somewhere in NASA's human spaceflight standards there is a requirement numbered V2 11001. Its title is "Suited Donning and Doffing." It says spacesuits must allow for "efficient and effective donning and doffing," in normal operations and in emergencies.</p>
    <p>Before a launch or a walk on another world, someone has to get dressed. Afterward, someone has to come home and take it all off. NASA's own description of EVA preparation runs from unstowing the suit through checkout, donning, doffing, and stowage. The suit is the first thing a crew puts on and the last thing it takes off.</p></div></div>
  <div class="era"><p class="when">1966</p><div><p class="mono mute">Where it started · Gemini</p><h3>A problem about clothing</h3>
    <p>A 1966 NASA Technical Note (TN D-3291) describes the suit built for the Gemini program. The capsule was too small for a crew member to fully put on or take off the conventional suit in flight. So the design priority became long-term comfort: a soft suit that served mostly as a flight suit, with a torso garment worn throughout the mission.</p>
    <p>You stepped into it through a pressure-sealing zipper. The helmet had a quick doff-and-don capability. The document describes an approach followed to simplify donning and doffing and to improve the suit's operational use. One of the real engineering problems in spaceflight was how a person gets in and out of the thing that protects them.</p></div></div>
  <div class="era"><p class="when">2017</p><div><p class="mono mute">The same problem, decades later</p><h3>Budgeted into life support</h3>
    <p>A 2017 NASA Office of Inspector General report on spacesuit development describes a next-generation life support system sized for 100 EVAs, with 8 hours per EVA plus 2 hours of suit donning and doffing built into the budget. Even the life support hardware has to account for the time spent getting in and out.</p></div></div>
  <div class="era" style="border-bottom:3px solid var(--ink)"><p class="when">Now</p><div><p class="mono mute">What we make</p><h3>The idea, not the engineering</h3>
    <p>We make clothes for people who understand that how you suit up matters, and that every departure assumes a return. Our designs borrow the language of the suit: the seams, the layers, the ritual of putting something on with intent.</p>
    <p>We borrow the idea, not the engineering. These are garments, not flight hardware.</p></div></div>
</div></section>
<section class="on-band"><div class="wrap">
  <p class="pull">Suit up. Reach orbit.<br><em>Repeat.</em></p>
  <p class="mute" style="margin-top:24px">Ad astra eleganter.</p>
  <p style="margin-top:32px"><a class="btn" href="product.html">Reserve the flagship</a></p>
</div></section>
<section><div class="wrap sources">
  <p class="mono mute">Sources</p>
  <ul>
    <li><a href="https://www.nasa.gov/wp-content/uploads/2025/09/ochmo-tb-050-spacesuits.pdf" rel="noopener">NASA-STD-3001 Technical Brief, Spacesuits (OCHMO-TB-050), derived from NASA-STD-3001 Volume 2, Rev E</a></li>
    <li><a href="https://ntrs.nasa.gov/api/citations/19660007653/downloads/19660007653.pdf" rel="noopener">NASA Technical Note TN D-3291, Gemini space suit (1966)</a></li>
    <li><a href="https://oig.nasa.gov/docs/IG-17-018.pdf" rel="noopener">NASA OIG Report IG-17-018, "NASA's Management and Development of Spacesuits" (April 2017)</a></li>
  </ul>
  <p class="mute disclaimer">Don &amp; Doff Co. is an independent brand and is not affiliated with, sponsored by, or endorsed by NASA. References to NASA documents are for historical and informational purposes only.</p>
</div></section>
"""
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
