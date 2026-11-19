"""Make articulated zero-thickness paper cards from the approved side-view illustration.
Run: python make_elias_cards.py output_directory
The original drawing is sampled with explicit hand-traced contours. No image model,
depth reconstruction, rig plugin or external sample library is used.
"""
from pathlib import Path
import argparse,json,math,shutil,struct
from PIL import Image,ImageEnhance,ImageOps
from paper_mesh import PaperGroup,ears

K=.226
GROUND=820.5
# Coordinates are twice the native dimensions of the cropped profile.
PIVOTS={'Body':(280,410),'Head':(313,174),'Scarf':(267,181)}
DEPTH={'Body':0.,'Head':-.22,'Scarf':.17}
PARENT={'Body':None,'Head':'Body','Scarf':'Body'}
for side in 'LR':
    PIVOTS.update({'UpperArm_'+side:(280,242),'Forearm_'+side:(248,365),
                   'Thigh_'+side:(285,441),'Shin_'+side:(285,441+40.3/K),'Foot_'+side:(285,441+72/K)})
    layer=-.54 if side=='R' else .64
    for i,part in enumerate(['UpperArm','Forearm','Thigh','Shin','Foot']):
        n=part+'_'+side
        DEPTH[n]=layer if part in ('UpperArm','Forearm') else (.31 if side=='R' else .91)
        PARENT[n]={'UpperArm':'Body','Forearm':'UpperArm_'+side,'Thigh':None,'Shin':'Thigh_'+side,'Foot':'Shin_'+side}[part]

def shape(s):
    values=list(map(float,s.replace(',',' ').split()))
    return list(zip(values[::2],values[1::2]))

def ink_texture(ref,out):
    src=Image.open(ref).convert('RGB')
    if src.size==(512,512):
        source=src.crop((0,0,240,439))
    elif src.size==(1536,1024):
        source=src.crop((433,14,673,453))
    else:
        raise ValueError('Use the 512 x 512 Elias atlas or a 1536 x 1024 source illustration.')
    canvas=Image.new('RGB',(512,512),source.getpixel((55,154)))
    canvas.paste(source,(0,0))
    far=ImageEnhance.Color(source).enhance(.77)
    rgb=far.split();far=Image.merge('RGB',tuple(p.point(lambda c,s=s:round(c*s)) for p,s in zip(rgb,(.79,.83,.88))))
    canvas.paste(far,(256,0))
    canvas.save(out/'T_EliasCutStock.png')

