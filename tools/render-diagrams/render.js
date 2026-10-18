// Renders the first ```mermaid block of each README listed in diagrams.json
// to its PNG. Mermaid is pinned to 11.12.0: 11.4.x draws arrowheads on
// open links (A --- B), which makes undirected links look one-way.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const repo = path.resolve(__dirname, '..', '..');
const map = JSON.parse(fs.readFileSync(path.join(__dirname, 'diagrams.json'), 'utf8'));

(async () => {
  const browser = await chromium.launch(
    process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}
  );
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 1.5 });
  await page.setContent('<html><body style="background:#fff"><div id="c"></div></body></html>');
  await page.addScriptTag({ path: require.resolve('mermaid/dist/mermaid.min.js') });
  await page.evaluate(() => mermaid.initialize({ startOnLoad: false, theme: 'default' }));

  let failed = 0;
  for (const [md, png] of Object.entries(map)) {
    const text = fs.readFileSync(path.join(repo, md), 'utf8');
    const m = text.match(/```mermaid\n([\s\S]*?)```/);
    if (!m) { console.error(`no mermaid block: ${md}`); failed++; continue; }
    const res = await page.evaluate(async (src) => {
      try {
        const { svg } = await mermaid.render('d' + Math.random().toString(36).slice(2), src);
        document.getElementById('c').innerHTML = svg;
        return { ok: true, arrows: (svg.match(/marker-end="url/g) || []).length };
      } catch (e) { return { ok: false, err: e.message }; }
    }, m[1]);
    if (!res.ok) { console.error(`FAIL ${md}: ${res.err}`); failed++; continue; }
    const el = await page.$('#c svg');
    await el.screenshot({ path: path.join(repo, png) });
    console.log(`ok   ${png}${res.arrows ? `  (${res.arrows} arrowheads)` : ''}`);
  }
  await browser.close();
  process.exit(failed ? 1 : 0);
})();
