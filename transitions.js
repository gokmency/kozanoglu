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
})();
