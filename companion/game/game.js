(() => {
  const ids = ['north-america','south-america','europe','africa','asia','oceania'];
  const names = {'north-america':'Северная Америка','south-america':'Южная Америка',europe:'Европа',africa:'Африка',asia:'Азия',oceania:'Океания'};
  const key = 'kvassistent-globe-v14';
  const saved = JSON.parse(localStorage.getItem(key) || '{}');
  const state = { total: Number(saved.total) || 0, counts: Object.fromEntries(ids.map(id => [id, Number(saved.counts?.[id]) || 0])), index: Number(saved.index) || 0, paused: false, seconds: 10 };
  const totalEls = [document.getElementById('total'), document.getElementById('corner-total')];
  const countdown = document.getElementById('countdown');
  const globe = document.getElementById('globe');
  const sites = [...document.querySelectorAll('.site')];
  const stats = document.getElementById('continent-stats');
  const pause = document.getElementById('pause');
  const sound = document.getElementById('sound');
  let audioOn = false;

  function save(){ localStorage.setItem(key, JSON.stringify({total:state.total,counts:state.counts,index:state.index})); }
  function render(){
    totalEls.forEach(el => el.textContent = state.total.toLocaleString('ru-RU'));
    countdown.textContent = state.seconds;
    sites.forEach(site => site.querySelector('small').textContent = state.counts[site.dataset.id]);
    stats.innerHTML = ids.map(id => `<article><span>${names[id]}</span><strong>${state.counts[id]}</strong></article>`).join('');
  }
  function beep(){
    if(!audioOn) return;
    const Ctx = window.AudioContext || window.webkitAudioContext; if(!Ctx) return;
    const ctx = new Ctx(), osc = ctx.createOscillator(), gain = ctx.createGain();
    osc.type='sine'; osc.frequency.setValueAtTime(180,ctx.currentTime); osc.frequency.exponentialRampToValueAtTime(620,ctx.currentTime+.22);
    gain.gain.setValueAtTime(.08,ctx.currentTime); gain.gain.exponentialRampToValueAtTime(.001,ctx.currentTime+.28); osc.connect(gain).connect(ctx.destination); osc.start(); osc.stop(ctx.currentTime+.3);
  }
  function launch(id){
    const site = sites.find(s => s.dataset.id===id); if(!site) return;
    const g = globe.getBoundingClientRect(), r = site.getBoundingClientRect();
    const x = r.left-g.left+r.width/2, y = r.top-g.top+r.height/2;
    const cx=g.width/2, cy=g.height/2, vx=x-cx, vy=y-cy, len=Math.hypot(vx,vy)||1;
    const distance=Math.max(innerWidth,innerHeight)*.46;
    const rocket=document.createElement('div'); rocket.className='rocket launch';
    rocket.style.left=`${x}px`; rocket.style.top=`${y}px`; rocket.style.setProperty('--dx',`${vx/len*distance}px`); rocket.style.setProperty('--dy',`${vy/len*distance}px`); rocket.style.setProperty('--angle',`${Math.atan2(vy,vx)*180/Math.PI+90}deg`);
    rocket.innerHTML='<i class="cap"></i><i class="bottle"></i><i class="fin l"></i><i class="fin r"></i><i class="flame"></i>';
    globe.appendChild(rocket); setTimeout(()=>rocket.remove(),2500);
    state.total++; state.counts[id]++; state.index=(ids.indexOf(id)+1)%ids.length; state.seconds=10; save(); render(); beep();
  }
  sites.forEach(site=>site.addEventListener('click',()=>launch(site.dataset.id)));
  document.getElementById('launch-now').addEventListener('click',()=>launch(ids[state.index%ids.length]));
  pause.addEventListener('click',()=>{state.paused=!state.paused;pause.textContent=state.paused?'Продолжить':'Пауза';});
  document.getElementById('reset').addEventListener('click',()=>{state.total=0;state.index=0;state.seconds=10;ids.forEach(id=>state.counts[id]=0);save();render();});
  sound.addEventListener('click',()=>{audioOn=!audioOn;sound.textContent=`Звук: ${audioOn?'вкл.':'выкл.'}`;sound.setAttribute('aria-pressed',String(audioOn));});
  setInterval(()=>{if(state.paused)return;state.seconds--;if(state.seconds<=0)launch(ids[state.index%ids.length]);render();},1000);
  render();
})();
