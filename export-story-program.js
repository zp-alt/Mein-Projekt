const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 540, height: 960 });
  await page.goto('file://' + path.resolve('story-program.html'));
  await page.waitForTimeout(1500);

  const clip = { x: 0, y: 0, width: 540, height: 960 };
  await page.screenshot({
    path: 'story-program.png',
    clip,
    deviceScaleFactor: 2
  });

  await browser.close();
  console.log('Saved story-program.png');
})();
