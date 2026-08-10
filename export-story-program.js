const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 540, height: 960 },
    deviceScaleFactor: 2   // → 1080×1920px output, perfect Story quality
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'story-program.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);
  const el = await page.$('.wrap');
  const box = await el.boundingBox();
  await page.screenshot({ path: path.resolve(__dirname, 'story-program.png'), clip: box });
  console.log('Saved story-program.png — 1080×1920px');
  await browser.close();
})();
