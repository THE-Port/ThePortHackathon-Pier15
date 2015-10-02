# from array import array 

#FINDS BOTH BASELINE AND MEAN LINE


import numpy
from numpy import NaN, Inf, arange, isscalar, asarray, array, mean
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot

# def calc_baseline(x,y):   
#     zeroed_y=[]   
#     for n in range(len(y)): 
#         line_y=array(y[n][0:1]+y[n][-41:-1])
#         line_x=array(x[n][0:1]+x[n][-41:-1])
#         p=scipy.polyfit(baseline_x,baseline_y,1)
#         baseline_y=array(x[n])*p[0]+p[1]
#         zeroed_y.append(baseline_y)
#     return zeroed_y

#f= open('input.txt', 'r')
#f = open('export_elpho_drug_ISZ.txt','r') 
f = open('export_elpho_drug_ISZ+RIF.txt','r') 

pairs = f.readlines()
x_axis = []
y_axis = []

for pair in pairs:
	values = pair.split()
	x_axis.append(float(values[0]))
	y_axis.append(float(values[1]))

two = numpy.column_stack((x_axis,y_axis))
variance = numpy.var(asarray(two),)

# calc_baseline(x_axis, y_axis)
# print zeroed_y 

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

series = y_axis
maxtab, mintab = peakdet(series,0.1)
basel = findMean(series)



x_axis = asarray(x_axis)
y_axis = asarray(y_axis)
mean = []
cut = []
cutx = []
cuty=[]

for y in y_axis:
	mean.append(float(basel))

highcut = basel + ((variance-basel)/6)
lowcut = basel - ((variance-basel)/6)

for a in range (0,len(two)):
	if two[a][1] > lowcut and two[a][1] < highcut:
		cut.append(two[a])


for m in range (0, len(cut)):
	cutx.append(cut[m][0])
	cuty.append(cut[m][1])

base = peakutils.baseline(y_axis, 2)

pyplot.figure(figsize=(10,6))

pyplot.plot(x_axis, y_axis, label="data")
pyplot.plot(x_axis, base, label = "baseline")
pyplot.plot(x_axis, mean, label= "mean")
pyplot.plot(cutx, cuty, label= "cut")

pyplot.plot()
pyplot.legend()

pyplot.show()