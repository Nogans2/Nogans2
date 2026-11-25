const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:1600},deviceScaleFactor:2});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:process.argv[3]});
console.log(await p.evaluate(()=>{const r=s=>{const e=document.querySelector(s);return e?Math.round(e.getBoundingClientRect().bottom):null};return {mods:r('#mods'),foot:Math.round(document.querySelector('.foot').getBoundingClientRect().top),hero:document.querySelector('.hero')?Math.round(document.querySelector('.hero').getBoundingClientRect().top):null}}));await b.close()})()
