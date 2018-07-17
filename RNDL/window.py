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

        self.tf_chatlog = QTextEdit(self)
        self.tf_chatlog.resize(960, 280)
        self.tf_chatlog.move(20, 20)
        self.tf_chatlog.setReadOnly(True)
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.darkGray)
        self.tf_chatlog.setPalette(palette)
        font = self.tf_chatlog.font()
        font.setPointSize(15)
        self.tf_chatlog.setFont(font)

        self.tf_address = QLineEdit(self)
        self.tf_address.resize(60, 60)
        self.tf_address.move(20, 320)
        font = self.tf_address.font()
        font.setPointSize(35)
        self.tf_address.setFont(font)

        self.tf = QLineEdit(self)
        self.tf.move(100, 320)
        self.tf.resize(800, 60)
        font = self.tf.font()
        font.setPointSize(30)
        self.tf.setFont(font)

    @pyqtSlot()
    def onClick(self):
        print('PyQt5 button click')
        print(self.tf.text())



if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = Window()

    sys.exit(app.exec_())