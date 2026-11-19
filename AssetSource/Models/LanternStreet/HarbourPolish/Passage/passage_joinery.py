"""Hinged cross-passage joinery for the waterfront cottage, in centimetres."""
import math
from paper_mesh import PaperGroup
SPAN=math.hypot(72.,164.)
YAW=math.degrees(math.atan2(164.,72.))
HINGE=(289.,-82.,0.)
def door():
    g=PaperGroup('AcrossPassageOakLeaf');w=SPAN
    # Faces total 8cm, exactly matching the rotated closed blocker. Decorative
    # boards sit within that envelope, with a single clear handle on both sides.
    g.panel(w/2,0,126,w,5.8,250,'walnut',1.8)
    for i in range(9):
        x=(i+.5)*w/9
        g.panel(x,-3.1,126,w/9-.7,1.6,245,'wood' if i%4 else 'oak',1)
        g.panel(x,3.1,126,w/9-.7,1.6,245,'wood' if i%4 else 'walnut',1)
    for side in (-1,1):
        for x in (8,w-8):g.panel(x,side*3.5,126,11,.9,247,'oak',1)
        for z in (12,130,236):g.panel(w/2,side*3.5,z,w-8,.9,12,'oak',1)
        for z in (39,209):
            g.panel(18,side*4.05,z,33,.7,4,'char',1)
            for x in (6,25):g.disc(x,side*4.55,z,1.2,1.2,.5,'brass',10)
        g.panel(w-18,side*4.15,94,6,1,15,'bronze',1)
        g.disc(w-18,side*5.4,97,3.5,3.5,2.3,'brass',14)
    return g
def frame():
    g=PaperGroup('AcrossPassageJambs');w=SPAN
    for x in (-6.5,w+6.5):
        g.panel(x,0,128,12,15,256,'walnut',1.3)
        g.panel(x,-7.5,131,8,2,243,'oak',.8)
        g.panel(x,0,7.5,15,18,15,'stone',1)
    g.panel(w/2,0,257,w+28,18,12,'wood',2)
    g.panel(w/2,-9,256,w+25,2.5,4,'oak',1)
    g.panel(w/2,0,1.8,w+15,21,3.6,'oak',1)
    # The hinge jamb is physically joined to the rear wall. The open side in
    # front stays visible through the frame once the oak leaf has swung away.
    for z in (11,246):g.panel(-33,0,z,49,12,9,'wood',1)
    g.panel(-31,0,123,46,7,233,'teal',1)
    for x in (-49,-33,-17):g.panel(x,-4,121,2,1,225,'wood')
    return g
def haze():
    g=PaperGroup('WickHaze')
    # Camera-facing sheet following the same gently sloping pool as the real spotlight.
    g.face([(-56,0,0),(75,0,0),(4,0,100),(-5,0,100)],'cream')
    g.uvs[:]=[(0.,1.),(1.,1.),(1.,0.),(0.,0.)]
    return g
def haze_mask(path):
    import struct,zlib
    w,h=128,192;data=bytearray()
    for j in range(h):
        data.append(0);v=j/(h-1)
        fade=(min(1.,v*15)**2)*(1-v)**.49
        for i in range(w):
            u=i/(w-1)
            a=max(0,math.sin(math.pi*u))**2.7*fade
            b=round(255*.16*a)
            data.extend((b,b,b,255))
    def c(tag,p):
        return struct.pack('>I',len(p))+tag+p+struct.pack('>I',zlib.crc32(tag+p)&0xffffffff)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+c(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+c(b'IDAT',zlib.compress(data,9))+c(b'IEND',b''))

