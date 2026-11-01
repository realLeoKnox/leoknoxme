import {preferredLocale} from './language.mjs';
const menu = document.querySelector('.menu');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  document.querySelector('#nav').classList.toggle('open', open);
});
document.querySelectorAll('#nav a').forEach(link => link.addEventListener('click', () => {
  menu?.setAttribute('aria-expanded', 'false');
  document.querySelector('#nav').classList.remove('open');
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.setAttribute('aria-expanded', 'false');
    document.querySelector('#nav').classList.remove('open');
    menu.focus();
  }
});
const interestButtons = [...document.querySelectorAll('[data-interest]')];
function selectInterest(key) {
  interestButtons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.interest === key)));
  document.querySelectorAll('[data-interest-panel]').forEach(panel => {panel.hidden = panel.dataset.interestPanel !== key;});
}
interestButtons.forEach(button => button.addEventListener('click', () => selectInterest(button.dataset.interest)));
if (interestButtons.length) selectInterest(interestButtons[0].dataset.interest);
document.querySelector('#copy-email')?.addEventListener('click', async event => {
  const button = event.currentTarget, status = document.querySelector('#copy-status');
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText('leo@leosoffice.com');
    button.textContent = button.dataset.copied; status.textContent = button.dataset.copyStatus;
  } catch { status.textContent = button.dataset.copyFail; }
});
const locales = ['en','zh-Hant','zh-Hans'];
let remembered = null, dismissed = false;
try {remembered = localStorage.getItem('leo-language'); dismissed = sessionStorage.getItem('leo-language-dismissed') === 'yes';} catch { /* Storage is optional. */ }
const current = document.documentElement.lang;
const wanted = locales.includes(remembered) ? remembered : preferredLocale(navigator.languages || [navigator.language]);
const paths = {en:'', 'zh-Hant':'zh-hant/', 'zh-Hans':'zh-hans/'};
const base = current === 'en' ? './' : '../';
const banner = document.querySelector('#language-suggestion');
const isError = document.querySelector('meta[name="robots"]')?.content.includes('noindex');
if (banner && wanted !== current && !dismissed && !isError) {
  const link = document.querySelector('#suggested-language');
  link.textContent = {en:'Prefer English? Read this page in English →','zh-Hant':'偏好繁體中文？切換至繁體中文版 →','zh-Hans':'偏好简体中文？切换至简体中文版 →'}[wanted];
  link.href = base + paths[wanted] + location.hash;
  link.lang = wanted; link.hreflang = wanted; link.dataset.language = wanted;
  banner.hidden = false;
}
document.querySelector('#dismiss-language')?.addEventListener('click', () => {
  banner.hidden = true;
  try {sessionStorage.setItem('leo-language-dismissed','yes');} catch { /* No persistence required. */ }
});
document.querySelectorAll('[data-language]').forEach(link => link.addEventListener('click', () => {
  try {localStorage.setItem('leo-language',link.dataset.language);} catch { /* Links still work. */ }
  const target = new URL(link.href);target.hash = location.hash;link.href = target.href;
}));
