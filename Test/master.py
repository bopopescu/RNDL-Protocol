import serial
import encoder
from serialutil import *
#from transmitter import *
#from receiver import *
from window import *

app = QApplication(sys.argv)    
window = Window()

sys.exit(app.exec_())
