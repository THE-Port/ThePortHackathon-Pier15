import numpy as np
import matplotlib.pyplot as plt

xs = []
ys = []

for i in xrange(1000):
    xs.append(float(i))
    ys.append(np.random.normal(loc=0., scale=0.01, size=1))

peakpos1 = 200.0
peakpos2 = 300.0
peakpos3 = 700.0
peakpos4 = 800.0
nbins = 50.


a = plt.hist(np.random.normal(loc=peakpos1, scale=2.0, size=500),bins = nbins, range = (peakpos1-(nbins/2.),peakpos1+(nbins/2.)))
b = plt.hist(np.random.normal(loc=peakpos2, scale=2.0, size=500),bins = nbins, range = (peakpos2-(nbins/2.),peakpos2+(nbins/2.)))

c = plt.hist(np.random.normal(loc=peakpos3, scale=2.0, size=500),bins = nbins, range = (peakpos3-(nbins/2.),peakpos3+(nbins/2.)))
d = plt.hist(np.random.normal(loc=peakpos4, scale=2.0, size=500),bins = nbins, range = (peakpos4-(nbins/2.),peakpos4+(nbins/2.)))

for i in xrange(len(a[0])):
    ys[int(a[1][i])] = ys[int(b[1][i])] + a[0][i]
for i in xrange(len(c[0])):
    ys[int(b[1][i])] = ys[int(b[1][i])] + b[0][i]

for i in xrange(len(c[0])):
    ys[int(c[1][i])] = ys[int(c[1][i])] + c[0][i]
for i in xrange(len(d[0])):
    ys[int(d[1][i])] = ys[int(d[1][i])] + d[0][i]

plt.clf()
plt.plot(xs, ys)
plt.show()

f = open('generated_data.txt','w')
for i in xrange(len(xs)):
    f.write('%0.3f\t%0.3f\n' %(xs[i],ys[i]))

f.close()
