"""Original cut-paper enamel waymarker for Lantern Street. Dimensions are centimetres."""
from paper_mesh import PaperGroup


def upper_quay_sign():
    g = PaperGroup('UpperQuayWaymarker')
    # The cast-iron shoe and oak upright sit on the quay behind the walking lane.
    g.panel(0, 4, 4, 20, 14, 8, 'slate', 2)
    g.panel(0, 4, 43, 10, 8, 80, 'wood', 1)
    g.panel(-3, -.25, 37, 2, 1, 60, 'oak')
    g.panel(0, -1, 95, 94, 8, 58, 'walnut', 5)
    g.panel(0, -5.5, 95, 90, 2, 54, 'brass', 4)
    g.panel(0, -7, 95, 86, 2, 50, 'navy', 3)
    for x in [-38,38]:
        for z in [76,114]:
            g.disc(x, -8.6, z, 1.2, 1.2, .5, 'brass', 8)
    # One continuous painted silhouette: three ascending treads, with a slim up arrow.
    g.outline([(-28,76),(-28,82),(-14,82),(-14,91),(0,91),(0,100),
               (14,100),(14,109),(29,109),(29,114),(9,114),(9,105),
               (-5,105),(-5,96),(-19,96),(-19,87),(-33,87),(-33,76)], -8.8,.5,'cream')
    g.outline([(-31,99),(-29,97),(-12,110),(-13,104),(-9,105),
               (-8,116),(-19,115),(-20,112),(-15,113)],-8.8,.5,'cream')
    return g
