
#FINDS BOTH BASELINE AND MEAN LINE


import numpy
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from peakfind import findArea, findBaseline

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

def findMean(ys):
    basel = mean(ys)
    return basel

def cutdata(x_axis, y_axis, threshold):
    cut = []
    cutx = []
    cuty=[]

    two = numpy.column_stack((x_axis,y_axis))
    variance = numpy.var(asarray(two))
    basel = findMean(y_axis)
    highcut = basel + ((variance-basel)/(threshold))
    lowcut = basel - ((variance-basel)/(threshold))

    for a in range (0,len(two)):
        if two[a][1] > lowcut and two[a][1] < highcut:
            cut.append(two[a])

    for m in range (0, len(cut)):
        cutx.append(cut[m][0])
        cuty.append(cut[m][1])
    

    return cutx, cuty   

def meanarray(y_axis):
    mean = []
    meanval = findMean(y_axis)
    for y in y_axis:
        mean.append(float(meanval))
    return mean    

def removePeaks(final_peaks, x_axis, y_axis):
    basel = findMean(y_axis)
    two = numpy.column_stack((x_axis,y_axis))
    withoutpeaks = []
    withoutpeaksx = []
    withoutpeaksy = []
    delete = {}

    for peak in final_peaks:
        low, up, area = findArea(peak, x_axis, y_axis, basel)
        #print "low : ",low
        #print "up : ",up
        for a in range (0,len(two)):
            if two[a][0] > low and two[a][0] < up:
                try:
                    foo = delete[str(a)]
                except:
                    delete[str(a)] = True

    # withoutpeaks = numpy.delete(two, delete)
    withoutpeaks = []
    for _index in range(len(two)):
        try:
            foo = delete[str(_index)]
            # pass as its meant to be deleted
        except:
            withoutpeaks.append(two[_index])

    for m in range (0, len(withoutpeaks)):
        #print m,",",withoutpeaks[m]
        withoutpeaksx.append(withoutpeaks[m][0])
        withoutpeaksy.append(withoutpeaks[m][1])

    return withoutpeaksx, withoutpeaksy

if __name__=="__main__":

    #f= open('input.txt', 'r')
    #f = open('export_elpho_drug_ISZ.txt','r') 
    f = open('export_elpho_drug_ISZ+RIF.txt','r') 

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


    for pair in maxtab:
        final_peaks.append((float(x_axis[int(pair[0])]), float(pair[1])))

    if len(final_peaks) > 4:
        final_peaks.pop(0)

    #print(final_peaks)

    withoutpeaksx, withoutpeaksy = removePeaks(final_peaks, x_axis, y_axis)


    # basel1, basel2 = findBaseline(series, final_peaks, x_axis)

    # peaknum = 0 

    # for peak in final_peaks:
    #     if peaknum in [0,1]:
    #         basel = basel1
    #     else:
    #         basel = basel2
    #     low, up, area = findArea(peak,x_axis,y_axis,basel)
    #     peaknum = peaknum + 1


    cutx, cuty = cutdata(x_axis, y_axis,15)
    mean = meanarray(y_axis)

    x_axis = asarray(x_axis)
    y_axis = asarray(y_axis)
    cutx = asarray(cutx)
    cuty = asarray(cuty)
    mean = asarray(mean)
    withoutpeaksx = asarray(withoutpeaksx)
    withoutpeaksy = asarray(withoutpeaksy)

    base = peakutils.baseline(y_axis, 2)
    cutbase = peakutils.baseline(cuty, 2)

    pyplot.figure(figsize=(10,6))

    pyplot.plot(x_axis, y_axis, label="data")
    pyplot.plot(x_axis, base, label = "baseline")
    pyplot.plot(x_axis, mean, label= "mean")
    pyplot.plot(cutx, cuty, label= "cut")
    pyplot.plot(cutx, asarray(cutbase), label = "cut baseline")
    pyplot.plot(withoutpeaksx, withoutpeaksy, label = "without peaks")


    pyplot.plot()
    pyplot.legend()

    pyplot.show()

