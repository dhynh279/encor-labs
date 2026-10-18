# Nogales — RIPng Site with HSRP and EtherChannel

Nogales runs **RIPng** internally and redistributes it into the **OSPFv3 area 0** backbone at its edge router. Two routers share an HSRPv2 virtual gateway, and the access layer is a three-switch LACP triangle.

## Topology (from final configs)

```mermaid
flowchart TB
    A51(["Area 51 Edge<br/>2001:db8:1:1::1"])
    R1["R1 · hostname Nogales<br/>ISR 4221<br/>RID 11.11.11.11<br/>RIPng ⇄ OSPFv3 10"]
    R2["R2<br/>HSRP standby<br/>…:2002::3"]
    R3["R3<br/>HSRP active · pri 150<br/>…:2002::2"]
    VIP{{"HSRPv2 group 1<br/>VIP …:2002::1"}}
    CORE["Core_SW"]
    R4["R4<br/>router-on-a-stick<br/>…:2002::4"]
    S1["S1"]
    S2["S2"]
    S3["S3"]

    A51 ===|"S0/2/0 · 2001:db8:1:1::2/64 · OSPF area 0"| R1
    R1 ---|"S0/1/0 · …:2001::/64"| R2
    R1 ---|"S0/1/1 · …:2000::/64"| R3
    R2 -->|"Gi0/0/0"| CORE
    R3 -->|"Gi0/0/0"| CORE
    R2 -.- VIP -.- R3
    CORE ---|"Gi0/0/1"| R4
    R4 ---|"Gi0/0/0 trunk · .20 .30 .40"| S1
    S1 ===|"Po1 · Gi1/0/23-24 · LACP"| S2
    S2 ===|"Po2 · Gi1/0/15-16 · LACP"| S3
    S3 ===|"Po1 ↔ S1 Po2 · Gi1/0/19-20 · LACP"| S1
    S2 --- MC["Gi1/0/5 · VLAN 40 McDonald's"]
    S3 --- TB["Gi1/0/1 · VLAN 30 Taco Bell"]
    S3 --- SB["Gi1/0/2 · VLAN 20 Starbucks"]
```

## Devices

| Device | Role | Config |
|---|---|---|
| R1 (`Nogales`) | Site edge; OSPFv3 10 area 0 to Area 51; RIPng `process1` inside; mutual redistribution + `default-information originate`; IPsec crypto maps | [r1-edge.txt](configs/r1-edge.txt) |
| R2 | RIPng; HSRPv2 standby on the core LAN | [r2.txt](configs/r2.txt) |
| R3 | RIPng; HSRPv2 active (priority 150, preempt) | [r3.txt](configs/r3.txt) |
| R4 | RIPng; router-on-a-stick for VLAN 20/30/40; DHCPv6 | [r4.txt](configs/r4.txt) |
| Core_SW | Joins R2, R3, R4 on `…:2002::/64` | [core-sw.txt](configs/core-sw.txt) |
| S1, S2, S3 | Access triangle, LACP, port-security | [s1](configs/s1.txt) · [s2](configs/s2.txt) · [s3](configs/s3.txt) |

## VLANs and addressing

| VLAN | Name | Prefix | Addressing |
|---|---|---|---|
| 20 | Starbucks (50 hosts) | `2001:db8:cafe:2003::/64` | R4 `::1`; **stateless DHCPv6** (`other-config-flag`, pool `Servers`) |
| 30 | Taco Bell (270 hosts) | `2001:db8:cafe:2004::/64` | R4 EUI-64; SLAAC |
| 40 | McDonald's (3000 hosts) | `2001:db8:cafe:2005::/64` | R4 EUI-64; SLAAC |
| 999 | Void / blackhole | — | all unused ports, shut |
| 1000 | Native | — | trunk native VLAN |
| — | R1 ↔ R3 | `2001:db8:cafe:2000::/64` | `::1` / `::2` |
| — | R1 ↔ R2 | `2001:db8:cafe:2001::/64` | `::1` / `::2` |
| — | Core LAN | `2001:db8:cafe:2002::/64` | VIP `::1`, R3 `::2`, R2 `::3`, R4 `::4` |

## Switching and security

- **EtherChannel**: LACP triangle; each link pairs one `active` side with one `passive` side. Trunks allow only 20,30,40 with native VLAN 1000.
- **Port-security** on every access port: `maximum 5`, `mac-address sticky`; `switchport nonegotiate` on unused ports.
- **Management**: local `Admin` user, `login local`, `transport input ssh` on the access switches.

## IPsec

R1 carries three crypto-map entries (AES-256 / SHA-256 / DH 14 / PFS 14, 900 s SA lifetime):

| Entry | Peer | ACL |
|---|---|---|
| `cmap 10` | Bangkok R1 `2001:db8:1:2::2` | `TEN` — Nogales → Bangkok `5000–5006` |
| `cmap 20` | Bangkok R2 `2001:db8:1:3::2` | `twenty` — same set |
| `cmap 30` | Vegas Edge `2001:db8:1:5::2` | `thirty` — Nogales → Vegas `3001–3060` |

In the final save the map is **not applied** to S0/2/0 and the GRE `Tunnel0` to Maine is gone. The 10/07 version that still had both is kept at [snippets/r1-edge-10-07-with-gre-and-cryptomap.txt](snippets/r1-edge-10-07-with-gre-and-cryptomap.txt).
