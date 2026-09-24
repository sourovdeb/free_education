(() => {
  const $ = (selector) => document.querySelector(selector);
  const settings = $('#reading-settings');
  const toggle = $('.settings-toggle');
  const key = 'letter-room-settings';
  const saved = JSON.parse(localStorage.getItem(key) || '{}');
  const apply = () => {
    const scale = $('[data-font-scale]').value;
    const line = $('[data-line-scale]').value;
    document.documentElement.style.setProperty('--font-size', (18 * scale / 100) + 'px');
    document.documentElement.style.setProperty('--leading', (line / 100).toFixed(2));
    document.body.classList.toggle('high-contrast', $('[data-contrast]').checked);
    document.body.classList.toggle('reduce-motion', $('[data-motion]').checked);
    localStorage.setItem(key, JSON.stringify({scale, line, contrast:$('[data-contrast]').checked, motion:$('[data-motion]').checked}));
  };
  if (!toggle) return;
  $('[data-font-scale]').value = saved.scale || 100;
  $('[data-line-scale]').value = saved.line || 180;
  $('[data-contrast]').checked = !!saved.contrast;
  $('[data-motion]').checked = !!saved.motion;
  apply();
  toggle.addEventListener('click', () => {
    const open = settings.hidden;
    settings.hidden = !open;
    toggle.setAttribute('aria-expanded', String(open));
  });
  settings.addEventListener('input', apply);
})();
