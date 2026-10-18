# Known Issues & Review Notes

Found while going back through the final (12/04) configs. The configs are left exactly as they ran; this is the list of what I'd fix.

## Core (Rudolph)

| # | Issue | Fix |
|---|---|---|
| C1 | CL-2 has `login` on vty with no password and no console password, so there's no way to get SSH or console access with credentials. The other core switches use `login local`. | `login local` + `transport input ssh` |
| C2 | CL-2 runs `spanning-tree mode pvst`; the rest of the core runs rapid-pvst. It only matters on CL-2's few L2 ports, but it's inconsistent. | `spanning-tree mode rapid-pvst` |
| C3 | BFD is configured on the Core ↔ CL-4 links, but `bfd all-interfaces` isn't on CL-2, so the Core ↔ CL-2 path falls back to normal OSPF dead timers. | Add BFD on CL-2 (or `ip ospf bfd` per interface) |
| C4 | Core-1 Gi1/0/12 has both `switchport access vlan 1000` and trunk config. | Remove the leftover access line |
| C5 | Router IDs on the Meraki leafs (1.10.1.3/.5/.7) are only in the plan; the Meraki side isn't CLI-configurable, so nothing in this repo shows it. | — |

## Distribution (Comet)

| # | Issue | Fix |
|---|---|---|
| D1 | DSW-7's uplinks to CL-3 and CL-5 (Meraki) use static `/30` addresses, while every other Meraki-facing DSW port uses `ip address dhcp`. These adjacencies probably never formed. | Match the others (`ip address dhcp`) or configure the Meraki side statically |
| D2 | DSW-5/6 downlinks to Blitzen set `switchport trunk allowed vlan` and `portfast trunk` but not `switchport mode trunk`, so they rely on DTP. | `switchport mode trunk` + `switchport nonegotiate` |
| D3 | DSW-5's VLAN 10 SVI is `10.10.20.130`, which is also the Proxmox server's address in Blitzen's table. That's an IP conflict on the server VLAN. | Move the SVI or the server |
| D4 | DSW-6 VLAN 10 SVI `10.10.20.231` sits in the middle of the server range rather than next to the VIP. Not wrong, but easy to collide with. | `.131` |
| D5 | Zone 1 DHCP pools exist on **both** DSW-1 and DSW-2 for the same subnets; two DHCP servers for one /29 risk duplicate leases. | One server, or split the ranges |
| D6 | DSW-3 has `network 10.10.20.224 0.0.0.31 area 20` but no interface in that range. DSW-4 has the same. | Remove |
| D7 | DSW-7 Loopback1 (router ID) is a /28 instead of a /32. | `/32` |
| D8 | Every DSW puts a management loopback in the same `201.10.0.240/28`. OSPF advertises loopbacks as /32s, so it works, but the shared mask is misleading. | Use /32s |
| D9 | Interface descriptions don't match the far end (e.g. DSW-2 Gi1/0/2 says "Core-2" but connects to CL-2). | Re-describe from the cable list |

## Access

| # | Zone | Issue | Fix |
|---|---|---|---|
| A1 | Vixen | S1 and S2 both set STP priority 24576 for VLANs 10,20 and 28672 for 30,40, so the root bridge is decided by MAC, not by design. The root should also be the HSRP-active DSW, not an access switch. | Root on DSW-1 (10/20) and DSW-2 (30/40) |
| A2 | Vixen | S1 `aaa authentication login default group radius none`: if RADIUS is unreachable, `none` lets anyone in. | Use `local` as the fallback |
| A3 | Vixen | Management IP on Vlan1 in `202.10.0.240/28`, which overlaps the core-wireless pool on DSW-3 (`202.10.0.0/24`). | Use a dedicated management VLAN/subnet |
| A4 | Blitzen | S2 Port-channel1 allows `10,67,414` native 414, but its member ports allow `1,10,67` native 1. Member/bundle mismatch suspends the channel; this is part of the VLAN-mismatch / STP errors seen on the final night. | Make the member ports match the port-channel |
| A5 | Blitzen | No SVI for management VLAN 67 on DSW-5/6, so the `10.10.20.0/28` switch management IPs aren't routable. | Add VLAN 67 SVIs + OSPF |
| A6 | Blitzen | The DNS router points at name server `10.10.20.253`, but the address table puts DNS at `10.10.20.227`. | Pick one |
| A7 | Dasher | SW1 defines `ip access-list standard SNMP-ACL` but the community references `SNMP_ACL`. An undefined ACL means no restriction, on a **RW** community. | Fix the name; use SNMPv3 or RO |
| A8 | Dasher | Neither switch has a management IP (Vlan1 shut, no other SVI), so the SNMP config can't be reached. | Add a management SVI |
| A9 | Dasher | Port-security script exists in `snippets/` but isn't applied to any access port in the final configs. | Apply it to Gi1/0/2, Gi1/0/4 |
| A10 | Blitzen | No port-security anywhere, and unused ports aren't shut or moved to the unused VLAN 117 (port-security was a zone requirement). Vixen only applies it to its shut unused ports. | Apply to all access ports |
