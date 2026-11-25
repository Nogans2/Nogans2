const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2]);await p.addStyleTag({content:'html{zoom:3.7795}@page{margin:0}'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
await p.pdf({path:process.argv[3],width:'800mm',height:'1600mm',printBackground:true,margin:{top:0,bottom:0,left:0,right:0}});await b.close()})()
