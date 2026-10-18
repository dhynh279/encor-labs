# IPv6 Addressing Plan

Everything uses the documentation range `2001:db8::/32`. No IPv4 anywhere.

| Block | Use |
|---|---|
| `2001:db8:1:N::/64` | WAN serial links, Area 51 Edge ↔ each site (Edge is always `::1`) |
| `2001:db8:1N:x::/64` | Site-to-site tunnel overlays (GRE / IPsec) |
| `2001:db8:cafe:1000::/52` | Area 51 |
| `2001:db8:cafe:2000::/52` | Nogales |
| `2001:db8:cafe:3000::/52` | Vegas |
| `2001:db8:cafe:4000::/52` | Maine |
| `2001:db8:cafe:5000::/52` | Bangkok |

## WAN links (Area 51 Edge-Router)

| Edge interface | Peer | Prefix | Edge | Peer |
|---|---|---|---|---|
| S0/1/0 | Nogales R1 S0/2/0 | `2001:db8:1:1::/64` | `::1` | `::2` |
| S0/2/1 | Bangkok R1 S0/1/0 | `2001:db8:1:2::/64` | `::1` | `::2` |
| S0/2/0 | Bangkok R2 S0/1/0 | `2001:db8:1:3::/64` | `::1` | `::2` |
| S0/0/1 | Maine R1 S0/1/0 | `2001:db8:1:4::/64` | `::1` | `::2` |
| S0/1/1 | Vegas Edge S0/1/0 | `2001:db8:1:5::/64` | `::1` | `::2` |
| S0/0/0 | Area 51 R2 S0/1/1 | link-local only | `fe80::1` | `fe80::2` |

## Tunnel overlays

| Tunnel | Endpoints | Prefix | Status in final configs |
|---|---|---|---|
| GRE | Nogales ↔ Vegas (planned IPsec) | `2001:db8:10:1::/64` | Not built as GRE; IPsec crypto map 30 instead |
| GRE | Nogales ↔ Bangkok (planned IPsec) | `2001:db8:11:1::/64` | Not built as GRE; IPsec crypto map 10/20 instead |
| GRE | Nogales ↔ Maine R2 | `2001:db8:12:1::/64` | Maine side configured; Nogales side removed in final |
| GRE | Vegas Edge ↔ Bangkok R1 | `2001:db8:13:1::/64` | Vegas `::2`, Bangkok `::1` |
| GRE | Vegas Edge ↔ Bangkok R2 | `2001:db8:13:2::/64` | Vegas `::2`, Bangkok `::1` |
| IPsec | Maine R2 ↔ Vegas Edge (planned) | `2001:db8:14:1::/64` | Not configured |

## OSPF router IDs

| Router | Process | Router ID |
|---|---|---|
| Area 51 Edge-Router | 10 | 19.19.19.19 |
| Area 51 R1 | 10 | 1.1.1.1 |
| Area 51 R2 | 10 | 2.2.2.2 |
| Nogales R1 (edge) | 10 | 11.11.11.11 |
| Vegas Edge | ospfv3 2 | 21.21.21.21 |
| Vegas R1 / R2 / R3 | 2 | 6.6.6.6 / 7.7.7.7 / 8.8.8.8 |
| Maine R1 / R2 | 10 | 4.0.0.1 / 4.0.0.2 |

## Area 51 — `2001:db8:cafe:1000::/52`

| Prefix | Name | Gateway | Router |
|---|---|---|---|
| `…:1000::/64` | RADIUS / server segment | `…:1000:100::1` | R1 Gi0/0/1 |
| `…:1001::/64` | VLAN 100 (300 hosts) | `…:1001:100:1::` | R2 Gi0/0/0.100 |
| `…:1002::/64` | VLAN 200 (200 hosts) | `…:1002:100:1::` | R2 Gi0/0/0.200 |
| `…:1003::/64` | VLAN 300 (300 hosts) | `…:1003:100:1::` | R2 Gi0/0/0.300 |
| `…:1004::/64` | VLAN 400 (20 hosts) | `…:1004:100:1::` | R1 Gi0/0/0.400 |
| `…:1005::/64` | VLAN 500 (1500 hosts) | `…:1005:100:1::` | R1 Gi0/0/0.500 |
| `…:1006::/64` | VLAN 600 — cameras | `…:1006:100:1::` | R1 Gi0/0/0.600 |
| `…:1007::/64` | Web + syslog servers | `…:1007:100::1` | R2 Gi0/0/1 |
| `…:1008::/64` | VLAN 6 — management | `…:1008:100::1` | R1 Gi0/0/0.6 |
| `…:1009::/64` | Loopback | `…:1009:100::5` | R2 Lo0 |

