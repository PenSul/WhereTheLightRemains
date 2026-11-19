"""An original 32-bar waltz for felt piano, plucked strings and a bowed bass.
Render from this score with Python, NumPy and the standard library.
"""
import json, wave
from pathlib import Path
import numpy as np
OUT=Path(__file__).parent
RATE=32000
# Slowly rocking 6/8, counted in two. The second strain opens into the relative major.
QUAVER=60/54/3
BAR=6*QUAVER
chords=[(50,57,62,65),(46,53,58,62),(53,60,65,69),(48,55,60,64),
        (43,50,55,58),(46,53,58,62),(45,52,57,64),(45,52,61,64),
        (50,57,62,65),(46,53,58,65),(53,60,65,69),(48,55,60,67),
        (43,50,58,62),(46,53,57,62),(45,52,57,61),(50,57,62,65),
        (53,60,65,69),(48,55,60,64),(50,57,62,65),(46,53,58,62),
        (55,62,67,70),(53,60,65,69),(50,57,62,65),(45,52,57,61),
        (50,57,62,65),(46,53,58,62),(53,60,65,69),(48,55,60,64),
        (43,50,55,58),(46,53,58,62),(45,52,57,61),(50,57,62,65)]
# (onset in eighths, MIDI pitch, duration in eighths). Spaces are part of the phrasing.
melody=[
[(1,69,1.6),(3,72,1),(4.5,74,1.7)],[(0,77,3.5),(4.5,74,1.2)],
[(0,72,2.5),(3,69,2.5)],[(0,67,4.8)],[(1,65,1.6),(3,67,1),(4.5,70,1.5)],
[(0,69,3.4),(4,65,1.5)],[(0,64,3),(3.5,61,1.3)],[(0,64,3.8)],
[(0,69,2.6),(3,72,1.4),(5,74,1)],[(0,77,2.7),(3,79,1.4),(5,77,1)],
[(0,76,2),(2.5,72,2),(5,69,.8)],[(0,67,3.8)],
[(0,70,2.8),(3.5,67,1.8)],[(0,65,2),(2.5,62,2.5)],[(0,64,2.5),(3.5,61,2)],[(0,62,4.8)],
[(1,72,1.8),(3,77,2.5)],[(0,76,2),(3,72,2.5)],[(0,74,2.7),(3.5,69,2)],[(0,70,4.5)],
[(0,74,1.6),(2,77,1),(3.5,79,2)],[(0,77,3),(4,72,1.5)],
[(0,74,2.9),(3,69,1.6)],[(0,68,1.2),(1.5,69,3.5)],
[(1,69,1.5),(3,72,1),(4.5,74,1.3)],[(0,77,3),(4,74,1.4)],
[(0,72,2.5),(3.5,69,1.8)],[(0,67,4.7)],[(1,65,1.5),(3,67,1),(4.5,70,1.2)],
[(0,69,2.5),(3,65,2.5)],[(0,64,2.4),(3.5,61,1.8)],[(0,62,4)]]
N=round(len(chords)*BAR*RATE)
stereo=np.zeros((N,2),dtype=np.float32)
rng=np.random.default_rng(1854)
def play(at,midi,length,kind,volume,pan):
    hz=440*2**((midi-69)/12)
    release={'felt':.7,'pluck':.75,'bow':.6}[kind]
    t=np.arange(round((length+release)*RATE))/RATE
    p=2*np.pi*hz*t
    if kind=='felt':
        wave0=sum(a*np.sin(k*p*(1+.00013*k*k))*np.exp(-t*(1.7+.7*k)) for k,a in [(1,1),(2,.33),(3,.21),(4,.10),(6,.055)])
        wave0+=.18*np.sin(p*1.0012)*np.exp(-1.1*t)
        env=(1-np.exp(-t*96))*np.exp(-np.maximum(0,t-length)*6)
    elif kind=='pluck':
        wave0=sum(a*np.sin(p*k)*np.exp(-t*(2+.7*k)) for k,a in [(1,1),(2,.52),(3,.19),(4,.12),(5,.08)])
        env=(1-np.exp(-t*135))*np.exp(-np.maximum(0,t-length)*7)
    else:
        angle=p+.018*np.sin(2*np.pi*4.4*t)
        wave0=sum(a*np.sin(angle*k) for k,a in [(1,1),(2,.35),(3,.35),(4,.12),(5,.10),(7,.046)])
        env=(1-np.exp(-t*3.1))*np.exp(-np.maximum(0,t-length)*6)*(.91+.09*np.sin(t*2.8))
    signal=wave0*env*volume
    ix=(np.arange(t.size)+round(at*RATE))%N
    stereo[ix,0]+=signal*np.sqrt(1-pan);stereo[ix,1]+=signal*np.sqrt(pan)
for bar,(chord,lead) in enumerate(zip(chords,melody)):
    base=bar*BAR
    for onset,note,l in lead:
        play(base+onset*QUAVER+rng.uniform(0,.023),note,l*QUAVER,'felt',rng.uniform(.58,.72),.43)
    for j,idx in enumerate([0,1,2,1,3,2]):
        if j==5 and bar%4==3:continue
        play(base+j*QUAVER+.035+rng.uniform(0,.016),chord[idx],.49,'pluck',(.22 if j in (0,3) else .13)*rng.uniform(.84,1.04),.69)
    if bar%4!=3 or bar>7:
        play(base+.09,chord[0]-12,BAR*(.68 if bar%4==3 else .88),'bow',.16,.35)
# Circular stereo early reflections preserve a continuous loop at the bar line.
dry=stereo.copy()
for delay,gain,flip in [(.047,.16,1),(.097,.11,0),(.149,.09,1),(.241,.06,0),(.323,.045,1),(.413,.025,0)]:
    stereo+=gain*np.roll(dry[:,::-1] if flip else dry,round(delay*RATE),axis=0)
stereo*=.56/np.abs(stereo).max()
pcm=np.rint(32767*stereo).astype('<i2')
with wave.open(str(OUT/'A_Light_Left_On.wav'),'wb') as f:
    f.setparams((2,2,RATE,0,'NONE','not compressed'));f.writeframes(pcm.tobytes())
stats={'title':'A Light Left On','bars':len(chords),'seconds':N/RATE,'sample_rate':RATE,'channels':2,'peak':float(np.abs(stereo).max()),'rms':float(np.sqrt(np.mean(stereo**2))),'boundary_delta':float(np.max(np.abs(stereo[0]-stereo[-1])))}
assert stats['rms']>.05 and stats['boundary_delta']<.035,stats
(OUT/'score.json').write_text(json.dumps(stats,indent=2))
print(stats)
