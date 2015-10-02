import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
import matplotlib.pyplot as plt

def peakdet(v, delta, x = None):

    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')
    
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')
    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

def findBaseline(ys):
    print "starting findBaseline"
    basel = mean(ys)
    print "returning a baseline of", basel
    return basel

def findArea(peak,xs,ys,baseline):
    print "starting findArea"
    print peak
    peaki = xs.index(peak[0])
    print peaki
    loweri=peaki
    upperi=peaki
    amp = peak[1]
    amp2 = peak[1]

    while amp > baseline:
        loweri = loweri - 1
        amp = ys[loweri]
        lowerx = xs[loweri]
    print "at amp", amp, "x", lowerx

    while amp2 > baseline:
        upperi = upperi + 1
        amp2 = ys[upperi]
        upperx = xs[upperi]
    print "at amp2", amp2, "x", upperx

def plotData(xs, ys, baseline):
    plt.plot(x_axis, y_axis)
    plt.plot((xs[0], xs[-1]), (baseline, baseline), 'r-')
    plt.show()

if __name__=="__main__":
    
    f = open('input.txt', 'r')
    #f = open('export_elpho_drug_ISZ.txt','r') 
    #f = open('generated_data.txt','r') 
    pairs = f.readlines()
    x_axis = []
    y_axis = []
    final_peaks = []

    for pair in pairs:
        values = pair.split()
        x_axis.append(float(values[0]))
        y_axis.append(float(values[1]))

    series = y_axis
    maxtab, mintab = peakdet(series,0.1)
    basel = findBaseline(series)

    for pair in maxtab:
        final_peaks.append((float(x_axis[int(pair[0])]), float(pair[1])))

    #print(maxtab)
    print(final_peaks)
    for peak in final_peaks:
        findArea(peak,x_axis,y_axis,basel)

    plotData(x_axis,y_axis,basel)
