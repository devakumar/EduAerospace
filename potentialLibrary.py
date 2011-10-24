from math import sin, cos, pi
from numpy import exp

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
		self._Type = elementInfo['type']
		self.strength = elementInfo['strength']
		if self._Type == 'uniformFlow':
			self.flowAngle = elementInfo['alpha']*pi/180.0
		else :
			self.pos = elementInfo['pos']
		if elementInfo.has_key('moving'):
			self.vel = elementInfo['moving']
		# Implement units of strength here
		self.units = None
		# Numerical tolerance values - Distance after or below which numerical
		# singularities are to be treated explicitly. APPROXIMATION
		if (self._Type == 'source') or (self._Type == 'sink'):
			self.__tolerance = 0.15
		elif self._Type == 'doublet':
			self.__tolerance = 0.006
		else :
			self.__tolerance = 0.0

	def inducedVelocityAt(self, pos = 0.0 + 0.0j):
		if self._Type == 'uniformFlow':
			return self.strength*exp(1j*self.flowAngle)
		elif (self._Type == 'source') or (self._Type == 'sink'):
			if abs(pos - self.pos) >= self.__tolerance :
				return 0.0
			else :
				return self.strength*((pos.real - self.pos.real) + 1j*(pos.imag - self.pos.imag))/abs(pos - self.pos)**2
		elif self._Type == 'doublet':
			x = pos.real - self.pos.real
			y = pos.imag - self.pos.imag
			r = abs(pos - self.pos)
			return self.strength*(x**2 - y**2 +1j*2*x*y)/(2.0*pi*r**4)


class potentialLibrary(object, potElement):
	""" """
	def __init__(self):
		""" """
		self.elements = []
		self.noSources = self.getNoSources()
		self.noSinks = self.getNoSinks()
		self.noDoublets = self.getNoDoublets()
		self.noVortices = self.getNoVortices()

	def addElement(self):
		pass

	def deleteElement(self):
		pass

	def getSourceList(self):
		pass

	def getSinkList(self):
		pass

	def getDoubletList(self):
		pass

	def getVortexList(self):
		pass

	def getNoSources(self):
		pass

	def getNoSinks(self):
		pass

	def getNoDoublets(self):
		pass

	def getNoVortices(self):
		pass
