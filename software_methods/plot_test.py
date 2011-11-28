from numpy import linspace, array, linalg, ones, shape, dot
import scipy.linalg
from math import pi, cos, sin
from pylab import show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D

x = linspace(0,0.27,11)
y = linspace(0,1.4,21)
point_list = []

ax = figure()
f = Axes3D(ax)


for i in range(11):
	b = []
	for j in range(21):
		b.append(array([x[i],y[j],0]))
	barray = array(b)
	f.plot(barray[:,0],barray[:,1],barray[:,2])
	f.hold(True)
	
for i in range(21):
	b = []
	for j in range(11):
		b.append(array([x[j],y[i],0]))
	barray = array(b)
	f.plot(barray[:,0],barray[:,1],barray[:,2])
	f.hold(True)
	
show()




