from pylab import ones


def crossProduct(v1,v2):
	cross = ones(3)
	cross[0] = v1[1]*v2[2] - v1[2]*v2[1]
	cross[1] = - v1[0]*v2[2] + v1[2]*v2[2] 
	cross[2] = v1[0]*v2[1] - v1[1]*v2[0]
	return cross

def dotProduct(v1,v2):
	dot = v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
	return dot 