def build(ref,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);ink_texture(ref,out)
    groups={}
    def part(n):
        nonlocal group,name,order
        name=n;group=PaperGroup('CardElias_'+n);order=0;groups[n]=group
    group=name=None;order=0
    def card(points,sample=None,offset=(0,0)):
        nonlocal order
        p=shape(points) if isinstance(points,str) else points
        tx,tz=PIVOTS[name];uoff=256 if name.endswith('_L') else 0
        if sample:
            x0,y0,x1,y1=sample
            left=min(x for x,y in p);top=min(y for x,y in p);w=max(x for x,y in p)-left;h=max(y for x,y in p)-top
            uv=[(x0+(x-left)*(x1-x0)/max(w,1.e-8),y0+(y-top)*(y1-y0)/max(h,1.e-8)) for x,y in p]
        else:uv=p
        # All points of each printed shape lie on exactly one plane. Small
        # ink offsets preserve the intended paper stacking order at grazing light.
        d=-.016*order;order+=1
        start=len(group.points)
        for (x,y),(s,t) in zip(p,uv):
            forward=(x+offset[0]-tx)*K;z=(tz-y-offset[1])*K
            group.points.append((d*.01,z*.01,forward*.01))
            group.normals.append((-1.,0.,0.))
            group.uvs.append(((uoff+s/2)/512,(t/2)/512))
        for a,b,c in ears(p):
            group.indices.extend((start+a,start+c,start+b))
    def oval(x,y,rx,ry,sample,n=18):
        card([(x+rx*math.cos(i*2*math.pi/n),y+ry*math.sin(i*2*math.pi/n)) for i in range(n)],sample)
    part('Body')
    # A tapered neck belongs to the shoulders. Give the head room to nod over
    # this underlap while the wool wrap stays with the coat.
    card('283,140 296,137 307,137 328,147 340,154 351,164 351,178 348,190 352,206 341,214 312,200 288,188 276,181 284,168 287,151',
         (308,151,325,163))
    card('323,147 336,149 349,156 351,165 348,179 348,191 352,206 344,204 333,185 326,175 321,163',
         (322,132,334,144))
    card('243,185 268,181 291,184 318,200 340,224 359,248 368,274 369,315 373,347 377,411 381,453 389,490 399,618 361,618 356,624 285,617 241,612 182,599 129,581 156,479 179,402 192,331 206,264 221,214')
    # Replace the sleeve baked into the concept with a continuous cut coat panel.
    # Its texture is the clean lower coat on the same artwork. The separate arm
    # and pocket move over it, revealing cloth rather than a second arm.
    card('241,225 254,206 276,202 301,211 320,234 326,266 321,306 323,344 336,388 353,436 355,481 351,512 341,524 316,527 281,518 255,498 238,469 217,433 207,398 202,365 207,329 216,278',(199,526,339,581))
    card('255,243 261,225 271,216 285,215 297,222 301,230 289,227 277,231 264,246',(199,527,264,570))
    card('278,466 303,460 327,445 339,429 345,439 350,459 346,488 336,506 320,513 299,511 279,501 275,484')
    # The scarf previously moved with the beard. Keep its seam fixed at the
    # shoulder and lower the fold several centimetres below the actual jaw.
    card('250,173 261,151 267,149 285,151 310,161 329,173 347,187 361,198 369,210 371,220 367,230 353,221 334,205 315,191 284,179 258,187 247,186',
         offset=(0,12))
    part('Head')
    card('274,110 274,94 278,80 287,67 300,59 310,55 315,50 328,45 343,43 359,45 374,49 387,56 394,55 403,61 407,66 405,71 397,79 393,81 397,95 399,108 398,117 396,122 398,133 402,143 409,153 409,157 405,159 396,159 392,157 392,165 395,170 391,173 387,176 387,183 390,194 390,201 387,207 382,210 374,209 358,202 345,191 334,185 328,174 323,160 312,151 302,151 287,149 274,145 262,133 259,117 267,115',
         offset=(2,-14))
    part('Scarf')
    card('265,178 249,195 233,218 209,266 199,300 186,336 166,373 151,391 145,391 128,379 121,373 147,327 160,300 126,340 110,351 104,348 95,331 86,330 81,321 99,311 130,294 161,273 192,243 219,212 237,192 244,183')
    for side in 'LR':
        part('UpperArm_'+side)
        oval(280,244,28,23,(250,252,289,289))
        card('267,231 279,225 291,225 302,231 309,242 313,258 314,274 310,294 302,320 295,345 297,357 290,369 270,380 245,388 226,382 215,372 216,357 220,332 228,307 237,275 246,249 254,239')
        part('Forearm_'+side)
        oval(250,365,28,20,(225,366,271,396))
        # A thumb/hand emerges from the concept cuff while the separate arms swing.
        card('299,441 319,431 327,431 335,439 344,448 348,456 349,462 345,468 342,469 339,466 335,470 330,470 326,467 323,468 317,466 310,456',(347,98,371,137))
        card('322,453 328,458 332,463 330,464 323,458',(351,151,359,156))
        card('222,351 237,343 254,347 268,349 284,349 294,356 306,379 320,398 330,417 333,429 321,444 294,460 282,463 267,442 247,416 231,394 217,374 216,362')
        part('Thigh_'+side)
        card('263,422 290,416 312,425 321,443 320,475 319,514 324,552 325,588 320,619 309,638 282,644 261,630 255,597 250,546 246,493 246,457',(259,639,330,707))
        part('Shin_'+side)
        oval(285,621,30,21,(261,638,316,675))
        card('257,610 269,605 294,604 314,609 321,620 326,645 332,682 336,713 338,732 338,743 330,747 255,747 254,731 254,704 254,662 253,631',(253,619,337,747))
        part('Foot_'+side)
        card('271,735 303,732 327,738 330,751 334,760 343,765 352,768 359,774 372,777 394,779 403,781 410,787 414,795 415,803 415,809 407,812 380,815 352,815 331,814 312,808 306,812 261,812 262,785 265,771 265,751')
    parts={}
    for name,g in groups.items():
        g.export(out/('SM_'+g.name+'.glb'))
        x,y=PIVOTS[name];side_shift=-5.7 if name.endswith('_L') and name.split('_')[0] in ('Thigh','Shin','Foot') else 0.
        parts[name]={'pivot_cm':[DEPTH[name],(x-285)*K+side_shift,(GROUND-y)*K], 'parent':PARENT[name],
                     'triangles':len(g.indices)//3,'normal':'-X','printed_depth_cm':round((max(v[0] for v in g.points)-min(v[0] for v in g.points))*100,4)}
    (out/'Elias-cards.json').write_text(json.dumps({'parts':parts,'physical_paper_layers':13,'source_image_crop':[433,14,673,453],'pixels_per_cm_in_tracing':1/K},indent=2))
    return parts

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('reference',nargs='?',type=Path,default=Path(__file__).with_name('T_EliasCutStock.png'));p.add_argument('directory',type=Path)
    a=p.parse_args();build(a.reference,a.directory)
