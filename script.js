(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('nav');

  function setOpen(open) {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  }

  toggle.addEventListener('click', function () {
    setOpen(!nav.classList.contains('open'));
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') setOpen(false);
  });

  document.getElementById('year').textContent = new Date().getFullYear();

  /* Menu */
  var tabs = document.getElementById('menu-tabs');
  var grid = document.getElementById('menu-grid');
  var menu = window.MENU || [];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  function show(id) {
    Array.prototype.forEach.call(tabs.children, function (b) {
      b.setAttribute('aria-selected', String(b.dataset.id === id));
    });
    grid.replaceChildren();
    var cat = menu.filter(function (c) { return c.id === id; })[0];
    if (!cat) return;
    cat.items.forEach(function (it) {
      var card = el('article', 'dish' + (it.img ? '' : ' dish-noimg'));
      if (it.img) {
        var img = el('img');
        img.src = it.img; img.alt = it.name; img.loading = 'lazy'; img.width = 560; img.height = 420;
        card.appendChild(img);
      }
      var body = el('div', 'dish-body');
      var head = el('div', 'dish-head');
      head.appendChild(el('h3', '', it.name));
      head.appendChild(el('span', 'price', it.price ? '$' + it.price.toFixed(2) : ''));
      body.appendChild(head);
      if (it.fa) { var fa = el('span', 'fa', it.fa); fa.lang = 'fa'; fa.dir = 'rtl'; body.appendChild(fa); }
      if (it.desc) body.appendChild(el('p', '', it.desc));
      card.appendChild(body);
      grid.appendChild(card);
    });
  }

  menu.forEach(function (c, i) {
    var b = el('button', '', c.title);
    b.type = 'button'; b.dataset.id = c.id; b.setAttribute('role', 'tab');
    b.addEventListener('click', function () { show(c.id); });
    tabs.appendChild(b);
    if (i === 0) show(c.id);
  });

  /* Contact form: set data-endpoint on the form (e.g. https://formsubmit.co/ajax/you@example.com) */
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');
  var ENDPOINT = form.dataset.endpoint || '';

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var data = new FormData(form);
    status.className = 'form-status';
    if (data.get('_honey')) return;
    if (!data.get('name').trim() || !/^\S+@\S+\.\S+$/.test(data.get('email')) || !data.get('message').trim()) {
      status.textContent = 'Please enter your name, a valid email and a message.';
      status.classList.add('err');
      return;
    }
    if (!ENDPOINT) {
      status.textContent = 'Online messages are not switched on yet. Please call (905) 764-0000.';
      status.classList.add('err');
      return;
    }
    var btn = form.querySelector('button');
    btn.disabled = true; status.textContent = 'Sending...';
    fetch(ENDPOINT, { method: 'POST', headers: { Accept: 'application/json' }, body: data })
      .then(function (r) { if (!r.ok) throw new Error(); form.reset(); status.textContent = 'Thank you! We will be in touch soon.'; status.classList.add('ok'); })
      .catch(function () { status.textContent = 'Sorry, something went wrong. Please call (905) 764-0000.'; status.classList.add('err'); })
      .then(function () { btn.disabled = false; });
  });
})();
