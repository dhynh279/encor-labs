# Known Issues & Review Notes

Things found while going back through the final saved configs. They're left as-is in `sites/*/configs/` so the files stay true to what ran; this is the list of what I'd fix next time.

## WAN-wide

| # | Issue | Where | Fix |
|---|---|---|---|
| W1 | `ipv6 router rip process1` / `redistribute rip process1` on the Area 51 Edge, but no interface has RIPng enabled, so the redistribution does nothing. | Area 51 Edge | Remove it — Nogales does the RIPng ⇄ OSPF redistribution at its own edge. |
| W2 | Crypto maps are defined but **not applied** (`ipv6 crypto map cmap` missing from the WAN interface). The 10/07 Nogales draft had it on S0/2/0; the final save doesn't. | Nogales R1, Vegas Edge | `interface Serial0/2/0` → `ipv6 crypto map cmap` (Nogales); `interface Serial0/1/0` → `ipv6 crypto map cmap` (Vegas). |
| W3 | Pre-shared keys configured with a prefix length (`address ipv6 2001:DB8:1:5::2/64`). Works, but a /128 is tighter. | Nogales R1, Vegas Edge | `crypto isakmp key <PSK> address ipv6 2001:db8:1:5::2/128` |
| W4 | Maine ↔ Nogales GRE: Maine R2 still has `Tunnel0` pointing at Nogales, but Nogales' final config dropped its `Tunnel0`. | Maine R2 / Nogales R1 | Restore Nogales `Tunnel0` (`2001:db8:12:1::1/64`, dest `2001:db8:cafe:4000::2`) from `sites/nogales/snippets/`. Also needs a route to `…:4000::2` on Nogales. |
| W5 | Device clocks were never set (timestamps in 1993, 2012 and 2026). Makes syslog correlation useless. | Several | `clock set` or NTP from the Area 51 edge. |

## Area 51

| # | Issue | Fix |
|---|---|---|
| A1 | R1 `logging host ipv6 2001:DB8:1007::3` is missing `cafe:` / `100:` — R2 correctly points at `2001:DB8:CAFE:1007:100::3`. | Match R2. |
| A2 | R1 `line vty 0 4` allows **telnet**; 5–14 are SSH. | `transport input ssh` on 0–4. |
| A3 | DHCPv6 pools have `address prefix` (stateful) but the interfaces don't set `ipv6 nd managed-config-flag`, so hosts SLAAC and never ask for a lease. | Add the M flag, or switch to stateless (`other-config-flag`) and drop the address prefix. |
| A4 | S4–S7 EtherChannel ring: port-channels have no switchport mode/VLAN config, so they're access ports in VLAN 1; ring isn't tied into any VLAN. | `switchport mode trunk` + allowed VLANs on Po1–Po4. |
| A5 | S7 has a paste artifact (`inistratively downvlan internal allocation policy ascending`). | Re-paste that line. |
| A6 | S3 Gi1/0/4 is described "Not In Use" but is up in VLAN 600. | Shut it or fix the description. |
| A7 | The original Visio drawing has R1/R2 and the VLAN groups swapped relative to the configs. The diagrams in this repo follow the configs. | — |

## Nogales

| # | Issue | Fix |
|---|---|---|
| N1 | `line vty` has `login` with no password and no `login local` → nobody can SSH in. Switches are fine (`login local`). | `login local` + a local user. |
| N2 | Redistribution metrics were dropped from the final save (`redistribute rip process1` without `metric`). OSPF uses the default 20, RIPng uses 1 — fine, but different from the draft. | — |
| N3 | Banner has `^CCCCC` garbage from a bad paste. | Re-enter the banner. |

## Vegas

| # | Issue | Fix |
|---|---|---|
| V1 | `Tunnel0` has a second, bogus address `2001:DB8:DB8:13:1::2/64`. | `no ipv6 address 2001:DB8:DB8:13:1::2/64` |
| V2 | HSRP mismatch: R2 uses `standby 10 ipv6 autoconfig` on `…:3040::/64`, R3 uses VIP `…:3050::ffff` on a different /64. They sit on the same switch, so HSRP may elect but the VIP isn't a usable gateway for one subnet. | Put R2 and R3 on one subnet (`…:3030::/64` was reserved for this) with one VIP. |
| V3 | Final S1 only trunks VLANs 100,200 and has no VLAN 300/400 access ports, but R1 routes 100–400. The 9/30 draft had 300/400. | Add 300,400 to the Gi1/0/1 trunk and access ports. |
| V4 | S2 has no VLANs/descriptions — R2, R3 and the Edge all share VLAN 1. | Dedicated transit VLAN. |
| V5 | Leftover empty processes: `router ospfv3 10` (Edge), `router ospf 1` (R2). | Remove. |
| V6 | `aaa authentication login VegasUsr local none` — `none` fallback means login succeeds with no credentials if the local DB can't be used; the list also isn't applied to any line. | Drop `none`, apply with `login authentication VegasUsr`. |

## Maine

| # | Issue | Fix |
|---|---|---|
| M1 | Two RIPng processes: `ipv6 router rip RIPng` (redistributes OSPF) and `ipv6 router rip RIPNG` (enabled on Tunnel0). Names are case-sensitive, so the tunnel never gets the OSPF routes. | Use one process name. |
| M2 | Login banner printed the default username and passwords (removed in this repo). | Never put creds in a banner. |
| M3 | R1/R2 vty `login` without a password (same as N1). | `login local`. |

## Bangkok

| # | Issue | Fix |
|---|---|---|
| B1 | The final on-hardware Bangkok configs weren't saved to the shared project folder — only the Packet Tracer design files, the ACL, and the address table. | See `sites/bangkok/README.md` for what's known from peer configs. |
| B2 | ACL `BLOCK_MAINE_VEGAS` denies `…:4000::/64` and `…:3000::/64` — those are only the first /64 of each site (Maine's R1–R2 link and nothing at Vegas). To block whole sites it needs the /52s. | `deny ipv6 2001:db8:cafe:4000::/52 any` / `deny ipv6 2001:db8:cafe:3000::/52 any` |
| B3 | HSRP link prefix written as `2001:db9:cafe:5006` in the address table. | Typo — `db8`. |
