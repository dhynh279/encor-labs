"""Small SVG topology library in the style of the CCNA case study diagram.

A spec file builds a Diagram, adds areas, nodes and links, and calls save().
Labels at link ends are pushed clear of the boxes automatically.
"""
import math, html

NODE_STYLE = {
    'router':   ('#eef2ff', '#4f46e5'),   # routers / L3 switches
    'switch':   ('#ecfdf5', '#059669'),   # L2 switches
    'lan':      ('#ecfdf5', '#059669'),   # LAN segments, hosts, servers
    'external': ('#f9fafb', '#6b7280'),   # other sites / ISP / out of scope
    'firewall': ('#fff7ed', '#ea580c'),
    'meraki':   ('#ecfeff', '#0891b2'),
}
LINK_STYLE = {
    # kind: (color, width, dash, band, legend text)
    'serial':       ('#dc2626', 2.5, None, False, 'serial link'),
    'ethernet':     ('#111827', 2.0, None, False, 'Ethernet'),
    'fiber':        ('#2563eb', 2.5, None, False, 'fiber (SFP)'),
    'etherchannel': ('#111827', 2.0, None, False, 'EtherChannel (LACP/PAgP bundle)'),
    'tunnel':       ('#7c3aed', 2.0, '7 5', True,  'tunnel up (GRE / IPsec overlay)'),
    'tunnel_down':  ('#d97706', 2.0, '7 5', False, 'tunnel configured, not working at the deadline'),
    'dhcp':         ('#0891b2', 2.0, '4 4', False, 'routed link, address from Meraki DHCP'),
    'mismatch':     ('#9ca3af', 2.0, '3 5', False, "addresses don't match in final saves"),
    'hsrp':         ('#6b7280', 1.5, '2 4', False, 'HSRP group (virtual gateway)'),
}

def esc(s): return html.escape(str(s), quote=False)

