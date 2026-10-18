# Team 4 — Provider-Edge OSPF Network · `192.168.0.0/16`

A small provider-style network: a central **PE-0** with serial links to four PEs, and each PE serving one customer block (two data centers, two sites) in its own OSPF area. It reaches the rest of the WAN through its ASA and Team 3.

## Topology (from the team's scripts)

```mermaid
flowchart TB
    T3(["Team 3 ASA<br/>172.0.0.213"])
    ASA{{"ASA-LOCAL<br/>EIGRP 200 ⇄ OSPF 1"}}
    PE0["PE-0<br/>area 0 hub"]
    PE1["PE-1"]
    PE2["PE-2"]
    PE3["PE-3<br/>default-information originate"]
    PE4["PE-4"]
    DC1["DC-1 L3 · area 1<br/>192.168.64.0/19"]
    DC2["DC-2 L3 · area 2<br/>192.168.96.0/19"]
    S1["Site-1 L3 · area 3<br/>192.168.0.0/19<br/>SD-WAN managers"]
    S2["Site-2 L3 · area 4<br/>192.168.32.0/19"]

    T3 ---|"172.0.0.212/30"| ASA
    ASA ---|"192.168.255.220/30"| PE3
    PE0 ---|".244/30"| PE1
    PE0 ---|".240/30"| PE2
    PE0 ---|".252/30"| PE3
    PE0 ---|".248/30"| PE4
    PE1 ---|".232/30"| DC1
    PE2 ---|".236/30"| DC2
    PE3 ---|".224/30"| S1
    PE4 ---|".228/30"| S2
```

| Block | Use |
|---|---|
| `192.168.0.0/19` | Site 1 (vManage, vSmart, vBond) |
| `192.168.32.0/19` | Site 2 |
| `192.168.64.0/19` | DC-1 |
| `192.168.96.0/19` | DC-2 |
| `192.168.128.0/28` | Management loopbacks (DC-1 `.1` … Site-2 `.9`) |
| `192.168.255.x/30` | PE links |

DHCP for each block runs on its PE, and the L3 switches relay to it (`ip helper-address`).

## Files

These are the **paste-in scripts** the team loaded, not `show run` output, so they show what was intended rather than a saved running state.

[pe-0](configs/pe-0.txt) · [pe-1](configs/pe-1.txt) · [pe-2](configs/pe-2.txt) · [pe-3](configs/pe-3.txt) · [pe-4](configs/pe-4.txt) · [dc-1-l3](configs/dc-1-l3.txt) · [dc-2-l3](configs/dc-2-l3.txt) · [site-1-l3](configs/site-1-l3.txt) · [site-2-l3](configs/site-2-l3.txt) · [dhcp-pools](configs/dhcp-pools.txt) · [asa](configs/asa.txt) (`show run`)
