# Lab 02 — OSPFv2/v3 multi-area

Blueprint 3.2.b · Platform: Packet Tracer, 4× ISR4331 · In progress (started 2026-10-17)

## Topology

![Physical topology](topology/lab02-physical.png)

![Logical topology](topology/lab02-logical.png)

| Link | Ports | IPv4 | IPv6 | Area |
|---|---|---|---|---|
| R1 ↔ R2 | G0/0/0 ↔ G0/0/0 | 10.0.12.0/30 | 2001:db8:12::/64 | 1 |
| R2 ↔ R3 | G0/0/1 ↔ G0/0/0 | 10.0.23.0/30 | 2001:db8:23::/64 | 0 |
| R3 ↔ R4 | G0/0/1 ↔ G0/0/0 | 10.0.34.0/30 | 2001:db8:34::/64 | 2 |

Lower-numbered router gets .1 / ::1. Cabling: copper cross-over.

| Router | Lo0 (RID) | Other loopbacks | Role |
|---|---|---|---|
| R1 | 1.1.1.1/32 | Lo1–Lo4 172.16.0–3.1/24 | Internal, area 1 |
| R2 | 2.2.2.2/32 | — | ABR 1/0 |
| R3 | 3.3.3.3/32 | — | ABR 0/2 |
| R4 | 4.4.4.4/32 | Lo0 IPv6 2001:db8:4::4/128 | Internal, area 2 |

`ipv6 unicast-routing` on all routers.

## Stages

| # | Stage | Status |
|---|---|---|
| 1 | Build + addressing | Done — all neighbor pings successful (IPv4 + IPv6) |
| 2 | OSPFv2: point-to-point links, passive loopbacks, R1 Lo1–4 as /24 | Next |
| 3 | R2 `area 1 range 172.16.0.0 255.255.252.0`; R3 `area 2 filter-list prefix` deny 172.16.2.0/24 in | — |
| 4 | OSPFv3 | — |
| 5 | Break/fix: hello mismatch, MTU (EXSTART), area mismatch | — |

## Stage 1 verification

`show ip interface brief` / `show ipv6 interface brief` on each router, then directly connected pings:

| From | Targets | Result |
|---|---|---|
| R2 | 10.0.12.1, 10.0.23.2, 2001:db8:12::1, 2001:db8:23::2 | Success |
| R3 | 10.0.34.2, 2001:db8:34::2 | Success |

Remote loopbacks not reachable yet — expected until Stage 2.

## Packet Tracer quirks
- If `ospfv3 1 ipv6 area X` is rejected, use `ipv6 router ospf 1` + `ipv6 ospf 1 area X`.
- If `ip ospf network point-to-point` is rejected on loopbacks, skip it — the /32s still summarize under the /22.

## Next
- Stage 2 OSPFv2; baseline `show ip route ospf` on R4 (expect O IA for all area 0/1 prefixes) before Stage 3.
- Save final `show run` from each router to `configs/R1.txt`–`R4.txt` and the `.pkt` to this folder.
