# python libraries
import os
import platform
import sys
import re
import time
from math import *
from pylab import linspace, array
from matplotlib.backends.backend_qt4agg \
		import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.patches import FancyArrowPatch
import numpy as np
# PyQt4 libraries
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# Local libraries
from potentialLibrary import *
from plot import *

from math import *
from numpy import *
from ui import ui_mainwindow
from cfdSolver import *

__version__ = "1.0.0"

class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow):
	""" """
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.filename = None
		self.setupUi(self)
		self.setCentralWidget(self.centralwidget)
		self.scope = 'potentialFlows'
		#self.scope = 'cfd'

		# Potential flow variable declarations
		self.potLibrary = potentialLibrary()
		self.potStrengthRange = [-10000.0, 10000.0]
		self.plotType = 'pathLines'
		self.potElemRange = None
		self.potMinStreakParticles = 28
		self.potStreakParticles = []
		self.timer = None
		self.elementTreeItemDict = {}
		self.cfdSimulatescope = None

		# Potential flow related connections
		QObject.connect(self.pushButton_Add, SIGNAL("clicked()"), self.potaddElement)
		QObject.connect(self.pushButton_Remove, SIGNAL("clicked()"), self.potRemoveElement)
		QObject.connect(self.pushButton_Clear, SIGNAL("clicked()"), self.potClearData)
		QObject.connect(self.pushButton_Simulate, SIGNAL("clicked()"), self.potSimulate)
		QObject.connect(self.pushButton_toggleSimulation, SIGNAL("clicked()"), self.toggleSimulation)
		QObject.connect(self.pushButton_potAddpatch, SIGNAL("clicked()"), self.potAddStreakParticles)
		QObject.connect(self.pushButton_potRemoveTracers, SIGNAL("clicked()"), self.potRemoveSreakParticles)
		QObject.connect(self.pushButton_clearPlot, SIGNAL("clicked()"), self.clearPlot)
		QObject.connect(self.pushButton_setAxesRange, SIGNAL("clicked()"), self.setCustomAxisRange)
		QObject.connect(self.pushButton_setDefaultAxesRange, SIGNAL("clicked()"), self.setDefaultAxisRange)
		QObject.connect(self.pushButton_potClearPotElements, SIGNAL("clicked()"), self.potClearAllPotElements)
		QObject.connect(self.radioButton_Source, SIGNAL("clicked()"), self.potSourceSelected)
		QObject.connect(self.radioButton_Sink, SIGNAL("clicked()"), self.potSinkSelected)
		QObject.connect(self.radioButton_Doublet, SIGNAL("clicked()"), self.potDoubletSelected)
		QObject.connect(self.radioButton_UniformFlow, SIGNAL("clicked()"), self.potUniformFlowSelected)
		QObject.connect(self.radioButton_Vortex, SIGNAL("clicked()"), self.potVortexSelected)
		QObject.connect(self.radioButton_StreamLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.radioButton_PathLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.comboBox_pathLines, SIGNAL("currentIndexChanged(QString)"), self.potSetPatchInputParameters)
		QObject.connect(self.pushButton_cfdSimulate, SIGNAL("clicked()"), self.cfdSimulate)
		QObject.connect(self.pushButton_advecSimulate, SIGNAL("clicked()"), self.advecSimulate)

		QObject.connect(self.pushButton_burgSimulate, SIGNAL("clicked()"), self.burgSimulate)

		QObject.connect(self.action_Potential_Flows, SIGNAL("activated()"), self.setPotentialFlowsActivated)
		QObject.connect(self.actionPanel_Methods, SIGNAL("activated()"), self.setPanelMethodsActivated)
		QObject.connect(self.actionCFD, SIGNAL("activated()"), self.setCFDActivated)



		if self.scope == 'potentialFlows' :
			self.potTime = 0.0
			self.InputPotentialFlows_Dock.setHidden(False)
			self.InputCFD_Dock.setHidden(True)
			# The following will set the input widget accordingly
			self.radioButton_Source.setChecked(True)
			self.potSetVisible(self.radioButton_UniformFlow.isChecked())
			self.comboBox_pathLines.setCurrentIndex(1)
			self.comboBox_pathLines.setCurrentIndex(0)

		elif self.scope == 'cfd' :
			self.InputCFD_Dock.setHidden(False)
			self.InputPotentialFlows_Dock.setHidden(True)

		if self.scope == 'potentialFlows' or self.scope == 'cfd':
			# Following block will set window for visulaization. A matplotlib Figure window
			self.graphicWidget = Plot()
			self.graphicWidget.setParent(self)
			self.navigationTollBar = NavigationToolbar(self.graphicWidget, self)
			self.verticalLayout = QVBoxLayout()
			self.horizontalLayout_navig = QHBoxLayout()
			self.horizontalLayout_fig = QHBoxLayout()
			#self.groupBox_customizePlot.setParent(self.horizontalLayout_fig)
			#self.verticalLayout.addLayout(self.horizontalLayout_fig)
			self.verticalLayout.addWidget(self.graphicWidget)
			self.horizontalLayout_navig.addWidget(self.navigationTollBar)
			self.pushButton_showFigCustomization = QPushButton()
			self.pushButton_showFigCustomization .setObjectName("pushButton_showFigCustomization")
			self.horizontalLayout_navig.addWidget(self.pushButton_showFigCustomization)
			self.pushButton_showFigCustomization.setText("&Options>>")
			QObject.connect(self.pushButton_showFigCustomization, SIGNAL("clicked()"), self.toggleFigOptions)
			self.verticalLayout.addLayout(self.horizontalLayout_navig)
			self.horizontalLayout_fig.addLayout(self.verticalLayout)
			self.horizontalLayout_fig.addWidget(self.groupBox_customizePlot)
			self.horizontalLayout_Main.addLayout(self.horizontalLayout_fig)
			self.axisRange = array(self.graphicWidget.item.axis())
			self.groupBox_customizePlot.setHidden(True)
			self.axisRange = array(self.graphicWidget.item.axis())

	# Potential flow related SLOTS		
	def setPotentialFlowsActivated(self):
		""" Activates potential flow parameters """
		self.scope = 'potentialFlows'

	def potaddElement(self):
		""" SLOT for add action in  GUI """
		self.elementInfo = {}
		X = self.doubleSpinBox_FlowAngle_OR_X.value()
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
			self.elementInfo['strength'] = -1*self.elementInfo['strength']
		elif self.radioButton_UniformFlow.isChecked():
			self.elementInfo['type'] = 'uniformFlow'
			self.elementInfo['angle'] = self.doubleSpinBox_FlowAngle_OR_X.value()
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
		message = "Added " + self.elementInfo['type'] + " element with strength = " + str(self.elementInfo['strength'])
		self.statusbar.showMessage(message , 1500)
		# Plot the addes element in the figure widget
		self.graphicWidget.plotPotElements([self.potLibrary.elements[-1]])
		self.potResizeGraphicWindow()
		if self.potStreakParticles != []: self.potAutoscaleAxis()
		# Add this treeElement and potElement to the dictionary
		self.elementTreeItemDict[self.treeWidgetItem] = self.potLibrary.elements[-1]
		self.pushButton_Remove.setEnabled(True)
		self.pushButton_potClearPotElements.setEnabled(True)
		self.graphicWidget.fig.canvas.draw()

	def potRemoveElement(self):
		""" Remove selected item in the tree widgte """
		selected = self.treeWidget_potElements.selectedItems()
		if self.elementTreeItemDict.has_key(selected[0]):
			self.potLibrary.deleteElement(self.elementTreeItemDict[selected[0]])
			del self.elementTreeItemDict[selected[0]]
			message = "Removed the element. It may appear in the list"
			self.statusbar.showMessage(message , 2000)
			# self.treeWidget_potElements.topLevelItem(0).removeChild(self.treeWidget_potElements.topLevelItem(0).child(1))
			# Need to clear the plot before plotting
			self.graphicWidget.plotPotElements(self.potLibrary.elements)
			self.graphicWidget.fig.canvas.draw()
			# The following thing is not working - Check why. However the element from the library is deleted
			self.treeWidget_potElements.removeItemWidget(selected[0], 0)
		else :
			message = " Nothing to remove"
			self.statusbar.showMessage(message , 1500)

	def potClearData(self):
		""" Clears the values in DoubleSpinBoxes and sets them to default
		values """
		self.doubleSpinBox_FlowAngle_OR_X.setValue(0.0)
		self.doubleSpinBox_Y.setValue(0.0)
		self.doubleSpinBox_Strength.setValue(0.0)

	def potSourceSelected(self):
		""" """
		self.potSetVisible(False)
		self.doubleSpinBox_Strength.setMinimum(0.0)

	def potSinkSelected(self):
		""" """
		self.potSetVisible(False)
		self.doubleSpinBox_Strength.setMinimum(0.0)

	def potDoubletSelected(self):
		""" """
		self.potSetVisible(False)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potVortexSelected(self):
		""" """
		self.potSetVisible(False)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potUniformFlowSelected(self):
		""" """
		self.potSetVisible(True)
		self.doubleSpinBox_Strength.setRange(self.potStrengthRange[0], self.potStrengthRange[1])

	def potSetVisible(self, isUniform):
		""" """
		if isUniform: 
			self.label_X.setText("Flow angle")
			self.doubleSpinBox_FlowAngle_OR_X.setMinimum(-360.0)
			self.doubleSpinBox_FlowAngle_OR_X.setMaximum(360.0)
			self.doubleSpinBox_FlowAngle_OR_X.setSingleStep(1.0)
			self.doubleSpinBox_FlowAngle_OR_X.resize(self.doubleSpinBox_Strength.size())
			self.label_Strength.setText("Velocity")
		else : 
			self.doubleSpinBox_FlowAngle_OR_X.setMinimum(-10000.0)
			self.doubleSpinBox_FlowAngle_OR_X.setMaximum(10000.0)
			self.doubleSpinBox_FlowAngle_OR_X.setSingleStep(0.1)
			self.label_X.setText("(X, Y)")
			self.label_Strength.setText("Strength")
		self.doubleSpinBox_Y.setHidden(isUniform)

	def potSimulate(self):
		""" SLOT for simulate button click """
		if self.timer != None :
			self.killTimer(self.timer)
		self.clearPlot()
		self.graphicWidget.fig.canvas.draw()
		if self.potStreakParticles != []:
			self.graphicWidget.clearStreakParticles() # To clear streak line in the plot window
		if (self.potLibrary.elements != []):
			if (self.plotType == 'pathLines'):
				if self.potStreakParticles == [] :
					self.potAddDefaultStreakParticles()
				# Start simulation in real time	
				self.potTime = 0.0
				self.pushButton_toggleSimulation.setEnabled(True)
				self.pushButton_toggleSimulation.setText("&Pause")
				self.count = 0
				self.timerEvent(None)
				self.statusbar.showMessage("Simulating ...")
				self.timer = self.startTimer(0.001)
			elif (self.plotType == 'velMagnitude') :
				self.pushButton_toggleSimulation.setEnabled(False)
				self.potAddStreamParticles()
			elif (self.plotType == 'streamLines') :
				self.statusbar.showMessage("Plotting the stream lines...This may take some time") # This is not being shown while execution - BUGGG
				self.pushButton_toggleSimulation.setEnabled(False)
				self.pushButton_toggleSimulation.setText("&Play")
				self.potPlotStreamLines()
			else :
				raise NameError("Unknown plotType")

		else :
			self.statusbar.showMessage("No potential flow elements found. You can add them from the potential flows input box")

	def potResizeGraphicWindow(self):
		""" Resizes the plot widget based on the present elements """
		self.potElemRange = self.potLibrary.getRange()
		if (self.potElemRange != None) and (abs(array(self.potElemRange)) > abs(array(self.graphicWidget.defalutRange))).any() :
			maxLim = max(abs(array(self.potElemRange)))
			additional = array([-maxLim*1.5 - 5, maxLim*1.5 + 5, -maxLim*1.5 -5, maxLim*1.5 + 5])
			self.graphicWidget.item.axis(array(self.potElemRange) + additional)
			self.graphicWidget.fig.canvas.draw()
			self.axisRange = array(self.graphicWidget.item.axis())

		elif self.potElemRange == None :
			self.potElemRange = [-1.0, 1.0, -1.0, 1.0]
			self.graphicWidget.item.axis(array(self.graphicWidget.defalutRange))

	def potAutoscaleAxis(self):
		""" To set auto scale on if axis limits are exceeded"""
		if self.plotType != 'velMagnitude' and self.potStreakParticles != []:
			xRange = [item.pos.real for item in self.potStreakParticles]
			yRange = [item.pos.imag for item in self.potStreakParticles]
			if min(xRange) < self.axisRange[0]: self.axisRange += array([min(xRange) - self.axisRange[0], 0, 0, 0])
			if max(xRange) > self.axisRange[1]: self.axisRange += array([0, max(xRange) -self.axisRange[1], 0, 0])
			if min(yRange) < self.axisRange[2]: self.axisRange += array([0, 0, min(yRange) -self.axisRange[2], 0])
			if max(yRange) > self.axisRange[3]: self.axisRange += array([0, 0, 0, max(yRange) -self.axisRange[3]])
			self.graphicWidget.item.axis(array(self.axisRange))
			self.graphicWidget.fig.canvas.draw()
		else :
			#self.graphicWidget.item.axis('equal')
			self.axisRange = self.graphicWidget.item.axis()

	def potAdvectParticles(self, dt = 0.01, integType = 'euler'):
		""" Advect the particles for a given time step """
		for streak in self.potStreakParticles :
			streak.velocity = self.potLibrary.velocityAt(streak.pos)
			self.potSingularitiesTreatment()
			if integType == 'rk2':
				streak.k1 = dt*streak.velocity
				streak.k2 = dt*self.potLibrary.velocityAt(streak.pos + streak.k1)
			streak.advect(dt = dt, integType = integType)
		
	def potSingularitiesTreatment(self):
		""" Treat the particles if they are close to any singularity """
		for streakParticle in self.potStreakParticles :
			for sink in self.potLibrary.sinks :
				if abs(streakParticle.pos - sink.pos) < sink.__tolerance/5.0 :
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

	def potAddDefaultStreakParticles(self):
		""" Add specified streak particles """
		self.potAddDefaultParticlesAtX( self.axisRange[0])
		self.graphicWidget.plotStreakParticles(self.potStreakParticles)

	def potAddStreakParticles(self):
		""" Add specified streak particles """
		patchType = self.comboBox_pathLines.currentText()
		if patchType == 'Square':
			center = complex(self.doubleSpinBox_centerX.value(), self.doubleSpinBox_centerY.value())
			length = self.doubleSpinBox_patchInfo1.value()
			minCoord = center - 1j*length/2.0
			maxCoord = center + 1j*length/2.0
			self.potAddParticlesAt(minCoord.real - length/2.0, yMin = minCoord.imag, yMax = maxCoord.imag, tag = 'X')
			self.potAddParticlesAt(maxCoord.real + length/2.0, yMin = minCoord.imag, yMax = maxCoord.imag, tag = 'X')
			self.potAddParticlesAt(minCoord.imag, yMin = minCoord.real - length/2.0, yMax = maxCoord.real + length/2.0, tag = 'Y')
			self.potAddParticlesAt(maxCoord.imag, yMin = minCoord.real - length/2.0, yMax = maxCoord.real + length/2.0, tag = 'Y')
		elif patchType == 'Circular' :
			center = complex(self.doubleSpinBox_centerX.value(), self.doubleSpinBox_centerY.value())
			radius = self.doubleSpinBox_patchInfo1.value()
			for theta in linspace(0, 2*pi, (10*round(radius) + 1)*5):
				position = center + radius*exp(1j*theta)
				newParticle = particle(position.real, position.imag)
				self.potStreakParticles.append(newParticle)
		self.graphicWidget.plotStreakParticles(self.potStreakParticles)
		self.potAutoscaleAxis()
		self.graphicWidget.fig.canvas.draw()

	def potAddParticlesAt(self, startX, tag = 'X', noParticles = 3, yMin = -5.0, yMax = 5.0):
		""" Adds particles at x """
		newNoParticles = 2*(int(abs(yMax - yMin)) + 1)
		if newNoParticles > noParticles :
			noParticles = newNoParticles
		for yCoord in linspace(yMin, yMax, noParticles) :
			if tag == 'X': newParticle = particle(startX, yCoord)
			elif tag == 'Y': newParticle = particle(yCoord, startX)
			else :
				raise NameError("Unknown tag for adding the particles")
			self.potStreakParticles.append(newParticle)

	def potAddDefaultParticlesAtX(self, startX, n = 30):
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

	def potRemoveSreakParticles(self):
		""" Removes all streak particles """
		self.potStreakParticles = []
		self.potResizeGraphicWindow()
		#self.clearPlot()
		self.graphicWidget.fig.canvas.draw()
	
	def clearPlot(self):
		"""  Clears the plot window without changing the axis limits """
		self.graphicWidget.item.cla()
		self.graphicWidget.item.set_autoscale_on(False)
		self.graphicWidget.item.grid(True)
		if self.scope == 'potentialFlows':
			self.graphicWidget.plotPotElements(self.potLibrary.elements)
			self.graphicWidget.plotStreakParticles(self.potStreakParticles, plotType = 'point')
			self.potAutoscaleAxis()
		self.graphicWidget.fig.canvas.draw()

	def toggleFigOptions(self):
		""" Enables figure options """
		self.groupBox_customizePlot.setHidden(not self.groupBox_customizePlot.isHidden())
		if self.groupBox_customizePlot.isHidden():
			self.pushButton_showFigCustomization.setText("&Options>>")
		else :
			self.pushButton_showFigCustomization.setText("&<<Hide")
	def potSetPlotScope(self):
		""" Sets plot type and displays required input properties for that scope """
		if (self.radioButton_StreamLines.isChecked()):
			self.plotType = 'streamLines'
			# To set the patch input parameters invisible
			self.potSetPatchParamInVisibile(True)
		elif (self.radioButton_PathLines.isChecked()):
			self.plotType = 'pathLines'
			self.potSetPatchParamInVisibile(False)
			self.comboBox_pathLines.setCurrentIndex(1)
			self.comboBox_pathLines.setCurrentIndex(0)
		else :
			pass

	def potSetPatchParamInVisibile(self, invisible):
		""" sets the patch visible when path lines is selected and invisible
		for all other inputs"""
		self.label_center.setHidden(invisible)
		self.doubleSpinBox_centerX.setHidden(invisible)
		self.doubleSpinBox_centerY.setHidden(invisible)
		self.label_patchInfo1.setHidden(invisible)
		self.doubleSpinBox_patchInfo1.setHidden(invisible)
		self.doubleSpinBox_patchInfo2.setHidden(invisible)
		self.label_patchInfo1.setHidden(invisible)
		self.comboBox_pathLines.setHidden(invisible)
		self.pushButton_potAddpatch.setHidden(invisible)

	def potSetPatchInputParameters(self):
		""" Sets corresponding input parameters for the patch of selected type"""
		patchType = self.comboBox_pathLines.currentText()
		if patchType == 'Square':
			self.label_center.setHidden(False)
			self.doubleSpinBox_centerX.setHidden(False)
			self.doubleSpinBox_centerY.setHidden(False)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setMinimum(0.0)
			self.doubleSpinBox_patchInfo1.setSingleStep(1.0)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("length")
		elif patchType == 'Circular':
			self.label_center.setHidden(False)
			self.doubleSpinBox_centerX.setHidden(False)
			self.doubleSpinBox_centerY.setHidden(False)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setMinimum(0.0)
			self.doubleSpinBox_patchInfo1.setSingleStep(1.0)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("Radius")
		elif patchType == 'Line at X' or patchType == 'Line at Y':
			self.label_center.setHidden(True)
			self.doubleSpinBox_centerX.setHidden(True)
			self.doubleSpinBox_centerY.setHidden(True)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			if patchType == 'Line at X': self.label_patchInfo1.setText("At X ")
			elif patchType == 'Line at Y': self.label_patchInfo1.setText("At Y ")
		elif patchType == 'Rectangular':
			self.potSetPatchParamInVisibile(False)
			self.doubleSpinBox_patchInfo1.setMinimum(0.0)
			self.doubleSpinBox_patchInfo1.setSingleStep(1.0)
			self.doubleSpinBox_patchInfo2.setMinimum(0.0)
			self.doubleSpinBox_patchInfo2.setSingleStep(1.0)
			self.label_patchInfo1.setText("(l, b)")
		else :
			pass

	""" Obsolate - No longer in the package """
	def potAddStreamParticles(self):
		""" Takes the dimensions of plot widget and plots stream lines by
		advecting the particles for a small time step dt """
		noOfParticlesAtX = int(self.axisRange[3] - self.axisRange[2])*3
		noOfParticlesAtY = int(self.axisRange[1] - self.axisRange[0])*2
		self.potStreakParticles = [particle(x, y) for x in linspace(self.axisRange[1], self.axisRange[0], \
				noOfParticlesAtY) for y in linspace(self.axisRange[2]+0.1, self.axisRange[3]-0.1, noOfParticlesAtX)]
		self.graphicWidget.item.grid(False)
		self.graphicWidget.plotStreakParticles(self.potStreakParticles, tag = "velMagnitude")
		self.graphicWidget.fig.canvas.draw()

	""" This function is unused as of now """
	def potVelocityPlot(self):
		""" Takes the dimensions of plot widget and plots stream lines by
		advecting the particles for a small time step dt """
		noOfParticlesAtX = int(self.axisRange[3] - self.axisRange[2])*3
		noOfParticlesAtY = int(self.axisRange[1] - self.axisRange[0])*2
		self.potStreakParticles = [particle(x, y) for x in linspace(self.axisRange[1], self.axisRange[0], \
				noOfParticlesAtY) for y in linspace(self.axisRange[2]+0.1, self.axisRange[3]-0.1, noOfParticlesAtX)]
		self.graphicWidget.item.grid(False)
		for steps in range(2):
			self.potAdvectParticles(dt = 0.02)
			for index in range(0, len(self.potStreakParticles)):
				positions = [(pos.real, pos.imag) for pos in self.potStreakParticles[index].history]
				axis = self.graphicWidget.fig.gca()
				axis.add_patch(FancyArrowPatch(positions[0],positions[-1],arrowstyle='->',mutation_scale=15))
		self.graphicWidget.fig.canvas.draw()

	def potPlotStreamLines(self):
		""" Plot stream lines """
		self.axisRange = array(self.graphicWidget.item.axis())
		noOfParticlesAtX = int(self.axisRange[3] - self.axisRange[2])*30
		noOfParticlesAtY = int(self.axisRange[1] - self.axisRange[0])*20
		self.potStreakParticles = [particle(x, y) for x in linspace(self.axisRange[1], self.axisRange[0], \
				noOfParticlesAtY) for y in linspace(self.axisRange[2]+0.1, self.axisRange[3]-0.1, noOfParticlesAtX)]
		velocities = array([self.potLibrary.streamFunctionAt(item.pos) for item in self.potStreakParticles])
		v = np.arange(min(velocities), max(velocities), 0.1)
		x = array([item.pos.real for item in self.potStreakParticles])
		y = array([item.pos.imag for item in self.potStreakParticles])
		x = x.reshape(noOfParticlesAtY, noOfParticlesAtX)
		y = y.reshape(noOfParticlesAtY, noOfParticlesAtX)
		velocities = velocities.reshape(noOfParticlesAtY, noOfParticlesAtX)
		self.graphicWidget.item.contour(x, y, velocities)
		#self.graphicWidget.item.colorbar()
		self.graphicWidget.item.axis('equal')
		self.potStreakParticles = []
		self.graphicWidget.fig.canvas.draw()
		self.statusbar.showMessage("Done :)")
		self.graphicWidget.item.axis(self.axisRange)

	def setCustomAxisRange(self):
		""" Set the axis range as rendered """
		Xmin = self.doubleSpinBox_figXmin.value()
		Xmax = self.doubleSpinBox_figXmax.value()
		Ymin = self.doubleSpinBox_figYmin.value()
		Ymax = self.doubleSpinBox_figYmax.value()
		self.graphicWidget.item.axis(array([Xmin, Xmax, Ymin, Ymax]))
		self.graphicWidget.fig.canvas.draw()

	def potClearAllPotElements(self):
		""" Removes all potential elements """
		self.potLibrary.elements = []
		for index in range(5):
			childCount =  self.treeWidget_potElements.topLevelItem(index).childCount()
			for childNo in range(childCount):
				child = self.treeWidget_potElements.topLevelItem(index).child(childNo)
				del self.elementTreeItemDict[child]
				self.treeWidget_potElements.removeItemWidget(child, 0)
		self.statusbar.showMessage("Removed all elements")

	def setDefaultAxisRange(self):
		""" Set the axis range Default - based on potential elements and
		particles """
		if self.scope == 'potentialFlows':
			self.potResizeGraphicWindow()
			self.potAutoscaleAxis()
		elif self.scope == 'cfd':
			self.graphicWidget.item.axis(array(self.axisRange))
		self.graphicWidget.fig.canvas.draw()

	def timerEvent(self, event, dt = 0.01):
		""" Supposed to update the plot """
		if self.scope == 'potentialFlows':
			if self.plotType == "velMagnitude" :
				repeat = 2
				maxCount = 10
				self.clearPlot()
			else :
				repeat = 1
				maxCount = self.count + 1
			for instnace in range(repeat):
				self.potAdvectParticles(dt = dt, integType = 'rk2')
				self.potTime += dt
				if self.graphicWidget.plots != None :
					for index in range(0, len(self.potStreakParticles)):
						xData = [pos.real for pos in self.potStreakParticles[index].history]
						yData = [pos.imag for pos in self.potStreakParticles[index].history]
						self.graphicWidget.plots[index].set_data(xData, yData)
				self.graphicWidget.fig.canvas.draw()
				if self.count > maxCount:
					self.killTimer(self.timer)
				else :
					self.count += 1
			self.potAutoscaleAxis()
			self.statusbar.showMessage("Time = " + str(self.potTime))
		if self.scope == 'cfd':
			if self.cfdSimulatescope =='shock':
				if self.cfdSolver.itr>self.cfdSolver.itrf :
						self.killTimer(self.timer)
				else:
					self.clearPlot()
					self.cfdflux()
					umax = self.cfdSolver.maxofu()
					self.cfdSolver.dt=  1.0 *self.cfdSolver.cfl* self.cfdSolver.dx/umax
					self.cfdSolver.update()
					print " ri ",self.cfdSolver.ri,
					self.shockboundaryCondtn()
					self.cfdSolver.itr=self.cfdSolver.itr+1
					self.cfdSolver.t=self.cfdSolver.t+self.cfdSolver.dt
					self.cfdSolver.plt()
					print "t ",self.cfdSolver.t,"itr",self.cfdSolver.itr
					self.graphicWidget.item.plot(self.cfdSolver.x,self.cfdSolver.rho_initial,'r')
					self.graphicWidget.item.plot(self.cfdSolver.x,self.cfdSolver.rho,'b')
					self.graphicWidget.fig.canvas.draw()

			elif self.cfdSimulatescope=='burg':
				if self.timeElapsed > self.totalTime:
						self.killTimer(self.timer)
				else:
					self.clearPlot()
					self.burgItr()
					self.graphicWidget.item.plot(self.x,self.uinit,'r')
					self.graphicWidget.item.plot(self.x,self.u,'k')
					self.graphicWidget.fig.canvas.draw()

				
			else:
				if self.t > self.itr:
						self.killTimer(self.timer)
				else:
					self.clearPlot()
					self.advecItr()
					self.graphicWidget.item.plot(self.x,self.uinit,'r')
					self.graphicWidget.item.plot(self.x,self.u,'k')
					self.graphicWidget.fig.canvas.draw()

	""" CFD declarations """
	def setCFDActivated(self):
		""" Set the CFD parameters on initialization """
		self.scope = 'cfd'

	def cfdSimulate(self):
		self.cfdSimulatescope='shock'
		self.clearPlot()
		self.cfdInputfnc()
		self.graphicWidget.item.set_autoscale_on(True)
		self.graphicWidget.fig.canvas.draw()
		self.cfdSolver = cfdSolver(self.cfdInput)
		self.cfdSolver.read_data()
		self.cfdSolver.grid()
		self.cfdSolver.initialisation()
		self.shockboundaryCondtn()
		self.cfdSolver.t =0.0
		self.cfdSolver.itr=0
		self.timerEvent(None)
		self.timer = self.startTimer(self.doubleSpinBox_shockTimer.value()*1000)
		
		
		
		
		
		
		
			#print "DTIMe", dt
			#print "For itr ",itr," The time is",t," and dt is",dt
			#print U[49][0],"  ",U[49][1],"  ",U[49][2]," \t ",U[50][0]," ",U[50][1]," ",U[50][2],"\t ",U[51][0]," ",U[51][1]," ",U[51][2]
			#print netflux[49][0],"  ",netflux[49][1],"  ",netflux[49][2]," \t ",netflux[50][0]," ",netflux[50][1]," ",netflux[50][2],"\t ",netflux[51][0]," ",netflux[51][1]," ",netflux[51][2]

