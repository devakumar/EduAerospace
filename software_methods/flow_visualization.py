from mpl_toolkits.mplot3d import Axes3D
from pylab import array, plot, show, linspace


class particle:
	""" this class represents a particle which is strengthless and moves in accordance the flow veocity field"""
	def __init__(self,x,y,z):
		self.coord = array([x,y,z])
		
	def velocity(self,panels_3d,horshoe_panels,freestream):
		""" this function calculates the velocity for given singularity ddistribution and freestream"""
		velocity = array([0,0,0])
		for panel in panels_3d:
			velocity += panel.velocity_coeff(self.coord)*panel.strength
		for pan in horshoe_panels:
			velocity += pan.velocity_coeff(self.coord)*pan.strength
		velocity += freestream
		return velocity
		
def simulate(panels_3d,horshoe_panels,freestream):
	"""this function simulates the given distribution for 5 sec and returns the positions of particles in an array which were at specific locations"""
	pt_list = []		
#	y = linspace(-0.2,1.9,20) for lifting line
#	z = linspace(-0.2,0.2,5)

#	y = linspace(-0.2,5.2,20) 3d panel methods
#	z = linspace(-0.5,0.5,5)


	for i in y:
		for j in z:
			pt_list.append(particle(0.25,i,j))
	t,i = 0,0	
	time_array = []	
	while t<2:
		print i+1
		position_array = []
		for point in pt_list:
			position_array.append(point.coord)
			point.coord += point.velocity(panels_3d,horshoe_panels,freestream) * 0.1
		t += 0.1
		i += 1
		time_array.append(position_array)
	return array(time_array)

	

	
	
			
