import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets, QtGui
import os
import shutil

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        with open('setting/Path Files Location.txt', 'r') as f:
            file_read_1 = f.read()       
        self.file_read_1 = file_read_1.replace("\\", '/')
        self.setWindowTitle('Fiber Inspect Monitoring')

        desired_size = (25, 30)

        icon_TRUE = QPixmap("temp/icon/True.ico")
        self.resized_icon_TRUE = icon_TRUE.scaled(*desired_size)

        icon_FALSE = QPixmap("temp/icon/False.ico")
        self.resized_icon_FALSE = icon_FALSE.scaled(*desired_size)

        self.icon_1 = QLabel(self)       
        self.icon_1.setPixmap(self.resized_icon_TRUE)
        self.icon_1.setGeometry(203, 20, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_2 = QLabel(self)       
        self.icon_2.setPixmap(self.resized_icon_TRUE)
        self.icon_2.setGeometry(623, 20, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_3 = QLabel(self)       
        self.icon_3.setPixmap(self.resized_icon_TRUE)
        self.icon_3.setGeometry(203, 60, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_4 = QLabel(self)       
        self.icon_4.setPixmap(self.resized_icon_TRUE)
        self.icon_4.setGeometry(623, 60, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_5 = QLabel(self)       
        self.icon_5.setPixmap(self.resized_icon_TRUE)
        self.icon_5.setGeometry(203, 100, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_6 = QLabel(self)       
        self.icon_6.setPixmap(self.resized_icon_TRUE)
        self.icon_6.setGeometry(623, 100, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_7 = QLabel(self)       
        self.icon_7.setPixmap(self.resized_icon_TRUE)
        self.icon_7.setGeometry(203, 140, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_8 = QLabel(self)       
        self.icon_8.setPixmap(self.resized_icon_TRUE)
        self.icon_8.setGeometry(623, 140, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_9 = QLabel(self)       
        self.icon_9.setPixmap(self.resized_icon_TRUE)
        self.icon_9.setGeometry(203, 180, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_10 = QLabel(self)       
        self.icon_10.setPixmap(self.resized_icon_TRUE)
        self.icon_10.setGeometry(623, 180, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_11 = QLabel(self)       
        self.icon_11.setPixmap(self.resized_icon_TRUE)
        self.icon_11.setGeometry(203, 220, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 

        self.icon_12 = QLabel(self)       
        self.icon_12.setPixmap(self.resized_icon_TRUE)
        self.icon_12.setGeometry(623, 220, self.resized_icon_TRUE.width(), self.resized_icon_TRUE.height()) 
        
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.val_1 = QLineEdit('', self)
        self.val_1.setReadOnly(True)
        self.val_1.setAlignment(Qt.AlignCenter)
        self.val_1.setFont(font)
        self.val_1.setGeometry(20,20,180,30)

        self.val_2 = QLineEdit('', self)
        self.val_2.setReadOnly(True)
        self.val_2.setAlignment(Qt.AlignCenter)
        self.val_2.setFont(font)
        self.val_2.setGeometry(230,20,180,30)

        self.val_3 = QLineEdit('', self)
        self.val_3.setReadOnly(True)
        self.val_3.setAlignment(Qt.AlignCenter)
        self.val_3.setFont(font)
        self.val_3.setGeometry(440,20,180,30)

        self.val_4 = QLineEdit('', self)
        self.val_4.setReadOnly(True)
        self.val_4.setAlignment(Qt.AlignCenter)
        self.val_4.setFont(font)
        self.val_4.setGeometry(650,20,180,30)

        self.val_5 = QLineEdit('', self)
        self.val_5.setReadOnly(True)
        self.val_5.setAlignment(Qt.AlignCenter)
        self.val_5.setFont(font)
        self.val_5.setGeometry(20,60,180,30)

        self.val_6 = QLineEdit('', self)
        self.val_6.setReadOnly(True)
        self.val_6.setAlignment(Qt.AlignCenter)
        self.val_6.setFont(font)
        self.val_6.setGeometry(230,60,180,30)

        self.val_7 = QLineEdit('', self)
        self.val_7.setReadOnly(True)
        self.val_7.setAlignment(Qt.AlignCenter)
        self.val_7.setFont(font)
        self.val_7.setGeometry(440,60,180,30)

        self.val_8 = QLineEdit('', self)
        self.val_8.setReadOnly(True)
        self.val_8.setAlignment(Qt.AlignCenter)
        self.val_8.setFont(font)
        self.val_8.setGeometry(650,60,180,30)

        self.val_9 = QLineEdit('', self)
        self.val_9.setReadOnly(True)
        self.val_9.setAlignment(Qt.AlignCenter)
        self.val_9.setFont(font)
        self.val_9.setGeometry(20,100,180,30)

        self.val_10 = QLineEdit('', self)
        self.val_10.setReadOnly(True)
        self.val_10.setAlignment(Qt.AlignCenter)
        self.val_10.setFont(font)
        self.val_10.setGeometry(230,100,180,30)

        self.val_11 = QLineEdit('', self)
        self.val_11.setReadOnly(True)
        self.val_11.setAlignment(Qt.AlignCenter)
        self.val_11.setFont(font)
        self.val_11.setGeometry(440,100,180,30)

        self.val_12 = QLineEdit('', self)
        self.val_12.setReadOnly(True)
        self.val_12.setAlignment(Qt.AlignCenter)
        self.val_12.setFont(font)
        self.val_12.setGeometry(650,100,180,30)

        self.val_13 = QLineEdit('', self)
        self.val_13.setReadOnly(True)
        self.val_13.setAlignment(Qt.AlignCenter)
        self.val_13.setFont(font)
        self.val_13.setGeometry(20,140,180,30)

        self.val_14 = QLineEdit('', self)
        self.val_14.setReadOnly(True)
        self.val_14.setAlignment(Qt.AlignCenter)
        self.val_14.setFont(font)
        self.val_14.setGeometry(230,140,180,30)

        self.val_15 = QLineEdit('', self)
        self.val_15.setReadOnly(True)
        self.val_15.setAlignment(Qt.AlignCenter)
        self.val_15.setFont(font)
        self.val_15.setGeometry(440,140,180,30)

        self.val_16 = QLineEdit('', self)
        self.val_16.setReadOnly(True)
        self.val_16.setAlignment(Qt.AlignCenter)
        self.val_16.setFont(font)
        self.val_16.setGeometry(650,140,180,30)

        self.val_17 = QLineEdit('', self)
        self.val_17.setReadOnly(True)
        self.val_17.setAlignment(Qt.AlignCenter)
        self.val_17.setFont(font)
        self.val_17.setGeometry(20,180,180,30)

        self.val_18 = QLineEdit('', self)
        self.val_18.setReadOnly(True)
        self.val_18.setAlignment(Qt.AlignCenter)
        self.val_18.setFont(font)
        self.val_18.setGeometry(230,180,180,30)

        self.val_19 = QLineEdit('', self)
        self.val_19.setReadOnly(True)
        self.val_19.setAlignment(Qt.AlignCenter)
        self.val_19.setFont(font)
        self.val_19.setGeometry(440,180,180,30)

        self.val_20 = QLineEdit('', self)
        self.val_20.setReadOnly(True)
        self.val_20.setAlignment(Qt.AlignCenter)
        self.val_20.setFont(font)
        self.val_20.setGeometry(650,180,180,30)

        self.val_21 = QLineEdit('', self)
        self.val_21.setReadOnly(True)
        self.val_21.setAlignment(Qt.AlignCenter)
        self.val_21.setFont(font)
        self.val_21.setGeometry(20,220,180,30)

        self.val_22 = QLineEdit('', self)
        self.val_22.setReadOnly(True)
        self.val_22.setAlignment(Qt.AlignCenter)
        self.val_22.setFont(font)
        self.val_22.setGeometry(230,220,180,30)

        self.val_23 = QLineEdit('', self)
        self.val_23.setReadOnly(True)
        self.val_23.setAlignment(Qt.AlignCenter)
        self.val_23.setFont(font)
        self.val_23.setGeometry(440,220,180,30)

        self.val_24 = QLineEdit('', self)
        self.val_24.setReadOnly(True)
        self.val_24.setAlignment(Qt.AlignCenter)
        self.val_24.setFont(font)
        self.val_24.setGeometry(650,220,180,30)

        self.label_slot = QLabel('มีทั้งหมด [0] SLOTs', self)
        self.label_slot.setFont(font)
        self.label_slot.setGeometry(140,260,150,20)

        self.label_tx = QLabel('มี TX ทั้งหมด [0] เส้น', self)
        self.label_tx.setFont(font)
        self.label_tx.setStyleSheet("color: #003DFF;")
        self.label_tx.setGeometry(340,260,180,20)

        self.label_rx = QLabel('มี RX ทั้งหมด [0] เส้น', self)
        self.label_rx.setFont(font)
        self.label_rx.setStyleSheet("color: #FFA500;")
        self.label_rx.setGeometry(550,260,180,20)
        
        self.array_text_box_1 = [self.val_1, self.val_2, self.val_3, self.val_4, self.val_5, self.val_6, self.val_7, self.val_8, self.val_9, self.val_10, self.val_11, self.val_12]
        self.array_text_box_2 = [self.val_13, self.val_14, self.val_15, self.val_16, self.val_17, self.val_18, self.val_19, self.val_20, self.val_21, self.val_22, self.val_23, self.val_24]
        self.array_icon = [self.icon_1, self.icon_2, self.icon_3, self.icon_4, self.icon_5, self.icon_6, self.icon_7, self.icon_8, self.icon_9, self.icon_10, self.icon_11, self.icon_12]

        self.array_text_box = self.array_text_box_1 + self.array_text_box_2

        self.setGeometry(500,110,0,0)
        self.setFixedSize(860, 290)

        self.time_delay()

    def read_fiber(self):
        list_data_fiber = [f for f in os.listdir(self.file_read_1) if f.endswith(".html")]
        list_data_fiber.sort(key=lambda x: os.path.getmtime(os.path.join(self.file_read_1, x)), reverse=True) 
        list_data_fiber = list_data_fiber[:24]

        SN_Fiber = []
        for i in list_data_fiber:
            SN_Fiber.append(i.split('.')[0])

        for i in range(len(self.array_text_box)):
            self.array_text_box[i].setText('')
            self.array_text_box[i].setStyleSheet("background-color: #FFFFFF;")
        
        for i in range(len(self.array_icon)):
            self.array_icon[i].setVisible(False)

        if len(SN_Fiber) > 0:
            tx = 0
            rx = 0
            for index in range(24):
                if index != len(SN_Fiber):
                    if SN_Fiber[index][0] == 'R':
                        self.array_text_box[index].setText(SN_Fiber[index])
                        self.array_text_box[index].setStyleSheet("background-color: #00EDFF;")
                        tx += 1
                    elif SN_Fiber[index][0] == 'W':
                        self.array_text_box[index].setText(SN_Fiber[index])
                        self.array_text_box[index].setStyleSheet("background-color: #FFA500;")
                        rx += 1
                    else:
                        self.array_text_box[index].setText(SN_Fiber[index])
                        self.array_text_box[index].setStyleSheet("background-color: #FFFFFF;")
                    self.label_tx.setText(f"มี TX ทั้งหมด [{tx}] เส้น")
                    self.label_rx.setText(f"มี RX ทั้งหมด [{rx}] เส้น")
                else:
                    break

            if len(SN_Fiber) % 2 == 0:
                self.label_slot.setText(f"มีทั้งหมด [{int(len(SN_Fiber) / 2)}] SLOTs")
                index = 0
                for x in range(int(len(SN_Fiber) / 2)):
                    if str(SN_Fiber[index][-4:]) == str(SN_Fiber[index + 1][-4:]):
                        if SN_Fiber[index][0] != SN_Fiber[index + 1][0]:
                            self.array_icon[x].setVisible(True)
                            self.array_icon[x].setPixmap(self.resized_icon_TRUE)
                        else:
                            self.array_icon[x].setVisible(True)   
                            self.array_icon[x].setPixmap(self.resized_icon_FALSE)
                    elif str(SN_Fiber[index][-4:]) != str(SN_Fiber[index + 1][-4:]):
                        if SN_Fiber[index][0] and SN_Fiber[index + 1][0]:
                            self.array_icon[x].setVisible(True)   
                            self.array_icon[x].setPixmap(self.resized_icon_FALSE)   
                        else:
                            self.array_icon[x].setVisible(True)   
                            self.array_icon[x].setPixmap(self.resized_icon_FALSE)  
                    index += 2

        else:
            self.label_slot.setText("มีทั้งหมด [0] SLOTs")
            for i in range(len(self.array_text_box)):
                self.array_text_box[i].setText('')
                self.array_text_box[i].setStyleSheet("background-color: #FFFFFF;")
   
        self.time_delay()
    
    def time_delay(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_fiber)
        self.timer.start(200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
