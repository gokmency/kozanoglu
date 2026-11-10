(()=>{"use strict";
  const GATES=['(max-width: 720px)','(orientation: portrait) and (max-width: 1024px)','(orientation: portrait) and (pointer: coarse)','(orientation: landscape) and (pointer: coarse) and (max-height: 560px)','(prefers-reduced-motion: reduce)'];
  const root=document.documentElement,overlay=document.querySelector('.page-transition'),desktop=()=>!GATES.some(query=>matchMedia(query).matches);
  let leaving=false,arrivalTimer=0,cleanupTimer=0;
  function clearTransition(){clearTimeout(arrivalTimer);clearTimeout(cleanupTimer);root.classList.remove('page-arriving','page-reloading','page-leaving','page-transition-ready');leaving=false}
  function revealPage(){if(!overlay||!desktop()){clearTransition();return}if(root.classList.contains('page-reloading'))arrivalTimer=setTimeout(()=>root.classList.add('page-transition-ready'),240);else if(root.classList.contains('page-arriving'))requestAnimationFrame(()=>requestAnimationFrame(()=>root.classList.add('page-transition-ready')));else return;cleanupTimer=setTimeout(clearTransition,760)}
  function eligibleLink(anchor,event){if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||anchor.target==='_blank'||anchor.hasAttribute('download'))return null;let url;try{url=new URL(anchor.href,location.href)}catch(error){return null}if(url.origin!==location.origin||!/^https?:$/.test(url.protocol))return null;if(url.pathname===location.pathname&&url.search===location.search&&url.hash)return null;if(url.href===location.href)return null;return url}
  addEventListener('click',event=>{if(!desktop()||leaving)return;const anchor=event.target.closest('a[href]');if(!anchor)return;const url=eligibleLink(anchor,event);if(!url)return;event.preventDefault();leaving=true;try{sessionStorage.setItem('kozanoglu-page-transition','1')}catch(error){}root.classList.remove('page-transition-ready','page-arriving','page-reloading');root.classList.add('page-leaving');setTimeout(()=>location.assign(url.href),290)});
  addEventListener('pageshow',event=>{if(event.persisted)clearTransition()});
  revealPage();
  /* içerik görünür oldukça yumuşak giriş + mobil arama düğmesi (alt sayfalar) */
  if('IntersectionObserver'in window){
    if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
      const items=document.querySelectorAll('.section-head,.cards>.card,.steps>.step,.topic-grid>li,.area-row,.faq-item,.story-grid>*,.people>.person,.location-block,.post-card,.post-feature,.split-facts>div,.hood-list,.local-grid>*,.cta>*,.contact-layout>*,.tldr,.doc-list>li,.m-chapter,.m-area');
      const vh=innerHeight,io=new IntersectionObserver(entries=>{let n=0;entries.forEach(entry=>{if(!entry.isIntersecting)return;const el=entry.target;io.unobserve(el);el.style.setProperty('--rv-d',Math.min(n++,5)*70+'ms');el.classList.add('in');setTimeout(()=>{el.classList.remove('rv','in');el.style.removeProperty('--rv-d')},1400)})},{rootMargin:'0px 0px -8% 0px'});
      items.forEach(el=>{if(el.getBoundingClientRect().top<vh*.92)return;el.classList.add('rv');io.observe(el)});
    }
    const fab=document.querySelector('.call-fab'),head=document.querySelector('.page-hero,.post-hero'),foot=document.querySelector('.site-footer');
    if(fab&&head){let headIn=true,footIn=false;const sync=()=>document.body.classList.toggle('fab-on',!headIn&&!footIn);new IntersectionObserver(([e])=>{headIn=e.isIntersecting;sync()},{threshold:.15}).observe(head);if(foot)new IntersectionObserver(([e])=>{footIn=e.isIntersecting;sync()},{threshold:.35}).observe(foot)}
  }
})();
