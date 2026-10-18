# Verification

Results as recorded in the presentation (slides 26–45), with the screenshot for each test. All tests were run from Windows hosts on the real hardware.

## Colorado VLAN 100

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/vlan-100/to-isp.png) |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-lima.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-snmp.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-syslog.png) |
| Germany | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-germany.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-vlan-200.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/vlan-100/to-vlan-300.png) |

## Colorado VLAN 200

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/vlan-200/to-isp.png) |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/vlan-200/to-lima.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/vlan-200/to-snmp.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/vlan-200/to-syslog.png) |
| Germany | ICMP | PASS | — |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/vlan-200/to-vlan-100.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/vlan-200/to-vlan-300.png) |

## Colorado VLAN 300

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/vlan-300/to-isp.png) |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-lima.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-snmp.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-syslog.png) |
| Germany | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-germany.png) |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-vlan-100.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/vlan-300/to-vlan-200.png) |

## Lima LAN

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/lima/to-isp.png) |
| Germany | ICMP | PASS | [screenshot](../evidence/pings/lima/to-germany.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/lima/to-snmp.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/lima/to-syslog.png) |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/lima/to-vlan-100.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/lima/to-vlan-200.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/lima/to-vlan-300.png) |

## Syslog server (Belgum)

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/syslog-server/to-isp.png) |
| Germany | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-germany.png) |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-lima.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-snmp.png) |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-vlan-100.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-vlan-200.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/syslog-server/to-vlan-300.png) |

## SNMP server (Belgum)

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | HTTP | PASS | [screenshot](../evidence/pings/snmp-server/to-isp.png) |
| Germany | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-germany.png) |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-lima.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-syslog.png) |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-vlan-100.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-vlan-200.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/snmp-server/to-vlan-300.png) |

## Germany LAN

| Destination | Protocol | Result | Evidence |
|---|---|---|---|
| ISP web server | ICMP | FAIL (blocked by GERMANY-ACL, as designed) | [screenshot](../evidence/pings/germany/to-isp.png) |
| ISP web server | HTTP | PASS | — |
| Lima | ICMP | PASS | [screenshot](../evidence/pings/germany/to-lima.png) |
| SNMP server | ICMP | PASS | [screenshot](../evidence/pings/germany/to-snmp.png) |
| Syslog server | ICMP | PASS | [screenshot](../evidence/pings/germany/to-syslog.png) |
| VLAN 100 | ICMP | PASS | [screenshot](../evidence/pings/germany/to-vlan-100.png) |
| VLAN 200 | ICMP | PASS | [screenshot](../evidence/pings/germany/to-vlan-200.png) |
| VLAN 300 | ICMP | PASS | [screenshot](../evidence/pings/germany/to-vlan-300.png) |

## Other checks

| Check | Result | Evidence |
|---|---|---|
| ISAKMP SA Colorado ↔ Germany | QM_IDLE / ACTIVE on both ends | [Colorado](../evidence/ipsec/colorado-isakmp-sa.png) · [Germany](../evidence/ipsec/germany-isakmp-sa.png) |
| IPsec SAs | Packets encrypted/decrypted, ESP SAs ACTIVE, PFS group 19 | [Colorado](../evidence/ipsec/colorado-ipsec-sa.png) · [Germany](../evidence/ipsec/germany-ipsec-sa.png) |
| NAT translations | PAT entries on Colorado (`55.69.241.1`) and Germany (`77.100.10.1`), static NAT on the ISP | [Colorado](../evidence/nat/colorado.png) · [Germany](../evidence/nat/germany.png) · [ISP](../evidence/nat/isp.png) |
| Web server through static NAT | IIS page loads at `64.100.231.1` | [screenshot](../evidence/misc/isp-web-server.png) |
| Telnet from Germany to the ISP | Refused (ACL) | [screenshot](../evidence/misc/germany-telnet-blocked.png) |
| ISP → private addresses | Unreachable (no route to `172.26.x.x` from outside) | [screenshot](../evidence/pings/isp/capture.png) |
| ISP routing table | Static routes to the NAT pools; no route to any private `172.26.x.x` address | [screenshot](../evidence/pings/isp/iproute.png) |
| Syslog | Lima's messages arrive in Kiwi Syslog | [screenshot](../evidence/pings/syslog-server/kiwi-syslog.png) |
| SNMP traps | Config-change and syslog traps arrive from the router | [screenshot](../evidence/pings/snmp-server/capture.png) |
| DHCP | Pools configured at Colorado, Germany and Lima; test hosts got addresses from them (e.g. Germany host `172.26.0.22`, above the excluded range) | [Colorado](../evidence/dhcp/colorado.png) · [Germany](../evidence/dhcp/germany.png) · [Lima](../evidence/dhcp/lima.png) |
| VLANs | `show vlan brief` on COLO-LAN | [screenshot](../evidence/misc/show-vlan-brief.png) |
| OSPF / RIP | Routing-process configuration on each router | [routing/](../evidence/routing/) |
