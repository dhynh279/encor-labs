from topo import Diagram
OUT = 'highlights/north-pole/docs/diagrams/access-dasher'
def build():
    d = Diagram(1100, 750)
    d.node('d7', 300, 55, 240, 56, 'DSW-7', ['HSRP active VLAN 90, 100'], 'external')
    d.node('d8', 800, 55, 240, 56, 'DSW-8', ['HSRP active VLAN 110, 120'], 'external')
    d.area(40, 130, 1020, 540, 'Zone 3 · Dasher · 10.10.30.0/24 · HSRPv1 on DSW-7/8', bottom=True)
    d.node('sw1', 300, 290, 220, 50, 'SW1', [], 'switch')
    d.node('sw2', 800, 290, 220, 50, 'SW2', [], 'switch')
    for a in ('d7', 'd8'):
        for b in ('sw1', 'sw2'):
            d.link(a, b, 'ethernet')
    d.note(550, 700, 'DSW Gi1/0/23-24 → SW Gi1/0/13-14 · trunk 90, 100, 110, 120 · native 200', 's')
    d.link('sw1', 'sw2', 'etherchannel', None, None, 'Po1 · Gi1/0/21-24 · LACP active/passive')
    d.node('mk', 800, 480, 280, 64, 'Meraki SW3 · servers', ['Email .254 · RADIUS .246', 'SNMP .238 · Proxmox .230'], 'meraki')
    d.link('sw1', 'mk', 'ethernet', 'Gi1/0/17')
    d.link('sw2', 'mk', 'ethernet', 'Gi1/0/17')
    d.node('pc', 200, 480, 220, 64, 'Access ports', ['Gi1/0/2 · VLAN 110', 'Gi1/0/4 · VLAN 90'], 'lan')
    d.link('sw1', 'pc', 'ethernet')
    d.note(550, 724, 'VLAN 90 Email · 100 RADIUS · 110 SNMP · 120 Proxmox (/29s) · 200 native · 500 void · port-security on access ports', 's')
    d.legend(560, 570, [('meraki', 'Meraki MS (cloud-managed)')])
    return d
