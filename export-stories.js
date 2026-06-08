const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const filePath = 'file://' + path.resolve(__dirname, 'weekly-stories.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });

  // Wait for Google Fonts to load (fallback after 3s)
  await page.waitForTimeout(3000);

  const stories = await page.locator('.story').all();
  console.log(`Found ${stories.length} stories`);

  const labels = [
    '01-opener',
    '02-unterricht',
    '03-termin',
    '04-produkt',
    '05-tipp',
  ];

  for (let i = 0; i < stories.length; i++) {
    const outFile = path.resolve(__dirname, `story-${labels[i]}.png`);
    await stories[i].screenshot({ path: outFile });
    console.log(`Saved: story-${labels[i]}.png`);
  }

  await browser.close();
  console.log('Done.');
})();
