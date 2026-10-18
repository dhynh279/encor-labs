# CCNP ENCOR (350-401 v1.2) Labs

Lab files, configs and notes for the 9-lab ENCOR workbook.

| Lab | Topic | Platform |
|---|---|---|
| 01 | Layer 2: trunks, LACP, Rapid PVST+, guards | Packet Tracer |
| 02 | OSPFv2/v3 multi-area | Packet Tracer |
| 03 | eBGP best path + PBR | Packet Tracer / GNS3 |
| 04 | NAT/PAT, HSRP, NTP | Packet Tracer |
| 05 | VRF-lite, GRE over IPsec | GNS3/EVE-NG or DevNet CML |
| 06 | AAA, ACLs, CoPP | Packet Tracer |
| 07 | IP SLA, NetFlow, SPAN, syslog, SNMPv3 | GNS3/EVE-NG or DevNet CML |
| 08 | NETCONF, RESTCONF, YANG | DevNet Cat8000v sandbox |
| 09 | Python, EEM, Ansible | DevNet Cat8000v sandbox |

## Layout
Each `labNN-*/` folder holds the `.pkt` / topology file, `configs/<device>.txt` (final `show run`), and `NOTES.md` (verification output, break/fix findings).

## Capstone

| Project | Topic | Platform |
|---|---|---|
| [project-meridian](project-meridian) | Five-site IPv6-only WAN: OSPFv3 / RIPng / BGP, HSRP, EtherChannel, GRE, IPsec | Real hardware (ISR 4221, Cat 1000) + Packet Tracer |
| [north-pole](north-pole) | Three-tier campus: multi-area OSPF, BFD, HSRP, Meraki MS core leafs, wireless | Real hardware (Cat 9300L, Meraki MS) + Packet Tracer |
