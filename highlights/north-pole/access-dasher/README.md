# Zone 3 — Team Dasher · `10.10.30.0/24` · OSPF area 30

Two Catalyst access switches bundled with LACP, each dual-linked to DSW-7/DSW-8, and both trunked to a Meraki switch that hosts the servers.

```mermaid
flowchart TB
    D7(["DSW-7<br/>HSRP active 90/100"])
    D8(["DSW-8<br/>HSRP active 110/120"])
    SW1["SW1"]
    SW2["SW2"]
    MK["Meraki (SW3)"]
    D7 & D8 ---|"Gi1/0/23-24 → Gi1/0/13-14<br/>trunk 90,100,110,120 · native 200"| SW1 & SW2
    SW1 ===|"Po1 · Gi1/0/21-24 · LACP active/passive"| SW2
    SW1 & SW2 ---|"Gi1/0/17 trunk"| MK
    MK --- SRV["Email .254 · RADIUS .246<br/>SNMP .238 · Proxmox .230"]
    SW1 --- P["Gi1/0/2 · VLAN 110<br/>Gi1/0/4 · VLAN 90"]
```

| VLAN | Name | Subnet | Gateway (VIP) |
|---|---|---|---|
| 90 | Email | `10.10.30.248/29` | `.249` |
| 100 | RADIUS | `10.10.30.240/29` | `.241` |
| 110 | SNMP | `10.10.30.232/29` | `.233` |
| 120 | Proxmox | `10.10.30.224/29` | `.225` |
| 200 | Native | | |
| 500 | Void (unused ports, shut) | | |

- **SNMP**: v2c traps (link, STP, port-security, config, envmon, …) to the SNMP server `10.10.30.238`, with a community restricted by ACL (see known issues A7/A8).
- Scripts the team pasted in: [snippets/vlans.txt](snippets/vlans.txt), [snippets/port-security.txt](snippets/port-security.txt).

Configs: [sw1.txt](configs/sw1.txt) · [sw2.txt](configs/sw2.txt)
