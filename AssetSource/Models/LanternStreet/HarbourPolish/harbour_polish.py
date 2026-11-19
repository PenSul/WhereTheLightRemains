"""Lantern Street scenic flats, mooring furniture and moving paper-cut silhouettes in cm."""
import math
from paper_mesh import PaperGroup


def panorama():
    group=PaperGroup('PaintedHarbour', (0,1750,0))
    # Mirror the far ends of the panorama to continue the opposite bank beyond the camera.
    # The shoreline is fixed at z=47. Extra painted sky and sea cover tall viewports.
    sections=[(2300,0.),(975,.055),(446,.25),(47,.712),(-190,.92),(-750,.99),(-1800,1.)]
    for left,right,reverse in [(-5350,-1800,True),(-1800,1750,False),(1750,5300,True)]:
        for (top,vtop),(bottom,vbottom) in zip(sections,sections[1:]):
            group.face([(left,1750,bottom),(right,1750,bottom),(right,1750,top),(left,1750,top)],'sky')
            a,b=(1.,0.) if reverse else (0.,1.)
            group.uvs[-4:]=[(a,vbottom),(b,vbottom),(b,vtop),(a,vtop)]
    return group


def western_quay():
    g=PaperGroup('MooringHouseWest',(-975,55,100))
    g.panel(-1131,4,-47,633,281,90,'stone')
    for row in range(3):
        for i in range(9):
            g.panel(-1410+i*70,-141,-9-row*26,68,9,23,'slate' if row!=0 else 'sand',1.5)
    for i in range(9):
        g.panel(-1410+i*70,0,-.8,68,277,2,'tile' if i%3==0 else 'sand')
    # An attached net shed closes the back of the kitchen. The low return rail defines the walk limit.
    g.panel(-1048,189,132,469,23,266,'blue',2)
    for i in range(19):
        x=-1265+i*24
        g.panel(x,171,132,22.5,7,245,'teal' if i%4 else 'dress',1)
    for zz in (19,244):g.panel(-1046,156,zz,473,12,13,'walnut',2)
    g.outline([(-1298,259),(-1040,341),(-801,259)],182,23,'slate')
    g.stroke(-1299,258,-1040,342,162,12,18,'roof')
    g.stroke(-1040,342,-795,258,162,12,18,'roof')
    # A sliding door, its top runner and an irregularly coiled line read as a working quay.
    g.panel(-1080,149,98,121,14,191,'wood',2)
    for i in range(6):g.panel(-1132+i*20.4,139,98,17,4,182,'oak' if i%3==0 else 'wood',1)
    g.stroke(-1134,20,-1027,175,134,7,5,'walnut')
    g.panel(-1087,128,200,162,8,5,'ink')
    for x in (-1153,-1072):g.disc(x,125,193,4.5,4.5,3,'ink',12)
    for xx in (-923,-890):
        g.disc(xx,142,145,19,25,2,'rope',18);g.disc(xx,139,146,13,18,3,'teal',17)
    for y in (-46,118):
        g.panel(-802,y,48,11,11,98,'walnut',1.5)
        g.panel(-802,y,97,13,13,4,'brass',1)
    g.panel(-802,36,76,7,169,9,'oak',1)
    for x in (-1370,-1270):
        g.lathe(x,50,[(0,12),(3,15),(26,8),(31,14),(34,14)],'char',18)
    return g


def mooring():
    g=PaperGroup('HarbourMoorings',(550,490,0))
    for base in (-1190,724,1884,2860):
        g.panel(base,510,28,151,64,10,'wood',1)
        for i in (-1,0,1):
            x=base+62*i
            g.panel(x,480,-1,7,8,80,'walnut',1);g.panel(x,480,36,9,10,5,'sand',1)
        for i in range(8):g.panel(base-63+i*18,501,35,16,57,2,'oak')
        for a,b in ((base-62,base),(base,base+62)):
            for i in range(7):
                s=i/7;t=(i+1)/7
                g.stroke(a+s*(b-a),43-8*math.sin(s*math.pi),a+t*(b-a),43-8*math.sin(t*math.pi),485,1.5,2,'rope')
    return g


def skiff():
    g=PaperGroup('TideSkiff')
    pts=[(-72,11),(-56,-3),(-38,-10),(30,-11),(57,-4),(72,12),(43,6),(0,3),(-43,6)]
    g.outline(pts,0,14,'deep')
    g.stroke(-66,9,-40,5,-1,2.8,2,'sand');g.stroke(-40,5,39,5,-1,2.8,2,'sand');g.stroke(39,5,70,12,-1,2.8,2,'sand')
    g.stroke(3,4,4,98,7,2.8,2,'walnut')
    g.stroke(-60,10,4,95,5,1,2,'rope');g.stroke(4,94,64,10,5,1,2,'rope')
    g.outline([(2,82),(-39,16),(2,12)],6,1.2,'linen')
    g.outline([(7,80),(38,19),(8,15)],7,1,'sand')
    g.panel(-23,3,10,24,5,5,'brick',1)
    return g


def silvering():
    g=PaperGroup('HarbourSilvering')
    for i in range(62):
        x=-1560+(i*493)%5150;z=-91+(i*59)%121;w=7+(i*13)%33
        g.outline([(x-w,z),(x-w*.55,z+1.15),(x+w*.65,z+1.5),(x+w,z+.6),(x+w*.32,z-.4)],0,1,'mist' if i%4 else 'sea_light')
    return g


def gulls():
    g=PaperGroup('HarbourTerns')
    for x,z,s in [(-43,7,.68),(-5,0,1),(52,13,.82)]:
        outline=[(-15,1),(-10,4.5),(-5,3.9),(0,0),(3,1.3),(10,3),(15,2.3),(11,1),(5,0),(1,-2.1),(-2,-1.6),(-7,2)]
        g.outline([(x+dx*s,z+dz*s) for dx,dz in outline],0,1,'slate')
    return g


def detail_groups():return [western_quay(),mooring(),skiff(),silvering(),gulls(),panorama()]

