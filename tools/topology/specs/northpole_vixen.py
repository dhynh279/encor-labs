from topo import Diagram
OUT = 'highlights/north-pole/docs/diagrams/access-vixen'
def build():
    d = Diagram(1100, 720)
    d.node('d1', 300, 55, 240, 56, 'DSW-1', ['HSRP active VLAN 10, 20'], 'external')
    d.node('d2', 800, 60, 240, 64, 'DSW-2', ['HSRP active VLAN 30, 40', 'Gi1/0/35-36 → S1, S2'], 'external')
    d.area(40, 130, 1020, 520, 'Zone 1 · Vixen · 10.10.10.0/24 · gateways + DHCP on DSW-1/2', bottom=True)
    d.node('s1', 300, 270, 260, 64, 'S1', ['mgmt 202.10.0.242/28', 'AAA → RADIUS'], 'switch')
    d.node('s2', 800, 270, 220, 50, 'S2', [], 'switch')
    d.link('d1', 's1', 'ethernet', 'Fa1/0/35', None, 'trunk · native 100', mid_t=0.6)
    d.link('d1', 's2', 'ethernet', 'Fa1/0/36', None)
    d.link('d2', 's1', 'ethernet')
    d.link('d2', 's2', 'ethernet')
    d.link('s1', 's2', 'etherchannel', None, None, 'Po1 · Gi1/0/13-16 · PAgP desirable')
    d.node('mk', 800, 470, 260, 64, 'Meraki SW3', ['SNMP 10.10.10.238', 'Proxmox 10.10.10.230'], 'meraki')
    d.link('s1', 'mk', 'ethernet', 'Gi1/0/11', None)
    d.link('s2', 'mk', 'ethernet', 'Gi1/0/11', None)
    d.node('rad', 160, 470, 220, 56, 'RADIUS 10.10.10.246', ['VLAN 20'], 'lan')
    d.node('em', 420, 570, 220, 50, 'Email server', ['VLAN 10'], 'lan')
    d.link('s1', 'rad', 'ethernet', 'Gi1/0/1')
    d.link('s1', 'em', 'ethernet', 'Gi1/0/2')
    d.note(550, 680, 'Meraki uplinks Gi1/0/11 are from the team drawing · STP priority 24576 for VLANs 10/20, 28672 for 30/40 · VLANs 99/100/999 void/native/unused', 's')
    d.legend(640, 570, [('meraki', 'Meraki MS (cloud-managed)')])
    return d
