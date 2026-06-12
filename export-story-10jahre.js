const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 360, height: 640, deviceScaleFactor: 4 });

  const file = path.resolve(__dirname, 'story-10jahre.html');
  await page.goto('file://' + file);
  await page.waitForTimeout(1200);

  await page.screenshot({
    path: path.resolve(__dirname, 'story-10jahre.png'),
    omitBackground: true,
    clip: { x: 0, y: 0, width: 360, height: 640 }
  });

  console.log('Done: story-10jahre.png');
  await browser.close();
})();
