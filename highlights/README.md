# Highlights

Four projects built and configured on real Cisco hardware between April and December 2025. Every project folder has the final configs, redrawn topologies, addressing, verification or outcome notes, and a review of what I'd change next time.

| Project | When | Scale | My role | Core skills |
|---|---|---|---|---|
| [**CCNA Case Study 2025**](ccna-case-study-2025) | Apr 2025 | 5 routers, 1 switch, 4 sites + ISP | **Solo**: design, build, verification, presentation | VLSM · OSPF + RIP redistribution · GRE over IPsec · NAT/PAT · ACLs · DHCP · VLANs · NTP/Syslog/SNMP |
| [**North Pole**](north-pole) | Nov – Dec 2025 | ~30 switches, 5 teams | **Core layer**: Catalyst core, OSPF area 0, BFD, Meraki onboarding | Three-tier campus · multi-area OSPF · BFD · HSRP · EtherChannel · Meraki MS · wireless |
| [**Project Lattice**](project-lattice) | Oct – Nov 2025 | 4 networks + MPLS hub | **Team 3**: EIGRP intranet, hub hand-off, transit for Team 4 | MPLS/LDP core · EIGRP · OSPF area types + virtual links · RIP · redistribution · ASA |
| [**Project Meridian**](project-meridian) | Sep – Oct 2025 | 5 sites, IPv6-only | **Bangkok site**: subnetting, BGP → OSPFv3, GRE, IPsec | IPv6 · OSPFv3 · RIPng · BGP · HSRP · EtherChannel · GRE · IPsec |

## What I did on each

**CCNA Case Study 2025** — everything. I designed the VLSM plan and logical topology, prototyped it in Packet Tracer over seven revisions, built it on ISR 4221 routers, ran a 50-test verification matrix with screenshots, and presented it. → [showcase](ccna-case-study-2025)

**North Pole** — on the core team I:
- racked the core switches and ran the SFP fiber links between them
- built OSPF area 0 with BFD for fast failover
- configured every distribution-facing interface
- got the Meraki switches into the Meraki cloud by trunking the campus VLAN and switching them to Layer 3 with DHCP

→ [core page](north-pole/core-rudolph)

**Project Lattice** — on Team 3 I:
- installed the serial cards
- built the cable to the hub
- worked out the EIGRP → OSPF redistribution and the hub firewall's ICMP rules with the hub team
- brought Team 4 into the WAN through our network
- brought our two branch sites in with RIP → EIGRP, since their Catalyst 1000s don't support EIGRP

→ [team page](project-lattice/team3)

**Project Meridian** — on the Bangkok team I:
- subnetted the site
- found that the IP cameras wouldn't auto-configure on our /80 subnets and renumbered the site to /64s
- moved the site from BGP to OSPFv3 when redistribution wouldn't work
- brought up the GRE tunnels to Vegas and worked on IPsec with Nogales

→ [site page](project-meridian/sites/bangkok)

Teammates' names, paperwork and credentials are left out of every project. Configs are otherwise as they ran.
