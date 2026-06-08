const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true, ignoreHTTPSErrors: true });
  const context = await browser.newContext({ ignoreHTTPSErrors: true,
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 900 },
  });
  const page = await context.newPage();

  const urls = [
    'https://us.davines.com/products/this-is-a-medium-hold-modeling-gel',
    'https://www.sephora.com/product/davines-this-is-medium-hold-modeling-gel-P512800',
    'https://genejuarez.com/products/davines-this-is-a-medium-hold-modeling-gel',
  ];

  for (const url of urls) {
    try {
      console.log('Trying:', url);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await page.waitForTimeout(2000);

      // Try to find the main product image
      const imgSrc = await page.evaluate(() => {
        const selectors = [
          'img[data-testid*="product"]',
          '.product-image img',
          '.product__image img',
          '.product-single__photo img',
          'img[alt*="davines"]',
          'img[alt*="Davines"]',
          'img[alt*="Medium Hold"]',
          'img[alt*="medium hold"]',
          '.product-media img',
          'picture img',
        ];
        for (const sel of selectors) {
          const el = document.querySelector(sel);
          if (el && el.src) return el.src;
        }
        // Fallback: biggest image on page
        const imgs = Array.from(document.images);
        imgs.sort((a, b) => (b.naturalWidth * b.naturalHeight) - (a.naturalWidth * a.naturalHeight));
        return imgs[0]?.src || null;
      });

      if (imgSrc) {
        console.log('Found image:', imgSrc);
        // Download the image
        const imgResponse = await page.request.get(imgSrc);
        const buffer = await imgResponse.body();
        const ext = imgSrc.includes('.png') ? 'png' : 'jpg';
        const outPath = path.resolve(__dirname, `davines-product.${ext}`);
        require('fs').writeFileSync(outPath, buffer);
        console.log('Saved:', outPath);
        break;
      } else {
        // Take full page screenshot as fallback
        await page.screenshot({ path: path.resolve(__dirname, 'davines-page.png'), fullPage: false });
        console.log('Took page screenshot as fallback');
        break;
      }
    } catch (e) {
      console.log('Failed:', e.message);
    }
  }

  await browser.close();
})();
