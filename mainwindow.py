# python libraries
import os
import platform
import sys
import re
from pylab import linspace
from matplotlib.backends.backend_qt4agg \
		import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.patches import FancyArrowPatch
# PyQt4 libraries
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# Local libraries
from potentialLibrary import *
from plot import *
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

		# Potential flow related connections
		QObject.connect(self.pushButton_Add, SIGNAL("clicked()"), self.potaddElement)
		QObject.connect(self.pushButton_Remove, SIGNAL("clicked()"), self.potRemoveElement)
		QObject.connect(self.pushButton_Clear, SIGNAL("clicked()"), self.potClearData)
		QObject.connect(self.pushButton_Simulate, SIGNAL("clicked()"), self.potSimulate)
		QObject.connect(self.pushButton_toggleSimulation, SIGNAL("clicked()"), self.toggleSimulation)
		QObject.connect(self.pushButton_potAddpatch, SIGNAL("clicked()"), self.potAddStreakParticles)
		QObject.connect(self.radioButton_Source, SIGNAL("clicked()"), self.potSourceSelected)
		QObject.connect(self.radioButton_Sink, SIGNAL("clicked()"), self.potSinkSelected)
		QObject.connect(self.radioButton_Doublet, SIGNAL("clicked()"), self.potDoubletSelected)
		QObject.connect(self.radioButton_UniformFlow, SIGNAL("clicked()"), self.potUniformFlowSelected)
		QObject.connect(self.radioButton_Vortex, SIGNAL("clicked()"), self.potVortexSelected)
		QObject.connect(self.radioButton_StreamLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.radioButton_PathLines, SIGNAL("clicked()"), self.potSetPlotScope)
		QObject.connect(self.comboBox_pathLines, SIGNAL("currentIndexChanged(QString)"), self.potSetPatchInputParameters)
		QObject.connect(self.pushButton_cfdSimulate, SIGNAL("clicked()"), self.cfdSimulate)

		if self.scope == 'potentialFlows' :
			self.InputPotentialFlows_Dock.setHidden(False)
			self.InputCFD_Dock.setHidden(True)
			# The following will set the input widget accordingly
			self.radioButton_Source.setChecked(True)
			self.potSetVisible(self.radioButton_UniformFlow.isChecked())
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
			self.comboBox_pathLines.setCurrentIndex(1)
			self.comboBox_pathLines.setCurrentIndex(0)
		elif self.scope == 'cfd' :
			self.InputCFD_Dock.setHidden(False)
			self.InputPotentialFlows_Dock.setHidden(True)
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
			message = "Removed the element. Nothing to worry if it still appears in the list"
			self.statusbar.showMessage(message , 1500)
			# self.treeWidget_potElements.topLevelItem(0).removeChild(self.treeWidget_potElements.topLevelItem(0).child(1))
			# Need to clear the plot before plotting
			self.graphicWidget.plotPotElements(self.potLibrary.elements)
			self.graphicWidget.show()
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
		self.clearPlot()
		self.graphicWidget.plotPotElements(self.potLibrary.elements)
		self.graphicWidget.item.set_autoscale_on(True)
		self.graphicWidget.plotStreakParticles(self.potStreakParticles)
		self.graphicWidget.item.set_autoscale_on(False)
		self.graphicWidget.fig.canvas.draw()
		self.pushButton_toggleSimulation.setEnabled(True)
		self.pushButton_toggleSimulation.setText("&Pause")
		self.count = 0
		if self.potStreakParticles != []:
			self.graphicWidget.clearStreakParticles() # To clear streak line in the plot window
		if (self.plotType == 'pathLines') and (self.potLibrary.elements != []) :
			self.potStreakParticles == [] :
		elif (self.plotType == 'streamLines') and (self.potLibrary.elements != []):
			self.statusbar.showMessage("Plotting the stream lines. This may take some time...")
			self.potAddStreamParticles()

		# Start simulation in real time	
		self.timerEvent(None)
		if self.timer != None :
			self.killTimer(self.timer)
		self.timer = self.startTimer(0.001)

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

	def timerEvent(self, event):
		""" Supposed to update the plot """
		if self.plotType == "stremLines" :
			repeat = 2
			maxCount = 10
		else : 
			repeat = 1
			maxCount = self.count + 1
		for instnace in range(repeat):
			self.potAdvectParticles(dt = 0.01, integType = 'rk2')
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
		# to set auto scale on if axis limits are exceeded
		if self.plotType != "stremLines" and self.potStreakParticles != []:
			xRange = [item.pos.real for item in self.potStreakParticles]
			yRange = [item.pos.imag for item in self.potStreakParticles]
			if min(xRange) < self.axisRange[0]: self.axisRange += array([min(xRange) - self.axisRange[0], 0, 0, 0])
			if max(xRange) > self.axisRange[1]: self.axisRange += array([0, max(xRange) -self.axisRange[1], 0, 0])
			if min(yRange) < self.axisRange[2]: self.axisRange += array([0, 0, min(yRange) -self.axisRange[2], 0])
			if max(yRange) > self.axisRange[3]: self.axisRange += array([0, 0, 0, max(yRange) -self.axisRange[3]])
			self.graphicWidget.item.axis(array(self.axisRange))
			self.graphicWidget.fig.canvas.draw()
		else :
			self.graphicWidget.item.axis('equal')
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
			for theta in linspace(0, 2*pi, 180):
				position = center + radius*exp(1j*theta)
				newParticle = particle(position.real, position.imag)
				self.potStreakParticles.append(newParticle)
		self.graphicWidget.item.set_autoscale_on(True)
		self.graphicWidget.plotStreakParticles(self.potStreakParticles)
		self.graphicWidget.item.set_autoscale_on(False)
		self.graphicWidget.fig.canvas.draw()

	def potAddParticlesAt(self, startX, tag = 'X', noParticles = 30, yMin = -5.0, yMax = 5.0):
		""" Adds particles at x """
		if int(abs(yMax - yMin)) > noParticles :
			noParticles = int(abs(yMax - yMin))
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
	
	def clearPlot(self):
		"""  Clears the plot window without changing the axis limits """
		self.graphicWidget.item.cla()
		self.graphicWidget.item.set_autoscale_on(False)
		self.graphicWidget.item.grid(True)

	def potSetPlotScope(self):
		""" Sets plot type and displays required input properties for that scope """
		if (self.radioButton_StreamLines.isChecked()):
			self.plotType = 'streamLines'
			# To set the patch input parameters invisible
			self.potSetPatchInVisibility(True)
		elif (self.radioButton_PathLines.isChecked()):
			self.plotType = 'pathLines'
			self.potSetPatchInVisibility(False)
			self.comboBox_pathLines.setCurrentIndex(1)
			self.comboBox_pathLines.setCurrentIndex(0)
		else :
			pass

	def potSetPatchInVisibility(self, invisible):
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
			self.doubleSpinBox_patchInfo1.setMinimum(0.1)
			self.doubleSpinBox_patchInfo1.setSingleStep(0.1)
			self.doubleSpinBox_patchInfo2.setHidden(True)
			self.label_patchInfo1.setText("length")
		elif patchType == 'Circular':
			self.label_center.setHidden(False)
			self.doubleSpinBox_centerX.setHidden(False)
			self.doubleSpinBox_centerY.setHidden(False)
			self.label_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setHidden(False)
			self.doubleSpinBox_patchInfo1.setMinimum(0.1)
			self.doubleSpinBox_patchInfo1.setSingleStep(0.1)
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
			self.potSetPatchInVisibility(False)
			self.doubleSpinBox_patchInfo1.setMinimum(0.1)
			self.doubleSpinBox_patchInfo1.setSingleStep(0.1)
			self.doubleSpinBox_patchInfo2.setMinimum(0.1)
			self.doubleSpinBox_patchInfo2.setSingleStep(0.1)
			self.label_patchInfo1.setText("(l, b)")
		else :
			pass

	def potAddStreamParticles(self):
		""" Takes the dimwentions of plot widget and plots stream lines by
		advecting the particles for a small time step dt """
		noOfParticlesAtX = int(self.axisRange[3] - self.axisRange[2])*3
		noOfParticlesAtY = int(self.axisRange[1] - self.axisRange[0])*2
		self.potStreakParticles = [particle(x, y) for x in linspace(self.axisRange[1], self.axisRange[0], \
				noOfParticlesAtY) for y in linspace(self.axisRange[2]+0.1, self.axisRange[3]-0.1, noOfParticlesAtX)]
		self.graphicWidget.item.grid(False)
		self.graphicWidget.plotStreakParticles(self.potStreakParticles, tag = "streamLines")
		self.graphicWidget.fig.canvas.draw()

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

	""" CFD declarations """
	def cfdSimulate(self):
		self.clearPlot()
		self.cfdInput()
		lst=[0.5,0.5,self.cfdInput['cfl'],self.cfdInput['length'],self.cfdInput['diphrmPostn'],self.cfdInput['numCells'] ]
		#self.graphicWidget.item.plot(lst,'or')
		self.graphicWidget.item.set_autoscale_on(True)
		self.graphicWidget.fig.canvas.draw()
		self.cfdSolver = cfdSolver(self.cfdInput)
		self.cfdSolver.main()
#		self.graphicWidget.item.plot(self.cfdSolver.x,self.cfdSolver.ri,'r')
		temp1rho=[]
		temp2ui=[]
		temp3pi=[]
		xplt=[]
		for i in range(int(self.cfdInput['numCells']) ):
			xplt.append(self.cfdSolver.x[i] ) 
			temp1= self.cfdSolver.U[i][0]
			temp1rho.append(temp1)
			temp2 =(self.cfdSolver.U[i][1])/temp1
			temp2ui.append(temp2 )
			temp3pi.append( ((self.cfdSolver.U[i][2]-(0.5*temp2*temp2*temp1))*(self.cfdInput['gamma']-1))  )
		self.graphicWidget.item.plot(xplt,temp1rho,'r')
		self.graphicWidget.item.plot(xplt,temp2ui,'g')
		self.graphicWidget.item.plot(xplt,temp3pi,'b')
		self.graphicWidget.item.set_xlim(0,self.cfdInput['length'])
	def cfdInput(self):
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
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	application = MainWindow()
	application.show()
	app.exec_()
