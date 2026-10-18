from topo import Diagram
OUT = 'highlights/project-lattice/docs/diagrams/team2'
def build():
    d = Diagram(1200, 830)
    d.node('hub', 600, 50, 260, 50, 'Hub', ['P2 Gi1/0/13 · 8.8.9.108/30'], 'external')
    d.area(40, 120, 1120, 630, 'Team 2 · OSPF 50 area 99 · 10.0.0.0/16', bottom=True)
    d.node('asa', 600, 200, 300, 56, 'ASA · PAT', ['Gi1/3 8.8.9.50 · default → 8.8.9.49'], 'firewall')
    d.link('hub', 'asa', 'mismatch')
    d.node('r1', 330, 360, 240, 56, 'R1', ['SD-WAN edge 1'])
    d.node('r2', 870, 360, 280, 56, 'R2', ['SD-WAN edge 2 · default-info originate'])
    d.link('asa', 'r1', 'ethernet', None, None, '10.0.50.244/30')
    d.link('asa', 'r2', 'ethernet', None, None, '10.0.50.240/30')
    d.node('core', 600, 500, 260, 56, 'CSW1_2 core stack', ['SVIs + DHCP'], 'switch')
    d.link('r1', 'core', 'ethernet', None, 'Fa3/0/1', '10.0.50.252/30', mid_t=0.4)
    d.link('r2', 'core', 'ethernet', None, 'Fa4/0/1', '10.0.50.248/30', mid_t=0.4)
    d.node('a1', 280, 660, 230, 56, 'ASW1 · floor 1', ['VLAN 10 · 10.0.0.0/21'], 'switch')
    d.node('a2', 600, 660, 230, 56, 'ASW2 · floor 2', ['VLAN 20 · 10.0.16.0/21'], 'switch')
    d.node('a3', 920, 660, 230, 56, 'ASW3 · floor 3', ['VLAN 30 · 10.0.32.0/21'], 'switch')
    d.link('core', 'a1', 'ethernet', 'Fa4/0/2')
    d.link('core', 'a2', 'ethernet', 'Fa4/0/3')
    d.link('core', 'a3', 'ethernet', 'Fa4/0/4')
    d.note(600, 790, "ASA outside 8.8.9.50 points at P4's segment, not P2's 8.8.9.108/30 (known issue T2-2) · VLAN 40 mgmt, 50 Ansible", 's')
    d.legend(860, 38, [('firewall', 'ASA firewall')])
    return d
