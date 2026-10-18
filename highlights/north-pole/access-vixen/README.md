# Zone 1 — Team Vixen · `10.10.10.0/24` · OSPF area 10

Two Catalyst access switches bundled with PAgP, dual-homed to DSW-1/DSW-2, plus a Meraki switch for the servers. Gateways (HSRP) and DHCP live on the distribution pair.

```mermaid
flowchart TB
    D1(["DSW-1<br/>HSRP active 10/20"])
    D2(["DSW-2<br/>HSRP active 30/40"])
    S1["S1<br/>mgmt 202.10.0.242/28<br/>AAA → RADIUS"]
    S2["S2"]
    MK["Meraki (SW3)"]
    D1 ---|"Fa1/0/35 · trunk native 100"| S1
    D1 ---|"Fa1/0/36"| S2
    D2 ---|"Gi1/0/35-36"| S1 & S2
    S1 ===|"Po1 · Gi1/0/13-16 · PAgP desirable"| S2
    S1 & S2 ---|"Gi1/0/11 trunk (per drawing)"| MK
    S1 --- RAD["Gi1/0/1 · VLAN 20<br/>RADIUS 10.10.10.246"]
    S1 --- EM["Gi1/0/2 · VLAN 10 (Email)"]
    MK --- SN["SNMP 10.10.10.238<br/>Proxmox 10.10.10.230"]
```

| VLAN | Name | Subnet | Gateway (VIP) |
|---|---|---|---|
| 10 | Email | `10.10.10.248/29` | `.250` |
| 20 | RADIUS | `10.10.10.240/29` | `.242` |
| 30 | SNMP | `10.10.10.232/29` | `.234` |
| 40 | Proxmox | `10.10.10.224/29` | `.226` |
| 100 | Native | | |
| 999 | Unused (shut, port-security max 4) | | |

- **AAA**: S1 authenticates logins against the RADIUS server `CCNAS` at `10.10.10.246` (ports 1645/1646).
- **STP**: both switches set priority 24576 for VLANs 10/20 and 28672 for 30/40 (see known issue A1).
- Final night: the Meraki came online briefly, then the zone lost its uplink and it wasn't recovered in time.

Configs: [s1.txt](configs/s1.txt) · [s2.txt](configs/s2.txt). The link mapping is from the DSW port descriptions and the team drawing ([vixen-access.pdf](../docs/original-diagrams/vixen-access.pdf)).
