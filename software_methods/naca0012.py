from numpy import linspace, array, linalg, ones, shape, dot
from matplotlib.mlab import load
import scipy.linalg
from math import pi, cos, sin
from pylab import show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D

import framework
import non_lifting_panelmethods
import vortexLattice
import flow_visualization
ax = figure()
f = Axes3D(ax)
naca = load('naca0012.dat')
np = len(naca)


grid_points = []
for z in linspace(0,5,5):
	points = [array([naca[i][0],z,naca[i][1]]) for i in range(np)]
	point_array = array(points)
	f.plot(point_array[:,0],point_array[:,1],point_array[:,2])
	grid_points.append(point_array)
grid_point_array = array(grid_points)

for i in range(len(grid_point_array[1,:])):
	f.plot(grid_point_array[:,i,0],grid_point_array[:,i,1],grid_point_array[:,i,2])


index = 0
panels = []
for i in range(len(grid_point_array[:,1])-1):
	for j in range(len(grid_point_array[1,:])-1):
		
		corner1 = grid_point_array[i,j]
		corner2 = grid_point_array[i,j+1]
		corner3 = grid_point_array[(i+1),(j+1)]
		corner4 = grid_point_array[i+1,j]
		
		panels.append(non_lifting_panelmethods.panel(corner1,corner2,corner3,corner4,index,1))
		index += 1
		
freestream = [40*cos(3*2*pi/180),0,40*sin(3*2*pi/180)]
pan_list = panels
A = non_lifting_panelmethods.compute_A_matrix(pan_list,panels[0:len(grid_point_array[:,0])-1],panels[0:-len(grid_point_array[:,0])+1])
B = framework.compute_B_matrix(pan_list,freestream)
strengths = framework.solve_for_strength(A,B)

for panel,strength in pan_list,strengths:
	panel.strength = strength

hsv_list = []

for Upanel in panels[0:len(grid_point_array[:,0])-1]:
	hsv.append(vortexlattice.horShoe(Upanel.index,Upanel.corner4,Upanel.corner1,array([1,1,1]),Upanel.strength,array[1,0,0]))
for Lpanel in panels[0:-len(grid_point_array[:,0])+1]:
	hsv.append(vortexlattice.horShoe(Lpanel.index,Lpanel.corner3,Upanel.corner2,array([1,1,1]),Lpanel.strength,array[1,0,0]))
	
	
t_array = flow_visualization.simulate(pan_list,hsv_list,freestream)	

for i in range(len(time_array[0,:])):
		f.plot(time_array[:,i,0],time_array[:,i,1],time_array[:,i,2])

print t_array.shape
show()
	
