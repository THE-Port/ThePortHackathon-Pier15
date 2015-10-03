
#FINDS BOTH BASELINE AND MEAN LINE


import numpy
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
#from peakfind.py import findArea

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

#def removePeaks(peaks):

if __name__=="__main__":

    #f= open('input.txt', 'r')
    f = open('export_elpho_drug_ISZ.txt','r') 
    #f = open('export_elpho_drug_ISZ+RIF.txt','r') 

    pairs = f.readlines()
    x_axis = []
    y_axis = []

    for pair in pairs:
        values = pair.split()
        x_axis.append(float(values[0]))
        y_axis.append(float(values[1]))

    maxtab, mintab = peakdet(y_axis,0.1)
    basel = findMean(y_axis)

    cutx, cuty = cutdata(x_axis, y_axis,15)
    mean = meanarray(y_axis)

    x_axis = asarray(x_axis)
    y_axis = asarray(y_axis)
    cutx = asarray(cutx)
    cuty = asarray(cuty)
    mean = asarray(mean)

    base = peakutils.baseline(y_axis, 2)
    cutbase = peakutils.baseline(cuty, 2)

    pyplot.figure(figsize=(10,6))

    pyplot.plot(x_axis, y_axis, label="data")
    pyplot.plot(x_axis, base, label = "baseline")
    pyplot.plot(x_axis, mean, label= "mean")
    pyplot.plot(cutx, cuty, label= "cut")
    pyplot.plot(cutx, asarray(cutbase), label = "cut baseline")


    pyplot.plot()
    pyplot.legend()

    pyplot.show()

