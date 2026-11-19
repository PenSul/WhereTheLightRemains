"""Editable set design for Lantern Street. Dimensions are in centimetres."""
import math
import random
from paper_mesh import PaperGroup

def quay_stone(g,j,left_limit=None):
    """A 520cm street module, including its faced seawall and footing, on the original street grid."""
    x=-820+j*520
    def panel(cx,y,z,w,d,h,color,bevel=0):
        if left_limit is not None:
            left=max(cx-w/2,left_limit);right=cx+w/2
            if right-left<.2:return
            cx=(left+right)/2;w=right-left
        g.panel(cx,y,z,w,d,h,color,bevel)
    panel(x+260,-4,-44,521,290,86,'stone')
    for k in range(7):
        panel(x+37.5+k*74,-146,-15,72,15,23,'chalk' if (j+k)%4 else 'sand',2)
        panel(x+37.5+k*74,-145,-46,71,16,32,'slate' if (j+k)%3 else 'navy',2)
        panel(x+37.5+k*74,-56,-2,72,158,3,'tile' if (j+k)%4==1 else 'sand',1)
    panel(x+260,-117,-83,520,65,18,'deep')
    panel(x+260,-249,-106,523,240,5,'water')
    for k in range(13):
        rx=(k*53+j*31)%494
        panel(x+rx,-210-(k*19)%113,-103,16+(k*13)%55,2+(k%4),.9,'mist' if k%4==0 else 'sea_dark')

