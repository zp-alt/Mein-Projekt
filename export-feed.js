const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    deviceScaleFactor: 3,
    viewport: { width: 2400, height: 2400 },
  });
  const page = await context.newPage();

  const filePath = 'file://' + path.resolve(__dirname, 'feed-posts.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.waitForTimeout(4000);

  const posts = await page.locator('.post').all();
  console.log(`Found ${posts.length} posts`);

  const labels = ['01-bowl-cut', '02-textur', '03-chess', '04-praezision', '05-hands', '06-afro'];

  for (let i = 0; i < posts.length; i++) {
    const outFile = path.resolve(__dirname, `feed-${labels[i]}.png`);
    await posts[i].screenshot({ path: outFile });
    console.log(`Saved: feed-${labels[i]}.png`);
  }

  await browser.close();
  console.log('Done.');
})();
