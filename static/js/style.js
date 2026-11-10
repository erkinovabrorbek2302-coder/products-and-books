(() => {
  const root = document.documentElement;
  const $ = (s) => document.querySelector(s);

  // Mobil menyu
  const toggle = $('#navToggle'), links = $('#navLinks');
  toggle?.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });

  // Tungi rejim
  $('#themeToggle')?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  // Bosh sahifadagi raqamlar sanab chiqiladi
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-count]').forEach((el) => {
    const end = Number(el.dataset.count) || 0;
    if (calm || end === 0) return;
    const t0 = performance.now(), dur = 900;
    const tick = (t) => {
      const p = Math.min((t - t0) / dur, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });

  // Mahsulotlarni sahifani yangilamasdan filtrlash
  const filter = $('#productFilter');
  if (filter) {
    const cards = [...document.querySelectorAll('[data-name]')];
    const none = $('#noResults');
    filter.addEventListener('input', () => {
      const q = filter.value.trim().toLowerCase();
      let shown = 0;
      cards.forEach((c) => {
        const ok = c.dataset.name.includes(q);
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (none) none.hidden = shown > 0;
    });
  }

  // Izoh maydoni yozilgan sari kengayadi
  document.querySelectorAll('textarea').forEach((ta) => {
    ta.addEventListener('input', () => {
      ta.style.height = 'auto';
      ta.style.height = ta.scrollHeight + 'px';
    });
  });
})();