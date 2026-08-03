const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1200, height: 500 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-weekly-update-kw32.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  for (let i = 1; i <= 3; i++) {
    const el = await page.$(`.slide:nth-child(${i})`);
    const box = await el.boundingBox();
    await page.screenshot({ path: path.resolve(__dirname, `kw32-slide-${i}.png`), clip: box });
    console.log(`Saved kw32-slide-${i}.png`);
  }
  await browser.close();
})();
