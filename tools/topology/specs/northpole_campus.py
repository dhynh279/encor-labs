from topo import Diagram
OUT = 'highlights/north-pole/docs/diagrams/campus'
def build():
    d = Diagram(1500, 1010)
    d.node('up', 750, 50, 260, 50, 'Campus uplink', ['VLAN 3900 · DHCP'], 'external')
    d.area(60, 105, 1380, 300, 'Core · Rudolph · OSPF 8008 area 0 · 100.10.0.0/24')
    d.node('c1', 550, 190, 240, 56, 'RDLPH-CORE-1', ['Cat 9300L · RID 1.10.1.1'])
    d.node('c2', 950, 190, 240, 56, 'RDLPH-CORE-2', ['Cat 9300L · RID 1.10.1.2'])
    d.node('cl2', 330, 340, 230, 56, 'RDLPH-CL-2', ['Catalyst · RID 1.10.1.4'])
    d.node('mk', 750, 340, 250, 56, 'CL-1 · CL-3 · CL-5', ['Meraki MS · L3 + trunk'], 'meraki')
    d.node('cl4', 1170, 340, 230, 56, 'RDLPH-CL-4', ['Cat 9300L · RID 1.10.1.6'])
    d.link('up', 'c1', 'ethernet', None, 'Gi1/0/11 trunk')
    for c in ('c1', 'c2'):
        d.link(c, 'cl2', 'ethernet')
        d.link(c, 'mk', 'ethernet')
        d.link(c, 'cl4', 'fiber', None, None, 'BFD', mid_t=0.6)

    d.area(60, 420, 440, 500, 'Area 10 · Vixen')
    d.area(530, 420, 440, 500, 'Area 20 · Blitzen')
    d.area(1000, 420, 440, 500, 'Area 30 · Dasher')
    d.node('d1', 220, 540, 160, 50, 'DSW-1', ['RID 10.1.1.1'])
    d.node('d2', 400, 540, 160, 50, 'DSW-2', ['RID 10.1.1.2'])
    d.node('d3', 650, 540, 160, 50, 'DSW-3', ['RID 20.1.1.3'])
    d.node('d4', 850, 540, 160, 50, 'DSW-4', ['RID 20.1.1.4'])
    d.node('d5', 650, 700, 160, 50, 'DSW-5', ['RID 20.1.1.5'])
    d.node('d6', 850, 700, 160, 50, 'DSW-6', ['RID 20.1.1.6'])
    d.node('d7', 1135, 540, 160, 50, 'DSW-7', ['RID 30.1.1.7'])
    d.node('d8', 1325, 540, 160, 50, 'DSW-8', ['RID 30.1.1.8'])
    for x in ('d1', 'd2', 'd3', 'd4'):
        d.link('cl2', x, 'ethernet')
    for x in ('d3', 'd4', 'd7', 'd8'):
        d.link('cl4', x, 'ethernet')
    for a in ('d3', 'd4'):
        for b in ('d5', 'd6'):
            d.link(a, b, 'ethernet')
    d.link('d5', 'd6', 'ethernet', None, None, '2 × /30')

    d.node('vix', 280, 850, 340, 76, 'Vixen access', ['S1 · S2 · Meraki SW3', '10.10.10.0/24 · HSRPv2 on DSW-1/2'], 'lan')
    d.node('blz', 750, 850, 340, 76, 'Blitzen access', ['S1 – S8 (S6 Meraki)', '10.10.20.0/24 · HSRPv2 on DSW-5/6'], 'lan')
    d.node('das', 1220, 850, 340, 76, 'Dasher access', ['SW1 · SW2 · Meraki SW3', '10.10.30.0/24 · HSRPv1 on DSW-7/8'], 'lan')
    for a, b in (('d1', 'vix'), ('d2', 'vix'), ('d5', 'blz'), ('d6', 'blz'), ('d7', 'das'), ('d8', 'das')):
        d.link(a, b, 'ethernet')
    d.note(750, 955, 'distribution links 200.10.0.0/24 /30s · the Meraki leafs also uplink DSW-1/2/3/4/7/8 (see the distribution page)', 's')
    d.note(750, 980, 'wireless SVIs and DHCP (VLANs 11–15, 202.10.0.0/22 + 202.10.4.0/24) on DSW-3', 's')
    d.legend(1150, 150, [('meraki', 'Meraki MS (cloud-managed)')])
    return d
