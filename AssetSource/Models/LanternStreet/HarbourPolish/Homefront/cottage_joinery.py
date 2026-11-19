"""Original cut-paper harbour cottage and kitchen joinery, authored in world centimetres."""
import math
from paper_mesh import PaperGroup


def sash(g,x,z,w,h):
    # Inset glass with a deeper reveal, timber sill, meeting rail and two linen curtains.
    g.panel(x,158,z,w+13,14,h+14,'walnut',1.7)
    g.panel(x,148,z,w,5,h,'window',1.5)
    for s in (-1,1):
        left=x+s*(w*.5-1)
        g.outline([(left,z+h*.47),(left-s*w*.25,z+h*.47),(left-s*w*.12,z+h*.06),
                   (left-s*w*.06,z-h*.42),(left,z-h*.46)],143,2,'linen')
        g.panel(x+s*(w/2+1),142,z,4,9,h+5,'oak')
    for dz in (-h/2,0,h/2):
        g.panel(x,138,z+dz,w+7,9,4.3,'wood')
    g.panel(x,138,z,3.6,8,h,'wood')
    g.panel(x,142,z-h*.5-5,w+20,29,6,'stone',2)
    g.panel(x,151,z+h*.5+7,w+17,18,7,'chalk',1)


def west_cottage():
    g=PaperGroup('MooringHouseWest',(-975,55,100))
    # The paving extends to y=267, under the cottage's foundations at y=157..279.
    g.panel(-1123,63,-45,655,408,88,'stone')
    for row in range(3):
        for i in range(10):
            x=-1449+(i+.5)*67-(row%2)*23
            g.panel(x,-141,-10-row*25,65,8,23,'sand' if row==0 else 'slate',1.2)
    for i in range(10):
        g.panel(-1417+i*65,61,-.8,64.2,405,2,'tile' if i%3==0 else 'sand')
    g.panel(-1069,218,-9,516,122,58,'stone')
    for i in range(13):
        g.panel(-1306+i*39.6,154,12,38,13,20,'stone' if i%3 else 'sand',1.7)
    g.panel(-1069,220,143.5,516,99,255,'plaster')
    # A simple rendered facade with a stone skirt and return quoins. Timber fascias follow the roof.
    g.panel(-1069,168,31,517,11,17,'stone',1.5)
    for x in (-1319,-818):
        for i in range(8):
            g.panel(x,166,49+28*i,14+9*(i%2),13,24,'chalk',1.5)
    left,right=-1341,-798
    for end in (left+5,right-5):
        pts=[(end,143,270),(end,260,361),(end,354,269)]
        g.face(pts if end==right-5 else list(reversed(pts)),'wood')
    # Eight overlapping slate courses climb a real slope towards the ridge.
    for row in range(8):
        y=138+row*15
        z=269+row*11.3
        for i in range(13):
            l=max(left,left+i*47-(row%2)*23);r=min(right,left+(i+1)*47-(row%2)*23-1)
            if l>=r:continue
            g.face([(l,y,z),(r,y,z),(r,y+17,z+13),(l,y+17,z+13)],('slate','blue','roof','slate','blue')[(i*13+row*7)%5])
            g.face([(l,y,z-1.5),(r,y,z-1.5),(r,y,z),(l,y,z)],'roof')
    g.panel(-1069,145,268,540,19,11,'walnut',1.5)
    g.panel(-1069,255,359,545,15,7,'slate',2)
    g.face([(left,256,359),(right,256,359),(right,358,273),(left,358,273)],'roof')
    # Brick chimney emerges from the roof, with a stone cap and one chimney pot.
    g.panel(-1136,238,363,35,28,67,'brick_dark',1)
    for k in range(4):
        g.panel(-1136,222,338+k*13,35,3,1.7,'stone')
    g.panel(-1136,238,397,42,35,7,'stone',1)
    g.lathe(-1136,238,[(399,8),(403,8),(416,6),(420,8)],'brick',12)
    sash(g,-1199,154,88,103)
    sash(g,-889,155,80,102)
    # The path runs across the front of this scenery door; the gameplay door is inside.
    dx=-1030
    g.panel(dx,157,116,112,19,214,'walnut',3)
    g.panel(dx,143,113,93,9,198,'teal',2)
    for x in (dx-48,dx+48):g.panel(x,138,114,8,16,204,'wood',1)
    g.panel(dx,137,217,107,17,10,'oak',2)
    g.panel(dx,137,169,62,6,51,'window',2)
    for x in (dx-32,dx,dx+32):g.panel(x,131,169,3.3,6,52,'oak')
    for z in (143,169,195):g.panel(dx,131,z,65,6,3.5,'oak')
    for x in (dx-20,dx+20):
        g.panel(x,136,78,32,5,84,'deep',1.6)
        g.panel(x,131.5,78,26,3.5,75,'teal',1.5)
    g.panel(dx+34,128,104,5,4,13,'bronze',1)
    g.disc(dx+34,123,105,3.2,3.2,6,'brass')
    g.panel(dx,147,8,122,58,16,'stone',2.5)
    g.panel(dx,110,3.4,133,32,7,'stone',2)
    # Narrow rain canopy: roof slab physically meets the facade and two curved timber brackets.
    for x in (dx-51,dx+51):
        g.panel(x,154,218,6,14,28,'walnut')
        g.face([(x-2,153,205),(x-2,119,228),(x-2,153,228)],'wood')
        g.face([(x+2,153,228),(x+2,119,228),(x+2,153,205)],'wood')
    g.face([(dx-67,111,229),(dx+67,111,229),(dx+67,171,246),(dx-67,171,246)],'slate')
    g.panel(dx,112,227,136,7,5,'walnut',1)
    # One firmly grounded clay pot beside the sash, with six cut-paper stems.
    px,py=-951,147
    g.lathe(px,py,[(0.25,8),(3,9),(23,15),(27,16),(30,15)],'brick',14)
    for i,(ox,oz) in enumerate([(-14,43),(-21,51),(-7,57),(8,52),(17,39),(12,58)]):
        g.stroke(px,30,px+ox,oz,py-2,1.8,1.7,'leaf')
        g.outline([(px+ox,oz-1),(px+ox-5,oz+6),(px+ox-2,oz+12),(px+ox+3,oz+5)],py-2-i*.16,1.3,'grass' if i in (1,3) else 'leaf')
    # Preserve the physical lane's west-end railing and rear anchor with full depth.
    for y in (-46,118):
        g.panel(-802,y,48,11,11,98,'walnut',1.5)
        g.panel(-802,y,97,13,13,4,'brass',1)
    g.panel(-802,36,76,7,169,9,'oak',1)
    return g


