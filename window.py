import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self.setGeometry(50, 50, 1000, 400)
        self.setWindowTitle("LoRa Test")

        self.init_gui()

        self.show()

    def init_gui(self):
        btn = QPushButton("Send", self)
        btn.clicked.connect(self.onClick)
        btn.resize(60, 60)
        btn.move(920, 320)

        self.tf = QLineEdit(self)
        self.tf.move(20, 320)
        self.tf.resize(880, 60)
        font = self.tf.font()
        font.setPointSize(30)
        self.tf.setFont(font)

        self.chatlog = QTextEdit(self)
        self.chatlog.resize(960, 280)
        self.chatlog.move(20, 20)
        self.chatlog.setReadOnly(True)
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.darkGray)
        self.chatlog.setPalette(palette)


        self.chatlog.setText("test\nasdf")        
        

    @pyqtSlot()
    def onClick(self):
        print('PyQt5 button click')
        print(self.tf.text())


app = QApplication(sys.argv)    
window = Window()

sys.exit(app.exec_())

        
        
