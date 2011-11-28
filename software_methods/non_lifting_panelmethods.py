from numpy import linspace, array, linalg, ones, shape, dot
import scipy.linalg
from math import pi, cos, sin
from pylab import plot, show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D
import vortexLattice
from vector_operations import crossProduct,dotProduct
import framework

class panel(object):
	""" this class is to represent a panel in 3d made of 4 filaments"""
	def __init__(self,corner1,corner2,corner3,corner4,index,strength):
		self.index = index
		self.corner1 = corner1
		self.corner2 = corner2
		self.corner3 = corner3
		self.corner4 = corner4
		self.strength = strength
		self.normal = crossProduct(corner3-corner1,corner2-corner4)
		self.normal_cap = self.normal/linalg.norm(self.normal)
		self.controlpoint = 1/4*(corner1 + corner2 + corner3 + corner4)


	def velocity_coeff(self,point):
		""" this function computes the velocity co-effecient due to the panel on any point"""
		r1 = point - self.corner1
		r2 = point - self.corner2	
		r3 = point - self.corner3	
		r4 = point - self.corner4
	
		r12 = self.corner2 - self.corner1
		r23 = self.corner3 - self.corner2
		r34 = self.corner4 - self.corner3
		r41 = self.corner1 - self.corner4
		
		n12 = crossProduct(r1,r2)
		n23 = crossProduct(r2,r3)
		n34 = crossProduct(r3,r4)
		n41 = crossProduct(r4,r1)
		
		ncap_12 = n12/linalg.norm(n12)
		ncap_23 = n23/linalg.norm(n23)
		ncap_34 = n34/linalg.norm(n34)
		ncap_41 = n41/linalg.norm(n41)
	
		v12 = ncap_12 * (1/(4*pi)) * dotProduct(r12,(r1/linalg.norm(r1)-r2/linalg.norm(r2)))/linalg.norm(crossProduct(r1,r2))
		v23 = ncap_23 * (1/(4*pi)) * dotProduct(r23,(r2/linalg.norm(r2)-r3/linalg.norm(r3)))/linalg.norm(crossProduct(r2,r3))
		v34 = ncap_34 * (1/(4*pi)) * dotProduct(r34,(r3/linalg.norm(r3)-r4/linalg.norm(r4)))/linalg.norm(crossProduct(r3,r4))
		v41 = ncap_41 * (1/(4*pi)) * dotProduct(r41,(r4/linalg.norm(r4)-r1/linalg.norm(r1)))/linalg.norm(crossProduct(r4,r1))
	
		v_net = v12 + v23 + v34 + v41
		return v_net


		
		
def compute_A_matrix(panel_list,kutta_Ulist,kutta_Llist):               
	""" the function which returns a matrix of influence co-effecients"""
	print(len(panel_list))
	a = ones((len(panel_list),len(panel_list)))
	for panelm in panel_list:
		for paneln in panel_list:
				a[panelm.index][paneln.index] = framework.compute_influence_coeffs(panelm,paneln)
				if paneln in kutta_Ulist:
					hsv = vortexLattice.horseShoe(1,paneln.corner4,paneln.corner1,1,1,array([1,0,0]))
					a[panelm.index][paneln.index] += framework.compute_influence_coeffs(panelm,hsv)
				elif paneln in kutta_Llist:				
					hsv = vortexLattice.horseShoe(1,paneln.corner3,paneln.corner2,1,1,array([1,0,0]))
					a[panelm.index][paneln.index] += framework.compute_influence_coeffs(panelm,hsv)
	return a
	








