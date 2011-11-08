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
