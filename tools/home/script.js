(()=>{"use strict";
  const GATES=['(max-width: 720px)','(orientation: portrait) and (max-width: 1024px)','(orientation: portrait) and (pointer: coarse)','(orientation: landscape) and (pointer: coarse) and (max-height: 560px)','(prefers-reduced-motion: reduce)'];
  const MQLS=GATES.map(q=>matchMedia(q)),gated=()=>MQLS.some(m=>m.matches),$=id=>document.getElementById(id),root=document.documentElement;
  const hero=document.querySelector('.hero-journey'),stage=$('heroStage'),video=$('heroVideo'),hud=$('hud'),rail=$('railFill'),loadLine=$('loadLine'),endFooter=$('endFooter'),finalContact=$('finalContact'),chapterNumber=$('chapterNumber'),chapterLabel=$('chapterLabel');
  const LABELS=['Cephe','Arka Giriş','Eşik','Görüşme','Masa'],SRC='assets/hero-scrub-48.mp4',FPS=48,MAX_RATE=.27,EASE=8.4;
  const bands=[...document.querySelectorAll('.band')].map(el=>({el,start:+el.dataset.start,end:+el.dataset.end,op:-1,k:-1}));
  const clamp=(v,a=0,b=1)=>v<a?a:v>b?b:v,smooth=v=>v*v*(3-2*v);

  /* Kaydırma konumu hedefi verir; ekrandaki ilerleme ona kare kare yumuşatılarak yaklaşır.
     Video, metin ve göstergeler aynı yumuşatılmış değerden beslenir. */
  let on=false,started=false,frames=0,lastFrame=0,maxTime=0,top=0,travel=1,target=0,shown=0,raf=0,stamp=0;
  let seeking=false,seekAt=0,seekedAt=0,want=-1,have=-1,sceneP=-1,chapter=-1,footOp=-1;

  function measure(){top=hero.offsetTop;travel=Math.max(1,hero.offsetHeight-innerHeight)}
  const scrollProgress=()=>clamp((scrollY-top)/travel);

  /* Bir kare ekrana gerçekten çizilmeden sıradaki kare istenmez (requestVideoFrameCallback);
     böylece hızlı kaydırmada çözülen her kare görünür, boşa giden seek olmaz. */
  const RVFC='requestVideoFrameCallback'in HTMLVideoElement.prototype;
  function seek(frame){
    if(!frames)return;
    if(seeking){want=frame;return}
    if(frame===have)return;
    seeking=true;seekAt=performance.now();seekedAt=0;have=frame;
    if(RVFC)video.requestVideoFrameCallback(painted);
    try{video.currentTime=Math.min((frame+.5)/FPS,maxTime)}catch(e){seeking=false;have=-1}
  }
  function painted(){if(!seeking)return;seeking=false;if(want>=0){const f=want;want=-1;seek(f)}}
  function onSeeked(){if(RVFC)seekedAt=performance.now();else painted()}
  function setFade(el,op,shift){el.style.opacity=op.toFixed(3);el.style.transform='translate3d(0,'+shift.toFixed(2)+'px,0)';el.style.visibility=op<.004?'hidden':'visible'}
  function render(p){
    if(Math.abs(p-sceneP)<.0002)return;sceneP=p;
    rail.style.transform='scaleY('+p.toFixed(4)+')';
    for(const b of bands){
      const ramp=Math.min(.02,(b.end-b.start)/3),op=Math.min(b.start===0?1:smooth(clamp((p-b.start)/ramp)),smooth(clamp((b.end-p)/ramp))),k=smooth(clamp((p-b.start)/Math.max(ramp*1.35,.024)));
      if(Math.abs(op-b.op)>.004||Math.abs(k-b.k)>.004||(op===0&&b.op!==0)||(op===1&&b.op!==1)){b.op=op;b.k=k;setFade(b.el,op,(1-k)*26)}
    }
    const f=smooth(clamp((p-.94)/.045));
    if(Math.abs(f-footOp)>.004||(f===0&&footOp!==0)||(f===1&&footOp!==1)){
      footOp=f;hud.style.opacity=(1-f).toFixed(3);setFade(endFooter,f,(1-f)*18);setFade(finalContact,f,(1-f)*22);
      const active=f>.82;endFooter.classList.toggle('visible',active);document.body.classList.toggle('footer-active',active);
    }
    stage.classList.toggle('scrolled',p>.012);
    const c=Math.min(LABELS.length-1,Math.floor(p*LABELS.length));
    if(c!==chapter){chapter=c;chapterNumber.textContent=String(c+1).padStart(2,'0');chapterLabel.textContent=LABELS[c]}
  }

  function tick(now){
    raf=0;if(!on)return;
    const dt=clamp((now-(stamp||now))/1000,.001,.05);stamp=now;
    const delta=target-shown,settle=delta>0?1-.28*smooth(clamp((shown-.88)/.12)):1,max=dt*MAX_RATE*settle;
    shown+=clamp(delta*(1-Math.exp(-dt*EASE)),-max,max);
    if(Math.abs(target-shown)<.00008)shown=target;
    if(seeking&&((seekedAt&&now-seekedAt>70)||now-seekAt>600))painted();
    render(shown);seek(Math.round(shown*lastFrame*FPS));
    if(shown!==target||seeking||want>=0)raf=requestAnimationFrame(tick);else stamp=0;
  }
  const kick=()=>{if(!raf&&on)raf=requestAnimationFrame(tick)};
  function onScroll(){target=scrollProgress();kick()}
  function onResize(){measure();onScroll()}

  async function loadVideo(){
    if(video.src)return;
    const conn=navigator.connection;if(conn&&conn.saveData){loadLine.remove();return}
    video.preload='auto';
    try{
      const res=await fetch(SRC);if(!res.ok||!res.body)throw 0;
      const total=+res.headers.get('content-length')||0,reader=res.body.getReader(),chunks=[];let got=0;
      for(;;){const {done,value}=await reader.read();if(done)break;chunks.push(value);got+=value.length;if(total)loadLine.style.transform='scaleX('+Math.min(1,got/total).toFixed(3)+')'}
      video.src=URL.createObjectURL(new Blob(chunks,{type:'video/mp4'}));
    }catch(e){video.src=SRC}
    video.load();
  }
  function start(){
    if(started)return;started=true;
    stage.style.backgroundImage="url('assets/hero-poster.webp')";
    const go=()=>{if(on)loadVideo()};
    if('requestIdleCallback'in window)requestIdleCallback(go,{timeout:900});else setTimeout(go,200);
  }
  function enable(){
    if(on)return;on=true;sceneP=footOp=-1;chapter=-1;bands.forEach(b=>{b.op=b.k=-1});
    measure();start();if(started&&!video.src)loadVideo();
    addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onResize,{passive:true});
    target=shown=scrollProgress();render(shown);kick();
  }
  function disable(){
    if(!on)return;on=false;removeEventListener('scroll',onScroll);removeEventListener('resize',onResize);
    if(raf)cancelAnimationFrame(raf);raf=0;stamp=0;
  }
  const apply=()=>gated()?disable():enable();

  video.addEventListener('loadedmetadata',()=>{
    const d=video.duration||0;frames=Math.round(d*FPS);have=-1;maxTime=Math.max(0,d-.004);
    lastFrame=Math.max(0,frames-1)/FPS;target=scrollProgress();if(Math.abs(target-shown)>.2)shown=target;
    seek(Math.round(shown*lastFrame*FPS));
  });
  video.addEventListener('seeked',onSeeked);
  video.addEventListener('canplay',()=>{video.classList.add('ready');stage.classList.add('video-ready');onScroll()},{once:true});
  video.addEventListener('error',()=>{seeking=false;want=-1;frames=0;video.classList.add('failed');stage.classList.add('video-ready')});
  MQLS.forEach(m=>m.addEventListener('change',apply));
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{if(on)onResize()});

  /* açılış ekranı */
  const intro=$('brandIntro'),preview=new URLSearchParams(location.search).has('intro');let seen=false;
  try{seen=sessionStorage.getItem('kozanoglu-intro-seen')==='1'}catch(e){}
  const skip=!preview&&(seen||window.__kozaNavType==='reload'||window.__kozaNavType==='back_forward'||root.classList.contains('page-arriving'));
  if(intro&&!skip&&!gated()){
    root.classList.add('intro-active');
    if(!preview)try{sessionStorage.setItem('kozanoglu-intro-seen','1')}catch(e){}
    setTimeout(()=>{root.classList.add('intro-out');root.classList.remove('intro-active')},880);setTimeout(()=>intro.remove(),1650);
  }else if(intro)intro.remove();

  apply();

  /* mobil: alt bilgi görünürken menüyü, ilk ekranda arama düğmesini gizle */
  if('IntersectionObserver'in window){
    const body=document.body;let heroIn=true,footIn=false;const sync=()=>body.classList.toggle('fab-on',!heroIn&&!footIn);
    new IntersectionObserver(([e])=>{footIn=e.isIntersecting;body.classList.toggle('mobile-footer-view',footIn);sync()},{threshold:.08}).observe($('mobileFooter'));
    new IntersectionObserver(([e])=>{heroIn=e.isIntersecting;sync()},{threshold:.2}).observe($('staticHero'));
  }
})();
