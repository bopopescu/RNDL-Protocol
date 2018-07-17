from window import *
from transceiver import *
import threading


class RNDLMasterGUI(Window):

    def __init__(self):
        super(RNDLMasterGUI, self).__init__()

        self.chatlog = ""
        self.tf_chatlog.setText(self.chatlog)
        self.trans = Transceiver("COM10")



    @pyqtSlot()
    def onClick(self):
        self.send_request()
    
        
    def send_request(self):
        self.chatlog = self.chatlog + "| " + self.tf_address.text() + " | >> " + self.tf.text()  + "\n" 
        self.tf_chatlog.setText(self.chatlog)      
        self.repaint()
        self.update()
        #TODO: check for invalid chars
        reply = self.trans.request_data(self.tf_address.text(), self.tf.text())

        self.chatlog = self.chatlog + "| " + self.tf_address.text() + " | << " + reply  + "\n" 
        self.tf_chatlog.setText(self.chatlog)      

        



app = QApplication(sys.argv)    
window = RNDLMasterGUI()
sys.exit(app.exec_())

  
