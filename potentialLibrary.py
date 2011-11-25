from math import sin, cos, pi, atan2
from numpy import exp, array

class particle(object):
	def __init__(self, xCoord, yCoord):
		self.pos = xCoord + 1j*yCoord
		self.velocity = 0.0
		self.k1 = 0.0
		self.k2 = 0.0
		self.history = [self.pos]
	def advect(self, dt = 0.01, integType = 'euler'):
		if integType == 'euler':
			self.pos = self.velocity*dt + self.pos
		elif integType == 'rk2' :
			self.pos = self.pos + 0.5*(self.k1 + self.k2)
		else :
			raise NameError("Integration type unknown")
		self.history.append(self.pos)

class potElement(object):
	""" Definies a potential flow element 
	    Attributes:
		----------
			_Type : 'uniformFlow' | 'source' | 'sink' | 'doublet' | 'vortex'
			strength : "Gives strength of the potential flow element"
			unit : "Gives the units of strength"
			pos : 
			flowAngle :
			vel : 
		Methods :
		-------
			inducedVelocityAt(pos)"""
	def __init__(self, elementInfo):
		self.elementInfo = elementInfo
		self._Type = elementInfo['type']
		self.strength = elementInfo['strength']
		if self._Type == 'uniformFlow':
			self.flowAngle = elementInfo['angle']*pi/180.0
		else :
			self.pos = elementInfo['pos']
		if elementInfo.has_key('moving'):
			self.vel = elementInfo['moving']
		# Implement units of strength here
		self.units = None
		# Numerical tolerance values - Distance after or below which numerical
		# singularities are to be treated explicitly. APPROXIMATION
		if (self._Type == 'source') or (self._Type == 'sink'):
			self.__tolerance = 0.5
		elif self._Type == 'doublet':
			self.__tolerance = 0.5
		elif self._Type == 'vortex':
			self.__tolerance = 0.5
		else :
			self.__tolerance = 0.0

	def inducedVelocityAt(self, pos = 0.0 + 0.0j):
		if self._Type == 'uniformFlow':
			return self.strength*exp(1j*self.flowAngle)
		elif (self._Type == 'source') or (self._Type == 'sink'):
			theta = atan2(pos.imag - self.pos.imag, pos.real - self.pos.real)
			if abs(pos - self.pos) <= self.__tolerance :
				r = abs(pos - self.pos)
				return self.strength*r*exp(1j*theta)/self.__tolerance
			else :
				return self.strength*( pos - self.pos)/abs(pos - self.pos)**2
		elif self._Type == 'doublet':
			x = pos.real - self.pos.real
			y = pos.imag - self.pos.imag
			r = abs(pos - self.pos)
			if ( ((cmp(self.strength, 0) and cmp(pos.real, self.pos.real)) or \
					(cmp(0, self.strength) and cmp(self.pos.real, pos.real))) and (r < self.__tolerance)) :
				return self.strength*pow(r, 2.0)*((pow(x, 2.0) - pow(y, 2.0)) + 1j*2.0*x*y)/pow(self.__tolerance, 2.0)
			else :
				return self.strength*(x**2 - y**2 +1j*2*x*y)/(2.0*pi*r**4)
		elif self._Type == 'vortex':
			if abs (pos - self.pos) > 1e-4 :
				temp = -1j*self.strength/(2.0*pi*(pos - self.pos))
				return temp.real -1j*temp.imag
			else :
				theta = atan2(pos.imag - self.pos.imag, pos.real - self.pos.real)
				temp = -1j*self.strength*exp(1j*theta)/(2.0*pi*self.__tolerance)
				return temp.real -1j*temp.imag
		else :
			raise NameError('element type', self._Type, 'unknown')


class potentialLibrary(object):
	""" class potentialLibrary(object, potElement): - can this be used?"""
	def __init__(self):
		""" """
		self.elements = []
		self.uniformFlows = self.getUniformList()
		self.sources = self.getSourceList()
		self.sinks = self.getSinkList()
		self.doublets = self.getDoubletList()
		self.vortices = self.getVortexList()
		self.elemRange = self.getRange()

	def addElement(self, elementInfo):
		newElement = potElement(elementInfo)
		self.elements.append(newElement)

	def deleteElement(self, element):
		self.elements.remove(element)

	def getSourceList(self):
		return [element for element in self.elements if element._Type == 'source']

	def getSinkList(self):
		return [element for element in self.elements if element._Type == 'sink']

	def getDoubletList(self):
		return [element for element in self.elements if element._Type == 'doublet']

	def getVortexList(self):
		return [element for element in self.elements if element._Type == 'vortex']

	def getUniformList(self):
		return [element for element in self.elements if element._Type == 'uniformFlow']

	def velocityAt(self, pos):
		""" Returns the velocity at pos due to all the elements present in the
		library """
		velList = [element.inducedVelocityAt(pos) for element in self.elements]
		return sum(velList)

	def getRange(self):
		""" Gives x and y limits of the elements. Returns [xMin, xMax, yMin, yMax] """
		if self.elements != [] :
			xCoord = [element.pos.real for element in self.elements if element._Type != 'uniformFlow']
			yCoord = [element.pos.imag for element in self.elements if element._Type != 'uniformFlow']
			if xCoord != [] :
				return [min(xCoord), max(xCoord), min(yCoord), max(yCoord)]
			else :
				return None
		else :
			return None
