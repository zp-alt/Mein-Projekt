const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1080, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'look51-logo.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1000);

  const el = await page.$('.wrap');
  const box = await el.boundingBox();
  await page.screenshot({
    path: path.resolve(__dirname, 'look51-with-logo.png'),
    clip: box
  });
  console.log('Saved look51-with-logo.png');
  await browser.close();
})();
