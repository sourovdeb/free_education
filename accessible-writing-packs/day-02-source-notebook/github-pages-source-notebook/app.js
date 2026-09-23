(() => {
  const config = window.SOURCE_NOTEBOOK_CONFIG || {};
  const $ = (selector) => document.querySelector(selector);
  const key = 'source-notebook-pages-settings';
  const saved = JSON.parse(localStorage.getItem(key) || '{}');
  const body = document.body;
  const settings = $('#settings');
  const toggle = $('#settings-toggle');
  const font = $('#font-scale');
  const line = $('#line-scale');
  const contrast = $('#contrast');
  const motion = $('#motion');
  function save(){localStorage.setItem(key,JSON.stringify({profile:body.dataset.profile,scale:font.value,line:line.value,contrast:contrast.checked,motion:motion.checked}));}
  function apply(){document.documentElement.style.setProperty('--font-size',(18*font.value/100)+'px');document.documentElement.style.setProperty('--leading',(line.value/100).toFixed(2));body.classList.toggle('high',contrast.checked);body.classList.toggle('reduced',motion.checked);save();}
  body.dataset.profile=saved.profile||config.profile||'source';font.value=saved.scale||100;line.value=saved.line||172;contrast.checked=!!saved.contrast;motion.checked=!!saved.motion;apply();
  toggle.onclick=()=>{const open=settings.hidden;settings.hidden=!open;toggle.setAttribute('aria-expanded',String(open));};
  document.querySelectorAll('[data-profile]').forEach(button=>button.onclick=()=>{body.dataset.profile=button.dataset.profile;apply();});
  [font,line,contrast,motion].forEach(control=>control.addEventListener('input',apply));
  const tools=$('#optional-tools');
  const banner=!!config.optional?.bannerMaker, activities=!!config.optional?.activities;
  if(banner||activities){tools.hidden=false;$('#banner-link').hidden=!banner;$('#activities-link').hidden=!activities;}
})();