## Nogales — `2001:db8:cafe:2000::/52`

| Prefix | Name | Addresses |
|---|---|---|
| `…:2000::/64` | R1 S0/1/1 ↔ R3 S0/1/1 | `::1` / `::2` |
| `…:2001::/64` | R1 S0/1/0 ↔ R2 S0/1/0 | `::1` / `::2` |
| `…:2002::/64` | Core LAN (R2, R3, R4 via Core_SW) | VIP `::1`, R3 `::2`, R2 `::3`, R4 `::4` |
| `…:2003::/64` | VLAN 20 "Starbucks" (50 hosts) | R4 `::1`, stateless DHCPv6 |
| `…:2004::/64` | VLAN 30 "Taco Bell" (270 hosts) | R4 EUI-64, SLAAC |
| `…:2005::/64` | VLAN 40 "McDonald's" (3000 hosts) | R4 EUI-64, SLAAC |
| — | VLAN 999 blackhole, VLAN 1000 native | |

## Vegas — `2001:db8:cafe:3000::/52`

| Prefix | Name | Addresses |
|---|---|---|
| `…:3001::/64` | VLAN 100 | R1 `::1` |
| `…:3002::/64` | VLAN 200 | R1 `::1` |
| `…:3003::/64` | VLAN 300 | R1 `::1` |
| `…:3004::/64` | VLAN 400 — RADIUS | R1 `::1` |
| `…:3010::/64` | R1 S0/1/0 ↔ R2 S0/1/0 | `::1` / `::2` |
| `…:3020::/64` | R1 S0/1/1 ↔ R3 S0/1/0 | `::1` / `::2` |
| `…:3030::/64` | HSRP (planned) | |
| `…:3040::/64` | R2 Gi0/0/0 → S2 | `::1` |
| `…:3050::/64` | R3 Gi0/0/0 → S2 | `::1`, HSRP VIP `::ffff` |
| `…:3060::/64` | Edge Gi0/0/0 → S2 | `::1` |

## Maine — `2001:db8:cafe:4000::/52`

| Prefix | Name | Gateway |
|---|---|---|
| `…:4000::/64` | R1 S0/1/1 ↔ R2 S0/1/0 | `::1` / `::2` |
| `…:4001::/64` | VLAN 15 Acadia | R2 `::1` |
| `…:4002::/64` | VLAN 30 Baxter | R2 `::1` |
| `…:4003::/64` | VLAN 45 Cameras | R2 `::1` |
| `…:4004::/64` | VLAN 60 Wireless | R2 `::1` |
| — | VLAN 75 native, VLAN 99 void | |

## Bangkok — `2001:db8:cafe:5000::/52` (final, after renumbering)

| Prefix | Name |
|---|---|
| `…:5000::/64` | Serial / point-to-point links |
| `…:5001::/64` | LAN 1 |
| `…:5002::/64` | LAN 2 |
| `…:5003::/64` | Cameras |
| `…:5004::/64` | Servers (syslog `…:5004::4`) |
| `…:5005::/64` | Management |
| `…:5006::/64` | HSRP link (written as `2001:db9:…` in the team table — typo) |

The first Bangkok plan carved `…:5000::/64` into /80s and /127s. It was thrown out on 9/29 because the IP cameras would only auto-configure on a /64, so every segment was moved to its own /64.

## Hosts used for end-to-end ping tests

| Site | Address | Device |
|---|---|---|
| Area 51 | `2001:db8:cafe:1007:100::2` | Web server |
| Area 51 | `2001:db8:cafe:1006:240:8cff:feb1:641f` | Camera |
| Nogales | `2001:db8:cafe:2004:9f8d:11d0:5863:221f` | Host |
| Nogales | `2001:db8:cafe:2005:f9ed:bf5b:a6d1:dc3e` | Host |
| Vegas | `2001:db8:cafe:3001:9785:c363:1292:a05e` | Host |
| Vegas | `2001:db8:cafe:3002:58d0:1c45:6b16:d262` | Host |
| Maine | `2001:db8:cafe:4002:a33e:91fc:f7d:9858` | Host |
| Maine | `2001:db8:cafe:4003:c5f8:9707:846c:7c07` | Host |
| Bangkok | `2001:db8:cafe:5001:e77c:aef3:de95:7711` | Host |
| Bangkok | `2001:db8:cafe:5002:44e6:1421:1c46:27d7` | Host |
| Bangkok | `2001:db8:cafe:5003:240:8cff:feb1:6416` / `…6417` / `…641e` | Cameras |
