"""Editable original harbour tern, authored at true bird scale; shoulder and wrist have separate pivots."""
import math
from paper_mesh import PaperGroup


def ring(x,w,h,z=0):
    return [(x,w*math.cos(2*math.pi*i/12),z+h*math.sin(2*math.pi*i/12)) for i in range(12)]


def torso():
    g=PaperGroup('TernBody')
    sections=[(-12,.65,1.,-.5),(-8,2.35,2.,0),(-3,3.1,3.3,.3),(2,3.25,3.4,.8),(5.5,2.4,2.6,1.6),(7.5,2.3,2.5,2.7),(10.5,1.85,2.1,2.8),(12,1.2,1.1,2.5),(17,.13,.16,2.1)]
    rings=[ring(*row) for row in sections]
    for n,(lo,hi) in enumerate(zip(rings,rings[1:])):
        for i in range(12):
            j=(i+1)%12
            shade='mist' if 0<=i<6 else 'linen'
            if 4<=n<=6 and 0<=i<=5:shade='char'
            if n==7:shade='copper'
            g.face([lo[i],lo[j],hi[j],hi[i]],shade)
    g.face(list(reversed(rings[0])),'navy');g.face(rings[-1],'char')
    # The two tapered tail streamers form a recognisable fork even during a glide.
    for side in (-1,1):
        g.face([(-7,0,-.25),(-9,side*2.1,.45),(-21,side*6.4,1.35),(-14,side*1.4,.15)],'slate')
    return g


def sheet(g,base,upper,under):
    # Thin volumetric card preserves both light dorsal and slightly darker ventral surfaces.
    for i in range(len(base)-2):
        g.face([base[0],base[i+1],base[i+2]],upper)
        g.face([(x,y,z-.42) for x,y,z in (base[0],base[i+2],base[i+1])],under)
    for a,b in zip(base,base[1:]+base[:1]):
        g.face([a,(a[0],a[1],a[2]-.42),(b[0],b[1],b[2]-.42),b],'slate')


def wing(hand,outer):
    side=1 if hand=='Port' else -1
    g=PaperGroup('Tern'+hand+('Wrist' if outer else 'Shoulder'))
    if outer:
        # Long narrow primary feathers sweep back. A dark cap occupies the distal third only.
        root=[(2.6,0,.15),(.6,7,1.3),(-5.1,16.3,1.2),(-8.1,16.2,.5),(-4.5,5.5,-.15),(-3.7,0,0)]
        tip=[(-5.1,16.3,1.2),(-18,26.2,-.55),(-14.5,20.3,.1),(-8.1,16.2,.5)]
        sheet(g,[(x,side*y,z) for x,y,z in root],'slate','mist')
        sheet(g,[(x,side*y,z) for x,y,z in tip],'navy','slate')
    else:
        # Camber is modelled as a shallow ridge running out from the shoulder.
        lead=[(3.,0,.1),(3.6,7,1.4),(1.4,14.8,1.9),(-1.2,18.4,.9),(-3.5,18.1,.8),(-2.9,7.2,1.2),(-2.0,0,.4)]
        rear=[(-2.0,0,.4),(-2.9,7.2,1.2),(-3.5,18.1,.8),(-8.2,18,.5),(-7.6,10,.05),(-6.7,4.4,-.3),(-5.3,.2,-.3)]
        sheet(g,[(x,side*y,z) for x,y,z in lead],'mist','slate')
        sheet(g,[(x,side*y,z) for x,y,z in rear],'slate','window')
    return g


def pieces():
    return {'FlightBody':torso(),**{hand+joint:wing(hand,joint=='Wrist') for hand in ('Port','Starboard') for joint in ('Shoulder','Wrist')}}


def armature():
    # Unreal uses minus the paper set's depth coordinate.
    return {'FlightBody':(None,(0.,0.,0.)),'PortShoulder':('FlightBody',(1.5,-2.,1.3)),
            'StarboardShoulder':('FlightBody',(1.5,2.,1.3)),'PortWrist':('PortShoulder',(-3.9,-18.1,.8)),
            'StarboardWrist':('StarboardShoulder',(-3.9,18.1,.8))}

