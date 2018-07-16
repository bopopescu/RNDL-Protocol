import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QDialog):
 
    def __init__(self):
        super().__init__()

        self.button = None
        self.textfield = None
       
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle("LoRa Test")
        self.setGeometry(10, 10, 320, 100)
        self.move(600, 200)
        self.createGridLayout()
 
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Transmitter")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

        self.button = QPushButton('1')
        self.textfield = QLineEdit()
 
        layout.addWidget(self.button,0,0) 
        layout.addWidget(textfield,1,0) 
        
 
        self.horizontalGroupBox.setLayout(layout)
 
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
