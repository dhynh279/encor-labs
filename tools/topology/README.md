# tools/topology

Draws the topology diagrams for the Meridian, North Pole and Lattice highlights in the same style as the CCNA case study diagram.

- `topo.py`: small SVG library (nodes, dashed area regions, serial / Ethernet / fiber / EtherChannel / tunnel links, interface labels, legend)
- `specs/*.py`: one file per diagram; `OUT` is the output path, `build()` returns the diagram
- `build.py [filter]`: writes each spec's `.svg`, then renders a `.png` beside it with Playwright

```
npm install                      # once, for the PNG step
python3 build.py                 # all diagrams
python3 build.py meridian        # only specs whose name contains "meridian"
```

Set `CHROME_PATH` if Playwright can't find a Chromium build on its own.
