from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg \
		import FigureCanvasQTAgg as FigureCanvas

class Plot(FigureCanvas):
	""" used in plotting the details in GUI provided """
	def __init__(self):
		self.colors = {'source':'go','sink':'bo','doublet':'ro','vortex':'ko'}
		self.fig = Figure()
		self.item = self.fig.add_subplot(111)
		FigureCanvas.__init__(self, self.fig)
		self.item.set_xlim(-1.0, 1.0)
		self.item.set_ylim(-1.0, 1.0)
		self.item.grid(True)
		self.item.set_autoscale_on(True)
		self.xMaxReached = False
		self.timerEvent(None)

	def plotPoint(self, elementInfo):
		""" """
		if elementInfo['type'] != 'uniformFlow' :
			self.item.plot(elementInfo['pos'].real, elementInfo['pos'].imag, self.colors[elementInfo['type']])
			self.fig.canvas.draw()

	def simulate(self, xdata, ydata):
		""" """
		pass

	def getlims(self, data):
		""" Returns the extreme points of the data """
		pass
