import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

button = None
textfield = None

@pyqtSlot()
def onClick():
    print('PyQt5 button click')


if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(500, 40)
    w.setWindowTitle('Simple')
    

    layout = QHBoxLayout(w)

    button = QPushButton("Send", w)
    button.clicked.connect(onClick)
    textfield = QLineEdit(w)

    layout.addWidget(textfield)
    layout.addWidget(button)

    
    w.setLayout(layout)
    w.show()
    
    
    sys.exit(app.exec_())


