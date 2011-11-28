from numpy import linspace, array, linalg, ones, shape, dot
import scipy.linalg
from math import pi, cos, sin
from pylab import plot, show, figure, hold, ones, array
from mpl_toolkits.mplot3d import Axes3D
import vector_operations

def compute_A_matrix(panel_list):               
	""" the function which returns a matrix of influence co-effecients"""
	print(len(panel_list))
	a = ones((len(panel_list),len(panel_list)))
	for panelm in panel_list:
		for paneln in panel_list: 
			a[panelm.index][paneln.index] = compute_influence_coeffs(panelm,paneln)
	return a


def compute_influence_coeffs(panelm,paneln):    # mth control point by nth panel

	""" the function which computes the influnce co-efficient due to n-th panel on m-th control point"""
	v_net = paneln.velocity_coeff(panelm.controlpoint)
	normal_component = vector_operations.dotProduct(v_net,panelm.normal_cap)
	
	return normal_component

def compute_B_matrix(panel_list,freestream):
	""" the function which returns a matrix of the fresstream co-effecients"""
	print "\n", "\n"
	b = ones(len(panel_list))
	for panel in panel_list:
		b[panel.index] = vector_operations.dotProduct(freestream,panel.normal_cap)
	return b



def solve_for_strength(A,B):
	""" the function which solves for the strenghth of these vortex panels"""

	x,r,s,si = scipy.linalg.lstsq(A,B,0.0001)
	return x





