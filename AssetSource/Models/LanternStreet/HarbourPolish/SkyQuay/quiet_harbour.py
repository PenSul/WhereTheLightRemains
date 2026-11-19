"""Cut-paper wharf. Only the surface finish, apron joint and new bird silhouettes are authored here."""
from paper_mesh import PaperGroup


def wharf():
    front=PaperGroup('UpperQuay',(2350,72,90))
    front.panel(2350,0,77,580,278,154,'slate')
    for row in range(3):
        for i in range(8):
            front.panel(2090+i*73,-142,28+row*51,71,13,48,'stone' if (i+row)%4 else 'sand',3)
    # Previously the cream cap and eight differently coloured flags shared a top plane at 165.
    # Recess the mortar and let the 4cm stone flags provide the sole visible finish at floor height.
    front.panel(2350,-.5,154.25,582,293,13.5,'chalk',2)  # top 161, rear edge at 146
    for i in range(8):
        front.panel(2094+i*73,-.5,163,71,289,4,'tile' if i in (2,6) else 'sand',1)
    back=PaperGroup('HighStepsFloorReturn',(2350,204,98))
    back.panel(2350,231,77.75,584,170,166.5,'slate')    # y146..316, top 161; no overlap
    for i in range(8):
        back.panel(2094+i*73,231,163,71,167,4,'tile' if i%3==0 else 'sand',1)
    back.panel(2350,228,168,584,19,6,'stone')
    return front,back


def terns():
    g=PaperGroup('HarbourTernsHigh')
    # Three different wing poses, each with a slim swept wingtip and an ivory underside.
    for x,z,s,bank in ((-52,13,.68,0),(-5,0,1,1),(53,18,.79,2)):
        outlines=[
            [(-20,4),(-12,8),(-4,6),(1,1),(6,5),(15,8),(20,7),(12,5),(5,1),(2,-2),(-2,-2),(-7,3),(-12,5)],
            [(-22,7),(-14,10),(-8,9),(0,3),(3,1),(8,4),(17,5),(22,3),(14,3),(8,1),(3,-2),(-2,-2),(-7,3),(-14,7)],
            [(-18,5),(-11,7),(-4,4),(0,0),(5,3),(13,7),(20,8),(13,4),(7,1),(2,-2),(-2,-2),(-7,2),(-12,4)]]
        g.outline([(x+a*s,z+b*s) for a,b in outlines[bank]],0,1.6,'navy')
        g.outline([(x-3*s,z),(x+2*s,z-.8*s),(x+8*s,z+1.9*s),(x+4*s,z-1.3*s),(x,z-2.4*s)],-.3,.6,'linen')
    return g

