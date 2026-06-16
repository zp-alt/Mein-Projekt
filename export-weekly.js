const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1400, height: 1400 },
    deviceScaleFactor: 4
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'weekly-stories.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1000);

  const nums = ['s1','s2','s3','s5','s4'];
  for (const sel of nums) {
    const el = await page.$('.' + sel);
    const box = await el.boundingBox();
    await page.screenshot({
      path: path.resolve(__dirname, `weekly-${sel}.png`),
      clip: box
    });
    console.log('Saved weekly-' + sel + '.png');
  }
  await browser.close();
})();
