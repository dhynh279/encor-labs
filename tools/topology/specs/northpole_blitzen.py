from topo import Diagram
OUT = 'highlights/north-pole/docs/diagrams/access-blitzen'
def build():
    d = Diagram(1300, 790)
    d.node('d5', 400, 55, 260, 56, 'DSW-5', ['HSRP active · VLAN 10 VIP .129'], 'external')
    d.node('d6', 900, 55, 260, 56, 'DSW-6', ['HSRP standby'], 'external')
    d.area(40, 140, 1220, 560, 'Zone 2 · Blitzen · 10.10.20.0/24 · mgmt VLAN 67 (S1–S8 at .1–.8)', bottom=True)
    d.node('s1', 160, 280, 160, 46, 'S1 · .1', [], 'switch')
    d.node('s2', 540, 280, 160, 46, 'S2 · .2', [], 'switch')
    d.node('s5', 800, 280, 160, 46, 'S5 · .5', [], 'switch')
    d.node('s6', 1120, 280, 160, 46, 'S6 · Meraki', [], 'meraki')
    d.node('s3', 160, 460, 160, 46, 'S3 · .3', [], 'switch')
    d.node('s4', 540, 460, 160, 46, 'S4 · .4', [], 'switch')
    d.node('s7', 800, 460, 160, 46, 'S7 · .7', [], 'switch')
    d.node('s8', 1120, 460, 160, 46, 'S8 · .8', [], 'switch')
    for a in ('d5', 'd6'):
        for b in ('s1', 's2', 's5', 's6'):
            d.link(a, b, 'ethernet')
    d.link('s1', 's2', 'etherchannel', None, None, 'Po1 · Gi1/0/1-2 · LACP')
    d.link('s1', 's3', 'ethernet', 'Gi1/0/3')
    d.link('s2', 's4', 'ethernet', 'Gi1/0/3')
    d.link('s3', 's4', 'ethernet', None, None, 'Gi1/0/4', mid_cls='ip')
    d.link('s5', 's6', 'etherchannel', None, None, 'Po · Gi1/0/1-2')
    d.link('s5', 's7', 'etherchannel', None, None, 'Po3 · Gi1/0/3-4')
    d.link('s6', 's8', 'etherchannel', None, None, 'Po3 · Gi1/0/3-4')
    d.node('srv1', 160, 620, 240, 56, 'DNS / Email servers', ['VLAN 10 · 10.10.20.128/25'], 'lan')
    d.node('srv2', 1120, 620, 240, 56, 'Proxmox', ['VLAN 10 · .130'], 'lan')
    d.link('s3', 'srv1', 'ethernet')
    d.link('s8', 'srv2', 'ethernet', 'Gi1/0/24')
    d.note(650, 745, 'DSW-5/6 Gi1/0/23–24 trunk VLAN 1, 10, 67 down to S1/S2, plus trunks to S5/S6 · STP root VLAN 10 on DSW-5', 's')
    d.note(650, 768, 'no S6 config: the Meraki sat in that position · S2 port-channel/member VLAN mismatch (known issue A4)', 's')
    d.legend(470, 590, [('meraki', 'Meraki MS (cloud-managed)')])
    return d
