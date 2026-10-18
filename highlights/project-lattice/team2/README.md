# Team 2 — Three-Floor Campus · `10.0.0.0/16`

A campus with a stacked core switch, one access switch per floor (APs, printers, test PCs), two edge routers (an SD-WAN design with "Rogers" and "Verizon" ISP uplinks), and an ASA. Everything runs **OSPF process 50, area 99**. The team also stood up an Ubuntu Ansible server for automation.

## Topology (from final configs, 11/04)

```mermaid
flowchart TB
    HUB(["Hub"])
    ASA{{"ASA · PAT<br/>Gi1/3 8.8.9.50 → default 8.8.9.49"}}
    R1["R1 (SD-WAN edge 1)"]
    R2["R2 (SD-WAN edge 2)<br/>default-information originate"]
    CORE["CSW1_2 · core stack<br/>SVIs + DHCP"]
    A1["ASW1 · floor 1<br/>VLAN 10"]
    A2["ASW2 · floor 2<br/>VLAN 20"]
    A3["ASW3 · floor 3<br/>VLAN 30"]
    HUB --- ASA
    ASA ---|"10.0.50.244/30"| R1
    ASA ---|"10.0.50.240/30"| R2
    R1 ---|"10.0.50.252/30 · Fa3/0/1"| CORE
    R2 ---|"10.0.50.248/30 · Fa4/0/1"| CORE
    CORE ---|"Fa4/0/2"| A1
    CORE ---|"Fa4/0/3"| A2
    CORE ---|"Fa4/0/4"| A3
```

## Addressing

| VLAN | Use | Subnet | Gateway (core SVI) |
|---|---|---|---|
| 10 | Floor 1 — APs, printer, hosts (2000) | `10.0.0.0/21` | `.1` |
| 20 | Floor 2 | `10.0.16.0/21` | `.1` |
| 30 | Floor 3 | `10.0.32.0/21` | `.1` |
| 40 | Test / management /30s | `10.0.48.0/24` | `.1` |
| 50 | Ansible server | `10.0.49.0/24` (VLSM plan: `10.0.50.0/30`) | `.1` |

DHCP pools on the core for VLANs 10–40 (first 20 addresses excluded). Access switches have an SVI at `.5` in their floor's VLAN.

## Devices

[core-sw](configs/core-sw.txt) · [r1](configs/r1.txt) · [r2](configs/r2.txt) · [asw1](configs/asw1.txt) · [asw2](configs/asw2.txt) · [asw3](configs/asw3.txt) · [asa](configs/asa.txt)

The hub side of Team 2's link is P2 Gi1/0/13 (`8.8.9.108/30`, OSPF area 99), but the ASA's final save points at P4 instead (known issue T2-2).

The SD-WAN controllers (vManage/vSmart/vBond) were set up on Team 4's side; there's no SD-WAN overlay config in these saves.