def build(kitchen_fitout=None):
    groups=[];solids=[];stations=[]
    def group(name,x=0,y=0,z=0,tags=(),folder='Set'):
        g=PaperGroup(name,(x,y,z),tags,folder);groups.append(g);return g
    def collision(name,x,y,z,w,d,h,tags=()):
        solids.append(dict(name=name,location=(x,y,z),size=(w,d,h),tags=list(tags)))
    def station(i,title,x,z=92):
        stations.append(dict(id=i,title=title,location=(x,0,z)))

    def pane(g,x,y,z,w,h,lit=False,shutters=True):
        g.panel(x,y,z,w+18,10,h+18,'sand',5);g.panel(x,y-7,z,w+5,8,h+5,'walnut')
        g.panel(x,y-12,z,w-4,5,h-4,'amber' if lit else 'glass')
        g.panel(x,y-16,z,4,4,h,'oak');g.panel(x,y-16,z+3,w,4,4,'oak')
        g.panel(x,y-11,z-h/2-8,w+25,25,9,'chalk',2)
        if shutters:
            for side in [-1,1]:
                sx=x+side*(w*.5+22)
                g.panel(sx,y-7,z,29,8,h+10,'leaf',3)
                for k in range(6):g.panel(sx,y-13,z-h*.42+k*h*.16,23,4,3,'wood',1)
    def picture(g,x,y,z,w,h,portrait=False):
        g.panel(x,y,z,w+8,7,h+8,'walnut',3);g.panel(x,y-5,z,w,4,h,'brass',2);g.panel(x,y-9,z,w-6,4,h-6,'linen')
        if portrait:
            for dx,dz,col in [(-.16,0,'deep'),(.14,-.02,'dress')]:
                g.disc(x+dx*w,y-13,z+dz*h+.13*h,.09*w,.12*h,2,'portrait')
                g.outline([(x+(dx-.17)*w,z-h*.32),(x+(dx-.14)*w,z-.07*h),(x+dx*w,z+.02*h),(x+(dx+.11)*w,z-.10*h),(x+(dx+.17)*w,z-.32*h)],y-14,2,col)
        else:
            g.panel(x,y-13,z-.08*h,w*.78,2,h*.4,'water');g.outline([(x-w*.3,z-h*.08),(x-w*.12,z+h*.14),(x+w*.18,z-h*.08)],y-16,1,'slate')
    def chair(g,x,y,z):
        g.panel(x,y,z+49,44,44,7,'oak',3)
        for dx in (-16,16):
            for dy in (-15,15):g.panel(x+dx,y+dy,z+24,5,5,48,'wood')
        g.panel(x,y+16,z+88,40,4,8,'oak',2)
        for dx in (-16,16):g.panel(x+dx,y+16,z+68,5,5,53,'wood')
        g.panel(x,y+16,z+70,33,3,6,'wood')
    def candle(g,x,y,z,flame=True,scale=1.0):
        s=scale
        def cyl(profile,col):g.lathe(x,y,[(z+h*s,r*s) for h,r in profile],col)
        cyl([(0,6),(1,9),(3,8),(5,3),(10,3),(12,5)],'bronze')
        cyl([(10,3.8),(24,3.8),(25,3.2)],'wax')
        g.panel(x,y,z+25.9*s,.9*s,1.3*s,3.3*s,'char')
        if flame:
            g.outline([(x-2.8*s,z+29*s),(x-1*s,z+33*s),(x+1.8*s,z+37*s),(x+3*s,z+30*s),(x+.5*s,z+26*s)],y-1.4*s,2.5*s,'gold')
            g.disc(x,y-2*s,z+29*s,1.2*s,2.7*s,1*s,'flame',8)
    def potted(g,x,y,z,s=1):
        g.lathe(x,y,[(z,12*s),(z+25*s,18*s),(z+29*s,19*s),(z+33*s,17*s)],'brick',10)
        for dx,h in [(-24,65),(-9,80),(7,67),(24,72),(2,91)]:
            g.stroke(x,z+31*s,x+dx*s,z+h*s,y,1.5*s,2*s,'leaf')
            g.outline([(x+.55*dx*s,z+(h-20)*s),(x+(dx-5)*s,z+(h-9)*s),(x+dx*s,z+h*s),(x+(dx+6)*s,z+(h-8)*s)],y-1,3*s,'leaf')
    def book(g,x,y,z,w,h,color):
        g.panel(x,y,z+h/2,w,28,h,'ivory')
        g.panel(x,y,z+h-1,w+3,31,3,color,1);g.panel(x,y,z+1,w+3,31,3,color,1)
        g.panel(x-w*.46,y,z+h/2,4,31,h,color)
    def crate(g,x,y,z,w,d,h):
        g.panel(x,y,z+h/2,w,d,h,'wood',3)
        for i in range(5):
            px=x-w*.5+(i+.5)*w/5
            g.panel(px,y-d*.5-1,z+h/2,w/5-2,5,h-6,'oak' if i%3==0 else 'wood')
        for dx in (-w*.44,w*.44):g.panel(x+dx,y-d*.5-7,z+h/2,w*.09,9,h,'oak')
        for zz in (z+4,z+h-4):g.panel(x,y-d*.5-7,zz,w,10,9,'oak')
        g.stroke(x-w*.40,z+8,x+w*.40,z+h-8,y-d*.5-8,8,6,'sand')
        for dx in (-w*.43,w*.43):
            for zz in (z+5,z+h-5):g.disc(x+dx,y-d*.5-13,zz,1.7,1.7,1,'ink',8)
    def letter(g,x,y,z,w=33,h=43):
        g.outline([(x-.5*w,z-.5*h),(x+.38*w,z-.5*h),(x+.5*w,z-.37*h),(x+.48*w,z+.5*h),(x-.52*w,z+.46*h)],y,3,'cream')
        g.panel(x,y-2,z+h*.44,2.4,2,2.4,'bronze')
        for i,f in enumerate([.40,.70,.64,.62,.37]):
            g.panel(x-w*.34+f*w/2,y-2,z+h*(.23-i*.12),f*w,1,1.1,'portrait')
        g.disc(x+.21*w,y-3,z-.32*h,3,3,1,'brick',9)
    def arch(g,x,y,z,w,h,c):
        # lintel and voussoirs are separate folded stones surrounding a real aperture.
        r=w/2;cy=z+h-r
        for side in [-1,1]:g.panel(x+side*(r+5),y, z+(h-r)/2,11,16,h-r,c,2)
        for i in range(11):
            a=i*math.pi/11+.014;b=(i+1)*math.pi/11-.014
            p=[(x+(r+dr)*math.cos(t),cy+(r+dr)*math.sin(t)) for dr,t in [(0,a),(11,a),(11,b),(0,b)]]
            g.outline(p,y-8,16,c)
    def shop(g,x,y,w,h,wall,style):
        g.panel(x,y+22,h/2,w,48,h,wall,4);g.panel(x,y-8,17,w,16,34,'stone')
        g.panel(x,y-9,h-5,w+12,18,12,'chalk');g.panel(x,y+9,h+11,w+22,30,19,'roof')
        for j in (-1,0,1):pane(g,x+j*w*.285,y-10,h*.75,w*.12,h*.20,False,j!=0)
        if style=='shop':
            g.panel(x,y-13,102,w*.75,18,155,'walnut');g.panel(x,y-24,105,w*.69,7,139,'glass')
            for j in (-1,0,1):g.panel(x+j*w*.245,y-32,107,7,8,149,'wood')
            g.panel(x,y-31,143,w*.715,8,6,'oak');g.panel(x,y-32,26,w*.8,25,14,'chalk',2)
            # Paper awning with alternating cut scallops, hem projects towards camera.
            for i in range(9):
                a=x-w*.42+w*.84*i/9;b=a+w*.84/9
                col='cream' if i%2==0 else 'teal'
                g.face([(a,y-24,216),(b,y-24,216),(b,y-76,184),(a,y-76,184)],col)
                g.outline([(a,186),(b,186),(b,170),(b-5,165),(a+5,165),(a,170)],y-78,3,col)
            for dx in (-w*.385,w*.385):g.stroke(x+dx,165,x+dx,208,y-30,5,6,'bronze')
            # Apothecary silhouettes and a paper sailboat in the window.
            for i in range(7):
                rx=x-w*.28+i*13
                g.lathe(rx,y-31,[(35,4),(50,5),(53,3),(60+i%3*4,2)],'deep')
            g.outline([(x+18,52),(x+82,52),(x+73,43),(x+32,43)],y-35,5,'deep')
            g.stroke(x+53,50,x+53,116,y-37,2,2,'walnut')
            g.outline([(x+52,112),(x+24,58),(x+52,58)],y-33,2,'linen')
            g.outline([(x+56,105),(x+78,60),(x+56,60)],y-33,2,'sand')
        else:
            arch(g,x,y-12,0,103,184,'chalk')
            g.panel(x,y-4,81,98,10,162,'wood',2)
            for i in range(6):g.panel(x-40+i*16,y-12,82,14,5,160,'walnut' if i%3==0 else 'wood')
            g.disc(x+32,y-18,80,4.8,4.8,2,'brass')
            for side in [-1,1]:pane(g,x+side*w*.32,y-10,116,w*.13,89,False,False)
        for dx in (-w*.48,w*.48):
            for k in range(7):g.panel(x+dx,y-7,55+k*47,19 if k%2 else 28,9,12,'sand',1)

    # Distant sea theatre: skyline built as overlapping cardstock silhouettes.
    for past in [False,True]:
        label='Past' if past else 'Present'
        g=group('Harbour'+label,1000,1250,140,('Phase.'+label,),'01 Harbour')
        rng=random.Random(130)
        g.panel(900,2300,620,7800,14,2700,'dawn' if past else 'sky')
        g.panel(900,1900,85,6800,16,235,'peach' if past else 'light_sky')
        g.disc(1500,1860,305,50,50,4,'cream' if past else 'cloud',32)
        for k in range(25):
            x=-2000+k*270
            g.disc(x,1850,270+rng.randint(-10,100),rng.randint(43,104),rng.randint(3,12),3,'linen' if past else 'cloud',16)
        for j in range(37):
            x=-1700+j*157+rng.randrange(55);w=rng.randrange(80,210);h=rng.randrange(35,115)
            g.panel(x,1450,78+h/2,w,30,h,'distance' if not past else 'slate')
            g.outline([(x-w*.62,78+h),(x-w*.12,78+h+18),(x+w*.14,78+h+31),(x+w*.58,78+h)],1426,28,'distance' if not past else 'slate')
            if j%6==3:
                g.panel(x,1442,144+h,17,16,82,'slate');g.outline([(x-13,175+h),(x,203+h),(x+13,175+h)],1425,17,'slate')
            for k in range(3):g.panel(x+(k-1)*w*.23,1423,80+h*.6,4,3,7,'amber' if not past else 'linen')
        g.panel(1200,950,-95,6500,8,380,'water_warm' if past else 'water')
        for k in range(88):
            x=rng.randrange(-1600,4200);z=rng.randrange(-143,83);w=rng.randrange(10,100)
            g.panel(x,928,z,w,2,2,'sea_light' if k%3==0 else 'sea_dark',.5)
        for x,s in [(-500,.7),(680,1.0),(1460,.73),(2620,1.22),(3380,.72)]:
            water=49
            g.outline([(x-47*s,water+5*s),(x+58*s,water+7*s),(x+39*s,water-5*s),(x-33*s,water-6*s)],764,19,'deep')
            g.stroke(x+3*s,water,x+4*s,water+81*s,760,2*s,3,'walnut')
            g.outline([(x+6*s,water+76*s),(x+37*s,water+13*s),(x+7*s,water+13*s)],766,2,'sand' if past else 'mist')
            g.stroke(x-37*s,water+6*s,x+4*s,water+73*s,763,1.2*s,2,'slate')

    # The stage floor is a separate collision body; visual paving has no gameplay collision.
    collision('Walkable promenade',880,0,-45,3650,320,90)
    # The stop sits inside the visible stone quay (its leftmost paving starts at -820).
    collision('Home left return',-803,0,200,35,320,460)
    collision('Street terminus',2650,0,280,40,320,650)
    for j in range(7):
        g=group(f'QuaySection{j:02}',-820+j*520,0,0,folder='02 Quay')
        quay_stone(g,j)
    # Interior cross-section: open front, furniture behind the walk line. Warm/nave window lights signal Past.
    g=group('HomeTimber',-260,130,150,folder='03 Home')
    # Frame a real opening. The player now sees the moving harbour through the window.
    g.panel(-604.5,261,236,401,33,472,'plaster')
    g.panel(87.5,261,236,455,33,472,'plaster')
    g.panel(-272,261,85,267,33,170,'plaster')
    g.panel(-272,261,404.5,267,33,135,'plaster')
    for side,cx,w in [('L',-685,242),('R',74,346)]:g.panel(cx,233,220,w,13,364,'teal')
    g.panel(-280,227,120,1118,18,120,'wood')
    for x in range(-773,285,71):g.panel(x,213,97,58,8,90,'oak',4)
    g.panel(-257,204,150,1115,16,10,'sand');g.panel(-250,198,22,1120,30,18,'walnut')
    for x in [-801,-495,-48,300]:g.panel(x,191,220,19,32,440,'walnut')
    g.panel(-251,184,426,1130,55,25,'oak');g.panel(-251,206,460,1150,67,44,'roof',4)
    for xx in (-411,-133):g.panel(xx,185,253,13,18,180,'oak',2)
    for zz in (169,337):g.panel(-272,185,zz,292,18,12,'oak',2)
    for past in [False,True]:
        pg=group('HomeWindow'+('Past' if past else 'Present'),-320,153,180,('Phase.'+('Past' if past else 'Present'),),'03 Home')
        for xx in (-401,-143):pg.panel(xx,158,253,3,4,154,'sand' if past else 'slate')
    for x in [-404,-335,-267,-198,-139]:g.panel(x,145,253,5,10,159,'oak')
    g.panel(-271,145,263,271,10,5,'oak');g.panel(-272,143,170,299,22,9,'chalk',2)
    # The wedding print and one harbour postcard share a wall rail and little brass hooks.
    g.panel(-655,213,292,225,13,5,'walnut',1)
    for px,pz,pw,ph,portrait in [(-596,224,73,80,True),(-712,227,66,44,False)]:
        g.disc(px,197,287,2.2,2.2,1,'brass')
        for side in (-1,1):g.stroke(px,287,px+side*pw*.39,pz+ph*.43,197,1.3,2,'rope')
        picture(g,px,190,pz,pw,ph,portrait)
    if kitchen_fitout:
        kitchen_fitout(g)
    else:
        g.panel(15,164,186,90,23,10,'oak');g.panel(15,165,229,90,24,8,'wood')
        for i in range(6):
            g.panel(-17+i*11,157,203,8,17,28+4*(i%3),['slate','brick','sand'][i%3],1)
    g.panel(-330,108,82,178,81,10,'oak',4);g.panel(-330,109,75,161,66,8,'walnut')
    for xx in [-394,-266]:
        for yy in [80,138]:g.panel(xx,yy,39,8,8,78,'wood',2)
    g.panel(-330,97,88,118,76,2,'dress')
    for x in [-383,-282]:
        g.lathe(x,106,[(89,11),(91,15),(92,15)],'cream')
        g.lathe(x+9,125,[(89,4),(100,5.2),(102,4.9)],'chalk')
    chair(g,-222,83,0);chair(g,-453,86,0);potted(g,29,135,0,.85)
    # Main doorway faces the camera so the letter is visible from either side.
    # The walk-through doorway is a separate transverse set piece. The back wall
    # continues naturally behind it, leaving no second painted door in this spot.
    gd=group('HomeDoorClosed',237,98,100,('Gate.Door',),'03 Home')
    gd.panel(237,98,97,110,12,194,'wood',3)
    for i in range(5):gd.panel(193+i*22,89,96,19,5,183,'walnut' if i%3==1 else 'wood',2)
    gd.disc(276,83,88,5,5,2,'brass')
    # A writing cabinet supports both the wick and the letter. Its back stiles
    # continue behind the pinned sheet so the join reads from the side camera.
    for x in (108,190):
        for y in (66,119):
            g.panel(x,y,15,10,11,30,'walnut',1)
    g.panel(149,93,48,92,62,59,'wood',1.5)
    for x in (107,191):
        g.panel(x,62,49,7,7,58,'walnut',1)
    for z in (35,62):
        g.panel(149,60,z,73,6,23,'oak',2)
        for x in (128,170):
            g.disc(x,55,z+1,2.3,2.3,3,'bronze',10)
    g.panel(149,94,80,98,72,7,'walnut',1.5)
    g.panel(149,94,85,102,76,3,'oak',1)
    for x in (114,184):
        g.panel(x,109,124,7,9,88,'walnut',1)
    g.panel(149,109,127,67,8,81,'wood',1)
    g.panel(149,102.5,127,62,5,76,'oak',1)
    g.panel(149,106,167,77,12,5,'walnut',1)
    letter(g,149,99,135,34,43)
    length=math.hypot(72,164)
    collision('Closed house threshold',325,0,126,72+8*164/length,164+8*72/length,250,['Gate.Door'])
    solids[-1].update(local_size=(length,8,250),yaw=math.degrees(math.atan2(164,72)))
    station(1,'Table candle',-320);station(2,'Door letter',225);station(7,'Family photograph',-580)
    g=group('CandleMemory',-320,90,88,('Phase.Past',),'03 Home');candle(g,-321,92,90,True,1.60)
    g=group('DoorCandleEcho',162,77,86,('Echo.Letter',),'03 Home');candle(g,162,73,86.5,True,1.45)
    from mara_supper import mara_at_supper
    from rear_surfaces import rear_surfaces
    groups.extend([mara_at_supper(),*rear_surfaces()])
    g=group('HomeExterior',365,130,200,folder='04 Lantern Street')
    shop(g,440,201,232,379,'brick','door')
    for x in [357,532]:potted(g,x,144,0,.70)
    g=group('LanternBrackets',620,100,170,folder='04 Lantern Street')
    for x in (547,1401,2287):
        base=165 if x==2287 else 0
        g.panel(x,118,144+base,10,14,277,'walnut',2);g.panel(x+23,117,275+base,56,13,8,'oak',2)
        g.stroke(x+2,246+base,x+23,272+base,111,5,8,'wood')
        g.stroke(x+46,272+base,x+46,256+base,115,2.2,4,'bronze')
    g=group('OvergrownReeds',840,0,77,('Gate.Grass',),'04 Lantern Street')
    rng=random.Random(474)
    for i in range(42):
        x=776+rng.random()*110;y=-30+rng.random()*132;h=56+rng.random()*105
        tip=x+rng.uniform(-49,58);w=rng.uniform(3,7)
        g.outline([(x-w,0),(x-w*.8,h*.25),(x+(tip-x)*.24-w*.6,h*.61),(tip,h),(x+(tip-x)*.25+w*.6,h*.57),(x+w,h*.19),(x+w,1)],y,1.6,['grass','leaf','reed'][i%3])
        if i%6==0:g.disc(tip,y-1,h-5,3.8,9,2,'reed',8)
    collision('Tall grass obstruction',842,0,133,36,310,266,['Gate.Grass'])
    station(3,'Dry grass',730)
    g=group('GrassCandleEcho',755,15,0,('Echo.Grass',),'04 Lantern Street');candle(g,755,15,0,True,1.45)
    g=group('Apothecary',1275,185,180,folder='04 Lantern Street');shop(g,1334,244,377,412,'brick','shop')
    # A boarded recess joins the display to the shop instead of suspending a picture over water.
    g.panel(1048,244,122,245,24,240,'wood',3)
    for i in range(12):
        g.panel(941+i*19.55,228,122,18.5,6,218,'teal' if i%4 else 'dress',1)
    for x in (930,1167):g.panel(x,216,119,11,23,239,'walnut',2)
    g.panel(1048,213,239,254,34,12,'oak',2)
    g.panel(1048,227,248,266,49,10,'roof',3)
    g.panel(1048,215,19,240,13,24,'stone',2)
    for dx in (-22,22):g.stroke(1043,207,1043+dx,188,209,1.5,2,'rope')
    g.panel(1039,147,62,201,94,10,'wood',4);g.panel(1039,173,32,181,41,61,'walnut')
    candle(g,1003,131,67,True,1.2);candle(g,1053,133,67,True,1.2)
    picture(g,1043,218,162,70,61,True)
    g.panel(1123,217,186,55,33,9,'oak',2);potted(g,1118,207,191,.41)
    g=group('ThirdCandleEcho',1101,130,66,('Echo.Optional',),'04 Lantern Street')
    candle(g,1101,131,67,True,1.2)
    station(4,'Three candles',1150)
    g=group('ShippingCrateMemory',1520,84,73,('Phase.Past',),'04 Lantern Street')
    crate(g,1520,108,0,111,80,140);station(5,'Shipping crate',1520)
    g=group('LanternStreetSundries',1610,115,55,folder='04 Lantern Street')
    for x,h in [(1630,56),(1683,45)]:
        g.lathe(x,145,[(0,17),(h*.18,20),(h*.62,22),(h,17)],'wood')
        for z in [h*.22,h*.73]:g.lathe(x,145,[(z,21),(z+3,21)],'bronze')
    for px in (1746,1781):g.panel(px,205,37,7,12,74,'oak',1)
    g.panel(1763,197,94,58,9,81,'walnut',3)
    letter(g,1761,186,91,42,55)
    station(6,'Missing step',1920)
    g=group('RememberedStaircase',1918,20,62,('Memory.Stair',),'05 Raised landing')
    for i in range(8):
        h=20.625*(i+1);x=1789+i*35.8
        g.panel(x,16,h/2,36.3,98,h,'wood')
        g.panel(x,15,h-2,37.5,103,4,'oak',1)
        g.panel(x-17.4,15,h-10,2,100,13,'walnut')
    for i in (0,2,5,7):
        x=1789+i*35.8;h=20.625*(i+1)
        g.panel(x,61,h+38,5,6,77,'walnut',1)
    g.stroke(1787,96,2042,243,61,6,7,'oak')
    # A manifested shipping crate includes attached short packing cases for a safe ascent.
    # Once latched, permanent quay steps occupy the same route in both phases.
    for name,tags,crate_style in [('ManifestedCrateStair',('Echo.Platform',),True),('PermanentQuaySteps',('Route.Platform',),False)]:
        g=group(name,1930,0,67,tags,'05 Raised landing')
        for i,(x,w,h) in enumerate([(1820,91,40),(1892,76,81),(1965,78,122),(2023,47,145)]):
            if crate_style:crate(g,x,0,0,w,92,h)
            else:
                g.panel(x,0,h/2,w,104,h,'stone')
                g.panel(x,0,h-2,w+1,107,4,'sand',1)
                for tier in range(1,int(h//24)+1):
                    g.panel(x,-52,tier*23-9,w-4,1.2,1.3,'slate')
                    g.panel(x+w*(.17 if tier%2 else -.22),-52.2,tier*23-20,1.4,1.0,21,'slate')
            collision(name+f' tread {i+1}',x,0,h/2,w+2,179,h,tags)
    collision('Upper landing floor',2350,0,82.5,580,290,165)
    g=group('UpperQuay',2350,72,90,folder='05 Raised landing')
    g.panel(2350,0,77,580,278,154,'slate')
    for row in range(3):
        for i in range(8):
            x=2090+i*73;g.panel(x,-142,28+row*51,71,13,48,'stone' if (i+row)%4 else 'sand',3)
    g.panel(2350,0,156,582,294,18,'chalk',2)
    for i in range(8):g.panel(2094+i*73,-2,164,71,286,2,'sand',1)
    g=group('LandingFacade',2330,162,280,folder='05 Raised landing')
    g.panel(2385,218,348,468,29,365,'blue');g.panel(2385,195,518,478,25,19,'chalk',4)
    g.panel(2385,206,549,497,59,46,'roof',3)
    for x in (2205,2332,2495):pane(g,x,190,445,57,74,False,x==2205)
    g.panel(2428,183,259,99,9,188,'wood',2);arch(g,2428,179,167,108,198,'chalk')
    for i in range(5):g.panel(2389+i*19,173,245,16,5,149,'walnut' if i%2 else 'wood')
    g.disc(2462,165,242,5.7,5.7,2,'brass')
    # Sunburst carved over the landing door, repeated on the notebook's lamp.
    for i in range(9):
        a=i*math.pi/8;g.stroke(2428+22*math.cos(a),367+22*math.sin(a),2428+36*math.cos(a),367+36*math.sin(a),169,3,4,'brass')
    g.panel(2205,153,282,78,8,101,'oak',3);letter(g,2205,144,281,60,82)
    g.panel(2078,88,221,8,19,109,'oak',1);g.panel(2076,72,258,24,9,17,'brass',2)
    g.stroke(2071,258,2085,282,63,4,5,'bronze')
    potted(g,2313,125,165,.63)
    station(7,'Family photograph',-580) if not any(s['id']==7 for s in stations) else None
    station(8,'Neighbourhood notice',2200,256);station(9,'Street exit',2510,256);station(10,'Landing latch',2060,256)
    return groups,solids,stations

