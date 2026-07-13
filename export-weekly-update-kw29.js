const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 2400, height: 500 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-weekly-update-kw29.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  const slides = ['s1','s2','s3','s4','s5','s6'];
  for (let i = 0; i < slides.length; i++) {
    const el = await page.$(`.slide:nth-child(${i + 1})`);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `kw29-slide-${i+1}.png`),
      clip: box
    });
    console.log(`Saved kw29-slide-${i+1}.png`);
  }
  await browser.close();
})();
