const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  // deviceScaleFactor: 3 → 360*3=1080px wide, 640*3=1920px tall (Instagram Story)
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: 3,
    viewport: { width: 2400, height: 1800 },
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.resolve(__dirname, 'weekly-stories.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for fonts and images to fully render
  await page.waitForTimeout(4000);

  const stories = await page.locator('.story').all();
  console.log(`Found ${stories.length} stories`);

  const labels = [
    '01-opener',
    '02-hwk-salon',
    '03-termin',
    '04-produkt',
    '05-tipp',
    '06-hwk',
    '07-ciao',
  ];

  for (let i = 0; i < stories.length; i++) {
    const outFile = path.resolve(__dirname, `story-${labels[i]}.png`);
    await stories[i].screenshot({ path: outFile });
    console.log(`Saved: story-${labels[i]}.png`);
  }

  await browser.close();
  console.log('Done.');
})();
