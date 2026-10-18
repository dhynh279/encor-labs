# Addressing

All IPv4. The `100.x`, `200.x`, `201.x` and `202.x` blocks are used as private lab space.

| Block | Use |
|---|---|
| `100.10.0.0/24` | Core /30s (Core-1/2 ↔ core leafs) |
| `200.10.0.0/24` | Distribution /30s (core leafs ↔ DSWs, DSW ↔ DSW) |
| `201.10.0.240/28` | DSW management loopbacks (Lo0) |
| `202.10.0.0/22` + `202.10.4.0/24` | Wireless client VLANs 11–15 on DSW-3 |
| `10.10.10.0/24` | Zone 1 — Vixen |
| `10.10.20.0/24` | Zone 2 — Blitzen |
| `10.10.30.0/24` | Zone 3 — Dasher |

## Core links — `100.10.0.0/24` (OSPF 8008, area 0)

| Link | Subnet | Core side | Leaf side | Notes |
|---|---|---|---|---|
| Core-1 Gi1/0/18 ↔ CL-1 (Meraki) | `.252/30` | `.253` | Meraki | |
| Core-1 Gi1/0/1 ↔ CL-2 Fa1/0/13 | `.248/30` | `.249` | `.250` | |
| Core-1 Gi1/0/16 ↔ CL-3 (Meraki) | `.244/30` | `.245` | Meraki | |
| Core-1 Gi1/0/2 ↔ CL-4 Gi1/0/1 | `.240/30` | `.241` | `.242` | BFD |
| Core-1 Gi1/0/14 ↔ CL-5 (Meraki) | `.236/30` | `.237` | Meraki | |
| Core-2 Gi1/0/18 ↔ CL-1 (Meraki) | `.232/30` | `.233` | Meraki | |
| Core-2 Gi1/0/1 ↔ CL-2 Fa1/0/14 | `.228/30` | `.229` | `.230` | |
| Core-2 Gi1/0/16 ↔ CL-3 (Meraki) | `.224/30` | `.225` | Meraki | |
| Core-2 Gi1/0/2 ↔ CL-4 Gi1/0/2 | `.220/30` | `.221` | `.222` | BFD |
| Core-2 Gi1/0/14 ↔ CL-5 (Meraki) | `.216/30` | `.217` | Meraki | Planning drawing says `.196/30` |

Meraki uplink trunks (Core-1/Core-2 Gi1/0/20, 22, 24 → Meraki 5, 3, 1) carry VLANs 1, 414 and 3900.

## Distribution uplinks — `200.10.0.0/24`

| Core leaf | DSW | Subnet | Leaf | DSW | Area |
|---|---|---|---|---|---|
| CL-2 Fa1/0/36 | DSW-1 Fa1/0/2 | `.248/30` | `.250` | `.249` | 10 |
| CL-2 Fa1/0/33 | DSW-2 Gi1/0/2 | `.240/30` | `.242` | `.241` | 10 |
| CL-2 Fa1/0/35 | DSW-3 Gi1/0/2 | `.228/30` | `.230` | `.229` | 20 |
| CL-2 Fa1/0/34 | DSW-4 Gi1/0/1 | `.196/30` | `.198` | `.197` | 20 |
| CL-4 Gi1/0/14 | DSW-3 Gi1/0/4 | `.220/30` | `.222` | `.221` | 20 |
| CL-4 Gi1/0/16 | DSW-4 Gi1/0/3 | `.188/30` | `.190` | `.189` | 20 |
| CL-4 Gi1/0/13 | DSW-7 Gi1/0/2 | `.176/30` | `.178` | `.177` | 30 (p2p) |
| CL-4 Gi1/0/15 | DSW-8 Gi1/0/2 | `.164/30` | `.166` | `.165` | 30 (p2p) |
| CL-3 (Meraki) | DSW-7 Gi1/0/1 | `.180/30` | — | `.181` | 30 |
| CL-5 (Meraki) | DSW-7 Gi1/0/3 | `.168/30` | — | `.169` | 30 |
| CL-1/3/5 (Meraki) | DSW-1/2/3/4/8 | DHCP from Meraki | — | `ip address dhcp` | |

### Area 20 internal (DSW-3/4 ↔ DSW-5/6, all `ip ospf network point-to-point`)

