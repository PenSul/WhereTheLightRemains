"""Bake the animated notebook leaf, close open spread, and Lantern Street frontispiece.

Usage: python book_art.py PROJECT_FOLDER OUTPUT_FOLDER   (Pillow and NumPy)
Editable sources: the sampled left and right page stock beside this script and the first room's GLBs.
"""
from pathlib import Path
import sys, struct, json, hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter


def rgb(a):return np.clip(np.rint(a),0,255).astype(np.uint8)

def grain(X,Y):
    # Deterministic subdued paper formation. The fine grain itself comes from the original desk painting.
    return np.sin((X+.73*Y)*.068)*.48+np.sin(.097*Y-.013*X)*.41+np.cos(.23*X+.04*Y)*.31


def paper_source(repo):
    folder=repo/'AssetSource/UI/LanternStreetBook'
    pages=[]
    for filename in ('PaperSampleLeft.png','PaperSampleRight.png'):
        with Image.open(folder/filename) as image:
            assert image.size==(640,672),filename
            pages.append(np.asarray(image.convert('RGB'),dtype='float32'))
    return pages


def sample(im,u,v):
    h,w=im.shape[:2];return im[np.clip(np.rint(v*(h-1)).astype(int),0,h-1),np.clip(np.rint(u*(w-1)).astype(int),0,w-1)]


def spread(pages):
    W,H=1280,720;Y,X=np.mgrid[:H,:W].astype('float32');v=np.clip((Y-19)/675,0,1)
    d=np.abs(X-640);u=np.clip((d-2)/611,0,1);left=X<640
    # Lower and upper sheets bow by only a few millimetres at the centre of this flat spread.
    top=14+5*np.exp(-d/92)+1.4*np.sin(u*5)+2.0*u**3
    bottom=695-7*np.exp(-d/73)-1.3*np.sin(u*7)-3*u**2
    outer=619-1.9*np.cos(v*4)-6.0*np.maximum(0,1-np.minimum(v,1-v)*21)**2
    paper=np.where(left[...,None],sample(pages[0],1-u,v),sample(pages[1],u,v))
    # Bring both pages to a quiet reading value. Retain asymmetric lantern illumination and original grain.
    paper=paper*.72+np.array([243,222,189])*.28
    shade=-25*np.exp(-d/12)-8*np.exp(-d/39)+6.5*np.exp(-((d-30)/25)**2)-2.9*u**6
    paper=paper+(shade+grain(X,Y))[...,None]
    paper_mask=np.minimum(np.minimum(Y-top,bottom-Y),outer-d)
    # Narrow blue cloth cover, leather turn-in, and four compressed page edges. All type is live in UMG.
    noise=grain(X,Y)
    canvas=np.array([45,52,55],float)+noise[...,None]*1.10
    bound=(np.minimum.reduce([X-5,W-6-X,Y-4,H-7-Y])>0)
    canvas[bound]=np.array([86,68,52])+noise[bound,None]
    bind=(np.minimum.reduce([X-10,W-11-X,Y-7,H-11-Y])>0)
    canvas[bind]=np.array([116,90,66])+noise[bind,None]
    for offset,col in [(7,[113,90,66]),(5.6,[185,151,113]),(4.5,[139,111,83]),(3,[207,176,136]),(1.8,[157,128,96])]:
        m=(np.minimum(np.minimum(Y-top+offset*.24,bottom-Y+offset),outer-d+offset*.55)>.0)
        canvas[m]=np.array(col)+noise[m,None]*.8
    alpha=np.clip(paper_mask+.55,0,1)[...,None];canvas=canvas*(1-alpha)+paper*alpha
    return Image.fromarray(rgb(canvas),'RGB')


