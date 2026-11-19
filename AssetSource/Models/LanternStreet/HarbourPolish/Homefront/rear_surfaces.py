"""Rear floor returns for the photographed paper sets. Source units are centimetres.

Front playing surfaces end at y=141 or y=147 on the upper landing. The soles
continue behind the furthest near facade with an intentional underlap at each end.
The distant harbour is a different parallax plane and is visible through the alleys.
"""
from paper_mesh import PaperGroup


def group(name,x,y,z=0):
    return PaperGroup(name,(x,y,z),('Set.RearFloor',),'02 Quay')


def rear_surfaces():
    home=group('KitchenFloorReturn',-296,206,-18)
    # Quarter-sawn boards run from the kitchen skirting right under the stage.
    home.panel(-269,205,-31,1204,258,60,'wood')        # y 76..334; top -1
    for row in range(4):
        y=116+row*55
        left=-870;idx=0
        while left<332:
            width=min((126 if row%2 and idx==0 else 267),332-left)
            home.panel(left+width/2,y,-1.30,width-1.8,53,1.8,'wood' if (idx+row)%4 else 'oak')
            left+=width;idx+=1
    home.panel(-269,262,-9,1203,11,25,'walnut')
    home.panel(-269,261,2,1203,16,5,'oak')
    street=group('QuaysideFootwayReturn',1579,210,-22)
    street.panel(1579,211,-35,2508,270,68,'stone')     # y 76..346; top -1
    for row,(y,d) in enumerate(((125,81),(207,80),(292,86))):
        left=326;idx=0
        while left<2832:
            width=min((65 if row%2 and idx==0 else 141),2832-left)
            if width>2:
                street.panel(left+width/2,y,-1.65,width-2,d,2.55,'tile' if (idx+2*row)%5==0 else 'sand')
            left+=width;idx+=1
    # This low edge belongs to the wharf. The open silhouette above it keeps the sea visible.
    street.panel(1579,338,-19,2506,19,52,'slate')
    street.panel(1579,337,6.75,2506,22,5,'stone')
    landing=group('HighStepsFloorReturn',2350,204,98)
    landing.panel(2350,204,79,584,224,169,'slate')      # y 92..316; top 163.5
    for i in range(8):
        landing.panel(2095+73*i,206,163.9,71.8,220,1.0,'sand' if i%3 else 'tile')
    landing.panel(2350,228,166.5,584,19,9,'stone')
    return [home,street,landing]


# The layout intentionally shares continuous overlap with the existing quay while
# covering the old gap under the kitchen, shop and high-step noticeboard.
CHECKS=(('KitchenFloorReturn',141,244.5),('QuaysideFootwayReturn',141,266),('HighStepsFloorReturn',147,232.5))