| Link | Subnet | Addresses |
|---|---|---|
| DSW-3 Gi1/0/23 ↔ DSW-5 Fa1/0/1 | `200.10.0.160/30` | `.161` / `.162` |
| DSW-3 Gi1/0/24 ↔ DSW-6 Fa2/0/1 | `200.10.0.152/30` | `.153` / `.154` |
| DSW-4 Gi1/0/23 ↔ DSW-5 Fa1/0/2 | `200.10.0.156/30` | `.157` / `.158` |
| DSW-4 Gi1/0/24 ↔ DSW-6 Fa2/0/2 | `200.10.0.140/30` | `.141` / `.142` |
| DSW-5 Fa1/0/5 ↔ DSW-6 Fa2/0/5 | `200.10.0.148/30` | `.149` / `.150` |
| DSW-5 Fa1/0/6 ↔ DSW-6 Fa2/0/6 | `200.10.0.144/30` | `.145` / `.146` |

## Router IDs

| Device | RID | Device | RID |
|---|---|---|---|
| Core-1 | 1.10.1.1 | DSW-1 | 10.1.1.1 |
| Core-2 | 1.10.1.2 | DSW-2 | 10.1.1.2 |
| CL-2 | 1.10.1.4 | DSW-3 | 20.1.1.3 |
| CL-4 | 1.10.1.6 | DSW-4 | 20.1.1.4 |
| (CL-1/3/5 planned 1.10.1.3/.5/.7) | | DSW-5 / DSW-6 | 20.1.1.5 / 20.1.1.6 |
| | | DSW-7 / DSW-8 | 30.1.1.7 / 30.1.1.8 |

## Zone 1 — Vixen `10.10.10.0/24` (gateways on DSW-1/DSW-2, HSRPv2)

| VLAN | Name | Subnet | VIP | DSW-1 | DSW-2 | HSRP active | Server |
|---|---|---|---|---|---|---|---|
| 10 | Email | `.248/29` | `.250` | `.249` | `.251` | DSW-1 | `.254` |
| 20 | RADIUS | `.240/29` | `.242` | `.241` | `.243` | DSW-1 | `.246` |
| 30 | SNMP | `.232/29` | `.234` | `.233` | `.235` | DSW-2 | `.238` |
| 40 | Proxmox | `.224/29` | `.226` | `.225` | `.227` | DSW-2 | `.230` |
| 99 / 100 / 999 | void / native / unused | | | | | | |

DHCP pools for every VLAN on both DSW-1 and DSW-2.

## Zone 2 — Blitzen `10.10.20.0/24` (gateway on DSW-5/DSW-6, HSRPv2)

| VLAN | Name | Subnet | Gateway | Hosts |
|---|---|---|---|---|
| 10 | Servers | `10.10.20.128/25` | VIP `.129` (DSW-5 `.130` active, DSW-6 `.231`) | Email `.254`, Proxmox `.130`, Streaming `.229`, Proxy `.228`, DNS `.227` |
| 67 | Management | `10.10.20.0/28` | — | S1–S8 at `.1`–`.8` |
| 117 | Unused | | | |
| 414 | Native | | | |

The original design used four /29 server VLANs (50/60/70/80); Blitzen consolidated them into one /25 server VLAN mid-project.

## Zone 3 — Dasher `10.10.30.0/24` (gateways on DSW-7/DSW-8, HSRPv1)

| VLAN | Name | Subnet | VIP | DSW-7 | DSW-8 | Active |
|---|---|---|---|---|---|---|
| 90 | Email | `.248/29` | `.249` | `.250` | `.251` | DSW-7 |
| 100 | RADIUS | `.240/29` | `.241` | `.242` | `.243` | DSW-7 |
| 110 | SNMP | `.232/29` | `.233` | `.234` | `.235` | DSW-8 |
| 120 | Proxmox | `.224/29` | `.225` | `.226` | `.227` | DSW-8 |
| 200 / 500 | native / void | | | | | |

## Wireless (SVIs + DHCP on DSW-3, DNS `10.10.20.227`)

| VLAN | SSID | Subnet | Gateway |
|---|---|---|---|
| 11 | CORE-WIRELESS-1 | `202.10.0.0/24` | `.1` |
| 12 | DISTRO-WIRELESS-1 | `202.10.1.0/24` | `.1` |
| 13 | A10-WIRELESS-1 | `202.10.2.0/24` | `.1` |
| 14 | A20-WIRELESS-1 | `202.10.3.0/24` | `.1` |
| 15 | A30-WIRELESS-1 | `202.10.4.0/24` | `.1` |

All five SSIDs are WPA2-PSK on one autonomous AP ([distribution-comet/snippets/access-point-v3.txt](../distribution-comet/snippets/access-point-v3.txt)).
