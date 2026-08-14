const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 4 });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'story-aug14-urlaub.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);
  const el = await page.$('.wrap');
  const box = await el.boundingBox();
  await page.screenshot({ path: path.resolve(__dirname, 'story-aug14-urlaub.png'), clip: box });
  console.log('Saved story-aug14-urlaub.png — 1080×1920px');
  await browser.close();
})();
