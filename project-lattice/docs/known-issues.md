# Known Issues & Review Notes

Found while going back through the final saves. The configs are left as they ran.

## Hub

| # | Issue | Fix |
|---|---|---|
| H1 | P2 Gi1/0/4 and P3 Gi1/0/4 both have `8.8.7.13/30`, left over from the earlier PE-router design. | Remove both, or re-address if PEs come back |
| H2 | P3 has `network 8.7.0.0 0.0.0.255 area 0` (P1's management range) and P4 has `network 8.8.9.108 0.0.0.3` (P2's Team 2 link). Neither switch has an interface there. | Remove |
| H3 | P2 has `redistribute ospf 99` and a shut `router ospf 50`, but there's no OSPF process 99; area 99 is part of process 65535. | Remove both |
| H4 | P1 and P2 management SVIs are `/16`s (`8.7.0.0/16`, `8.6.0.0/16`) while their DHCP pools are `/24`s; P3/P4 use `/24`. | Use `/24` everywhere |
| H5 | Metric-1 redistribution (`redistribute rip metric 1`, `eigrp 1 metric 1`) works, but every external route looks equally cheap. | Set metrics that reflect the paths |

## Team 1

| # | Issue | Fix |
|---|---|---|
| T1-1 | The ASA's outside interface is `8.8.9.102`, the same address as EdgeR's hub link. Both can't be up on the hub's `/30`. | The ASA was meant to replace EdgeR in that path; re-address or remove EdgeR |
| T1-2 | The ASA's inside address `20.0.255.210/29` isn't on the area 0 switch segment (`.224/28`), and R2's "LinkToFirewall" port is on `.224/28`. They can't talk. | Put the ASA inside interface on `.224/28`, or give R2 a `.208/29` interface |
| T1-3 | Area 2 was designed as an NSSA but has no `area 2 nssa`. A virtual link can't transit an NSSA, which is probably why it was dropped. | Use a GRE tunnel or re-home area 7 if NSSA is a requirement |
| T1-4 | The R1 ↔ RA virtual link isn't needed: RA has only area 1, so it doesn't attach another area. | Remove |
| T1-5 | EdgeE's static default points into Team 1 (`Serial0/1/0` → NS) instead of toward the hub. | `ip route 0.0.0.0 0.0.0.0 8.8.9.105` |

## Team 2

| # | Issue | Fix |
|---|---|---|
| T2-1 | The ASA's Gi1/1 and R1's Gi0/0/1 are both `10.0.50.245/30`. | R1 should be `.246` |
| T2-2 | The ASA's outside interface is `8.8.9.50/30` with a default route to `8.8.9.49`, which is hub **P4**'s Team 3 port (`8.8.9.48/29`), not P2's Team 2 port (`8.8.9.109/30`, area 99). `8.8.9.50` is also the hub ASA's address on that P4 segment, so the two firewalls collide if both are plugged in. | Use P2's link: `8.8.9.110/30`, default via `8.8.9.109` |
| T2-3 | The ASA relies on a static default + PAT (`nat (INSIDE,OUTSIDE) dynamic interface`) toward the hub and doesn't advertise Team 2 into OSPF, so the rest of the WAN can only reach Team 2 through NAT. | Run OSPF area 99 on the outside interface (P2 is already the area 99 ABR) and drop the PAT |
| T2-4 | VLAN 40 SVI has a DHCP pool but no access ports; VLAN 50 (Ansible) isn't in OSPF. | Add as needed |
| T2-5 | Core switch runs `spanning-tree mode pvst`; access switches run rapid-pvst. | Match |

## Team 3 *(mine)*

| # | Issue | Fix |
|---|---|---|
| T3-1 | Mutual redistribution in a triangle at each site (EIGRP 200 ⇄ EIGRP 300 ⇄ RIP ⇄ EIGRP 200 on R6; same with 600 on R9) can loop routes back in. EIGRP's external AD of 170 hides most of it here, but route tags would make it safe. | Tag on redistribution and deny tagged routes coming back |
| T3-2 | `router eigrp 300` / `600` have no `network` statements; they exist only as redistribution stepping stones. RIP ⇄ EIGRP 200 directly would do the same job. | Simplify |
| T3-3 | R4 advertises `network 8.0.0.0` into EIGRP 200 as well as the specific `/30`. | Keep only the `/30` |
| T3-4 | The only saved ASA config (10/23) has `router eigrp 200` with no networks; the working version that carried Team 4 wasn't saved. | Save configs at the end of every session |

## Team 4

| # | Issue | Fix |
|---|---|---|
| T4-1 | PE-0 and PE-4 `network` statements use **subnet masks** (`255.255.255.252`) instead of wildcards. IOS reads them as wildcards, so a statement like `network 192.168.255.248 255.255.255.252 area 0` matches almost every interface, and all of them land in the first area listed. | Use `0.0.0.3` |
| T4-2 | Login banners printed the default username and password (removed here). | Never put credentials in a banner |
| T4-3 | PE-2's DHCP pool for DC-2 is named `DC-1`. | Rename |
