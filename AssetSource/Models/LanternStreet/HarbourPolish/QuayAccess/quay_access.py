"""Lantern Street's ashlar extension, gated service stair and working tender berth, in cm."""
import math
from cottage_joinery import west_cottage
from harbour_polish import mooring
from lantern_scenery import quay_stone

HEAD=(2631.,118.,165.)
TOE=(2817.,506.,36.)
WATER=-6.
COUNT=10
DX,DY,DZ=(b-a for a,b in zip(HEAD,TOE))
LENGTH=math.hypot(DX,DY)
SIDE=(-DY/LENGTH,DX/LENGTH)


def paving(g):
    left=-1451
    for j in (-2,-1):
        quay_stone(g,j,left)
        start=-820+j*520
        for k in range(7):
            x=start+37.5+k*74
            lo=max(left,x-36);hi=x+36
            if lo<hi:
                g.panel((lo+hi)/2,146,-2.15,hi-lo,242,3,'sand' if (j+k)%4 else 'tile',1)
    # The road module ends at y=141. The return remains under the cottage foundations at y=157.
    g.panel(-1135.5,202,-38.3,631,133,74,'stone')


def box(g,xy,z0,z1,colour):
    """Solid timber from four counterclockwise plan corners; all joints remain volumetric."""
    lo=[(x,y,z0) for x,y in xy];hi=[(x,y,z1) for x,y in xy]
    g.face(hi,colour);g.face(list(reversed(lo)),colour)
    for i,a in enumerate(lo):
        j=(i+1)%len(lo)
        g.face([a,lo[j],hi[j],hi[i]],colour)


def beam(g,a,b,width,depth,colour):
    dx=b[0]-a[0];dy=b[1]-a[1];q=math.hypot(dx,dy)
    nx=-dy/q*width/2;ny=dx/q*width/2
    ring=[(a[0]-nx,a[1]-ny,a[2]),(b[0]-nx,b[1]-ny,b[2]),(b[0]+nx,b[1]+ny,b[2]),(a[0]+nx,a[1]+ny,a[2])]
    top=[(x,y,z+depth/2) for x,y,z in ring];bottom=[(x,y,z-depth/2) for x,y,z in ring]
    g.face(top,colour);g.face(list(reversed(bottom)),colour)
    for i in range(4):j=(i+1)%4;g.face([bottom[i],bottom[j],top[j],top[i]],colour)


def stair_pos(t,side=0,up=0):
    return HEAD[0]+t*DX+side*SIDE[0],HEAD[1]+t*DY+side*SIDE[1],HEAD[2]+t*DZ+up


def board(g,t0,t1,width,top,depth,colour):
    plan=[stair_pos(t,s)[:2] for t,s in [(t0,-width/2),(t1,-width/2),(t1,width/2),(t0,width/2)]]
    box(g,plan,top-depth,top,colour)


def ripples(g,x,y,rx,ry):
    # Two broken bands at the pile and keel waterline, in the paper sea's own palette.
    for start,end in ((.10,1.21),(2.2,3.03),(3.31,4.29),(5.12,5.80)):
        for i in range(7):
            a=start+(end-start)*i/7;b=start+(end-start)*(i+1)/7
            plan=[(x+rx*s*math.cos(t),y+ry*s*math.sin(t),WATER) for s,t in ((.95,a),(1.04,a),(1.04,b),(.95,b))]
            g.face(plan,'mist')


def tender(g):
    x,y=2948,449
    outline=[(-88,0),(-58,-17),(5,-23),(57,-17),(75,-11),(75,11),(57,17),(5,23),(-58,17)]
    profiles=[]
    for scale,beam_scale,z in ((.82,.48,-8),(.94,.81,-2),(1,1,9),(1.01,1.02,12)):
        profiles.append([(x+u*scale,y+v*beam_scale,z+max(0,(abs(u)-35)*.095)) for u,v in outline])
    for i,colour in enumerate(('sea_dark','teal','oak')):
        for j in range(len(outline)):
            k=(j+1)%len(outline)
            g.face([profiles[i][j],profiles[i][k],profiles[i+1][k],profiles[i+1][j]],colour)
    # The dark floor, interior lining, two thwarts and mooring line make this a working berth.
    inner=[(x+u*.90,y+v*.80,3) for u,v in outline]
    g.face(inner,'wood')
    for i in range(len(outline)):
        k=(i+1)%len(outline)
        g.face([profiles[-1][i],profiles[-1][k],inner[k],inner[i]],'walnut')
    for xx,ww in ((-28,35),(31,32)):g.panel(x+xx,y,10,10,ww,3,'oak',1)
    for i in range(7):
        t=i/7;v=(i+1)/7
        pos=lambda s:(2902-34*s,485-35*s,45-32*s-7*math.sin(s*math.pi))
        beam(g,pos(t),pos(v),1.8,1.7,'rope')
    ripples(g,x+2,y,90,28)


def jetty(g):
    # Level top bearing sits under the masonry lip. Toe overlaps the pier deck at its exact height.
    board(g,-.055,.002,72,165.55,8,'wood')
    for i in range(COUNT):
        t0=i/COUNT;t1=(i+1)/COUNT
        h=HEAD[2]+(i+1)*DZ/COUNT+(.55 if i==COUNT-1 else 0.)
        for k in range(2):
            start=t0+k*.5/COUNT
            board(g,start,start+.5/COUNT-.001,70,h,5,'oak' if (i+k)%4 else 'wood')
        board(g,t0-.001,t0+.003,68,h+abs(DZ)/COUNT,abs(DZ)/COUNT+3,'wood')
    for side in (-30,30):
        beam(g,stair_pos(-.042,side,-13),stair_pos(1.035,side,-13),7.6,14,'walnut')
        for t in (0,.3,.6,1):
            x,y,z=stair_pos(t,side)
            g.panel(x,y,z+24,6.8,6.8,83,'wood',1)
        beam(g,stair_pos(-.023,side,63),stair_pos(1.02,side,63),6.5,4.8,'oak')
    # A second bent supports the long span on the lower stone quay at y=328.
    for side in (-26,26):
        xx,yy,zz=stair_pos(.53,side,-8)
        g.panel(xx,yy,zz/2,10,10,zz,'walnut',1)
    # T-shaped landing: beams, plank deck, four cutwater piles and fender caps.
    for y in (482,531):g.panel(2860,y,25,160,9,13,'walnut',1.5)
    for i in range(10):
        g.panel(2787+i*16.2,508,33.2,15.6,67,5.6,'oak' if i%4 else 'wood',.8)
    for xx in (2803,2920):
        for yy in (483,530):
            g.panel(xx,yy,(WATER+36)/2,9,9,36-WATER,'wood',.8)
            g.panel(xx,yy,WATER+2.5,9.7,9.7,6,'sea_dark',.6)
            ripples(g,xx,yy,13,8)
    for xx in (2902,2925):
        g.lathe(xx,486,[(36,3.7),(39,3.8),(42,3),(45,4),(47,4)],'char',12)
    tender(g)
    # This guard follows the actual collision face at x=2630 across the player lane.
    # The jetty is a harbour workers' access behind it. The chapter exit is the door.
    for y in (-65,40,115):
        g.panel(2634,y,201.5,8,8,73,'walnut',1)
        g.panel(2634,y,238,10,10,4,'bronze',1)
    for z in (203,231):
        g.panel(2634,25,z,6,187,5,'oak',1)


def groups():
    west=west_cottage(paving)
    dock=mooring((-1190,724,1884))
    jetty(dock)
    return west,dock

