import numpy as np
import matplotlib.pyplot as plt

xs = []
ys = []

for i in xrange(1000):
    xs.append(float(i))
    ys.append(np.random.normal(loc=0., scale=0.01, size=1))

peakpos1 = 700.0
peakpos2 = 200.0
nbins = 50.

b = plt.hist(np.random.normal(loc=peakpos1, scale=5.0, size=500),bins = nbins, range = (peakpos1-(nbins/2.),peakpos1+(nbins/2.)))

c = plt.hist(np.random.normal(loc=peakpos2, scale=5.0, size=500),bins = nbins, range = (peakpos2-(nbins/2.),peakpos2+(nbins/2.)))

for i in xrange(len(b[0])):
    ys[int(b[1][i])] = ys[int(b[1][i])] + b[0][i]

for i in xrange(len(c[0])):
    ys[int(c[1][i])] = ys[int(c[1][i])] + c[0][i]

plt.clf()
plt.plot(xs, ys)
plt.show()
