(() => {
  const button = document.querySelector('.theme-toggle');
  if (!button) return;
  const prefersDark = () => window.matchMedia('(prefers-color-scheme: dark)').matches;
  let saved;
  try { saved = window.localStorage.getItem('theme'); } catch (_) { /* Storage may be unavailable. */ }
  if (saved === 'light' || saved === 'dark') document.documentElement.dataset.theme = saved;
  const current = () => document.documentElement.dataset.theme || (prefersDark() ? 'dark' : 'light');
  const update = () => {
    const dark = current() === 'dark';
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  };
  update();
  button.addEventListener('click', () => {
    const next = current() === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { window.localStorage.setItem('theme', next); } catch (_) { /* Keep the theme for this page. */ }
    update();
  });
})();
