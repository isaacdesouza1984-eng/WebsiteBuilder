# Don & Doff Co.

Heritage (mono) pages are in this folder; the Agency colourway is in `agency/`.
Both are generated: edit `build.py`, `styles.css`, `script.js`, then run `python3 build.py`.

Campaign settings live in the `CAMPAIGN` block at the top of `script.js`
(threshold, units reserved, end date, ship estimate, Shopify store URL, product handle / variant IDs, Instagram).

Shopify store: https://16ituc-qb.myshopify.com (password-protected, redirects to donanddoff.com).
To enable Reserve: create the product, then set `productHandle` (or per-size `variantIds` for cart links).

Imagery in `images/`: product renders (`pl-*`), AI campaign scenes (`hero-salt`, `hangar`, `street`, `detail`),
and crest variants (`logo-*`, cut from the supplied monochrome crest).
