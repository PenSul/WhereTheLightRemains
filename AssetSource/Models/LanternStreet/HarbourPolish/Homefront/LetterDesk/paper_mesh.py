"""Small glTF writer for the painted paper scenery. Input is Unreal centimetres."""
from __future__ import annotations

import json
import math
import random
import struct
import zlib

PALETTE = {
    "ink":"282D39","navy":"354654","slate":"536779","mist":"94AAB3",
    "sky":"718395","dawn":"E8BC85","water":"587587","water_warm":"92A6A4",
    "cloud":"AEBAB8","sea_light":"B6C9C3","stone":"A49A85","chalk":"D0BFA4",
    "cream":"E5D3AF","linen":"CEBE9E","plaster":"B2A695","teal":"547377",
    "blue":"465F75","brick":"A25E4D","brick_dark":"784742","sand":"B8A286",
    "wood":"755744","oak":"94704D","walnut":"55453E","char":"383637",
    "bronze":"8C714E","brass":"B99052","gold":"E4B96D","flame":"FFE8AC",
    "glass":"657987","amber":"C68F52","leaf":"6C7963","grass":"818567",
    "reed":"AB9A68","red":"A75C4D","ivory":"DACBAF","portrait":"726657",
    "skin":"BF987A","hair":"9A8E7B","dress":"697C79","apron":"B4A790",
    "copper":"986A50","tile":"92856E","roof":"594F50","distance":"7F8E9D",
    "deep":"374B60","rope":"A49274","window":"5E6D76","wax":"E5CDA1",
    "light_sky":"B7B6B2","peach":"E5A976","petal":"B28A74","sea_dark":"405C70",
}
SWATCHES = list(PALETTE)
TILE = 64
GRID = 16
SHADES = (.70, .83, .96, 1.05)


