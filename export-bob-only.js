const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({ deviceScaleFactor: 3, viewport: { width: 2400, height: 2400 } });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, 'carousel-achromatisch.html'), { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);

  const slides = await page.locator('.slide').all();
  // Only re-export slide 4 (index 3)
  await slides[3].screenshot({ path: path.resolve(__dirname, 'achromatisch-4-bob.png') });
  console.log('Saved: achromatisch-4-bob.png');

  await browser.close();
})();