#		print " Time Final", self.cfdSolver.t
#		#self.output()
#		print " x ",self.x," ri ",self.cfdSolver.ri,
#		self.plt()
#		print " Time Final", self.t
		
		
#		self.graphicWidget.item.plot(self.cfdSolver.x,self.cfdSolver.ri,'r')
#		temp1rho=[]
#		temp2ui=[]
#		temp3pi=[]
#		xplt=[]
#		for i in range(int(self.cfdInput['numCells']) ):
#			xplt.append(self.cfdSolver.x[i] ) 
#			temp1= self.cfdSolver.U[i][0]
#			temp1rho.append(temp1)
#			temp2 =(self.cfdSolver.U[i][1])/temp1
#			temp2ui.append(temp2 )
#			temp3pi.append( ((self.cfdSolver.U[i][2]-(0.5*temp2*temp2*temp1))*(self.cfdInput['gamma']-1))  )
#		self.graphicWidget.item.plot(xplt,temp1rho,'r')
#		self.graphicWidget.item.plot(xplt,temp2ui,'g')
#		self.graphicWidget.item.plot(xplt,temp3pi,'b')
#		self.graphicWidget.item.set_xlim(0,self.cfdInput['length'])
	def cfdInputfnc(self):
		cfl = self.doubleSpinBox_CFL.value()
		cfdLength = self.doubleSpinBox_cfdLength.value()
		cfdDiphrmPostn = self.doubleSpinBox_cfdDiphrmPostn.value()
		cfdcellNum = self.doubleSpinBox_cfdcellNum.value()
		
		rho_l = self.doubleSpinBox_cfdrhoL.value()
		u_l = self.doubleSpinBox_cfduL.value()
		p_l = self.doubleSpinBox_cfdpresL.value()
		rho_r = self.doubleSpinBox_cfdrhoR.value()
		u_r = self.doubleSpinBox_cfduR.value()
		p_r = self.doubleSpinBox_cfdpresR.value()
		
		minfsq = self.doubleSpinBox_cfdminfsq.value()
		ku = self.doubleSpinBox_cfdku.value()
		kp = self.doubleSpinBox_cfdkp.value()
		sigma = self.doubleSpinBox_cfdsigma.value()
		beta = self.doubleSpinBox_cfdbeta.value()
		alpha = self.doubleSpinBox_cfdalpha.value()
		tf = self.doubleSpinBox_cfdtf.value()
		itrf = self.doubleSpinBox_cfditrf.value()
		cfdcellNum = self.doubleSpinBox_cfdcellNum.value()
		gamma = self.doubleSpinBox_cfdgamma.value()
		
		
		self.cfdInput={}
		self.cfdInput['cfl']=cfl
		self.cfdInput['length']=cfdLength
		self.cfdInput['diphrmPostn']=cfdDiphrmPostn
		self.cfdInput['numCells']=cfdcellNum
		
		self.cfdInput['minfsq']=minfsq
		self.cfdInput['ku']=ku
		self.cfdInput['kp']=kp 
		self.cfdInput['sigma']=sigma
		self.cfdInput['beta']=beta
		self.cfdInput['alpha']=alpha
		
		self.cfdInput['rho_l']=rho_l
		self.cfdInput['u_l']=u_l
		self.cfdInput['p_l']=p_l
		self.cfdInput['rho_r']=rho_r
		self.cfdInput['u_r']=u_r
		self.cfdInput['p_r']=p_r

		self.cfdInput['tf']=tf
		self.cfdInput['itrf']= itrf
		self.cfdInput['gamma'] = gamma
		

	def cfdflux(self):
		i=0
		while i<=self.cfdSolver.numCells:
			if self.VanLeer.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.vanleer(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.HLLC.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.HLLC(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.HLL.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.HLL(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.AUSM.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.ausm(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.AUSMp.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.ausmplus(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.AUSMUp.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.AUSMup(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
			if self.StegerWarming.isChecked():
				self.cfdSolver.fi[i]= self.cfdSolver.schemes.stegerwarming(Ui=self.cfdSolver.U[i],Ui1=self.cfdSolver.U[i+1] )
								
			#print "  vanleer: ", fi[i],
			#print U[i]," ",U[i+1]," ",fi[i]
			#fi[i]= schemes.stegerwarming(U[i],U[i+1] )
			#fi[i]= schemes.HLLC(U[i],U[i+1] )
			#print U[i]," ",U[i+1]," ",fi[i]
			i=i+1  
		#print " ",fi
		i=1
		while i<=self.cfdSolver.numCells:
			self.cfdSolver.netflux[i][0]= self.cfdSolver.fi[i-1][0]-self.cfdSolver.fi[i][0]
			self.cfdSolver.netflux[i][1]= self.cfdSolver.fi[i-1][1]-self.cfdSolver.fi[i][1]
			self.cfdSolver.netflux[i][2]= self.cfdSolver.fi[i-1][2]-self.cfdSolver.fi[i][2]
			i=i+1
	def shockboundaryCondtn(self):
		if self.radioButton_shockFree.isChecked():
			self.cfdSolver.U[0][0] = self.cfdSolver.U[1][0]
			self.cfdSolver.U[0][1] = self.cfdSolver.U[1][1]
			self.cfdSolver.U[0][2] = self.cfdSolver.U[1][2]

			self.cfdSolver.U[self.cfdSolver.numCells+1][0] = self.cfdSolver.U[self.cfdSolver.numCells][0]
			self.cfdSolver.U[self.cfdSolver.numCells+1][1] = self.cfdSolver.U[self.cfdSolver.numCells][1]
			self.cfdSolver.U[self.cfdSolver.numCells+1][2] = self.cfdSolver.U[self.cfdSolver.numCells][2]

		if self.radioButton_shockReflective.isChecked():
			self.cfdSolver.U[0][0] = self.cfdSolver.U[1][0]
			self.cfdSolver.U[0][1] = -1*self.cfdSolver.U[1][1]
			self.cfdSolver.U[0][2] = self.cfdSolver.U[1][2]

			self.cfdSolver.U[self.cfdSolver.numCells+1][0] = self.cfdSolver.U[self.cfdSolver.numCells][0]
			self.cfdSolver.U[self.cfdSolver.numCells+1][1] = -1*self.cfdSolver.U[self.cfdSolver.numCells][1]
			self.cfdSolver.U[self.cfdSolver.numCells+1][2] = self.cfdSolver.U[self.cfdSolver.numCells][2]

		if self.radioButton_shockComplement.isChecked():
			self.cfdSolver.U[0][0] =  self.cfdSolver.U[self.cfdSolver.numCells][0]
			self.cfdSolver.U[0][1] = self.cfdSolver.U[self.cfdSolver.numCells][1]
			self.cfdSolver.U[0][2] = self.cfdSolver.U[self.cfdSolver.numCells][2]

			self.cfdSolver.U[self.cfdSolver.numCells+1][0] =self.cfdSolver.U[1][0]
			self.cfdSolver.U[self.cfdSolver.numCells+1][1] = self.cfdSolver.U[1][1]
			self.cfdSolver.U[self.cfdSolver.numCells+1][2] = self.cfdSolver.U[1][2]
			
	def advecSimulate(self):
		self.cfdSimulatescope='advec'
		self.numCells=self.doubleSpinBox_advecCellNum.value()
		self.itr=self.doubleSpinBox_advecitrf.value()
		self.Length = self.doubleSpinBox_advecLength.value()
		self.c=self.doubleSpinBox_advecC.value()
		self.CFL=self.doubleSpinBox_advecCFL.value()
		self.timerdt=self.doubleSpinBox_advecTimer.value()
		self.deltaX=self.Length/self.numCells
		self.deltaT=fabs(self.CFL*self.deltaX/self.c)
		self.x=[]
		self.u=[]
		self.u0=[]
		self.uinit=[]
		# initialization
		#### Step Up Initialization
		if 	self.radioButton_stepUp.isChecked():
			i=0
			while i <= (self.numCells/2):
				self.x.append( self.Length*(i-1.0)/self.numCells )
				self.u.append( 1)
				self.uinit.append(1)
				self.u0.append(1)
				i+=1	
			i=self.numCells/2+1
			while i<=self.numCells+1:
				self.x.append(self.Length*(i-1.0)/self.numCells )
				self.u.append(2)
				self.uinit.append(2)
				self.u0.append( 2)
				i+=1
		#### Step Down Initialization
		if 	self.radioButton_stepDown.isChecked():
			i=0
			while i <= (self.numCells/2):
				self.x.append( self.Length*(i-1.0)/self.numCells )
				self.u.append(2)
				self.uinit.append(2)
				self.u0.append(2)
				i+=1	
			i=self.numCells/2+1
			while i<=numCells+1:
				self.x.append(self.Length*(i-1.0)/self.numCells )
				self.u.append(1)
				self.uinit.append(1)
				self.u0.append( 1)
				i+=1
		#### Sin Initialization
		if 	self.radioButton_advecSin.isChecked():
			i=0
			while i <= (self.numCells+1):		
				self.x.append(self.Length*(i - 1.0) / (self.numCells))
				self.u.append(math.sin(2.0 * 3.141592654 * self.x[i] / self.Length) )
				self.u0.append(		sin(2.0 * 3.141592654 * self.x[i] / self.Length) )
				self.uinit.append(	sin(2.0 * 3.141592654 * self.x[i] / self.Length) )
				i+=1
		#print "numCells: ",self.numCells," CFL",self.CFL," Itr: ",self.itr
		self.t=0
		self.timerEvent(None)
		self.timer = self.startTimer(self.timerdt*1000)


	def advecItr(self):
		self.t+=1
		#print " t: ",self.t
		i=1
		print "c: ",self.c
		while i <= self.numCells:
			##### FTCS
			if 	self.radioButton_FTCS.isChecked():
				#print i
				self.u[i] = self.u0[i] - (self.c * self.deltaT / (2.0*self.deltaX) ) * (self.u0[i+1] - self.u0[i-1])
			##### FTFS
			if 	self.radioButton_FTFS.isChecked():
				self.u[i] = self.u0[i] - (self.c * self.deltaT / self.deltaX) * (self.u0[i+1] - self.u0[i])
			##### FTBS
			if 	self.radioButton_FTBS.isChecked():            	
				self.u[i] = self.u0[i] - (self.c * self.deltaT / self.deltaX) * (self.u0[i] - self.u0[i-1])
            ##### Upwind
			if 	self.radioButton_Upwind.isChecked():            	
				if (self.c>0.0):
					self.u[i] = self.u0[i] - (self.c * self.deltaT / self.deltaX) * (self.u0[i] - self.u0[i-1])
				elif (self.c<0.0):
					self.u[i] = self.u0[i] - (self.c * self.deltaT / self.deltaX) * (self.u0[i+1] - self.u0[i])
        	##### Lax Wendroff
			if 	self.radioButton_LaxWendroff.isChecked():            	
				self.lamda = self.c * self.deltaT / self.deltaX
				self.u[i] = self.u0[i] - ( ( self.lamda / 2.0 ) * (self.u0[i+1] - self.u0[i-1])) + ( ( self.lamda * self.lamda / 2.0) * (self.u0[i+1] - 2.0 * self.u0[i] + self.u0[i-1]) ) 
				print "self.c: ",self.c," self.lamda: ",self.lamda,"self.u[",i,"]",self.u[i],"self.deltaT: ",self.deltaT, "self.deltaX: ",self.deltaX
		 	i+=1	
		print "c1: ",self.c
		i=1
		while i <= self.numCells:
			self.u0[i] = self.u[i]
			i+=1
		#### Boundary Conditions
		if self.radioButton_advecComplement.isChecked():
			self.u0[0] = self.u0[int(self.numCells)]
			self.u0[int(self.numCells)+1] = self.u0[1]
		if self.radioButton_advecFree.isChecked():
			self.u0[0] = self.u0[1]
			self.u0[int(self.numCells)+1] = self.u0[int(self.numCells)]
		if self.radioButton_advecReflective.isChecked():
			self.u0[0] = -1* self.u0[1]
			self.u0[int(self.numCells)+1] = -1*self.u0[int(self.numCells)]
		
	def burgSimulate(self):
		self.cfdSimulatescope='burg'

		self.numCells=self.doubleSpinBox_burgCellNum.value()
		self.totalTime=self.doubleSpinBox_burgtf.value()
		self.Length = self.doubleSpinBox_advecLength.value()
		self.CFL=self.doubleSpinBox_burgCFL.value()

		self.deltaX=self.Length/self.numCells
		self.deltaT= 0					#fabs(self.CFL*self.deltaX/self.c)
		self.x=numpy.zeros(self.numCells+2)
		self.u=numpy.zeros(self.numCells+2)
		self.u0=numpy.zeros(self.numCells+2)
		self.uinit=numpy.zeros(self.numCells+2)
		# initialization
	    # Length
		i=0
		while i <= (self.numCells+1):
			self.x[i] = (2.0*i - 1.0) / (2.0*self.numCells)
			i+=1
		#backward step: for shock propagation and smearing
		if 	self.radioButton_backstep.isChecked():
			i=0
			while i <= (self.numCells+1)/2.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 2.0
				i+=1

			i=((self.numCells+1)/2.0)+1
			while i <= (self.numCells+1):
				self.u[i] = self.u0[i] = self.uinit[i] = 1.0
				i+=1

		#forward step: for expansion evolution and smearing
		if self.radioButton_forwstep.isChecked():
			i=0
			while i <= (self.numCells+1)/2.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 1.0
				i+=1
			i=((self.numCells+1)/2.0)+1
			while i <= (self.numCells+1):
				self.u[i] = self.u0[i] = self.uinit[i] = 2.0
				i+=1

		# backward ramp:for shock formation from just a smooth slope
		if self.radioButton_backramp.isChecked():
			i=0
			while i <= (self.numCells+1)/4.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 2.0
				i+=1
			xTemp1 = self.x[int((self.numCells+1)/4.0)]
			xTemp2 = self.x[int((self.numCells+1)/2.0)+1]
			i=((self.numCells+1)/4.0)+1
			while i <= (self.numCells+1)/2.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 2.0 - (self.x[i] - xTemp1) / (xTemp2 - xTemp1) ;
				i+=1
			i=((self.numCells+1)/2.0)+1
			while i <= (self.numCells+1):
				self.u[i] = self.u0[i] = self.uinit[i] = 1.0
				i+=1

		#forward ramp: for expansion evolution from constant slope
		if self.radioButton_forwramp.isChecked():
			i=0
			while i <= (self.numCells+1)/4.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 1.0
				i+=1
			xTemp1 = self.x[int((self.numCells+1)/4.0)]
			xTemp2 = self.x[int((self.numCells+1)/2.0)+1]
			i=((self.numCells+1)/4.0)+1
			while i <= (self.numCells+1)/2.0:
				self.u[i] = self.u0[i] = self.uinit[i] = 1.0 + (self.x[i] - xTemp1) / (xTemp2 - xTemp1) 
				i+=1
			i=((self.numCells+1)/2.0)+1
			while i <= (self.numCells+1):
				self.u[i] = self.u0[i] = self.uinit[i] = 2.0
				i+=1
		self.timeElapsed=0.0
		self.timerEvent(None)
		self.timer = self.startTimer(self.doubleSpinBox_burgTimer.value()*1000)

	def burgItr(self):

		# deltaT calculation for burgers' equation
		uMax=0.0
		i=1
		while i <= self.numCells:
			if (fabs(self.u0[i]) > uMax):
				uMax = self.u0[i]
			i+=1
		deltaT = fabs(self.CFL*self.deltaX/uMax);

		i=1
		while i <= self.numCells:
			# Lax Method
			self.u[i] = (self.u0[i+1]+self.u0[i-1])/2.0 - (deltaT/self.deltaX)*( self.u0[i+1]*self.u0[i+1] - self.u0[i-1]*self.u0[i-1])/4.0 
			i+=1

		i=1
		while i <= self.numCells:
			self.u0[i] = self.u[i]
			i+=1
		#### Boundary Conditions
		if self.radioButton_burgComplement.isChecked():
			self.u0[0] = self.u0[int(self.numCells)]
			self.u0[int(self.numCells)+1] = self.u0[1]
		if self.radioButton_burgFree.isChecked():
			self.u0[0] = self.u0[1]
			self.u0[int(self.numCells)+1] = self.u0[int(self.numCells)]
		if self.radioButton_burgReflective.isChecked():
			self.u0[0] = -1* self.u0[1]
			self.u0[int(self.numCells)+1] = -1*self.u0[int(self.numCells)]
		self.timeElapsed = self.timeElapsed + deltaT;

	""" Panel methods declarations - Kailash Make your changes here when you
	pull/merge/push """
	def setPanelMethodsActivated(self):
		""" set panel method initial declarations """
		self.scope = 'panelMethods'

		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	application = MainWindow()
	application.show()
	app.exec_()