def kitchen_fitout(g):
    # A pegged, wall-mounted plate rack: the shelf back overlaps the teal plaster.
    cx=33
    g.panel(cx,218,246,96,20,69,'wood',2)
    g.panel(cx,205,247,85,6,55,'walnut',1)
    for side in (-1,1):
        x=cx+side*47
        g.panel(x,196,245,7,48,73,'oak',1.5)
        g.panel(x,209,204,7,38,18,'wood',1)
        g.disc(x,171,268,1.8,1.8,2,'bronze',10)
    g.panel(cx,198,213,106,51,7,'oak',1.5)
    g.panel(cx,198,281,107,49,6,'wood',1.5)
    g.panel(cx,195,277,103,51,3,'oak',1)
    # These supper plates stand in the groove behind a low retaining rail. Their bases
    # meet its deck; alternate depths let their rims overlap like stacked crockery.
    for xx,yy,r,tone in [(cx-23,201,19,'chalk'),(cx-2,196,22,'linen'),(cx+21,193,18,'chalk')]:
        zz=216.5+r
        g.disc(xx,yy,zz,r,r,2.7,tone,28)
        g.disc(xx,yy-1.0,zz,r*.77,r*.77,1.25,'dress',28)
        g.disc(xx,yy-1.8,zz,r*.69,r*.69,1,'cream',28)
    g.panel(cx,175,222,92,4,4.5,'oak',1)
    for xx in (cx-31,cx-10,cx+10,cx+31):g.panel(xx,176,220,2.4,4,9,'oak')
    # A modest dark-cased kitchen regulator balances the rack. Its hands and brass
    # parts stay inside the case, distinct from the playable candle and letter.
    x=158
    g.panel(x,218,292,48,20,84,'walnut',4)
    g.panel(x,203,293,43,12,76,'oak',3)
    g.panel(x,195,279,31,6,40,'walnut',2)
    g.stroke(x,285,x,269,190,1.8,2,'bronze')
    g.disc(x,189,268,5.6,5.6,2,'brass',18)
    g.panel(x,196,254,50,20,6,'wood',2)
    g.panel(x,197,332,56,21,7,'wood',2)
    g.disc(x,190,308,17.5,17.5,3,'bronze',32)
    g.disc(x,187.7,308,15.7,15.7,2.5,'linen',32)
    for i in range(12):
        dx=math.sin(i*math.pi/6);dz=math.cos(i*math.pi/6)
        g.stroke(x+dx*12.4,308+dz*12.4,x+dx*14.1,308+dz*14.1,187,1.2,1,'walnut')
    g.stroke(x,308,x-7,314,186,1.8,1.2,'char')
    g.stroke(x,308,x+7.5,317,185.8,1.45,1.2,'char')
    g.disc(x,185.2,308,1.9,1.9,1.2,'bronze',10)

