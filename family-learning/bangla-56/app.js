'use strict';
// No network requests, analytics, cookies, scores, or storage of child data.
const DATA=window.BANGLA_PAGES;
const root=document.querySelector('#app');
const q=s=>document.querySelector(s);
let current=1,round=0,chosen=[],found=[],waiting=false,audioURL=null;
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const image=(key,alt='',className='icon')=>`<img class="${className}" src="assets/${key}.svg" alt="${escapeHTML(alt)}">`;
const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
function sayStatus(t){q('#status').textContent=t;}
function speak(text){
 if(!('speechSynthesis' in window)){sayStatus('La voix est indisponible. Un adulte lit.');return;}
 const voice=speechSynthesis.getVoices().find(v=>/^bn(?:-|_)/i.test(v.lang)||v.lang==='bn');
 if(!voice){sayStatus('Aucune voix bangla installée. Un adulte lit le texte.');return;}
 speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=voice.lang;u.voice=voice;u.rate=.8;
 u.onerror=()=>sayStatus('Lecture vocale indisponible. Un adulte lit.');speechSynthesis.speak(u);
}
function controls(){
 q('#prev').disabled=current===1;q('#next').disabled=current===DATA.length;
 q('#pageSelect').value=String(current);q('#counter').textContent=`Page ${current} / ${DATA.length}`;
}
function card(x,i,letter=false){return `<button class="choice" data-choice="${i}" aria-label="${escapeHTML(x.fr+' : '+x.bn)}">${letter?`<span class="glyph" lang="bn">${x.glyph}</span>`:image(x.icon,x.fr)}<span class="bn" lang="bn">${x.bn}</span><span class="phon">${x.ph}</span><span>${x.fr}</span></button>`;}
function render(){
 current=Math.min(DATA.length,Math.max(1,parseInt(location.hash.slice(1),10)||window.START_PAGE||1));
 round=0;chosen=[];found=[];waiting=false;
 if('speechSynthesis' in window)speechSynthesis.cancel();
 const p=DATA[current-1];
 root.innerHTML=`<header class="lesson-head"><span class="eyebrow">BANGLA À LA MAISON · 3–4 ANS</span><h1 lang="bn">${p.title}</h1><h2>${p.fr}</h2><p>${p.action}</p></header><section id="game" aria-label="Jeu de la page"></section><p id="status" role="status" aria-live="polite">Avec un adulte. Sans chronomètre.</p><div class="tools"><button id="again">Rejouer</button><button id="listen">Voix bangla, si disponible</button></div><details><summary>Pour l’adulte</summary><p>${p.note}</p><p>La transcription aide ; elle ne reproduit pas tous les sons. Lisez en bangla si possible. L’enfant peut montrer sans parler.</p><p>Les 11–20, les signes rares et les opérations sont des découvertes facultatives.</p><label>Votre enregistrement pour cette page : <input id="audioFile" type="file" accept="audio/*"></label><audio id="parentAudio" controls hidden></audio><p>Lecture locale, sans téléversement. Effacée en changeant de page.</p></details>`;
 if(audioURL){URL.revokeObjectURL(audioURL);audioURL=null;}
 q('#listen').onclick=()=>speak(p.items.map(x=>x.bn).join('। '));q('#again').onclick=render;
 q('#audioFile').onchange=e=>{if(!e.target.files[0])return;if(audioURL)URL.revokeObjectURL(audioURL);audioURL=URL.createObjectURL(e.target.files[0]);q('#parentAudio').src=audioURL;q('#parentAudio').hidden=false;};
 controls();
 if(p.kind==='letters')letters(p);
 else if(p.kind==='count')countGame(p);
 else if(['add','subtract','groups','share'].includes(p.kind))mathGame(p);
 else if(p.kind==='poem')poem(p);
 else if(p.kind==='echo')echo(p);
 else if(p.kind==='feelings')feelings(p);
 else if(p.kind==='memory')memory(p);
 else match(p);
}
function match(p){
 const target=p.items[round%p.items.length];
 q('#game').innerHTML=`<h3>Montre : ${target.fr}</h3><p class="target" lang="bn">${target.bn} <span class="phon">${target.ph}</span></p><div class="choices">${shuffle(p.items.map((x,i)=>({x,i}))).map(({x,i})=>card(x,i)).join('')}</div>`;
 document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{
  if(Number(b.dataset.choice)===round%p.items.length){sayStatus('Tu l’as trouvé. Dis le mot, si tu veux.');buttonNext(()=>{round++;match(p);});}
  else{sayStatus('Regardons ensemble. Essaie une autre image.');b.classList.add('try');}
 });
}
function buttonNext(fn){let b=q('#continue');if(!b){b=document.createElement('button');b.id='continue';b.textContent='Encore un tour';q('#game').append(b);}b.onclick=()=>{sayStatus('À toi.');fn();};}
function letters(p){
 const target=p.items[round%p.items.length];let choices=p.items;
 if(choices.length===1)choices=[...choices,{...target,glyph:'আ',bn:'আম',ph:'am',fr:'mangue',icon:'mango'}];
 q('#game').innerHTML=`<h3>Retrouve cette forme</h3><p class="target giant" lang="bn">${target.glyph}</p><div class="choices">${shuffle(choices.map((x,i)=>({x,i}))).map(({x,i})=>card(x,i,true)).join('')}</div><details><summary>Dessiner avec le doigt</summary><canvas width="640" height="240" aria-label="Zone de dessin libre"></canvas><button id="clear">Effacer</button><p>Jeu libre. Le tracé n’est pas noté.</p></details>`;
 document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{
  if(b.querySelector('.glyph').textContent===target.glyph){sayStatus(`Même forme ! ${target.bn} : ${target.fr}.`);buttonNext(()=>{round++;letters(p);});}
  else sayStatus('Regarde les formes. Tu peux réessayer.');
 });
 const cv=q('canvas'),ctx=cv.getContext('2d');ctx.lineWidth=8;ctx.lineCap='round';ctx.strokeStyle='#11625d';let down=false;
 const pos=e=>{const r=cv.getBoundingClientRect();return [(e.clientX-r.left)*cv.width/r.width,(e.clientY-r.top)*cv.height/r.height];};
 cv.onpointerdown=e=>{down=true;cv.setPointerCapture(e.pointerId);ctx.beginPath();ctx.moveTo(...pos(e));};
 cv.onpointermove=e=>{if(down){ctx.lineTo(...pos(e));ctx.stroke();}};
 cv.onpointerup=cv.onpointercancel=()=>down=false;q('#clear').onclick=()=>ctx.clearRect(0,0,cv.width,cv.height);
}
function countGame(p){
 const target=p.items[round%p.items.length],n=target.count;let tapped=new Set();
 q('#game').innerHTML=`<h3>Compte les étoiles</h3><div class="tokens">${Array.from({length:n},(_,i)=>`<button data-token="${i}" aria-label="Étoile ${i+1}">${image('star')}</button>`).join('')||'<p>Il n’y a aucune étoile.</p>'}</div><p id="tally">0 objet touché</p><div class="number-choices">${shuffle([...new Set([Math.max(0,n-1),n,n+1])]).map(k=>`<button data-number="${k}"><span lang="bn">${bnNum(k)}</span><small>${k}</small></button>`).join('')}</div><p class="phon">Après avoir compté : ${target.ph}</p>`;
 document.querySelectorAll('[data-token]').forEach(b=>b.onclick=()=>{tapped.add(b.dataset.token);b.classList.add('tapped');b.setAttribute('aria-pressed','true');q('#tally').textContent=tapped.size+' objet(s) touché(s)';});
 document.querySelectorAll('[data-number]').forEach(b=>b.onclick=()=>{if(Number(b.dataset.number)===n){sayStatus(`${n} : ${target.bn} · ${target.ph}.`);buttonNext(()=>{round++;countGame(p);});}else sayStatus('Comptons ensemble, un par un.');});
}
const bnNum=n=>String(n).replace(/\d/g,d=>'০১২৩৪৫৬৭৮৯'[Number(d)]);
function mathGame(p){
 const g=q('#game');
 if(p.kind==='add'||p.kind==='subtract'){
  let n=p.kind==='add'?1:3,goal=2,done=false;
  const draw=()=>{g.innerHTML=`<h3>${p.kind==='add'?'Ajoute une pomme.':'Enlève une pomme.'}</h3><div class="tokens apples">${Array.from({length:n},()=>image('apple','pomme')).join('')}</div><button id="operate" ${done?'disabled':''}>${p.kind==='add'?'+ Une pomme':'− Une pomme'}</button><p id="equation" class="target" lang="bn">${done?p.items[0].bn:bnNum(n)}</p>`;q('#operate').onclick=()=>{if(done)return;n+=p.kind==='add'?1:-1;done=true;draw();sayStatus('Compte le résultat : deux pommes. '+p.items[0].ph);};};draw();
 }else if(p.kind==='groups'){
  let n=[0,0];const draw=()=>{g.innerHTML=`<h3>Deux pommes par panier</h3><div class="baskets">${n.map((v,i)=>`<button data-basket="${i}" ${v===2?'disabled':''} aria-label="Panier ${i+1}, ${v} pomme(s)">${image('basket')}<span>${Array.from({length:v},()=>image('apple','pomme','mini')).join('')}</span></button>`).join('')}</div><p>Appuie sur chaque panier.</p><p class="target" lang="bn">${n.every(v=>v===2)?p.items[0].bn:''}</p>`;document.querySelectorAll('[data-basket]').forEach(b=>b.onclick=()=>{n[Number(b.dataset.basket)]++;draw();if(n.every(v=>v===2))sayStatus('Deux groupes de deux : quatre. '+p.items[0].ph);});};draw();
 }else{
  let n=[0,0],left=4;const draw=()=>{g.innerHTML=`<h3>Partage entre deux assiettes</h3><p>${left} pomme(s) à partager.</p><div class="tokens apples">${Array.from({length:left},()=>image('apple','pomme')).join('')}</div><div class="baskets">${n.map((v,i)=>`<button data-plate="${i}" ${left===0?'disabled':''} aria-label="Assiette ${i+1}, ${v} pomme(s)">${image('plate')}<span>${Array.from({length:v},()=>image('apple','pomme','mini')).join('')}</span></button>`).join('')}</div><p>Appuie sur une assiette.</p><p class="target" lang="bn">${left===0&&n[0]===2?p.items[0].bn:''}</p>`;document.querySelectorAll('[data-plate]').forEach(b=>b.onclick=()=>{n[Number(b.dataset.plate)]++;left--;draw();if(left===0)sayStatus(n[0]===2?'Deux pommes chacun. '+p.items[0].ph:'Il n’y en a pas autant. Rejouons pour partager également.');});};draw();
 }
}
function poem(p){
 let line=0;const draw=()=>{const x=p.items[line];q('#game').innerHTML=`<h3>Un vers, un geste</h3><div class="poem-scene">${image(x.icon,x.fr)}<p class="bn" lang="bn">${x.bn}</p><p class="phon">${x.ph}</p><p>${x.fr}</p></div><button id="verse">${line<p.items.length-1?'Vers suivant':'Recommencer la comptine'}</button><p>${line+1} / ${p.items.length}</p>`;q('#verse').onclick=()=>{line=(line+1)%p.items.length;draw();sayStatus('Écoute le vers. Fais le geste.');};};draw();
}
function echo(p){
 let i=0;const draw=()=>{q('#game').innerHTML=`<h3>L’adulte dit. Tu réponds.</h3><div class="choices">${card(p.items[i],i)}</div><button id="echo">À toi de parler</button><button id="swap">Changer de mot</button>`;q('[data-choice]').onclick=()=>speak(p.items[i].bn);q('#echo').onclick=()=>sayStatus('Dis-le, ou montre. Aucun microphone.');q('#swap').onclick=()=>{i=(i+1)%p.items.length;draw();};};draw();
}
function feelings(p){q('#game').innerHTML=`<h3>Choisis ton ressenti</h3><div class="choices">${p.items.map((x,i)=>card(x,i)).join('')}</div>`;document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-choice]').forEach(k=>k.classList.remove('selected'));b.classList.add('selected');sayStatus(`${p.items[Number(b.dataset.choice)].bn} · On t’écoute. Tu peux changer.`);});}
function memory(p){
 const tiles=shuffle(p.items.flatMap((x,i)=>[{x,i},{x,i}]));
 q('#game').innerHTML=`<h3>Retrouve les paires d’images</h3><div class="memory">${tiles.map((t,i)=>`<button data-tile="${i}" aria-label="Carte cachée ${i+1}"><span class="back">?</span><span class="front" hidden>${image(t.x.icon,t.x.fr)}<span lang="bn">${t.x.bn}</span></span></button>`).join('')}</div><button id="turnback" hidden>Retourner ces deux cartes</button>`;
 document.querySelectorAll('[data-tile]').forEach(b=>b.onclick=()=>{
  const n=Number(b.dataset.tile);if(waiting||found.includes(n)||chosen.includes(n))return;
  b.querySelector('.back').hidden=true;b.querySelector('.front').hidden=false;b.setAttribute('aria-label',tiles[n].x.fr);chosen.push(n);
  if(chosen.length===2){if(tiles[chosen[0]].i===tiles[chosen[1]].i){found.push(...chosen);chosen=[];sayStatus(found.length===tiles.length?'Toutes les paires sont réunies.':'Une paire ! Dis son nom.');}
   else{waiting=true;sayStatus('Deux images différentes. Regarde-les.');q('#turnback').hidden=false;}}
 });
 q('#turnback').onclick=()=>{chosen.forEach(n=>{const b=q(`[data-tile="${n}"]`);b.querySelector('.back').hidden=false;b.querySelector('.front').hidden=true;b.setAttribute('aria-label','Carte cachée '+(n+1));});chosen=[];waiting=false;q('#turnback').hidden=true;};
}
q('#pageSelect').innerHTML=DATA.map(p=>`<option value="${p.id}">${p.id}. ${escapeHTML(p.fr)}</option>`).join('');
q('#pageSelect').onchange=e=>location.hash=e.target.value;
q('#prev').onclick=()=>location.hash=current-1;q('#next').onclick=()=>location.hash=current+1;
window.addEventListener('hashchange',render);render();
