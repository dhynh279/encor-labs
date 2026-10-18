# Lab 01 — Layer 2

## Topology
- SW1 Gi1/0/1-2 <-> SW2 Gi1/0/1-2 : LACP Po1 trunk
- SW1 Gi1/0/3 <-> SW3 Gi1/0/1 : trunk (root guard on SW1)
- SW2 Gi1/0/3 <-> SW3 Gi1/0/2 : trunk (root guard on SW2)
- PC10 -> SW3 Gi1/0/10 (V10, 192.168.10.11)
- PC20 -> SW3 Gi1/0/20 (V20, 192.168.20.11)
- PC10-B -> SW2 Gi1/0/10 (V10, 192.168.10.12)

## Verification

## Break/fix
1. LACP passive/passive:
2. Native VLAN mismatch:
3. BPDU guard err-disable:
