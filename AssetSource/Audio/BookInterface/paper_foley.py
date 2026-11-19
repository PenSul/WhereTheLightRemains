"""Render the paper notebook's original interface Foley. Python 3 and NumPy; no source recordings."""
from pathlib import Path
import wave
import numpy as np
RATE=48000
ROOT=Path(__file__).resolve().parent
def envelope(t,attack,release):
    return (1-np.exp(-np.maximum(t,0)/attack))*np.exp(-np.maximum(t,0)/release)*(t>=0)
def grain(t,rng,speed):
    white=rng.normal(size=len(t))
    # Grain against cold-pressed paper: broad soft band, with sharp hiss removed.
    fine=np.convolve(white,np.array([1,2,3,4,3,2,1])/16,'same')
    soft=np.convolve(fine,np.ones(40)/40,'same')
    return (fine-soft)*(.80+.20*np.cos(2*np.pi*speed*t))
def tap(t,hz,decay):
    return envelope(t,.002,decay)*(np.sin(2*np.pi*hz*t)+.30*np.sin(2*np.pi*1.94*hz*t+.28)+.11*np.sin(2*np.pi*2.65*hz*t))
def create(name,duration,seed,render,peak):
    n=round(duration*RATE);t=np.arange(n)/RATE
    samples=render(t,np.random.default_rng(seed))
    samples-=samples.mean()
    samples*=np.minimum(1,t/.001)*np.minimum(1,(duration-t)/.012)
    samples*=peak/np.max(np.abs(samples))
    data=(samples*32767).round().astype('<i2')
    with wave.open(str(ROOT/(name+'.wav')),'wb') as wav:
        wav.setparams((1,2,RATE,len(data),'NONE','not compressed'));wav.writeframes(data.tobytes())
create('SW_UILeafTouch',.110,4901,lambda t,r:
       .85*grain(t,r,53)*envelope(t,.0024,.014)+.16*tap(t,674,.010)+.047*tap(t-.009,1258,.012),.245)
create('SW_UIBookMark',.205,4902,lambda t,r:
       .75*grain(t,r,31)*envelope(t,.002,.025)+.22*tap(t,360,.021)+
       .12*tap(t-.025,747,.032)+.26*grain(t,r,35)*envelope(t-.033,.004,.015),.32)
create('SW_UIBookRelease',.188,4903,lambda t,r:
       .63*grain(t,r,19)*envelope(t,.009,.027)+.23*tap(t,476,.016)+
       .19*tap(t-.023,319,.023)+.14*grain(t,r,46)*envelope(t-.046,.004,.019),.285)

