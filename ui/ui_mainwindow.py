# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Tue Nov  1 22:48:16 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(824, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMouseTracking(False)
        MainWindow.setToolTip("")
        MainWindow.setWhatsThis("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_Main = QtGui.QHBoxLayout()
        self.horizontalLayout_Main.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_Main.setObjectName("horizontalLayout_Main")
        self.Input_Dock = QtGui.QDockWidget(self.centralwidget)
        self.Input_Dock.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Input_Dock.sizePolicy().hasHeightForWidth())
        self.Input_Dock.setSizePolicy(sizePolicy)
        self.Input_Dock.setMaximumSize(QtCore.QSize(400, 524287))
        self.Input_Dock.setAutoFillBackground(False)
        self.Input_Dock.setInputMethodHints(QtCore.Qt.ImhNone)
        self.Input_Dock.setFloating(False)
        self.Input_Dock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.Input_Dock.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.Input_Dock.setObjectName("Input_Dock")
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget_potElements = QtGui.QTreeWidget(self.dockWidgetContents_3)
        self.treeWidget_potElements.setTabKeyNavigation(True)
        self.treeWidget_potElements.setAlternatingRowColors(True)
        self.treeWidget_potElements.setObjectName("treeWidget_potElements")
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_potElements)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_potElements)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_potElements)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_potElements)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_potElements)
        self.verticalLayout_2.addWidget(self.treeWidget_potElements)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_Remove = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_Remove.setEnabled(False)
        self.pushButton_Remove.setObjectName("pushButton_Remove")
        self.horizontalLayout.addWidget(self.pushButton_Remove)
        self.pushButton_Edit = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_Edit.setEnabled(False)
        self.pushButton_Edit.setObjectName("pushButton_Edit")
        self.horizontalLayout.addWidget(self.pushButton_Edit)
        self.pushButton_toggleSimulation = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_toggleSimulation.setEnabled(False)
        self.pushButton_toggleSimulation.setObjectName("pushButton_toggleSimulation")
        self.horizontalLayout.addWidget(self.pushButton_toggleSimulation)
        self.pushButton_Simulate = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_Simulate.setObjectName("pushButton_Simulate")
        self.horizontalLayout.addWidget(self.pushButton_Simulate)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_Source = QtGui.QRadioButton(self.dockWidgetContents_3)
        self.radioButton_Source.setChecked(True)
        self.radioButton_Source.setObjectName("radioButton_Source")
        self.horizontalLayout_2.addWidget(self.radioButton_Source)
        self.radioButton_Sink = QtGui.QRadioButton(self.dockWidgetContents_3)
        self.radioButton_Sink.setObjectName("radioButton_Sink")
        self.horizontalLayout_2.addWidget(self.radioButton_Sink)
        self.radioButton_Doublet = QtGui.QRadioButton(self.dockWidgetContents_3)
        self.radioButton_Doublet.setObjectName("radioButton_Doublet")
        self.horizontalLayout_2.addWidget(self.radioButton_Doublet)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton_Vortex = QtGui.QRadioButton(self.dockWidgetContents_3)
        self.radioButton_Vortex.setObjectName("radioButton_Vortex")
        self.horizontalLayout_3.addWidget(self.radioButton_Vortex)
        self.radioButton_UniformFlow = QtGui.QRadioButton(self.dockWidgetContents_3)
        self.radioButton_UniformFlow.setObjectName("radioButton_UniformFlow")
        self.horizontalLayout_3.addWidget(self.radioButton_UniformFlow)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_X = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_X.setObjectName("label_X")
        self.horizontalLayout_8.addWidget(self.label_X)
        self.doubleSpinBox_X = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.doubleSpinBox_X.setMinimum(-1000.0)
        self.doubleSpinBox_X.setMaximum(1000.0)
        self.doubleSpinBox_X.setSingleStep(0.1)
        self.doubleSpinBox_X.setObjectName("doubleSpinBox_X")
        self.horizontalLayout_8.addWidget(self.doubleSpinBox_X)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_Y = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_Y.setObjectName("label_Y")
        self.horizontalLayout_9.addWidget(self.label_Y)
        self.doubleSpinBox_Y = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.doubleSpinBox_Y.setMinimum(-1000.0)
        self.doubleSpinBox_Y.setMaximum(1000.0)
        self.doubleSpinBox_Y.setSingleStep(0.1)
        self.doubleSpinBox_Y.setObjectName("doubleSpinBox_Y")
        self.horizontalLayout_9.addWidget(self.doubleSpinBox_Y)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_9)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_FlowAngle = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_FlowAngle.setObjectName("label_FlowAngle")
        self.horizontalLayout_11.addWidget(self.label_FlowAngle)
        self.doubleSpinBox_FlowAngle = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.doubleSpinBox_FlowAngle.setMinimum(-360.0)
        self.doubleSpinBox_FlowAngle.setMaximum(360.0)
        self.doubleSpinBox_FlowAngle.setSingleStep(1.0)
        self.doubleSpinBox_FlowAngle.setObjectName("doubleSpinBox_FlowAngle")
        self.horizontalLayout_11.addWidget(self.doubleSpinBox_FlowAngle)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_Strength = QtGui.QLabel(self.dockWidgetContents_3)
        self.label_Strength.setObjectName("label_Strength")
        self.horizontalLayout_10.addWidget(self.label_Strength)
        self.doubleSpinBox_Strength = QtGui.QDoubleSpinBox(self.dockWidgetContents_3)
        self.doubleSpinBox_Strength.setMinimum(-10000.0)
        self.doubleSpinBox_Strength.setMaximum(10000.0)
        self.doubleSpinBox_Strength.setSingleStep(0.1)
        self.doubleSpinBox_Strength.setObjectName("doubleSpinBox_Strength")
        self.horizontalLayout_10.addWidget(self.doubleSpinBox_Strength)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem1)
        self.pushButton_Clear = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.horizontalLayout_12.addWidget(self.pushButton_Clear)
        self.pushButton_Add = QtGui.QPushButton(self.dockWidgetContents_3)
        self.pushButton_Add.setObjectName("pushButton_Add")
        self.horizontalLayout_12.addWidget(self.pushButton_Add)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.Input_Dock.setWidget(self.dockWidgetContents_3)
        self.horizontalLayout_Main.addWidget(self.Input_Dock)
        self.verticalLayout_3.addLayout(self.horizontalLayout_Main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 824, 25))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Window = QtGui.QMenu(self.menubar)
        self.menu_Window.setObjectName("menu_Window")
        self.menu_Aerodynamics = QtGui.QMenu(self.menubar)
        self.menu_Aerodynamics.setObjectName("menu_Aerodynamics")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar_Icons = QtGui.QToolBar(MainWindow)
        self.toolBar_Icons.setObjectName("toolBar_Icons")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar_Icons)
        self.action_Save = QtGui.QAction(MainWindow)
        self.action_Save.setObjectName("action_Save")
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Tools = QtGui.QAction(MainWindow)
        self.action_Tools.setObjectName("action_Tools")
        self.action_Potential_Flows = QtGui.QAction(MainWindow)
        self.action_Potential_Flows.setObjectName("action_Potential_Flows")
        self.actionPanel_Methods = QtGui.QAction(MainWindow)
        self.actionPanel_Methods.setObjectName("actionPanel_Methods")
        self.actionCFD = QtGui.QAction(MainWindow)
        self.actionCFD.setObjectName("actionCFD")
        self.action_Clear_all = QtGui.QAction(MainWindow)
        self.action_Clear_all.setObjectName("action_Clear_all")
        self.action_Clear_All = QtGui.QAction(MainWindow)
        self.action_Clear_All.setObjectName("action_Clear_All")
        self.menu_File.addAction(self.action_Save)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Window.addAction(self.action_Clear_All)
        self.menu_Aerodynamics.addAction(self.action_Potential_Flows)
        self.menu_Aerodynamics.addAction(self.actionPanel_Methods)
        self.menu_Aerodynamics.addAction(self.actionCFD)
        self.menu_Aerodynamics.addSeparator()
        self.menu_Aerodynamics.addAction(self.action_Clear_all)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Aerodynamics.menuAction())
        self.menubar.addAction(self.menu_Window.menuAction())
        self.label_FlowAngle.setBuddy(self.doubleSpinBox_Strength)
        self.label_Strength.setBuddy(self.doubleSpinBox_Strength)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL("activated()"), MainWindow.close)
        QtCore.QObject.connect(self.actionCFD, QtCore.SIGNAL("activated()"), self.Input_Dock.show)
        QtCore.QObject.connect(self.actionCFD, QtCore.SIGNAL("activated()"), self.Input_Dock.setFocus)
        QtCore.QObject.connect(self.action_Potential_Flows, QtCore.SIGNAL("activated()"), self.Input_Dock.show)
        QtCore.QObject.connect(self.action_Potential_Flows, QtCore.SIGNAL("activated()"), self.Input_Dock.setFocus)
        QtCore.QObject.connect(self.actionPanel_Methods, QtCore.SIGNAL("activated()"), self.Input_Dock.show)
        QtCore.QObject.connect(self.actionPanel_Methods, QtCore.SIGNAL("activated()"), self.Input_Dock.setFocus)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.radioButton_Source, self.radioButton_Sink)
        MainWindow.setTabOrder(self.radioButton_Sink, self.radioButton_Doublet)
        MainWindow.setTabOrder(self.radioButton_Doublet, self.radioButton_Vortex)
        MainWindow.setTabOrder(self.radioButton_Vortex, self.radioButton_UniformFlow)
        MainWindow.setTabOrder(self.radioButton_UniformFlow, self.doubleSpinBox_X)
        MainWindow.setTabOrder(self.doubleSpinBox_X, self.doubleSpinBox_Y)
        MainWindow.setTabOrder(self.doubleSpinBox_Y, self.doubleSpinBox_Strength)
        MainWindow.setTabOrder(self.doubleSpinBox_Strength, self.pushButton_Clear)
        MainWindow.setTabOrder(self.pushButton_Clear, self.pushButton_Add)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "EduAeroSpace", None, QtGui.QApplication.UnicodeUTF8))
        self.Input_Dock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Input", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Added Elements", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeWidget_potElements.isSortingEnabled()
        self.treeWidget_potElements.setSortingEnabled(False)
        self.treeWidget_potElements.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", "Doublets", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.topLevelItem(1).setText(0, QtGui.QApplication.translate("MainWindow", "Sinks", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.topLevelItem(2).setText(0, QtGui.QApplication.translate("MainWindow", "Sources", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.topLevelItem(3).setText(0, QtGui.QApplication.translate("MainWindow", "Uniformflow", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.topLevelItem(4).setText(0, QtGui.QApplication.translate("MainWindow", "Vortices", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_potElements.setSortingEnabled(__sortingEnabled)
        self.pushButton_Remove.setText(QtGui.QApplication.translate("MainWindow", "&Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Edit.setText(QtGui.QApplication.translate("MainWindow", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_toggleSimulation.setText(QtGui.QApplication.translate("MainWindow", "&Play", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Simulate.setText(QtGui.QApplication.translate("MainWindow", "&Simulate", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_Source.setText(QtGui.QApplication.translate("MainWindow", "&Source", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_Sink.setText(QtGui.QApplication.translate("MainWindow", "S&ink", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_Doublet.setText(QtGui.QApplication.translate("MainWindow", "&Doublet", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_Vortex.setText(QtGui.QApplication.translate("MainWindow", "&Vortex", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_UniformFlow.setText(QtGui.QApplication.translate("MainWindow", "&Uniform flow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_X.setText(QtGui.QApplication.translate("MainWindow", "X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Y.setText(QtGui.QApplication.translate("MainWindow", "Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_FlowAngle.setText(QtGui.QApplication.translate("MainWindow", "&Flow angle", None, QtGui.QApplication.UnicodeUTF8))
        self.label_Strength.setText(QtGui.QApplication.translate("MainWindow", "Strength", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Clear.setText(QtGui.QApplication.translate("MainWindow", "&Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Add.setText(QtGui.QApplication.translate("MainWindow", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Window.setTitle(QtGui.QApplication.translate("MainWindow", "&Window", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Aerodynamics.setTitle(QtGui.QApplication.translate("MainWindow", "&Aerodynamics", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_Icons.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Tools.setText(QtGui.QApplication.translate("MainWindow", "&Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Potential_Flows.setText(QtGui.QApplication.translate("MainWindow", "&Potential Flows", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPanel_Methods.setText(QtGui.QApplication.translate("MainWindow", "Panel Methods", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCFD.setText(QtGui.QApplication.translate("MainWindow", "CFD", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_all.setText(QtGui.QApplication.translate("MainWindow", "&Clear all", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Clear_All.setText(QtGui.QApplication.translate("MainWindow", "&Clear All", None, QtGui.QApplication.UnicodeUTF8))

