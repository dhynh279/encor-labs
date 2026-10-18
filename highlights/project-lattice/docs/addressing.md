# Addressing

| Network | Block | Routing |
|---|---|---|
| Hub | `8.8.8.0/24` core mesh, `8.8.9.0/24` team hand-offs, `8.4–8.7.0.0` management, `100.20.30.40–43` loopbacks | OSPF 65535 area 0 + MPLS LDP |
| Team 1 | `20.0.0.0/16` | OSPF (areas 0,1,2,3,4,5,7) |
| Team 2 | `10.0.0.0/16` | OSPF 50 area 99 |
| Team 3 | `172.0.0.0/24` + `100.100/100.200.x.0/30` site links | EIGRP 200 (+ RIP, EIGRP 300/600 at sites) |
| Team 4 | `192.168.0.0/16` | OSPF areas 0–4 |

## Hub core mesh (`8.8.8.0/24`, all /30, `mpls ip`)

| Link | Subnet | Addresses |
|---|---|---|
| P1 Gi1/0/1 – P2 Gi1/0/1 | `8.8.8.12/30` | `.13` / `.14` |
| P1 Gi1/0/2 – P4 Gi1/0/2 | `8.8.8.16/30` | `.17` / `.18` |
| P1 Gi1/0/3 – P3 Gi1/0/1 | `8.8.8.20/30` | `.21` / `.22` |
| P2 Gi1/0/2 – P3 Gi1/0/2 | `8.8.8.24/30` | `.25` / `.26` |
| P2 Gi1/0/3 – P4 Gi1/0/3 | `8.8.8.28/30` | `.29` / `.30` |
| P3 Gi1/0/3 – P4 Gi1/0/1 | `8.8.8.32/30` | `.33` / `.34` |

## Hub hand-offs (`8.8.9.0/24`)

| Hub port | Subnet | Hub | Team side | Protocol |
|---|---|---|---|---|
| P1 Gi1/0/13 | `8.8.9.100/30` | `.101` | Team 1 EdgeR `.102` | RIP |
| P1 Gi1/0/14 | `8.8.9.104/30` | `.105` | Team 1 EdgeE `.106` | EIGRP 1 |
| P2 Gi1/0/13 | `8.8.9.108/30` | `.109` | Team 2 | OSPF area 99 |
| P4 Gi1/0/24 | `8.8.9.48/29` | `.49` | Hub ASA `.50` | OSPF |
| Hub ASA Gi1/8 | `8.8.9.40/30` | `.41` | Team 3 R4 `.42` | EIGRP 200 |

## Team 1 (`20.0.0.0/16`)

| Segment | Subnet | Addresses |
|---|---|---|
| Area 0 switch | `20.0.255.224/28` | R1 `.225`, R2 `.226`, R3 `.227`, R4 `.228`, R5 `.229` |
| R1 – RA (area 1) | `20.0.255.248/30` | `.250` / `.249` |
| RA – EdgeR (RIP) | `20.0.255.252/30` | `.254` / `.253` |
| R2 – NS (area 2) | `20.0.255.240/30` | `.242` / `.241` |
| NS – EdgeE (area 7) | `20.0.255.244/30` | `.246` / `.245` |
| R3 LAN (area 3) | `20.0.0.0/24` | `.1` |
| R4 Lo0 (area 4 stub) | `20.0.1.0/24` | `.1` |
| R5 Lo0 (area 5 totally stubby) | `20.0.2.0/24` | `.1` |
| ASA inside | `20.0.255.208/29` | `.210` |

## Team 2, Team 3, Team 4

See [team2](../team2/README.md#addressing), [team3](../team3/README.md#addressing) and [team4](../team4/README.md).