def drawtri(buf,depth,verts,colors):
    """Coverage and barycentric interpolation for the folded texture and scene print."""
    h,w=buf.shape[:2];p=np.asarray(verts,float);c=np.asarray(colors,float)
    lx=max(0,int(np.floor(p[:,0].min())));rx=min(w-1,int(np.ceil(p[:,0].max())))
    ly=max(0,int(np.floor(p[:,1].min())));ry=min(h-1,int(np.ceil(p[:,1].max())))
    if rx<lx or ry<ly:return
    (x1,y1,d1),(x2,y2,d2),(x3,y3,d3)=p
    area=(y2-y3)*(x1-x3)+(x3-x2)*(y1-y3)
    if abs(area)<.00001:return
    yy,xx=np.mgrid[ly:ry+1,lx:rx+1];x=xx+.5;y=yy+.5
    a=((y2-y3)*(x-x3)+(x3-x2)*(y-y3))/area
    b=((y3-y1)*(x-x3)+(x1-x3)*(y-y3))/area;cc=1-a-b
    dd=a*d1+b*d2+cc*d3;reg=depth[ly:ry+1,lx:rx+1]
    m=(a>=-.000001)&(b>=-.000001)&(cc>=-.000001)&(dd<=reg)
    if not np.any(m):return
    dst=buf[ly:ry+1,lx:rx+1];reg[m]=dd[m]
    if c.ndim==1:dst[m]=c
    else:dst[m]=a[m,None]*c[0]+b[m,None]*c[1]+cc[m,None]*c[2]


def leaf_mesh(pages):
    W,H=560,384;S=2
    # Mesh UVs remain fixed on a bent sheet. The thickest shadow lies at the gutter;
    # the fore-edge has a slight, bright curl, strongest towards the upper corner.
    U,V=np.meshgrid(np.linspace(0,1,79),np.linspace(0,1,41))
    def position(u,v):
        hinge=10*(1-v)+1.4
        width=443+100*v
        tip=np.maximum(0,(u-.75)/.25)**2*(1-v)**2
        lift=31*np.sin(np.pi*u)*(1-.43*v)-12*tip
        x=hinge+width*u-24*tip+2.5*np.sin(np.pi*v)*u**1.4
        y=52+323*v-lift-8*u*(1-v)-2*u*v-3.5*np.sin(u*np.pi)*v
        return x,y
    X,Y=position(U,V)
    p=sample(pages[1],U,V).astype(float)
    sh=(-20*np.exp(-U*36)+10*np.exp(-((U-.25)/.19)**2)-12*np.exp(-((U-.76)/.20)**2)
       +5*np.exp(-((U-.91)/.04)**2)-17*np.exp(-((U-.974)/.027)**2)*(1-V)**2
       +8*np.exp(-((U-.998)/.012)**2)*(1-V)**2+5*(1-V)*U)
    col=np.clip(p*.90+np.array([240,213,172])*.10+sh[...,None],0,255)
    coordinates=np.stack((X*S,Y*S,U*0),axis=-1)
    surface=np.zeros((H*S,W*S,4),np.float32);depth=np.full((H*S,W*S),1e7,np.float32)
    def rim_at(yoff,color):
        result=np.zeros_like(surface,dtype=np.uint8)
        pts=list(zip(X[0]*S,(Y[0]+yoff)*S))+list(zip(X[1:,-1]*S,(Y[1:,-1]+yoff)*S))+list(zip(X[-1,-2::-1]*S,(Y[-1,-2::-1]+yoff)*S))+list(zip(X[-2:0:-1,0]*S,(Y[-2:0:-1,0]+yoff)*S))
        out=Image.fromarray(result,'RGBA');ImageDraw.Draw(out).polygon(pts,fill=color);return out
    underside=rim_at(2.1,(107,78,53,255))
    underside.alpha_composite(rim_at(1.15,(191,151,104,255)))
    rgba=np.concatenate((col,np.full((*U.shape,1),255)),axis=-1)
    for j in range(U.shape[0]-1):
        for i in range(U.shape[1]-1):
            for a,b,c in (((j,i),(j,i+1),(j+1,i+1)),((j,i),(j+1,i+1),(j+1,i))):
                drawtri(surface,depth,[coordinates[a],coordinates[b],coordinates[c]],[rgba[a],rgba[b],rgba[c]])
    y,x=np.mgrid[:H*S,:W*S];surface[:,:,:3]+=grain(x/S,y/S)[...,None]*.83
    underside.alpha_composite(Image.fromarray(rgb(surface),'RGBA'))
    return underside.resize((W,H),Image.Resampling.LANCZOS)


