const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
  for (const [svg, png, w, h] of jobs) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
    await p.setContent('<html><body style="margin:0">' + fs.readFileSync(svg, 'utf8') + '</body></html>');
    await (await p.$('svg')).screenshot({ path: png }); await p.close();
    console.log('png ', png.replace(process.cwd() + '/', ''));
  }
  await b.close();
})();
