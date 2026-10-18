from topo import Diagram
OUT = 'highlights/project-meridian/docs/diagrams/wan'

def build():
    d = Diagram(1420, 1010)
    d.node('a51', 720, 300, 250, 56, 'AREA 51 R1 / R2', ['2001:db8:cafe:1000::/52'])
    d.node('edge', 720, 520, 250, 80, 'AREA 51 EDGE', ['WAN hub · OSPFv3 area 0', 'Cisco 2901 · RID 19.19.19.19'])
    d.node('nog', 380, 160, 240, 80, 'NOGALES', ['RIPng ⇄ OSPFv3', '2001:db8:cafe:2000::/52'])
    d.node('veg', 1060, 160, 240, 80, 'VEGAS', ['OSPFv3 area 1 (Edge is ABR)', '2001:db8:cafe:3000::/52'])
    d.node('mr1', 380, 760, 220, 64, 'MAINE R1', ['OSPFv3 area 2 (ABR)'])
    d.node('mr2', 380, 920, 220, 64, 'MAINE R2', ['2001:db8:cafe:4000::/52'])
    d.node('br1', 960, 800, 210, 64, 'BANGKOK R1', ['HSRP active'])
    d.node('br2', 1230, 800, 210, 64, 'BANGKOK R2', ['HSRP standby'])
    d.note(1095, 860, 'Bangkok: OSPFv3 (was BGP) · 2001:db8:cafe:5000::/52', 's')
    # serial links to the hub (hub side always ::1)
    d.link('edge', 'a51', 'serial', 'S0/0/0', 'S0/1/1', 'link-local')
    d.link('edge', 'nog', 'serial', 'S0/1/0', 'S0/2/0', '2001:db8:1:1::/64')
    d.link('edge', 'veg', 'serial', 'S0/1/1', 'S0/1/0', '2001:db8:1:5::/64')
    d.link('edge', 'mr1', 'serial', 'S0/0/1', 'S0/1/0', '2001:db8:1:4::/64')
    d.link('edge', 'br1', 'serial', 'S0/2/1', 'S0/1/0', '2001:db8:1:2::/64')
    d.link('edge', 'br2', 'serial', 'S0/2/0', 'S0/1/0', '2001:db8:1:3::/64', mid_t=0.45)
    d.link('mr1', 'mr2', 'serial', None, None, '2001:db8:cafe:4000::/64')
    # overlays
    d.link('veg', 'br2', 'tunnel', None, None, 'GRE · 2001:db8:13:2::/64', curve=-60)
    d.link('veg', 'br1', 'tunnel', None, None, 'GRE · 2001:db8:13:1::/64', curve=-10, mid_t=0.62)
    d.link('nog', 'veg', 'tunnel_down', None, None, 'IPsec')
    d.link('nog', 'br1', 'tunnel_down', None, None, 'IPsec', curve=430, mid_t=0.5)
    d.link('mr2', 'nog', 'tunnel_down', None, None, 'GRE · 2001:db8:12:1::/64', curve=-170, a_off=(-110, 0), b_off=(-120, 0))
    d.note(720, 625, 'every hub link: hub ::1, site ::2', 's')
    d.legend(1000, 930)
    return d
