import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class App(QWidget):

    def __init__(self):
        super(App, self).__init__()
        self.button = None
        print("init")

        self.textfield = None
        init_gui()

    def init_gui(self):
        self.resize(500, 40)
        self.setWindowTitle("LoRa Test")

        self.layout = QHBoxLayout(self)

        self.button = QPushButton("Send", self)
        self.button.clicked.connect(onClick)

        self.textfield = QLineEdit(self)

        self.layout.addWidget(self.textfield)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)
        self.show()

        sys.exit(app.exec_())

    @pyqtSlot()
    def onClick():
        print('PyQt5 button click')


app = App()

        
        
