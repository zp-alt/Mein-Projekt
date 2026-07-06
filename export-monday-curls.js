const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1200, height: 500 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-monday-curls.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  const slides = ['s1', 's2'];
  for (const sel of slides) {
    const el = await page.$('.' + sel);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `monday-curls-${sel}.png`),
      clip: box
    });
    console.log('Saved monday-curls-' + sel + '.png');
  }
  await browser.close();
})();
