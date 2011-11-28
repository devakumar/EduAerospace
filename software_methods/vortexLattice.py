from numpy import linspace, array, linalg, ones, shape, dot
import scipy.linalg
from math import pi, cos, sin
from pylab import plot, show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D
from vector_operations import crossProduct,dotProduct
import framework


class horseShoe(object):
	""" this is a class for representing horse shoe bound vortex"""
	def __init__(self,index,corner1,corner2,controlpoint,strength,r0):
		""" this function is to initialize te horse_shoe vortex with various variables"""
		self.index = index
		self.corner1 = corner1	
		self.corner2 = corner2
		self.strength = strength
		self.controlpoint = controlpoint
		self.normal = crossProduct((controlpoint-corner1), (controlpoint-corner2))
		self.normal_cap = self.normal/linalg.norm(self.normal)
		self.r0 = r0
	
	def velocity_coeff(self,point):
		"""this function returns the velocity of this panel at any point"""
			# for finite length portion of horshoevortex
		r1 = point - self.corner1
		r2 = point - self.corner2
		r0_ab = self.corner2 - self.corner1
		n_ab = crossProduct(r1,r2)
		n_cap_ab = n_ab/linalg.norm(n_ab)
	
		# for first semi infinte portion
		n_ac = crossProduct(r1,self.r0)
		n_cap_ac = n_ac/linalg.norm(n_ac)
		
		# for second semi infinite portion
		n_bc = crossProduct(r2,self.r0)
		n_cap_bc = n_bc/linalg.norm(n_bc)
		
		
		v_ab = n_cap_ab * (1/(4*pi)) * dotProduct(r0_ab,(r1/linalg.norm(r1) - r2/linalg.norm(r2)))/linalg.norm(crossProduct(r1,r2))
		v_ac = n_cap_ac * (1/(4*pi)) * (dotProduct(self.r0,r1/linalg.norm(r1)) + 1) / linalg.norm(crossProduct(r1,self.r0))   
		v_bc = n_cap_bc * (-1/(4*pi)) * (dotProduct(self.r0,r2/linalg.norm(r2)) + 1) / linalg.norm(crossProduct(r2,self.r0))
	
	
		v_net = v_ab + v_ac + v_bc
		return v_net
	
