const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

async function exportSlides(htmlFile, prefix, labels) {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: 3,
    viewport: { width: 2400, height: 2400 },
  });
  const page = await context.newPage();
  await page.goto('file://' + path.resolve(__dirname, htmlFile), { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);

  const slides = await page.locator('.slide').all();
  console.log(`[${prefix}] Found ${slides.length} slides`);

  for (let i = 0; i < slides.length; i++) {
    const outFile = path.resolve(__dirname, `${prefix}-${labels[i]}.png`);
    await slides[i].screenshot({ path: outFile });
    console.log(`Saved: ${prefix}-${labels[i]}.png`);
  }

  await browser.close();
}

(async () => {
  await exportSlides('carousel-achromatisch.html', 'achromatisch', [
    '1-opener', '2-undercut', '3-pixie', '4-bob', '5-closer'
  ]);
  await exportSlides('carousel-morphologie.html', 'morphologie', [
    '1-opener', '2-bowl', '3-shag', '4-ondulation', '5-undercut', '6-nackenlinie', '7-closer'
  ]);
  console.log('All done.');
})();
