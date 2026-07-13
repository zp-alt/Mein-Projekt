const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1536, height: 2260 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'look52-logo.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1000);

  const el = await page.$('.wrap');
  const box = await el.boundingBox();
  await page.screenshot({
    path: path.resolve(__dirname, 'look52-with-logo.png'),
    clip: box
  });
  console.log('Saved look52-with-logo.png');
  await browser.close();
})();
