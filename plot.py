from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
		import FigureCanvasQTAgg as FigureCanvas
from PyQt4.QtGui import *
from pylab import zeros

class Plot(FigureCanvas):
	""" used in plotting the details in GUI provided """
	def __init__(self):
		self.colors = {'source':'go','sink':'bo','doublet':'ro','vortex':'ko'}
		self.fig = Figure()
		self.item = self.fig.add_subplot(111)
		FigureCanvas.__init__(self, self.fig)
		self.defalutRange = [-5.0, 5.0, -5.0, 5.0]
		self.item.axis(self.defalutRange)
		self.item.grid(True)
		self.item.set_autoscale_on(False)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
				QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def plotPotElements(self, potElements):
		""" """
		for element in potElements:
			if element.elementInfo['type'] != 'uniformFlow' :
				self.item.plot(element.elementInfo['pos'].real, element.elementInfo['pos'].imag, self.colors[element.elementInfo['type']])
				self.fig.canvas.draw()

	def plotStreakParticles(self, particles):
		""" Initializing the plot of streak particles """
		self.plots = list(zeros(len(particles)))
		for index in range(0, len(particles)):
			xValues = [pos.real for pos in particles[index].history]
			yValues = [pos.imag for pos in particles[index].history]
			self.plots[index], = self.item.plot(xValues, yValues)
		self.fig.canvas.draw()
	
	def clearStreakParticles(self):
		""" Clear the plots corresponding to streak particles """
		pass

	def getlims(self, data):
		""" Returns the extreme points of the data """
		pass
