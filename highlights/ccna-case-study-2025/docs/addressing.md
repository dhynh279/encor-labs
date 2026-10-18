# Interface Addressing

From the final running-configs.

## COLORADO (HQ, OSPF RID 10.10.10.10)

| Interface | Address | Description |
|---|---|---|
| Gi0/0/1 | — (`ip nat inside`) | Trunk to COLO-LAN |
| Gi0/0/1.100 | `172.26.4.1/24` | VLAN 100 |
| Gi0/0/1.200 | `172.26.5.1/24` | VLAN 200 |
| Gi0/0/1.300 | `172.26.6.1/24` | VLAN 300 |
| Gi0/0/1.401 | `172.26.255.245/30` | Management (switch SVI `.246`) |
| S0/1/0 | `209.165.200.1/30` | To ISP · `ip nat outside` · `crypto map GREMAP` |
| S0/1/1 | `172.26.255.250/30` | To Belgum · `ip nat inside` |
| Tunnel0 | `1.1.1.1/30` | GRE to Germany (src S0/1/0 → dst `209.165.100.2`) |
| Lo0 | `10.10.10.10/32` | Router ID |

## GERMANY (branch)

| Interface | Address | Description |
|---|---|---|
| Gi0/0/0 | `172.26.0.1/22` | LAN · `ip nat inside` · `GERMANY-ACL in` |
| S0/1/0 | `209.165.100.2/30` | To ISP · `ip nat outside` · `crypto map GREMAP` |
| Tunnel0 | `1.1.1.2/30` | GRE to Colorado (dst `209.165.200.1`) |

## BELGUM (services, OSPF RID 20.20.20.20)

| Interface | Address | Description |
|---|---|---|
| Gi0/0/0 | `172.26.255.237/30` | Syslog server (`.238`) |
| Gi0/0/1 | `172.26.255.241/30` | SNMP server (`.242`) |
| S0/1/0 | `172.26.255.249/30` | To Colorado |
| S0/1/1 | `172.26.255.253/30` | To Lima |
| Lo0 | `20.20.20.20/32` | Router ID |

## LIMA (branch, OSPF RID 30.30.30.30)

| Interface | Address | Description |
|---|---|---|
| Gi0/0/0 | `172.26.7.1/26` | LAN |
| S0/1/0 | `172.26.255.254/30` | To Belgum |
| Lo0 | `30.30.30.30/32` | Router ID |

## ISP

| Interface | Address | Description |
|---|---|---|
| Gi0/0/0 | `10.0.0.1/8` | Web server LAN (`10.0.0.2` ↔ `64.100.231.1`) · `ip nat inside` |
| S0/1/0 | `209.165.100.1/30` | To Germany · `ip nat outside` |
| S0/1/1 | `209.165.200.2/30` | To Colorado · `ip nat outside` |

## DHCP pools

| Pool | Network | Excluded | Default router | Domain |
|---|---|---|---|---|
| COLO-VLAN100 | `172.26.4.0/24` | `.1–.10` | `172.26.4.1` | COLO.com |
| COLO-VLAN200 | `172.26.5.0/24` | `.1–.10` | `172.26.5.1` | COLO.com |
| COLO-VLAN300 | `172.26.6.0/24` | `.1–.10` | `172.26.6.1` | COLO.com |
| GERMANY-DHCP | `172.26.0.0/22` | `.0.1–.0.20` | `172.26.0.1` | GERM.com |
| LIMA | `172.26.7.0/26` | `.1–.10` | `172.26.7.1` | LIMA.com |
