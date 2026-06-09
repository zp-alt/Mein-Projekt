const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: 3,
    viewport: { width: 2400, height: 2400 },
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.resolve(__dirname, 'concept-cards.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);

  const cards = await page.locator('.card').all();
  console.log(`Found ${cards.length} cards`);

  const labels = [
    'B1-handwerk',
    'B2-gesamtkunstwerk',
    'B3-form-gefuehl',
    'W1-follikel',
    'W2-gedaechtnis',
    'W3-keratinisierung',
    'G1-afro-manifest',
    'G2-klimt',
    'G3-chevelure',
  ];

  for (let i = 0; i < cards.length; i++) {
    const outFile = path.resolve(__dirname, `card-${labels[i]}.png`);
    await cards[i].screenshot({ path: outFile });
    console.log(`Saved: card-${labels[i]}.png`);
  }

  await browser.close();
  console.log('Done.');
})();
