# python libraries
import os
import platform
import sys
import re
from pylab import linspace
from matplotlib.backends.backend_qt4agg \
		import NavigationToolbar2QTAgg as NavigationToolbar
# PyQt4 libraries
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# Local libraries
from potentialLibrary import *
from plot import *
from ui import ui_mainwindow

__version__ = "1.0.0"

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
	""" """
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.filename = None
		self.setupUi(self)
		self.setCentralWidget(self.centralwidget)
		self.scope = 'potentialFlows'

		# Potential flow variable declarations
		self.potLibrary = potentialLibrary()
		self.potStrengthRange = [-10000.0, 10000.0]
		self.plotType = 'pathLines'
		self.potElemRange = None
		self.potMinStreakParticles = 28
		self.potStreakParticles = []
		self.timer = None
		self.elementTreeItemDict = {}

		# Potential flow related connections
		QObject.connect(self.pushButton_Add, SIGNAL("clicked()"), self.potaddElement)
		QObject.connect(self.pushButton_Remove, SIGNAL("clicked()"), self.potRemoveElement)
		QObject.connect(self.pushButton_Clear, SIGNAL("clicked()"), self.potClearData)
		QObject.connect(self.pushButton_Simulate, SIGNAL("clicked()"), self.potSimulate)
		QObject.connect(self.pushButton_toggleSimulation, SIGNAL("clicked()"), self.toggleSimulation)
		QObject.connect(self.radioButton_Source, SIGNAL("clicked()"), self.potSourceSelected)
		QObject.connect(self.radioButton_Sink, SIGNAL("clicked()"), self.potSinkSelected)
		QObject.connect(self.radioButton_Doublet, SIGNAL("clicked()"), self.potDoubletSelected)
		QObject.connect(self.radioButton_Vortex, SIGNAL("clicked()"), self.potVortexSelected)
		QObject.connect(self.radioButton_StreamLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.radioButton_PathLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.comboBox_pathLines, SIGNAL("currentIndexChanged(QString)"), self.potSetPatchInputParameters)

		if self.scope == 'potentialFlows' :
			# The following will set the input widget accordingly
			self.potSetVisible(not self.radioButton_UniformFlow.isChecked())
			# Following block will set window for visulaization. A matplotlib Figure window
			self.graphicWidget = Plot()
			self.graphicWidget.setParent(self)
			self.navigationTollBar = NavigationToolbar(self.graphicWidget, self)
			self.verticalLayout = QVBoxLayout()
			self.verticalLayout.addWidget(self.graphicWidget)
			self.verticalLayout.addWidget(self.navigationTollBar)
			self.horizontalLayout_Main.addLayout(self.verticalLayout)
			self.graphicWidget.show()
			self.axisRange = array(self.graphicWidget.item.axis())

	# Potential flow related SLOTS		
	def potaddElement(self):
		""" SLOT for add action in  GUI """
		self.elementInfo = {}
		X = self.doubleSpinBox_X.value()
		Y = self.doubleSpinBox_Y.value()
		self.elementInfo['pos'] =  X + 1j*Y
		self.elementInfo['strength'] = self.doubleSpinBox_Strength.value()
		if self.radioButton_Doublet.isChecked():
			self.elementInfo['type'] = 'doublet'
			self.treeWidgetItem = QTreeWidgetItem([str(self.elementInfo['strength']) +\
					"@ (" + str(X) + ", " + str(Y) +")"], 0)
			self.treeWidget_potElements.topLevelItem(0).addChild(self.treeWidgetItem)
		elif self.radioButton_Sink.isChecked():
			self.elementInfo['type'] = 'sink'
			self.treeWidgetItem = QTreeWidgetItem([str(self.elementInfo['strength']) +\
					"@ (" + str(X) + ", " + str(Y) +")"], 1)
			self.treeWidget_potElements.topLevelItem(1).addChild(self.treeWidgetItem)
			self.elementInfo['strength'] = -1*self.elementInfo['strength']
		elif self.radioButton_Source.isChecked():
			self.elementInfo['type'] = 'source'
			self.treeWidgetItem = QTreeWidgetItem([str(self.elementInfo['strength']) +\
					"@ (" + str(X) + ", " + str(Y) +")"], 2)
			self.treeWidget_potElements.topLevelItem(2).addChild(self.treeWidgetItem)
		elif self.radioButton_UniformFlow.isChecked():
			self.elementInfo['type'] = 'uniformFlow'
			self.elementInfo['angle'] = self.doubleSpinBox_FlowAngle.value()
			self.treeWidgetItem = QTreeWidgetItem([str(self.elementInfo['strength']) +\
					"@ " + str(self.elementInfo['angle']) + "deg"], 3)
			self.treeWidget_potElements.topLevelItem(3).addChild(self.treeWidgetItem)
		elif self.radioButton_Vortex.isChecked():
			self.elementInfo['type'] = 'vortex'
			self.treeWidgetItem = QTreeWidgetItem([str(self.elementInfo['strength']) +\
					"@ (" + str(X) + ", " + str(Y) +")"], 4)
			self.treeWidget_potElements.topLevelItem(4).addChild(self.treeWidgetItem)
		else :
			# Pop up box here - Select an element of potential flow
			pass

		self.potLibrary.addElement(self.elementInfo)
		# Plot the addes element in the figure widget
		self.graphicWidget.plotPotElements([self.potLibrary.elements[-1]])
		self.potResizeGraphicWindow()
		# Add this treeElement and potElement to the dictionary
		self.elementTreeItemDict[self.treeWidgetItem] = self.potLibrary.elements[-1]
		self.pushButton_Remove.setEnabled(True)
		self.graphicWidget.fig.canvas.draw()

	def potRemoveElement(self):
		""" Remove selected item in the tree widgte """
		selected = self.treeWidget_potElements.selectedItems()
		if self.elementTreeItemDict.has_key(selected[0]):
			self.potLibrary.deleteElement(self.elementTreeItemDict[selected[0]])
			del self.elementTreeItemDict[selected[0]]
			# self.treeWidget_potElements.topLevelItem(0).removeChild(self.treeWidget_potElements.topLevelItem(0).child(1))
			# Need to clear the plot before plotting
			self.graphicWidget.plotPotElements(self.potLibrary.elements)
			self.graphicWidget.show()
			self.graphicWidget.fig.canvas.draw()
			# The following thing is not working - Check why. However the element from the library is deleted
			self.treeWidget_potElements.removeItemWidget(selected[0], 0)

	def potClearData(self):
		""" Clears the values in DoubleSpinBoxes and sets them to default
		values """
		self.doubleSpinBox_X.setValue(0.0)
		self.doubleSpinBox_Y.setValue(0.0)
		self.doubleSpinBox_Strength.setValue(0.0)

	def potSourceSelected(self):
		""" """
		self.potSetVisible(True)
		self.doubleSpinBox_Strength.setMinimum(0.0)

	def potSinkSelected(self):
		""" """
		self.potSetVisible(True)
		self.doubleSpinBox_Strength.setMinimum(0.0)

	def potDoubletSelected(self):
		""" """
		self.potSetVisible(True)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potVortexSelected(self):
		""" """
		self.potSetVisible(True)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potUniformFlowSelected(self):
		""" """
		self.potSetVisible(False)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potSetVisible(self, isUniform):
		""" """
		self.label_X.setHidden(not isUniform)
		self.doubleSpinBox_X.setHidden(not isUniform)
		self.label_Y.setHidden(not isUniform)
		self.doubleSpinBox_Y.setHidden(not isUniform)
		self.label_FlowAngle.setHidden(isUniform)
		self.doubleSpinBox_FlowAngle.setHidden(isUniform)
		if isUniform:
			self.label_Strength.setText("Strength")
		else :
			self.label_Strength.setText("Velocity")

	def potSimulate(self):
		""" SLOT for simulate button click """
		self.clearPlot()
		self.graphicWidget.plotPotElements(self.potLibrary.elements)
		self.graphicWidget.fig.canvas.draw()
		self.pushButton_toggleSimulation.setEnabled(True)
		self.pushButton_toggleSimulation.setText("&Pause")
		if self.potStreakParticles != []:
			self.graphicWidget.clearStreakParticles() # To clear streak line in the plot window
		if (self.plotType == 'pathLines') and (self.potLibrary.elements != []) :
			self.potStreakParticles = []
			self.potAddStreakParticles()
			
		self.count = 0
		self.timerEvent(None)
		if self.timer != None :
			self.killTimer(self.timer)
		self.timer = self.startTimer(0.001)

	def potResizeGraphicWindow(self):
		""" Resizes the plot widget based on the present elements """
		self.potElemRange = self.potLibrary.getRange()
		if (self.potElemRange != None) and (abs(array(self.potElemRange)) > abs(array(self.graphicWidget.defalutRange))).any() :
			maxLim = max(abs(array(self.potElemRange)))
			additional = array([-maxLim*3 - 5, maxLim*3 + 5, -maxLim*3 -5, maxLim*3 + 5])
			self.graphicWidget.item.axis(array(self.potElemRange) + additional)
			self.graphicWidget.fig.canvas.draw()
			self.axisRange = array(self.graphicWidget.item.axis())

		elif self.potElemRange == None :
			self.potElemRange = [-1.0, 1.0, -1.0, 1.0]
			self.graphicWidget.item.axis(array(self.graphicWidget.defalutRange))

	def timerEvent(self, event):
		""" Supposed to update the plot """
		for streak in self.potStreakParticles :
			streak.velocity = self.potLibrary.velocityAt(streak.pos)
			self.potSingularitiesTreatment()
			streak.advect()
		for index in range(0, len(self.potStreakParticles)):
			xData = [pos.real for pos in self.potStreakParticles[index].history]
			yData = [pos.imag for pos in self.potStreakParticles[index].history]
			self.graphicWidget.plots[index].set_data(xData, yData)
		self.graphicWidget.fig.canvas.draw()
		if self.count < 0:
			self.killTimer(self.timer)
		else :
			self.count += 1

	def potSingularitiesTreatment(self):
		""" Treat the particles if they are close to any singularity """
		for streakParticle in self.potStreakParticles :
			for sink in self.potLibrary.sinks :
				if abs(streakParticle.pos - sink.pos) < sink.__tolerance/02.0 :
					streakParticle.pos = sink.pos
	
	def toggleSimulation(self):
		""" Stops the simulation if present """
		if self.timer != None :
			self.killTimer(self.timer)
			self.timer = None
			self.pushButton_toggleSimulation.setText("&Play")
		else :
			self.timer = self.startTimer(0.001)
			self.pushButton_toggleSimulation.setText("&Pause")

	def potAddStreakParticles(self):
		""" Add specified streal particles """
		self.potAddParticlesAtX( self.axisRange[0])

	def potAddParticlesAtX(self, startX, n = 30):
		""" Adds particles at x """
		widthY = abs(self.axisRange[3] - self.axisRange[2])
		elementsWidth = abs(self.potElemRange[3] - self.potElemRange[2])
		if widthY > self.potMinStreakParticles :
			noParticles = int(widthY)
		else :
			noParticles = int(self.potMinStreakParticles)
		for yCoord in linspace(self.axisRange[2] + 0.5 , self.potElemRange[2] - elementsWidth/3, noParticles/4) :
			newParticle = particle(startX, yCoord)
			self.potStreakParticles.append(newParticle)
		for yCoord in linspace(self.potElemRange[2] - elementsWidth/3.0 -1.0, self.potElemRange[3] + elementsWidth/3.0 + 1.0, noParticles/2) :
			newParticle = particle(startX, yCoord)
			self.potStreakParticles.append(newParticle)
		for yCoord in linspace(self.potElemRange[3] + elementsWidth/3.0, self.axisRange[3] - 0.5, noParticles/4) :
			newParticle = particle(startX, yCoord)
			self.potStreakParticles.append(newParticle)

		self.graphicWidget.plotStreakParticles(self.potStreakParticles)
	
	def clearPlot(self):
		"""  Clears the plot window without changing the axis limits """
		self.graphicWidget.item.cla()
		self.graphicWidget.item.set_autoscale_on(False)
		self.graphicWidget.item.grid(True)

	def potSetPlotScope(self):
		""" Sets plot type and displays required input properties for that scope """
		if (self.radioButton_StreamLines.isChecked()):
			self.plotType = 'streamLines'
		elif (self.radioButton_PathLines.isChecked()):
			self.plotType = 'pathLines'
		else :
			pass

	def potSetPatchInputParameters(self):
		""" Sets corresponding input parameters for the patch of selected type"""
		patchType = self.comboBox_pathLines.currentText()
		if patchType == 'Square':
			self.label_center.setHidden(False)
			self.doubleSpinBox_centerX.setHidden(False)
			self.doubleSpinBox_centerY.setHidden(False)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.label_patchInfo2.setHidden(True)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("length")
		elif patchType == 'Circular':
			self.label_center.setHidden(False)
			self.doubleSpinBox_centerX.setHidden(False)
			self.doubleSpinBox_centerY.setHidden(False)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.label_patchInfo2.setHidden(True)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("Radius")
		elif patchType == 'Line at X':
			self.label_center.setHidden(True)
			self.doubleSpinBox_centerX.setHidden(True)
			self.doubleSpinBox_centerY.setHidden(True)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.label_patchInfo2.setHidden(True)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("At X ")
		else :
			pass


if __name__ == "__main__":
	app = QApplication(sys.argv)
	application = MainWindow()
	application.show()
	app.exec_()
