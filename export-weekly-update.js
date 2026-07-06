const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1400, height: 500 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-weekly-update.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  const slides = ['s1', 's2', 's3', 's4'];
  for (const sel of slides) {
    const el = await page.$('.' + sel);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `weekly-update-${sel}.png`),
      clip: box
    });
    console.log('Saved weekly-update-' + sel + '.png');
  }
  await browser.close();
})();
