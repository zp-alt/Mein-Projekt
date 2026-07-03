const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1400, height: 1400 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-hot.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1000);

  const slides = ['c1','c2','c3','c4','c5','c6','c7'];
  for (const sel of slides) {
    const el = await page.$('.' + sel);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `carousel-hot-${sel}.png`),
      clip: box
    });
    console.log('Saved carousel-hot-' + sel + '.png');
  }
  await browser.close();
})();
