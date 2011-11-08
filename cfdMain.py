
class cfd():
    def  __init__

    def addCfdElement(self):
		""" SLOT for add action in  GUI """
		self.elementInfo = {}
		self.elementInfo['cfl'] = self.doubleSpinBox_cfl.value()   
		self.elementInfo['numCell'] = self.doubleSpinBox_numCell.value()
        self.elementInfo['length'] = self.doubleSpinBox_length.value()
        self.elementInfo['diaghramPosition'] = self.doubleSpinBox_diphrmPostn.value()
        
        self.potLibrary.addElement(self.elementInfo)
		self.graphicWidget.plotPotElements([self.cfdLibrary.elements[-1]])
		self.potResizeGraphicWindow()
        
