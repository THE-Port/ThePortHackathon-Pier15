# from array import array 

import numpy
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

f= open('input.txt', 'r')
pairs = f.readlines()
x_axis = []
y_axis = []

for pair in pairs:
	values = pair.split()
	x_axis.append(float(values[0]))
	y_axis.append(float(values[1]))

# calc_baseline(x_axis, y_axis)
# print zeroed_y 


base = peakutils.baseline(y_axis, 2)
pyplot.figure(figsize=(10,6))
pyplot.plot(x_axis, y_axis)
pyplot.plot(x_axis, base)