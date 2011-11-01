from math import sin, cos, pi
from numpy import exp, array

class particle(object):
	def __init__(self, xCoord, yCoord):
		self.pos = xCoord + 1j*yCoord
		self.velocity = 0.0
		self.history = [self.pos]
	def advect(self, dt = 0.01):
		self.pos = self.velocity*dt + self.pos
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
			self.__tolerance = 0.05
		elif self._Type == 'doublet':
			self.__tolerance = 0.006
		else :
			self.__tolerance = 0.0

	def inducedVelocityAt(self, pos = 0.0 + 0.0j):
		if self._Type == 'uniformFlow':
			return self.strength*exp(1j*self.flowAngle)
		elif (self._Type == 'source') or (self._Type == 'sink'):
			if abs(pos - self.pos) <= self.__tolerance :
				return 0.0
			else :
				return self.strength*((pos.real - self.pos.real) + 1j*(pos.imag - self.pos.imag))/abs(pos - self.pos)**2
		elif self._Type == 'doublet':
			x = pos.real - self.pos.real
			y = pos.imag - self.pos.imag
			r = abs(pos - self.pos)
			return self.strength*(x**2 - y**2 +1j*2*x*y)/(2.0*pi*r**4)
		elif self._Type == 'vortex':
			if abs (pos - self.pos) > 1e-4 :
				return -1j*self.strength/(2.0*pi*(pos - self.pos))
			else:
				return 0.0 + 0.0j
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
