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

    while amp2 > baseline:
        upperi = upperi + 1
        amp2 = ys[upperi]
        upperx = xs[upperi]

    peak_area = 0.
    inter = loweri
    while inter < upperi:
        peak_area = peak_area + (ys[inter]-baseline)
        inter = inter + 1

    print "peak area", peak_area

    return lowerx, upperx, peak_area

def plotData(xs, ys, baseline, lows, highs, peak_poss, peak_areas,peak_match,area_match,decision):
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111)
    ax.spines["top"].set_visible(False)    
    ax.spines["bottom"].set_visible(False)    
    ax.spines["right"].set_visible(False)    
    ax.spines["left"].set_visible(False)    
    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()   
    plt.yticks(fontsize=20)    
    plt.xticks(fontsize=20)   
    ax.set_xlabel('Time (minutes)', fontsize=20)
    ax.set_ylabel('Light absorbtion', fontsize=20)
    plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                    labelbottom="on", left="off", right="off", labelleft="on") 
 
    plt.plot(x_axis, y_axis)
    #plt.plot((xs[0], xs[-1]), (baseline, baseline), 'r-')
    strings = ["Peak calculations"]
    for i in xrange(len(lows)):
        #plt.plot((lows[i], lows[i]), (min(ys), max(ys)), 'g-')
        #plt.plot((highs[i], highs[i]), (min(ys), max(ys)), 'b-')
        strings.append('$t_{%i} = %0.2f \; a_{1} = %0.2f$' %(i+1,peak_poss[i][0],peak_areas[i]))

    display_str = "\n".join(strings)
    ax.text(0.01, 0.75, display_str,
            verticalalignment='bottom', horizontalalignment='left',
            transform=ax.transAxes,
            color='green', fontsize=20)

    ax.text(0.01, 0.05, "Time corrected peak match = %0.2f\nTime corrected area match = %0.2f" %(peak_match,area_match),
            transform=ax.transAxes,
            color='orange', fontsize=20)

    ax.text(0.6, 0.05, decision,
            transform=ax.transAxes,
            color='red', fontsize=20)

    #plt.show()
    plt.savefig("trial_fig.png")

if __name__=="__main__":
    
    #f = open('input.txt', 'r')
    f = open('export_elpho_drug_ISZ.txt','r') 
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
    maxtab, mintab = peakdet(series,10.)
    basel = findBaseline(series)

    for pair in maxtab:
        final_peaks.append((float(x_axis[int(pair[0])]), float(pair[1])))

    if len(final_peaks) > 4:
        final_peaks.pop(0)

    print(final_peaks)

    lower_ranges = []
    upper_ranges = []
    peak_areas = []
    for peak in final_peaks:
        low, up, area = findArea(peak,x_axis,y_axis,basel)
        lower_ranges.append(low)
        upper_ranges.append(up)
        peak_areas.append(area)

    diff1 = final_peaks[2][0] / final_peaks[0][0]
    diff2 = final_peaks[3][0] / final_peaks[1][0]
    peak_match = abs(diff1/diff2)
    print diff1, diff2, peak_match

    ratio1 = (peak_areas[2]/final_peaks[2][0]) / (peak_areas[0]/final_peaks[0][0])
    ratio2 = (peak_areas[3]/final_peaks[3][0]) / (peak_areas[1]/final_peaks[1][0])
    area_match = abs(ratio1/ratio2)
    print ratio1, ratio2, area_match

    if (1-area_match) > 0.1 or (1-peak_match) > 0.1:
        decision = "FAIL"
    else:
        decision = "PASS"

    plotData(x_axis,y_axis,basel, lower_ranges, upper_ranges, final_peaks, peak_areas, peak_match, area_match, decision)
