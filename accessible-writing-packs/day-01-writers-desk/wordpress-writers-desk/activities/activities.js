(() => {
  const el = (id) => document.getElementById(id);
  const shuffle = (list) => list.map(v => [Math.random(),v]).sort((a,b)=>a[0]-b[0]).map(v=>v[1]);
  const words = ['a','small','place','for','thought']; let picked=[];
  function wordsDraw(){el('words').innerHTML='';shuffle(words).forEach(word=>{const b=document.createElement('button');b.className='token';b.textContent=word;b.onclick=()=>{picked.push(word);el('word-note').textContent='Your sentence: '+picked.join(' ');if(picked.join(' ')==='a small place for thought'){el('word-note').textContent='A small place for thought. You can reset or continue.'}};el('words').append(b)})}
  el('word-hint').onclick=()=>el('word-note').textContent='Hint: begin with “a”.';el('word-reset').onclick=()=>{picked=[];el('word-note').textContent='';wordsDraw()};wordsDraw();
  const icons=['●','●','▲','▲','■','■','◆','◆'];let open=[],matched=[],deck=shuffle(icons);
  function cardsDraw(){el('cards').innerHTML='';deck.forEach((icon,i)=>{const b=document.createElement('button');b.className='card';b.textContent=(open.includes(i)||matched.includes(i))?icon:'?';b.setAttribute('aria-label',(open.includes(i)||matched.includes(i))?'Card '+icon:'Hidden card');b.onclick=()=>{if(open.length===2||matched.includes(i))return;open.push(i);if(open.length===2){setTimeout(()=>{const buttons=[...el('cards').children];if(buttons[open[0]].dataset.icon===buttons[open[1]].dataset.icon){matched.push(...open);el('card-note').textContent='A pair found. Continue when ready.'}else{el('card-note').textContent='Not that pair. Try again or use Hint.'}open=[];cardsDraw()},500)}cardsDraw()};b.dataset.icon=icon;el('cards').append(b)})}
  el('card-hint').onclick=()=>el('card-note').textContent='Hint: two circles, two triangles, two squares, and two diamonds are present.';el('card-reset').onclick=()=>{open=[];matched=[];deck=shuffle(icons);cardsDraw()};cardsDraw();
  const pattern=['○','●','○','●'];function patternDraw(){el('pattern').innerHTML='';pattern.forEach(mark=>{const s=document.createElement('span');s.className='mark';s.textContent=mark;el('pattern').append(s)});['○','●','▲'].forEach(mark=>{const b=document.createElement('button');b.className='mark';b.textContent=mark;b.onclick=()=>{if(mark==='○'){el('pattern-note').textContent='That fits the pattern. Reset or continue.'}else{el('pattern-note').textContent='No penalty. The next mark follows the circle-dot pattern.'}};el('pattern').append(b)})}
  el('pattern-hint').onclick=()=>el('pattern-note').textContent='Hint: circle, dot, circle, dot, then circle.';el('pattern-reset').onclick=()=>{el('pattern-note').textContent='';patternDraw()};patternDraw();
  el('font').oninput=e=>document.documentElement.style.fontSize=e.target.value+'%';
  el('contrast').onchange=e=>document.body.classList.toggle('high',e.target.checked);
  el('motion').onchange=e=>document.body.classList.toggle('reduced',e.target.checked);
  el('sound').onchange=()=>{};
})();
