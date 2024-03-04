from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QMainWindow, QLineEdit, QMessageBox, QComboBox
from PUT_File_WinSCP import PUTFileWinSCP
from GET_File_WinSCP import GETFileWinSCP
from Read_Trigger_WinSCP import ReadTriggerWinSCP
import time
from datetime import datetime

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Get Log File Test')
        
        self.SN_Box = QLineEdit('', self)
        self.SN_Box.setAlignment(Qt.AlignCenter)
        self.SN_Box.setMaxLength(9)
        self.SN_Box.setGeometry(110,10,80,20)

        label = QLabel("Filter : ", self)
        label.move(10,3)
        self.drop_box = QComboBox(self)
        self.drop_box.addItem('All')
        self.drop_box.addItem('html')    
        self.drop_box.setGeometry(48,10,50,20)

        BT = QPushButton('Submit', self)
        BT.setGeometry(110,40,80,30)
        BT.clicked.connect(self.search_log_file)

        with open('temp/trigger/trigger.txt', 'w') as f:
                file_read = f.write(f'0,SN,N/A')
        PUT_File_WinSCP = PUTFileWinSCP()
        PUT_File_WinSCP.start_put_file()

        self.setFixedSize(300,100)
        self.trigger = 0

    def search_log_file(self):
        print("Sending trigger...")     
        with open('temp/trigger/trigger.txt', 'w') as f:
            file_read = f.write(f'1,{self.SN_Box.text()},{self.drop_box.currentText()}')
        PUT_File_WinSCP = PUTFileWinSCP()
        PUT_File_WinSCP.start_put_file()
            
        self.time_delay()    

    def time_delay(self):
        time.sleep(1)
        self.get_log_file()

    def get_log_file(self):
        Read_Trigger_WinSCP = ReadTriggerWinSCP()
        self.trigger = Read_Trigger_WinSCP.start_read_trigger_file()

        dt = datetime.now()
        current_date = dt.strftime("%H:%M:%S")

        print(f"Trigger : {self.trigger}, Time Usage : {current_date}")
        if self.trigger == b'1':
            GET_File_WinSCP = GETFileWinSCP()
            GET_File_WinSCP.start_get_file()
            with open('temp/trigger/trigger.txt', 'w') as f:
                file_read = f.write(f'0,SN,N/A')
            PUT_File_WinSCP = PUTFileWinSCP()
            PUT_File_WinSCP.start_put_file()

            dt = datetime.now()
            current_date = dt.strftime("%H:%M:%S")
            print(f"Trigger : {self.trigger}, Time Usage : {current_date}")
            QMessageBox.information(self, "Notify", "Transfer successfully!")
        else:
            self.time_delay()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()