def png_texture(output):
    """A repeating 1024px atlas. Subtle fibres stay at a readable physical scale."""
    rng = random.Random(14792)
    width = TILE*GRID
    base = {name:tuple(bytes.fromhex(color)) for name,color in PALETTE.items()}
    surface = bytearray()
    for y in range(width):
        surface.append(0)
        for x in range(width):
            cell = (y//TILE)*GRID + x//TILE
            color = base[SWATCHES[min(cell//4,len(SWATCHES)-1)]]
            # Small restrained fibres and mottle keep lit surfaces matte.
            grain = rng.uniform(-.035,.035)+.013*math.sin(.18*x+.035*y)+.010*math.sin(.06*y)
            surface.extend(max(0,min(255,round(ch*(SHADES[cell%4]+grain)))) for ch in color)
    def chunk(tag,data):
        return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    output.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,width,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(surface,8))+chunk(b'IEND',b''))


def normal(vs):
    # Newell normal supports irregular convex polygon faces.
    nx=ny=nz=0.
    for (x,y,z),(xx,yy,zz) in zip(vs,vs[1:]+vs[:1]):
        nx+=(y-yy)*(z+zz); ny+=(z-zz)*(x+xx); nz+=(x-xx)*(y+yy)
    length=math.sqrt(nx*nx+ny*ny+nz*nz) or 1
    return nx/length,ny/length,nz/length


def ears(points):
    """Triangulate counterclockwise planar cut-paper outlines."""
    ids=list(range(len(points)))
    def cross(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points,points[1:]+points[:1]))
    if area<0:ids.reverse()
    result=[]
    while len(ids)>3:
        for i in range(len(ids)):
            a,b,c=ids[i-1],ids[i],ids[(i+1)%len(ids)]
            pa,pb,pc=points[a],points[b],points[c]
            if cross(pa,pb,pc)<=1e-7:continue
            if any(min(cross(pa,pb,points[j]),cross(pb,pc,points[j]),cross(pc,pa,points[j]))>1e-7 for j in ids if j not in (a,b,c)):continue
            result.append((a,b,c));del ids[i];break
        else: raise ValueError(f'Cannot triangulate outline {points}')
    return result+[tuple(ids)]


class PaperGroup:
    def __init__(self,name,origin=(0,0,0),tags=(),folder='Set'):
        self.name=name
        self.origin=origin
        self.tags=list(tags)
        self.folder=folder
        self.points=[];self.uvs=[];self.normals=[];self.indices=[]

    def face(self,vs,color,shade=None):
        norm=normal(vs)
        if shade is None:
            light=-.24*norm[0]-.65*norm[1]+.58*norm[2]
            shade = 3 if light>.72 else 2 if light>.08 else 1 if light>-.45 else 0
        idx=SWATCHES.index(color)*4+shade
        cell_x,cell_y=idx%GRID,idx//GRID
        max_axis=max(range(3),key=lambda i:abs(norm[i]))
        ui,vi=((1,2),(0,2),(0,1))[max_axis]
        us=[p[ui] for p in vs]; vcoords=[p[vi] for p in vs]
        ulo,uhi=min(us),max(us);vlo,vhi=min(vcoords),max(vcoords)
        start=len(self.points)
        for p,u,v in zip(vs,us,vcoords):
            # Unreal glTF reader maps X,Z,Y into X,Y,Z and applies metre scaling.
            pt=tuple((a-b)*.01 for a,b in zip(p,self.origin))
            self.points.append((pt[0],pt[2],-pt[1]));self.normals.append((norm[0],norm[2],-norm[1]))
            self.uvs.append(((cell_x+.06+.88*(u-ulo)/max(1,uhi-ulo))/GRID,(cell_y+.06+.88*(vhi-v)/max(1,vhi-vlo))/GRID))
        for i in range(1,len(vs)-1):self.indices.extend((start,start+i,start+i+1))

    def outline(self,points,y,depth,color):
        area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(points,points[1:]+points[:1]))
        if area<0:points=list(reversed(points))
        front=[(x,y,z) for x,z in points];back=[(x,y+depth,z) for x,z in points]
        for a,b,c in ears(points):
            self.face([front[a],front[b],front[c]],color);self.face([back[c],back[b],back[a]],color)
        for i in range(len(points)):
            j=(i+1)%len(points);self.face([front[j],front[i],back[i],back[j]],color)

    def panel(self,x,y,z,w,d,h,c,bevel=0):
        l,r=x-w/2,x+w/2;b,t=z-h/2,z+h/2
        e=min(bevel,w/5,h/5)
        p=[(l+e,b),(r-e,b),(r,b+e),(r,t-e),(r-e,t),(l+e,t),(l,t-e),(l,b+e)] if e else [(l,b),(r,b),(r,t),(l,t)]
        self.outline(p,y-d/2,d,c)

    def stroke(self,x1,z1,x2,z2,y,w,d,c):
        dx,dz=x2-x1,z2-z1
        q=math.hypot(dx,dz)
        if q<1e-5:return
        nx,nz=-dz*w/(2*q),dx*w/(2*q)
        self.outline([(x1+nx,z1+nz),(x2+nx,z2+nz),(x2-nx,z2-nz),(x1-nx,z1-nz)],y,d,c)

    def lathe(self,x,y,profile,c,n=10):
        rings=[[(x+r*math.cos(2*math.pi*i/n),y+r*math.sin(2*math.pi*i/n),z) for i in range(n)] for z,r in profile]
        self.face(list(reversed(rings[0])),c);self.face(rings[-1],c)
        for a,b in zip(rings,rings[1:]):
            for i in range(n):
                j=(i+1)%n;self.face([a[i],a[j],b[j],b[i]],c)

    def disc(self,x,y,z,rx,rz,d,c,n=14):
        self.outline([(x+rx*math.cos(2*math.pi*i/n),z+rz*math.sin(2*math.pi*i/n)) for i in range(n)],y,d,c)

    def export(self,where):
        data=bytearray();views=[];access=[]
        def arr(values,fmt,kind,dtype,components,limit=False):
            offset=len(data);packer=struct.Struct('<'+fmt)
            for row in values:data.extend(packer.pack(*row))
            views.append({'buffer':0,'byteOffset':offset,'byteLength':len(data)-offset,'target':34963 if kind=='SCALAR' else 34962})
            item={'bufferView':len(views)-1,'componentType':dtype,'count':len(values),'type':kind}
            if limit:
                item['min']=[min(v[i] for v in values) for i in range(components)]
                item['max']=[max(v[i] for v in values) for i in range(components)]
            access.append(item)
        arr(self.points,'3f','VEC3',5126,3,True);arr(self.normals,'3f','VEC3',5126,3);arr(self.uvs,'2f','VEC2',5126,2);arr([(i,) for i in self.indices],'I','SCALAR',5125,1)
        name='SM_'+self.name
        doc={'asset':{'version':'2.0','generator':'WTLR Paper Theatre scene source'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'name':name,'mesh':0}],'meshes':[{'name':name,'primitives':[{'attributes':{'POSITION':0,'NORMAL':1,'TEXCOORD_0':2},'indices':3}]}],'buffers':[{'byteLength':len(data)}],'bufferViews':views,'accessors':access}
        header=json.dumps(doc,separators=(',',':')).encode();header+=b' '*((-len(header))%4)
        where.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(header)+len(data))+struct.pack('<I4s',len(header),b'JSON')+header+struct.pack('<I4s',len(data),b'BIN\0')+data)

