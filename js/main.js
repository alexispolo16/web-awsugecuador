(function () {
  var d = document, root = d.documentElement;
  root.classList.add('js');

  var header = d.querySelector('.site-header');
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  var toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('.label').textContent = open ? 'Cerrar' : 'Menú';
      nav.classList.toggle('open', open);
      d.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', function () { setOpen(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); toggle.focus(); } });
    window.matchMedia('(min-width: 1024px)').addEventListener('change', function (m) { if (m.matches) setOpen(false); });
  }

  var reveals = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

(function () {
  var d = document;

  var cd = d.querySelector('[data-countdown]');
  if (cd) {
    var target = new Date(cd.getAttribute('data-countdown')).getTime();
    var u = {}; ['d', 'h', 'm', 's'].forEach(function (k) { u[k] = cd.querySelector('[data-u="' + k + '"]'); });
    var pad = function (n) { return n < 10 ? '0' + n : String(n); };
    var tick = function () {
      var t = Math.max(0, target - Date.now());
      u.d.textContent = Math.floor(t / 864e5);
      u.h.textContent = pad(Math.floor(t / 36e5) % 24);
      u.m.textContent = pad(Math.floor(t / 6e4) % 60);
      u.s.textContent = pad(Math.floor(t / 1e3) % 60);
    };
    tick(); setInterval(tick, 1000);
  }

  var grid = d.getElementById('moments-grid'), more = d.querySelector('.more');
  var expand = function () { if (grid) grid.classList.add('expanded'); if (more) { more.setAttribute('aria-expanded', 'true'); more.hidden = true; } };
  if (more) more.addEventListener('click', expand);

  var chips = d.querySelectorAll('.chip[data-filter]');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === chip)); });
      d.querySelectorAll('.moment').forEach(function (m) { m.hidden = f !== 'all' && m.getAttribute('data-cat') !== f; });
      if (f !== 'all') expand();
    });
  });
})();

