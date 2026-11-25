const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:1600},deviceScaleFactor:2});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.screenshot({path:process.argv[3]});
const o=await p.evaluate(()=>[...document.querySelectorAll('.page *')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!='visible').length);
const last=await p.evaluate(()=>document.querySelector('#cmbs').getBoundingClientRect().bottom);console.log('cmbs bottom',last);await b.close()})()
