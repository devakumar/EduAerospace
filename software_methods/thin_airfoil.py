from numpy import linspace, array, linalg, ones, shape, dot
import scipy.linalg
from math import pi, cos, sin
from pylab import plot, show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D
from vector_operations import crossProduct,dotProduct
import framework
import vortexLattice
import flow_visualization

def create_list_of_panels(points):
	""" This function returns a list of panel or horseshoe vortices given the surface points"""
	panels = []
	index = 0
	print shape(points)
	for i in range(len(points[:,0]) - 1):
		for j in range(len(points[0,:]) - 1):
			cornerpt1 = (points[i][j]*3 + points[i+1][j])/4
			cornerpt2 = (points[i][j+1]*3 + points[i+1][j+1])/4
			mp1 = (points[i][j] + points[i][j+1]) /2
			mp2 = (points[i+1][j] + points[i+1][j+1])/2
			controlpt = (mp1 + 3*mp2)/4
			rnot = (points[i+1][j] - points[i][j])
			rnot_cap = rnot/linalg.norm(rnot)
			panels.append(vortexLattice.horseShoe(index,cornerpt1,cornerpt2,controlpt,1,rnot_cap))
			index = index + 1
	return panels



# input geometry
# descretize it to panels

x = linspace(0,0.27,11)
y = linspace(0,1.4,21)
point_list = []

for i in range(11):
	b = []
	for j in range(21):
		b.append(array([x[i],y[j],0]))
	point_list.append(b)
point_array = array(point_list)

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

freestream = [40*cos(3*2*pi/180),0,40*sin(3*2*pi/180)]
pan_list = create_list_of_panels(point_array)
A = framework.compute_A_matrix(pan_list)
B = framework.compute_B_matrix(pan_list,freestream)
strengths = framework.solve_for_strength(A,B)


X = []
Y = []
Z = []
for j in range(10):
	x = []
	y = []
	z = []
	for i in range(20): 
		x.append(pan_list[i+j*20].controlpoint[0])
		y.append(pan_list[i+j*20].controlpoint[1])
		z.append(-1.117*strengths[i+j*20]*40)
	f.plot(array(x),array(y),array(z))
	X.append(x)
	Y.append(y)
	Z.append(z)
	
for i in range(len(array(X)[:,1])):
	f.plot(array(X)[i,:],array(Y)[i,:],array(Z)[i,:])

#for i in range(len(pan_list)):
#	f.plot(array([pan_list[i].controlpoint[0],pan_list[i].controlpoint[0]]),array([pan_list[i].controlpoint[1],pan_list[i].controlpoint[1]]),array([0,strengths[i]]))
	
#for i in range(len(strengths)):
#	pan_list[i].strength = strengths[i]


#time_array = flow_visualization.simulate(pan_list,[],freestream)
#for i in range(len(time_array[:,0])):
#		f.plot(time_array[i,:,0],time_array[i,:,1],time_array[i,:,2])
#				
#print time_array.shape

show()
