# render-diagrams

Re-renders the Mermaid topology in each project README to the PNG copy under that project's `docs/diagrams/`. The README is the source of truth; the PNGs are for viewing outside GitHub.

```sh
cd tools/render-diagrams
npm install
npx playwright install chromium   # skip if CHROME_PATH points at an existing Chromium
npm run render
```

`diagrams.json` maps each README to its PNG. Mermaid is pinned to **11.12.0**. Version 11.4.x draws arrowheads on open links (`A --- B`), so undirected links come out looking one-way. The script prints an arrowhead count for each diagram, and every link in these topologies is undirected, so the count should be zero.
