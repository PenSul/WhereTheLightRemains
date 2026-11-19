"""Create an original smooth sprite falloff for air around a lit wick."""
import math,struct,zlib
from pathlib import Path
def mask_png(file):
    side=128;raw=bytearray()
    for y in range(side):
        raw.append(0)
        for x in range(side):
            r=math.hypot((x+.5-side/2)/(side/2),(y+.5-side/2)/(side/2))
            value=max(0.,(math.exp(-5.5*r*r)-math.exp(-5.5))/(1-math.exp(-5.5))) if r<1 else 0
            a=round(255*.24*value*value)
            raw.extend((a,a,a,255))
    def chunk(tag,data):
        return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    file.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',side,side,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))

