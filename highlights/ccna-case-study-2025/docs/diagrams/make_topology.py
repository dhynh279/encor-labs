# Generates topology.svg: python3 make_topology.py topology.svg
import sys
W,H=1320,880
o=[]
A=o.append
A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Helvetica, Arial, sans-serif">')
A('<rect width="100%" height="100%" fill="#ffffff"/>')
A('<defs><style>.t{font-size:13px;fill:#1f2937}.s{font-size:11.5px;fill:#374151}.h{font-size:15px;font-weight:700;fill:#111827}.lbl{font-size:11px;fill:#111827}.ip{font-size:11px;fill:#1d4ed8;font-family:Consolas,Menlo,monospace}</style></defs>')
def box(x,y,w,h,title,lines,fill="#eef2ff",stroke="#4f46e5"):
    A(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    ty=y-h/2+20
    A(f'<text class="h" x="{x}" y="{ty}" text-anchor="middle">{title}</text>')
    for i,l in enumerate(lines):
        A(f'<text class="s" x="{x}" y="{ty+17*(i+1)}" text-anchor="middle">{l}</text>')
def line(x1,y1,x2,y2,color="#111827",w=2,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}/>')
def tag(x,y,text,cls="ip",anchor="middle"):
    w=len(text)*6.7+10
    xx = x-w/2 if anchor=="middle" else (x if anchor=="start" else x-w)
    A(f'<rect x="{xx}" y="{y-9}" width="{w}" height="17" rx="3" fill="#ffffff" fill-opacity="0.92"/>')
    tx = x if anchor=="middle" else (xx+5 if anchor=="start" else x-5)
    A(f'<text class="{cls}" x="{tx}" y="{y+4}" text-anchor="{anchor}">{text}</text>')
RED="#dc2626"
SYS=(110,240); SNMP=(110,380); BEL=(400,300); LIM=(400,575); LLAN=(130,690)
COL=(690,480); SWX=(690,705); ISP=(1030,170); WEB=(1200,60); GER=(1150,480); GLAN=(1150,705)
A('<rect x="30" y="150" width="840" height="625" rx="28" fill="#f3f4f6" stroke="#9ca3af" stroke-dasharray="6 5"/>')
A('<text class="h" x="52" y="180" fill="#4b5563">OSPF process 50 · area 0</text>')
def pt(a,b,t): return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)
def link(a,b,color,la=None,lb=None,mid=None,ta=0.3,tb=0.7,w=2.5,dy=0):
    line(a[0],a[1],b[0],b[1],color,w)
    if la: x,y=pt(a,b,ta); tag(x,y+dy,la,"ip")
    if lb: x,y=pt(a,b,tb); tag(x,y+dy,lb,"ip")
    if mid: x,y=pt(a,b,0.5); tag(x,y-dy if dy else y,mid,"lbl")
# tunnel band
A(f'<line x1="{COL[0]}" y1="{COL[1]}" x2="{GER[0]}" y2="{GER[1]}" stroke="#7c3aed" stroke-opacity="0.18" stroke-width="22"/>')
line(COL[0],COL[1],GER[0],GER[1],"#7c3aed",2,"7 5")
tag((COL[0]+GER[0])/2,COL[1]-44,"Tunnel0 · GRE over IPsec","lbl")
tag((COL[0]+GER[0])/2,COL[1]-26,"RIPv2 · 1.1.1.0/30","lbl")
tag((COL[0]+GER[0])/2,COL[1]+28,"Colorado .1 · Germany .2","ip")
# serial
link(BEL,COL,RED,"S0/1/0 .249","S0/1/1 .250",None,0.32,0.66)
x,y=pt(BEL,COL,0.5); tag(x+62,y-14,"172.26.255.248/30","lbl")
link(BEL,LIM,RED,"S0/1/1 .253","S0/1/0 .254",None,0.33,0.67)
tag(BEL[0]-75,(BEL[1]+LIM[1])/2,"172.26.255.252/30","lbl")
link(COL,ISP,RED,"S0/1/0 209.165.200.1","S0/1/1 .2","209.165.200.0/30",0.33,0.74)
link(GER,ISP,RED,"S0/1/0 209.165.100.2","S0/1/0 .1",None,0.3,0.72)
x,y=pt(GER,ISP,0.5); tag(x+70,y,"209.165.100.0/30","lbl")
# ethernet
link(BEL,SYS,"#111827","G0/0/0 .237",None,None,0.6,0,2)
link(BEL,SNMP,"#111827","G0/0/1 .241",None,None,0.6,0,2)
link(LIM,LLAN,"#111827","G0/0/0 .1",None,None,0.55,0,2)
link(COL,SWX,"#111827","G0/0/1 trunk · .100 .200 .300 .401",None,None,0.5,0,2)
link(ISP,WEB,"#111827","G0/0/0 10.0.0.1",None,None,0.5,0,2)
link(GER,GLAN,"#111827","G0/0/0 172.26.0.1/22",None,None,0.5,0,2)
# devices
box(*BEL,180,72,"BELGUM",["RID 20.20.20.20"])
box(*LIM,180,72,"LIMA",["RID 30.30.30.30"])
box(*COL,220,100,"COLORADO (HQ)",["RID 10.10.10.10","OSPF ⇄ RIP · NTP master","PAT pool 55.69.241.0/29"])
box(*ISP,190,64,"ISP",["static NAT for web server"],"#f9fafb","#6b7280")
box(*GER,210,92,"GERMANY",["RIPv2 over tunnel","PAT 77.100.10.1","GERMANY-ACL (in, LAN)"])
box(*WEB,170,56,"Web server (IIS)",["10.0.0.2 ⇄ 64.100.231.1"],"#f9fafb","#6b7280")
box(*SYS,130,50,"Syslog",["172.26.255.238"],"#ecfdf5","#059669")
box(*SNMP,130,50,"SNMP",["172.26.255.242"],"#ecfdf5","#059669")
box(*LLAN,150,50,"Lima LAN",["172.26.7.0/26"],"#ecfdf5","#059669")
box(*SWX,250,104,"COLO-LAN switch",["VLAN 100 · 172.26.4.0/24","VLAN 200 · 172.26.5.0/24","VLAN 300 · 172.26.6.0/24","mgmt VLAN 401 · 172.26.255.246"],"#ecfdf5","#059669")
box(*GLAN,190,50,"Germany LAN",["172.26.0.0/22 · 512 hosts"],"#ecfdf5","#059669")
# legend
lx,ly=900,808
A(f'<rect x="{lx-10}" y="{ly-22}" width="400" height="86" rx="6" fill="#ffffff" stroke="#d1d5db"/>')
line(lx,ly,lx+40,ly,RED,2.5); A(f'<text class="t" x="{lx+50}" y="{ly+4}">serial link</text>')
line(lx,ly+22,lx+40,ly+22,"#111827",2); A(f'<text class="t" x="{lx+50}" y="{ly+26}">Ethernet</text>')
A(f'<line x1="{lx}" y1="{ly+44}" x2="{lx+40}" y2="{ly+44}" stroke="#7c3aed" stroke-opacity="0.18" stroke-width="14"/>'); line(lx,ly+44,lx+40,ly+44,"#7c3aed",2,"7 5")
A(f'<text class="t" x="{lx+50}" y="{ly+48}">GRE/IPsec tunnel (carried over the ISP links)</text>')
A('</svg>')
open(sys.argv[1],'w').write('\n'.join(o))
