"""Original Lantern Street foley synthesis. Run with Python 3 and an output directory."""
from array import array
import argparse, hashlib, json, math, random, sys, wave
from pathlib import Path

RATE = 32000
TAU = 2*math.pi
# Each entry contains native event id, duration, target dBFS and a separate noise seed.
CUES = {
    'BootStoneL':(1,.175,-12.5,128), 'BootStoneR':(2,.185,-12.6,133),
    'BootTimberL':(3,.207,-12.0,142), 'BootTimberR':(4,.223,-12.2,154),
    'BootLift':(5,.159,-15.0,167), 'LandStone':(6,.279,-9.4,178),
    'LandTimber':(7,.296,-9.5,189), 'DoorSwing':(10,.84,-11.8,490),
    'QuayLatch':(11,.45,-10.8,504), 'ReedsBurn':(12,.75,-13.1,530),
    'KeepWick':(13,.48,-13.2,619), 'KeepCrate':(14,.45,-12.5,662),
    'PlaceWick':(15,.415,-12.3,716), 'PlaceCrate':(16,.42,-10.9,726),
    'ReturnWick':(17,.455,-13.0,773), 'ReturnCrate':(18,.44,-12.4,793),
}

def blow(t,start,decay,attack=.0025):
    dt=t-start
    return (1-math.exp(-dt/attack))*math.exp(-dt/decay) if dt>=0 else 0.

def ring(t,start,decay,hz,attack=.0025):
    return blow(t,start,decay,attack)*math.sin(TAU*hz*(t-start))

def arc(t,start,length):
    p=(t-start)/length
    return math.sin(math.pi*p)**2 if 0<p<1 else 0.

def grain_pattern(rng,count,start,end):
    return [(rng.uniform(start,end),rng.uniform(.002,.010),rng.uniform(.1,.36)) for _ in range(count)]

def synth(name):
    _,duration,peak_db,seed=CUES[name]
    rng=random.Random(seed); flakes=grain_pattern(rng,13,.05,duration*.80)
    low=medium=slow=0.; samples=array('f')
    spr=rng.uniform(.94,1.06); foot=name.startswith(('Boot','Land'))
    wood='Timber' in name; heavy=name.startswith('Land')
    for i in range(round(RATE*duration)):
        t=i/RATE; n=rng.uniform(-1,1)
        low+=.22*(n-low); medium+=.075*(n-medium);slow+=.017*(medium-slow)
        sand=low-medium; fibre=medium-slow
        if foot and name!='BootLift':
            gap=(.044 if heavy else .032)*spr
            heel=blow(t,.004,.025*spr);toe=blow(t,gap,.035)
            y=.77*heel*fibre+.56*toe*sand+.17*heel*(n-low)
            if wood:
                for freq,gain,decay in [(117,.41,.066),(253,.21,.044),(472,.10,.033),(734,.06,.024)]:
                    y+=gain*(ring(t,.006,decay,freq*spr)+.34*ring(t,gap,decay*.71,freq*spr))
            else:
                y+=.40*ring(t,.005,.029,85*spr)+.10*ring(t,gap,.019,236*spr)+.05*ring(t,gap+.01,.018,521*spr)
                y+=.49*sand*arc(t,gap,.066)
            if heavy:y+=.44*ring(t,.006,.071,63*spr)+.48*fibre*arc(t,.04,.11)
        elif name=='BootLift':
            y=.75*sand*arc(t,.003,.079)+1.55*fibre*arc(t,.025,.095)+.11*ring(t,.012,.028,135)
        elif name=='DoorSwing':
            angle=arc(t,.055,.625)
            p=TAU*(159*t+19*t*t+1.35*math.sin(TAU*3.4*t))
            friction=(.62+.38*math.sin(TAU*(22*t+6*t*t)))**2
            y=.26*angle*friction*(math.sin(p)+.5*math.sin(2*p)+.23*math.sin(3*p))+.7*fibre*angle
            y+=.48*ring(t,.012,.052,121)+.2*ring(t,.021,.021,580)+.32*ring(t,.69,.049,93)+.31*sand*blow(t,.685,.045)
        elif name=='QuayLatch':
            y=.55*ring(t,.012,.041,638)+.16*ring(t,.012,.045,1244)+.9*sand*blow(t,.012,.03)
            y+=.53*ring(t,.158,.057,169)+.32*ring(t,.166,.04,359)+1.18*fibre*blow(t,.157,.061)+.28*sand*arc(t,.037,.103)
        elif name=='ReedsBurn':
            y=1.13*sand*arc(t,.013,.63)+.19*(n-low)*arc(t,.023,.55)
            y+=(n-low)*sum(g*blow(t,s,l,.0007) for s,l,g in flakes)
            y+=.21*ring(t,.012,.024,296)
        else:
            placing=name.startswith('Place');taking=name.startswith('Keep'); crate='Crate' in name
            sweep=arc(t,.016,.28 if placing else .34)
            y=.39*sand*sweep+.33*fibre*arc(t,.047,.275)
            if crate:
                for start,freq,vol,decay in [(.015,126,.62,.08),(.042,318,.23,.057),(.115,189,.22,.052)]:
                    shift=.16 if not (placing or taking) else 0
                    y+=vol*ring(t,start+shift,decay,freq*(1.12 if taking else 1))
                y+=.19*(n-low)*blow(t,.018 if placing else .073,.031)
            else:
                y+=.64*(n-low)*arc(t,.009,.12)+.9*sand*arc(t,.025,.16)
            # A very short related two-note glass figure: lift, touch down or return inward.
            tones=(468,624) if taking else ((312,468) if placing else (468,312))
            for k,hz in enumerate(tones):
                y+=(.13 if crate else .22)*ring(t,.033+.103*k,.067,hz,.007)
                y+=.036*ring(t,.041+.103*k,.044,2.013*hz,.008)
        end=min(1.,i/(RATE*.002),(duration-t)/.028)
        samples.append(y*max(0,end))
    gain=32767*10**(peak_db/20)/max(abs(x) for x in samples)
    pcm=array('h',(round(x*gain) for x in samples))
    if sys.byteorder!='little':pcm.byteswap()
    return pcm.tobytes()

def build(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    report={}
    for name,(code,duration,peak,seed) in CUES.items():
        p=folder/('SW_'+name+'.wav');raw=synth(name)
        with wave.open(str(p),'wb') as out:
            out.setparams((1,2,RATE,len(raw)//2,'NONE','not compressed'));out.writeframes(raw)
        with wave.open(str(p),'rb') as src:assert src.readframes(src.getnframes())==raw
        report[name]={'id':code,'seconds':duration,'peak_dbfs':peak,'rate':RATE,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (folder/'foley.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    build(parser.parse_args().folder)

