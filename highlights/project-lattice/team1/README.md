# Team 1 — OSPF Area Types & Virtual Links · `20.0.0.0/16`

One OSPF domain built to show each kind of area, with two different edge protocols to the hub. Each router uses its own OSPF process number (1–7). Process IDs are local, so they still form one domain.

## Topology (from final configs)

```mermaid
flowchart TB
    HUBR(["Hub P1 · RIP<br/>8.8.9.101"])
    HUBE(["Hub P1 · EIGRP 1<br/>8.8.9.105"])
    subgraph A0["Area 0 · switch segment 20.0.255.224/28"]
        R1["R1 .225<br/>RID 4.4.4.4"]
        R2["R2 .226<br/>RID 5.5.5.5"]
        R3["R3 .227<br/>RID 3.3.3.3"]
        R4["R4 .228<br/>RID 2.2.2.2"]
        R5["R5 .229<br/>RID 1.1.1.1"]
    end
    A3["Area 3 · regular<br/>20.0.0.0/24"]
    A4["Area 4 · stub<br/>20.0.1.0/24"]
    A5["Area 5 · totally stubby<br/>20.0.2.0/24"]
    RA["RA · RID 6.6.6.6<br/>area 1 · RIP ⇄ OSPF"]
    NS["NS · RID 7.7.7.7<br/>area 2 + area 7"]
    ER["EdgeR · RIP"]
    EE["EdgeE · RID 9.9.9.9<br/>EIGRP 1 ⇄ OSPF"]
    ASA{{"ASA (not passing traffic)"}}

    R3 --- A3
    R4 --- A4
    R5 --- A5
    R1 ---|"area 1 · .248/30<br/>virtual-link to RA"| RA
    RA ---|".252/30 · RIP"| ER
    ER ---|"8.8.9.100/30"| HUBR
    R2 ---|"area 2 · .240/30<br/>virtual-link to NS"| NS
    NS ---|"area 7 · .244/30"| EE
    EE ---|"8.8.9.104/30"| HUBE
    R2 -.-|"LinkToFirewall"| ASA
```

## Areas

| Area | Type | Where | Notes |
|---|---|---|---|
| 0 | Backbone | Switch segment `20.0.255.224/28`, R1–R5 | |
| 1 | Regular | R1 ↔ RA | Virtual link R1 ↔ RA |
| 2 | Regular (designed as NSSA) | R2 ↔ NS | Virtual link R2 ↔ NS, which attaches area 7. A virtual link can't cross an NSSA, which is likely why the NSSA was dropped. |
| 3 | Regular | R3 LAN `20.0.0.0/24` | |
| 4 | Stub | R4 loopback `20.0.1.0/24` | |
| 5 | Totally stubby | R5 loopback `20.0.2.0/24` | `area 5 stub no-summary` |
| 7 | Regular | NS ↔ EdgeE | Not connected to area 0, hence the virtual link through area 2 |

## Devices

[r1](configs/r1.txt) · [r2](configs/r2.txt) · [r3](configs/r3.txt) · [r4](configs/r4.txt) · [r5](configs/r5.txt) · [ra](configs/ra.txt) · [ns](configs/ns.txt) · [edge-r](configs/edge-r.txt) · [edge-e](configs/edge-e.txt) · [asa](configs/asa.txt)

The ASA never passed traffic. Over several sessions the team tried routed and transparent mode and adding it to OSPF, and concluded the unit itself (license or firmware) was the problem.
