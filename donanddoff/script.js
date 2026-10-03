/* ---------- Campaign configuration: edit these, nothing else ---------- */
const CAMPAIGN = {
  threshold: 50,                         // units needed to trigger production
  unitsReserved: 0,                      // update by hand (or from Shopify) as orders come in
  endsAt: "2026-10-24T23:59:00-04:00",   // fixed end date, Toronto time (EDT)
  estShip: "Estimated 5–6 weeks after the campaign closes",
  checkoutUrl: "",                       // Shopify product / checkout link, e.g. https://shop.example.com/products/flagship-tee
  instagram: "donanddoffco"
};

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* bind config to the page */
$$("[data-bind=threshold]").forEach(e => e.textContent = CAMPAIGN.threshold);
$$("[data-bind=reserved]").forEach(e => e.textContent = CAMPAIGN.unitsReserved);
$$("[data-bind=remaining]").forEach(e => e.textContent = Math.max(CAMPAIGN.threshold - CAMPAIGN.unitsReserved, 0));
$$("[data-bind=ship]").forEach(e => e.textContent = CAMPAIGN.estShip);
$$("[data-bind=ends]").forEach(e => e.textContent = new Date(CAMPAIGN.endsAt).toLocaleDateString("en-CA",
  { year: "numeric", month: "long", day: "numeric", timeZone: "America/Toronto" }));
$$("[data-bind=ig]").forEach(a => { a.href = "https://instagram.com/" + CAMPAIGN.instagram; if (!a.hasAttribute("data-keep")) a.textContent = "@" + CAMPAIGN.instagram; });

/* progress bar */
const pct = Math.min(100, Math.round(CAMPAIGN.unitsReserved / CAMPAIGN.threshold * 100));
requestAnimationFrame(() => $$(".bar-track>span").forEach(b => b.style.width = pct + "%"));
$$("[data-bind=pct]").forEach(e => e.textContent = pct + "%");

/* countdown */
const cd = $$("[data-countdown]");
if (cd.length) {
  const end = new Date(CAMPAIGN.endsAt).getTime();
  const pad = n => String(n).padStart(2, "0");
  const tick = () => {
    const left = Math.max(0, end - Date.now());
    const v = [Math.floor(left / 864e5), Math.floor(left % 864e5 / 36e5), Math.floor(left % 36e5 / 6e4), Math.floor(left % 6e4 / 1e3)];
    cd.forEach(c => {
      $$("b", c).forEach((b, i) => b.textContent = pad(v[i]));
      c.setAttribute("aria-label", left ? `${v[0]} days ${v[1]} hours remaining` : "Campaign closed");
    });
    if (!left) $$("[data-closed]").forEach(e => e.hidden = false);
  };
  tick(); setInterval(tick, 1000);
}

/* gallery */
const main = $("#main-img");
$$(".thumbs button").forEach(btn => btn.addEventListener("click", () => {
  main.src = btn.dataset.src; main.alt = btn.dataset.alt;
  $$(".thumbs button").forEach(b => b.setAttribute("aria-pressed", b === btn));
}));

/* reserve */
const form = $("#reserve");
if (form) form.addEventListener("submit", e => {
  e.preventDefault();
  const size = new FormData(form).get("size");
  const out = $(".status", form);
  if (!size) { out.textContent = "Select a size."; return; }
  if (!CAMPAIGN.checkoutUrl) { out.textContent = "Checkout opens when the Shopify store is connected."; return; }
  const u = new URL(CAMPAIGN.checkoutUrl); u.searchParams.set("size", size);
  location.href = u.toString();
});
