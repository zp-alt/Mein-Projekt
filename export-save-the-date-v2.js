const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1350 },
    deviceScaleFactor: 2
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'save-the-date-v2.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);
  const el = await page.$('.wrap');
  const box = await el.boundingBox();
  await page.screenshot({ path: path.resolve(__dirname, 'save-the-date-v2.png'), clip: box });
  console.log('Saved save-the-date-v2.png');
  await browser.close();
})();
