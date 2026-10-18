# Hub — MPLS Provider Core · `8.8.0.0/16`

The hub ties the four team networks together. The first design used four routers (P/PE). When the routers turned out not to have enough ports, it was rebuilt on 10/16 as **four Catalyst L3 switches in a full mesh** running **OSPF 65535 area 0**, with **`mpls ip` (LDP)** on every core link.

## Topology (from final configs, 11/06)

```mermaid
flowchart TB
    P1["P1<br/>Lo1 100.20.30.40<br/>mgmt VLAN1 8.7.0.1/16"]
    P2["P2<br/>Lo1 100.20.30.41<br/>mgmt 8.6.0.1/16"]
    P3["P3<br/>Lo1 100.20.30.42<br/>mgmt 8.5.0.1/24"]
    P4["P4<br/>Lo1 100.20.30.43<br/>mgmt 8.4.0.1/24"]
    P1 ===|"8.8.8.12/30"| P2
    P1 ===|"8.8.8.20/30"| P3
    P1 ===|"8.8.8.16/30"| P4
    P2 ===|"8.8.8.24/30"| P3
    P2 ===|"8.8.8.28/30"| P4
    P3 ===|"8.8.8.32/30"| P4
    P1 ---|"Gi1/0/13 · 8.8.9.100/30 · RIP"| T1R(["Team 1 EdgeR"])
    P1 ---|"Gi1/0/14 · 8.8.9.104/30 · EIGRP 1"| T1E(["Team 1 EdgeE"])
    P2 ---|"Gi1/0/13 · 8.8.9.108/30 · OSPF area 99"| T2(["Team 2"])
    P4 ---|"Gi1/0/24 · 8.8.9.48/29"| ASA{{"Hub ASA<br/>.50 / .41"}}
    ASA ---|"8.8.9.40/30 · EIGRP 200"| T3(["Team 3 R4"])
```

## Devices

| Device | Role | Config |
|---|---|---|
| P1 | Core; RIP and EIGRP 1 hand-offs to Team 1; mutual redistribution into OSPF; `default-information originate`; DHCP for its management VLAN | [p1.txt](configs/p1.txt) |
| P2 | Core; ABR for area 99 toward Team 2 | [p2.txt](configs/p2.txt) |
| P3 | Core | [p3.txt](configs/p3.txt) |
| P4 | Core; hand-off to the hub ASA (Team 3) | [p4.txt](configs/p4.txt) |
| Hub ASA | OSPF 65535 outside the hub, EIGRP 200 toward Team 3, two-way redistribution, PAT, ICMP permitted globally (10/30 save) | [asa.txt](configs/asa.txt) |

Core links (P1 gig1–3 etc.) and the planned PE addressing are in [hub-ip-table.png](../docs/original-diagrams/hub-ip-table.png). The early PE-router OSPF plan is in [snippets/early-pe-ospf-plan.txt](snippets/early-pe-ospf-plan.txt).
