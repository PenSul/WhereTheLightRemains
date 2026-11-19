"""Extract four transparent texture inputs from the original painted locket sheet."""
from pathlib import Path
from PIL import Image
import json, hashlib
root=Path(__file__).resolve().parent
original=Image.open(root/'EchoLockets.png').convert('RGBA')
W,H=original.size
names=('Empty','Candle','Crate','Bell')
records={}
for i,name in enumerate(names):
    x=(i%2)*W//2
    y=(i//2)*H//2
    cell=original.crop((x,y,((i%2)+1)*W//2,((i//2)+1)*H//2))
    a=cell.getchannel('A')
    strong=a.point(lambda a:255 if a>144 else 0)
    # Isolated paint specks should not decide the visual size of an icon.
    xx=[u for u in range(cell.width) if strong.crop((u,0,u+1,cell.height)).histogram()[255]>cell.height*.035]
    yy=[v for v in range(cell.height) if strong.crop((0,v,cell.width,v+1)).histogram()[255]>cell.width*.035]
    bb=(xx[0]-3,yy[0]-3,xx[-1]+4,yy[-1]+4)
    part=cell.crop(bb)
    part.thumbnail((245,245),Image.Resampling.LANCZOS)
    tile=Image.new('RGBA',(256,256))
    tile.alpha_composite(part,((256-part.width)//2,(256-part.height)//2))
    assert tile.getpixel((0,0))[3]==0
    dst=root/('T_Locket'+name+'.png')
    tile.save(dst)
    records[dst.name]=hashlib.sha256(dst.read_bytes()).hexdigest()
(root/'lockets.json').write_text(json.dumps({'source':'EchoLockets.png','authorship':'Original AI-assisted raster artwork, generated using OpenAI image generation for this project. Transparent medallions extracted from the original sheet.','textures':records},indent=2))

