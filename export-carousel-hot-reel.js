const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1600, height: 800 },
    deviceScaleFactor: 3  // 360*3=1080, 640*3=1920
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-hot-reel.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);

  const slides = ['c1','c2','c3','c4','c5','c6','c7'];
  for (const sel of slides) {
    const el = await page.$('.' + sel);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `carousel-hot-reel-${sel}.png`),
      clip: box
    });
    console.log('Saved carousel-hot-reel-' + sel + '.png');
  }
  await browser.close();
})();
