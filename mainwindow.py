# python libraries
import os
import platform
import sys
import re
from pylab import linspace
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
		self.plotType = 'streakLines'
		self.potElemRange = None
		self.potMinStreakParticles = 28
		self.potStreakParticles = []
		self.timer = None

		# Potential flow related connections
		QObject.connect(self.pushButton_Add, SIGNAL("clicked()"), self.addPotElement)
		QObject.connect(self.pushButton_Clear, SIGNAL("clicked()"), self.potClearData)
		QObject.connect(self.pushButton_Simulate, SIGNAL("clicked()"), self.potSimulate)
		QObject.connect(self.pushButton_toggleSimulation, SIGNAL("clicked()"), self.toggleSimulation)
		QObject.connect(self.radioButton_Source, SIGNAL("clicked()"), self.potSourceSelected)
		QObject.connect(self.radioButton_Sink, SIGNAL("clicked()"), self.potSinkSelected)
		QObject.connect(self.radioButton_Doublet, SIGNAL("clicked()"), self.potDoubletSelected)
		QObject.connect(self.radioButton_Vortex, SIGNAL("clicked()"), self.potVortexSelected)
		QObject.connect(self.radioButton_UniformFlow, SIGNAL("clicked()"), self.potUniformFlowSelected)
		QObject.connect(self.radioButton_UniformFlow, SIGNAL("clicked()"), self.horizontalLayout_7.invalidate)
		if self.scope == 'potentialFlows' :
			self.potSetVisible(not self.radioButton_UniformFlow.isChecked())
			self.graphicWidget = Plot()
			self.horizontalLayout_Main.addWidget(self.graphicWidget)
			self.graphicWidget.show()
			self.axisRange = array(self.graphicWidget.item.axis())

	# Potential flow related SLOTS		
	def addPotElement(self):
		""" SLOT for add action in  GUI """
		self.elementInfo = {}
		self.elementInfo['pos'] = self.doubleSpinBox_X.value() + 1j*self.doubleSpinBox_Y.value()
		self.elementInfo['strength'] = self.doubleSpinBox_Strength.value()
		if self.radioButton_Source.isChecked():
			self.elementInfo['type'] = 'source'
		elif self.radioButton_Sink.isChecked():
			self.elementInfo['type'] = 'sink'
			self.elementInfo['strength'] = -1*self.elementInfo['strength']
		elif self.radioButton_Doublet.isChecked():
			self.elementInfo['type'] = 'doublet'
		elif self.radioButton_Vortex.isChecked():
			self.elementInfo['type'] = 'vortex'
		elif self.radioButton_UniformFlow.isChecked():
			self.elementInfo['type'] = 'uniformFlow'
			self.elementInfo['angle'] = self.doubleSpinBox_FlowAngle.value()
		else :
			# Pop up box here - Select an element of potential flow
			pass

		self.potLibrary.addElement(self.elementInfo)
		self.graphicWidget.plotPotElements([self.potLibrary.elements[-1]])
		self.potResizeGraphicWindow()

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

	def potSetVisible(self, normal):
		""" Normal corresponds to all elements except uniform flow. 'normal' is a
		boolean, True if it doesnt correspond to Uniform flow"""
		self.label_X.setHidden(not normal)
		self.doubleSpinBox_X.setHidden(not normal)
		self.label_Y.setHidden(not normal)
		self.doubleSpinBox_Y.setHidden(not normal)
		self.label_FlowAngle.setHidden(normal)
		self.doubleSpinBox_FlowAngle.setHidden(normal)
		if normal:
			self.label_Strength.setText("Strength")
		else :
			self.label_Strength.setText("Velocity")

	def potSimulate(self):
		""" SLOT for simulate button click """
		if (self.plotType == 'streakLines') and (self.potLibrary.elements != []) :
			self.pushButton_toggleSimulation.setEnabled(True)
			self.pushButton_toggleSimulation.setText("&Pause")
			self.potStreakParticles = []
			# Clear the figure window here. Only the plotted elements
			self.graphicWidget.item.hold(False)
			self.graphicWidget.plotPotElements(self.potLibrary.elements)
			self.potResizeGraphicWindow()
			self.graphicWidget.fig.canvas.draw()
			startX = self.axisRange[0] + 1
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
			self.count = 0
			self.timerEvent(None)
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
				if abs(streakParticle.pos - sink.pos) < sink.__tolerance :
					streakParticle.pos = sink.pos
	
	def toggleSimulation(self):
		""" Stops the simulation if present """
		if self.timer != None :
			self.killTimer(self.timer)
			self.timer = None
			self.pushButton_toggleSimulation.setText("&Play")
		else :
			self.timer = self.startTimer(1)
			self.pushButton_toggleSimulation.setText("&Pause")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	application = MainWindow()
	application.show()
	app.exec_()
