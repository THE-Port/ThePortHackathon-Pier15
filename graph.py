import pylab

data = pylab.loadtxt("input.txt");

pylab.plot( data[:,0], data[:,1])

pylab.show()