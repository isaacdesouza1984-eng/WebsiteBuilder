(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Mobile nav
  const nav = document.querySelector(".nav");
  const burger = document.querySelector(".burger");
  burger.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
  });
  document.querySelectorAll("#menu a").forEach((a) =>
    a.addEventListener("click", () => {
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    })
  );

  // Starfield
  const canvas = document.getElementById("stars");
  const ctx = canvas.getContext("2d");
  let stars = [];
  function sizeStars() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = innerWidth * dpr;
    canvas.height = innerHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.round((innerWidth * innerHeight) / 5200);
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * innerWidth,
      y: Math.random() * innerHeight,
      r: Math.random() * 1.2 + 0.2,
      a: Math.random() * 0.6 + 0.15,
      s: Math.random() * 0.02 + 0.004,
      p: Math.random() * Math.PI * 2,
    }));
  }
  function drawStars(t) {
    ctx.clearRect(0, 0, innerWidth, innerHeight);
    for (const st of stars) {
      const tw = reduce ? 1 : 0.65 + 0.35 * Math.sin(st.p + t * st.s * 0.06);
      ctx.globalAlpha = st.a * tw;
      ctx.fillStyle = "#dfe7ff";
      ctx.beginPath();
      ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
      ctx.fill();
    }
    if (!reduce) requestAnimationFrame(drawStars);
  }
  sizeStars();
  addEventListener("resize", sizeStars);
  requestAnimationFrame(drawStars);

  // Countdown console: polls each station, then launches
  const clock = document.getElementById("clock");
  const polls = [...document.querySelectorAll("#polls li")];
  const foot = document.getElementById("console-foot");
  const clockWrap = clock.parentElement;
  const fmt = (n) => `00:00:${String(n).padStart(2, "0")}`;

  function runSequence() {
    let n = 10;
    polls.forEach((li) => li.classList.remove("ok"));
    clockWrap.classList.remove("launched");
    foot.classList.remove("ready");
    foot.textContent = "Polling stations…";
    clock.textContent = fmt(n);
    const timer = setInterval(() => {
      n -= 1;
      clock.textContent = fmt(Math.max(n, 0));
      const idx = 9 - n;
      if (idx >= 0 && idx < polls.length) polls[idx].classList.add("ok");
      if (n === 3) foot.textContent = "All stations GO. Cleared for launch.";
      if (n <= 0) {
        clearInterval(timer);
        clockWrap.classList.add("launched");
        foot.classList.add("ready");
        foot.textContent = "Liftoff. Monitoring in flight.";
        setTimeout(runSequence, 6000);
      }
    }, 1000);
  }
  if (reduce) {
    polls.forEach((li) => li.classList.add("ok"));
    clock.textContent = "00:00:00";
    clockWrap.classList.add("launched");
    foot.classList.add("ready");
    foot.textContent = "All stations GO. Cleared for launch.";
  } else {
    runSequence();
  }

  // Reveal on scroll
  const targets = document.querySelectorAll(".section-head, .card, .sequence li, .tier, .logo-card, .split > *, .clients > div");
  if ("IntersectionObserver" in window && !reduce) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      }),
      { threshold: 0.12 }
    );
    targets.forEach((el) => { el.classList.add("reveal"); io.observe(el); });
  }

  // Engagement buttons preselect the form topic
  const topic = document.getElementById("topic");
  document.querySelectorAll("[data-topic]").forEach((a) =>
    a.addEventListener("click", () => { topic.value = a.dataset.topic; })
  );

  // Contact form
  const form = document.getElementById("contact-form");
  const status = form.querySelector(".form-status");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const endpoint = form.dataset.endpoint;
    status.className = "form-status";
    if (!endpoint) {
      status.classList.add("err");
      status.textContent = "Contact form isn't connected yet. Please check back soon.";
      return;
    }
    status.textContent = "Transmitting…";
    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      });
      if (!res.ok) throw new Error(res.statusText);
      form.reset();
      status.classList.add("ok");
      status.textContent = "Transmission received. We'll be in touch within two business days.";
    } catch {
      status.classList.add("err");
      status.textContent = "Something went wrong sending your message. Please try again.";
    }
  });

  document.getElementById("year").textContent = new Date().getFullYear();
})();