class Diagram:
    def __init__(self, w, h, title=None):
        self.w, self.h, self.title = w, h, title
        self.areas, self.nodes, self.links, self.notes = [], {}, [], []
        self.used = []

    def area(self, x, y, w, h, label, fill='#f3f4f6', stroke='#9ca3af', bottom=False):
        self.areas.append((x, y, w, h, label, fill, stroke, bottom))

    def node(self, nid, x, y, w, h, title, lines=(), kind='router'):
        self.nodes[nid] = dict(x=x, y=y, w=w, h=h, title=title, lines=list(lines), kind=kind)

    def link(self, a, b, kind='ethernet', la=None, lb=None, mid=None, mid_off=0,
             curve=0, a_off=(0, 0), b_off=(0, 0), da=10, db=10, mid_t=0.5, mid_cls='lbl'):
        self.links.append(dict(a=a, b=b, kind=kind, la=la, lb=lb, mid=mid, mid_off=mid_off, curve=curve,
                               a_off=a_off, b_off=b_off, da=da, db=db, mid_t=mid_t, mid_cls=mid_cls))
        if kind not in self.used: self.used.append(kind)

    def note(self, x, y, text, cls='lbl', anchor='middle'):
        self.notes.append((x, y, text, cls, anchor))

    # ---------- geometry ----------
    def _inside(self, n, p, pad=2):
        return abs(p[0] - n['x']) <= n['w'] / 2 + pad and abs(p[1] - n['y']) <= n['h'] / 2 + pad

    def _path_pts(self, L):
        A, B = self.nodes[L['a']], self.nodes[L['b']]
        p0 = (A['x'] + L['a_off'][0], A['y'] + L['a_off'][1])
        p2 = (B['x'] + L['b_off'][0], B['y'] + L['b_off'][1])
        mx, my = (p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2
        dx, dy = p2[0] - p0[0], p2[1] - p0[1]
        ln = math.hypot(dx, dy) or 1
        c = (mx - dy / ln * L['curve'], my + dx / ln * L['curve'])
        pts = []
        N = 400
        for i in range(N + 1):
            t = i / N
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t ** 2 * p2[1]
            pts.append((x, y))
        return p0, c, p2, pts

    def _visible(self, L, pts):
        A, B = self.nodes[L['a']], self.nodes[L['b']]
        i0 = next(i for i, p in enumerate(pts) if not self._inside(A, p))
        i1 = max(i for i, p in enumerate(pts) if not self._inside(B, p))
        return pts[i0:i1 + 1]

    @staticmethod
    def _walk(pts, dist):
        acc = 0
        for i in range(1, len(pts)):
            seg = math.dist(pts[i - 1], pts[i]); acc += seg
            if acc >= dist: return pts[i], i
        return pts[-1], len(pts) - 1

    # ---------- drawing ----------
    def _tag(self, o, x, y, text, cls):
        cw = 6.6 if cls == 'ip' else 6.2
        w = len(text) * cw + 10
        o.append(f'<rect x="{x - w / 2:.1f}" y="{y - 9:.1f}" width="{w:.1f}" height="17" rx="3" fill="#ffffff" fill-opacity="0.94"/>')
        o.append(f'<text class="{cls}" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle">{esc(text)}</text>')

    def _end_label(self, o, vis, text, dist, from_end=False):
        if not text: return
        seq = vis[::-1] if from_end else vis
        w = len(text) * 6.6 + 10
        # push the label centre far enough along the link that its box clears the node
        p1, i = self._walk(seq, 5)
        p2, _ = self._walk(seq, 25)
        ux, uy = p2[0] - seq[0][0], p2[1] - seq[0][1]
        ln = math.hypot(ux, uy) or 1
        ux, uy = ux / ln, uy / ln
        need = abs(ux) * (w / 2) + abs(uy) * 9 + dist
        p, _ = self._walk(seq, need)
        self._tag(o, p[0], p[1], text, 'ip')

    def svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
             f'font-family="Segoe UI, Helvetica, Arial, sans-serif">',
             '<rect width="100%" height="100%" fill="#ffffff"/>',
             '<defs><style>.s{font-size:11.5px;fill:#374151}.h{font-size:15px;font-weight:700;fill:#111827}'
             '.a{font-size:15px;font-weight:700;fill:#4b5563}.t{font-size:13px;fill:#1f2937}'
             '.lbl{font-size:11px;fill:#111827}.ip{font-size:11px;fill:#1d4ed8;font-family:Consolas,Menlo,monospace}'
             '.tt{font-size:18px;font-weight:700;fill:#111827}</style></defs>']
        if self.title:
            o.append(f'<text class="tt" x="24" y="34">{esc(self.title)}</text>')
        for (x, y, w, h, label, fill, stroke, bottom) in self.areas:
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="{fill}" stroke="{stroke}" stroke-dasharray="6 5"/>')
            o.append(f'<text class="a" x="{x + 20}" y="{y + h - 16 if bottom else y + 28}">{esc(label)}</text>')
        geo = []
        # bands first, then lines
        for L in self.links:
            p0, c, p2, pts = self._path_pts(L)
            geo.append((L, p0, c, p2, pts))
            color, width, dash, band, _ = LINK_STYLE[L['kind']]
            if band:
                o.append(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{color}" stroke-opacity="0.16" stroke-width="20"/>')
        for (L, p0, c, p2, pts) in geo:
            color, width, dash, band, _ = LINK_STYLE[L['kind']]
            d = f' stroke-dasharray="{dash}"' if dash else ''
            path = f'M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
            if L['kind'] == 'etherchannel':
                dx, dy = p2[0] - p0[0], p2[1] - p0[1]; ln = math.hypot(dx, dy) or 1
                nx, ny = -dy / ln * 3, dx / ln * 3
                for s in (1, -1):
                    o.append(f'<path d="M{p0[0]+nx*s:.1f},{p0[1]+ny*s:.1f} Q{c[0]+nx*s:.1f},{c[1]+ny*s:.1f} {p2[0]+nx*s:.1f},{p2[1]+ny*s:.1f}" fill="none" stroke="{color}" stroke-width="{width}"/>')
            else:
                o.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>')
        # nodes
        for n in self.nodes.values():
            fill, stroke = NODE_STYLE[n['kind']]
            x, y, w, h = n['x'], n['y'], n['w'], n['h']
            o.append(f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            n_lines = 1 + len(n['lines'])
            top = y - (n_lines * 17) / 2 + 12
            o.append(f'<text class="h" x="{x}" y="{top:.1f}" text-anchor="middle">{esc(n["title"])}</text>')
            for i, l in enumerate(n['lines']):
                o.append(f'<text class="s" x="{x}" y="{top + 17 * (i + 1):.1f}" text-anchor="middle">{esc(l)}</text>')
        # labels last so they sit on top
        for (L, p0, c, p2, pts) in geo:
            vis = self._visible(L, pts)
            self._end_label(o, vis, L['la'], L['da'])
            self._end_label(o, vis, L['lb'], L['db'], from_end=True)
            if L['mid']:
                k = int((len(vis) - 1) * L['mid_t'])
                p = vis[k]; q = vis[min(k + 3, len(vis) - 1)]
                dx, dy = q[0] - p[0], q[1] - p[1]; ln = math.hypot(dx, dy) or 1
                mx, my = p[0] - dy / ln * L['mid_off'], p[1] + dx / ln * L['mid_off']
                self._tag(o, mx, my, L['mid'], L['mid_cls'])
        for (x, y, text, cls, anchor) in self.notes:
            o.append(f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(text)}</text>')
        o.append('</svg>')
        return '\n'.join(o)

    def legend(self, x, y, extra=()):
        """Add a legend box for the link kinds used (call after all links)."""
        items = [k for k in LINK_STYLE if k in self.used] + list(extra)
        self._legend = (x, y, items)

    def save(self, path):
        s = self.svg()
        if getattr(self, '_legend', None):
            x, y, items = self._legend
            rows = []
            for i, k in enumerate(items):
                yy = y + 22 * i
                if k in LINK_STYLE:
                    color, width, dash, band, text = LINK_STYLE[k]
                    if band:
                        rows.append(f'<line x1="{x}" y1="{yy}" x2="{x + 40}" y2="{yy}" stroke="{color}" stroke-opacity="0.16" stroke-width="14"/>')
                    if k == 'etherchannel':
                        rows.append(f'<line x1="{x}" y1="{yy - 3}" x2="{x + 40}" y2="{yy - 3}" stroke="{color}" stroke-width="{width}"/>')
                        rows.append(f'<line x1="{x}" y1="{yy + 3}" x2="{x + 40}" y2="{yy + 3}" stroke="{color}" stroke-width="{width}"/>')
                    else:
                        d = f' stroke-dasharray="{dash}"' if dash else ''
                        rows.append(f'<line x1="{x}" y1="{yy}" x2="{x + 40}" y2="{yy}" stroke="{color}" stroke-width="{width}"{d}/>')
                else:
                    fill, stroke = NODE_STYLE[k[0]]
                    rows.append(f'<rect x="{x + 6}" y="{yy - 8}" width="28" height="16" rx="3" fill="{fill}" stroke="{stroke}"/>')
                    text = k[1]
                rows.append(f'<text class="t" x="{x + 50}" y="{yy + 4}">{esc(text)}</text>')
            wbox = max(len(LINK_STYLE[k][4]) if k in LINK_STYLE else len(k[1]) for k in items) * 7.2 + 70
            box = f'<rect x="{x - 12}" y="{y - 20}" width="{wbox:.0f}" height="{22 * len(items) + 18}" rx="6" fill="#ffffff" stroke="#d1d5db"/>'
            s = s.replace('</svg>', box + '\n' + '\n'.join(rows) + '\n</svg>')
        open(path, 'w').write(s)
