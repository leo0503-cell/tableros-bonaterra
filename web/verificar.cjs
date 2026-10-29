const {chromium}=require('playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 for(const width of [390,1440]){
  const page=await browser.newPage({viewport:{width,height:900},reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto('http://127.0.0.1:8913',{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
  assert.equal(await page.locator('.filtros button').count(),4);
  await page.screenshot({path:`qa-hero-${width}.png`});
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert.equal(overflow,false);
  await page.getByRole('button',{name:'Construcción',exact:true}).click();assert.equal(await page.locator('.linea:visible').count(),2);
  await page.getByRole('button',{name:'Todos',exact:true}).click();assert.equal(await page.locator('.linea:visible').count(),9);
  await page.locator('.toma').first().click();assert.equal(await page.locator('dialog').evaluate(d=>d.open),true);
  await page.locator('dialog .accion').click();assert.equal(await page.locator('#f-material').inputValue(),'MDF Melamina');assert.match(await page.locator('#f-detalle').inputValue(),/Gris Chrome/);
  await page.evaluate(()=>{window.open=(url)=>{window.testURL=url}});await page.locator('.enviar').click();assert.match(await page.evaluate(()=>window.testURL),/^https:\/\/wa.me\/524492050503/);
  await page.locator('#inspiracion').scrollIntoViewIfNeeded();await page.screenshot({path:`qa-inspiracion-${width}.png`});
  assert.equal(await page.locator('.toma img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).length),0);
  if(width<600){await page.locator('.menu-toggle').click();assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false')}
  const pdf=await page.request.get('http://127.0.0.1:8913/catalogo-bonaterra.pdf');assert.equal(pdf.ok(),true);
  assert.deepEqual(errors,[]);console.log(JSON.stringify({width,images:'loaded',filters:'pass',gallery:'pass',quote:'pass',overflow,errors}));await page.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
