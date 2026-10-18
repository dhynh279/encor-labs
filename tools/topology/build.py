"""Build every topology: python3 build.py [name-filter]

Each specs/*.py defines OUT (repo-relative path without extension) and build() -> Diagram.
Writes <OUT>.svg and, if Playwright + Chromium are available, <OUT>.png.
"""
import importlib.util, os, sys, glob, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
flt = sys.argv[1] if len(sys.argv) > 1 else ''
jobs = []
for f in sorted(glob.glob(os.path.join(HERE, 'specs', '*.py'))):
    if flt not in os.path.basename(f): continue
    spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    d = m.build(); out = os.path.join(REPO, m.OUT)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    d.save(out + '.svg'); jobs.append([out + '.svg', out + '.png', d.w, d.h])
    print('svg ', m.OUT + '.svg')
png = os.path.join(HERE, 'png.js')
if jobs and os.path.isdir(os.path.join(HERE, 'node_modules', 'playwright')):
    subprocess.run(['node', png, json.dumps(jobs)], check=True)
else:
    print('(skipping PNGs: run `npm install` in tools/topology for Playwright)')
