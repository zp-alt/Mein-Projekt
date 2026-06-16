const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1400, height: 1400, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(__dirname, 'weekly-stories.html'));
  await page.waitForTimeout(800);

  const nums = ['s1','s2','s3','s4'];
  for (const sel of nums) {
    const el = await page.$('.' + sel);
    await el.screenshot({ path: path.resolve(__dirname, `weekly-${sel}.png`) });
    console.log('Saved weekly-' + sel + '.png');
  }
  await browser.close();
})();