def gltf(path):
    data=path.read_bytes();n=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+n].decode());base=28+n
    def acc(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];o=base+v.get('byteOffset',0)+a.get('byteOffset',0)
        dtype={5126:'<f4',5125:'<u4',5123:'<u2'}[a['componentType']];stride={'VEC3':3,'VEC2':2,'SCALAR':1}[a['type']]
        return np.frombuffer(data,dtype,count=a['count']*stride,offset=o).reshape(-1,stride)
    p=doc['meshes'][0]['primitives'][0];return acc(p['attributes']['POSITION']),acc(p['attributes']['TEXCOORD_0']),acc(p['indices']).reshape(-1,3)


def street(repo):
    # Same fixed starting-room meshes used by the playable map. No HUD, puzzle text or buttons in the print.
    sources=repo/'AssetSource/Models/LanternStreet';atlas=np.asarray(Image.open(sources/'T_LanternPaperAtlas.png').convert('RGB').resize((16,16),Image.Resampling.BOX))
    names={'HomeTimber':(-260,130,150),'HomeWindowPresent':(-320,153,180),'HomeDoorClosed':(237,98,100),'KitchenFloorReturn':(-296,206,-18),
           'QuaySection00':(-820,0,0),'QuaySection01':(-300,0,0),'QuaySection02':(220,0,0)}
    W,H=808,455;canvas=np.full((H,W,3),211,np.float32);depth=np.full((H,W),1e8,np.float32)
    for name,(ox,oy,oz) in names.items():
        points,uv,faces=gltf(sources/('SM_'+name+'.glb'));x=ox+100*points[:,0];y=oy-100*points[:,2];z=oz+100*points[:,1]
        dist=y+1070;fy=1120.; proj=np.column_stack((W*.50+(x+335)*fy/dist,H*.50-(z-155)*fy/dist,dist))
        for fi in faces:
            verts=proj[fi];u,v=uv[fi].mean(axis=0);c=atlas[min(15,int(v*16)),min(15,int(u*16))]
            drawtri(canvas,depth,verts,c)
    y,x=np.mgrid[:H,:W];original=Image.fromarray(rgb(canvas),'RGB').resize((640,360),Image.Resampling.LANCZOS)
    arr=np.asarray(original,dtype=float);light=arr@np.array([.299,.587,.114]);Y,X=np.mgrid[:360,:640]
    # Project-specific four-ink look: preserve the teal panelling and walnut silhouettes with restrained warm paper showing through.
    warm=light[...,None]*np.array([.83,.74,.62])+np.array([38.,36.,34.])
    ink=arr*.62+warm*.38+grain(X,Y)[...,None]*1.5
    mask=np.minimum.reduce([X-6.,633.-X,Y-6.,353.-Y])+np.sin(X*.117)*.48+np.sin(Y*.092)*.56
    ink=np.array([220,198,164])+np.clip(mask[...,None]/1.4,0,1)*(ink-np.array([220,198,164]))
    return Image.fromarray(rgb(ink),'RGB')


def main(repo,out):
    out.mkdir(parents=True,exist_ok=True);pages=paper_source(repo)
    images={'T_BookCleanSpread':spread(pages),'T_BookTurningLeaf':leaf_mesh(pages),'T_BookIntroStreet':street(repo)}
    artifacts={}
    for name,im in images.items():
        if im.mode=='RGB':im=im.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
        p=out/(name+'.png');im.save(p,optimize=True);artifacts[name]={'size':im.size,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    result={'editable_inputs':['AssetSource/UI/LanternStreetBook/PaperSampleLeft.png','AssetSource/UI/LanternStreetBook/PaperSampleRight.png','AssetSource/Models/LanternStreet/*.glb','AssetSource/Models/LanternStreet/T_LanternPaperAtlas.png'],
            'credit':'Project team, original and AI-assisted Paper Theatre visuals. Book paper sampled from the accepted team menu painting. The frontispiece renders the authored starting room, including its cut-paper window and family photograph.',
            'display_canvas':[1280,720],'desk_fold':[[697,306],[687,621]],'turn_leaf_rect':[692,255,548,373],'leaf_pivot':[0,.55],
            'spread_spine':640,'writeable_left':[54,58,590,653],'writeable_right':[685,58,1224,653],'artifacts':artifacts}
    (out/'book-art-manifest.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(artifacts))


if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))

