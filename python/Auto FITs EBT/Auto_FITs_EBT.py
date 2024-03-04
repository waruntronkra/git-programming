from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QApplication, QMainWindow, QDialog, QRadioButton, QFrame, QButtonGroup, QRadioButton, QMessageBox, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from Query_ATS import QueryATS
from Check_In_FITs import CheckInFITs
from Check_Out_FITs import CheckOutFITs
from Query_LC_Count import QueryLineCardCount
import win32com.client as win32
import time
import sys
import cv2
import os
import shutil

class CameraDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Camera')
        self.setFixedSize(600, 570)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setGeometry(10,10,580,500)

        self.capture_button = QPushButton('Capture !', self)
        self.capture_button.setStyleSheet('''
                                        font-size : 16px; 
                                        font-family : Century Gothic; 
                                        font-weight : bold;
                                    ''')
        self.capture_button.clicked.connect(self.capture_image)
        self.capture_button.setGeometry(250, 510, 100, 50)

        self.video_capture = cv2.VideoCapture(1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 milliseconds

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.video_label.setPixmap(pixmap)

    def capture_image(self):
        ret, frame = self.video_capture.read()
        if ret:
            if not os.path.exists('captured_image_1.png'):
                cv2.imwrite('captured_image_1.png', frame)
                QMessageBox.information(self,'PASS', f'Completed! -> Attache File #1')
            elif not os.path.exists('captured_image_2.png'):
                cv2.imwrite('captured_image_2.png', frame)
                QMessageBox.information(self,'PASS', f'Completed! -> Attache File #2')
            elif not os.path.exists('captured_image_3.png'):
                cv2.imwrite('captured_image_3.png', frame)
                QMessageBox.information(self,'PASS', f'Completed! -> Attache File #3')

    def closeEvent(self, event):
        self.video_capture.release()
        self.timer.stop()
        self.hide()
        event.accept()

class MessageBox(QMessageBox):
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet('color: white;')

class Main_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto FITs EBT')
        self.setStyleSheet('background-color : #131633;')
        self.setFixedSize(1280,850)

        header_text_1 = QLabel('Auto', self)
        header_text_1.setStyleSheet('''
                                        color : white; 
                                        font-size : 16px; 
                                        font-family : Century Gothic; 
                                        font-weight : bold;
                                    ''')
        header_text_1.setGeometry(13, 14, 50, 20)

        header_text_2 = QLabel('Check-In / Check-Out', self)
        header_text_2.setStyleSheet('''                                    
                                        color : white; 
                                        font-size : 16px; 
                                        font-family : Century Gothic;
                                        font-weight : 3px;
                                        color : #FDA006;
                                    ''')
        header_text_2.setGeometry(55, 14, 200, 20)

        header_text_3 = QLabel('FITs', self)
        header_text_3.setStyleSheet('''                                    
                                        color : #44FD06; 
                                        font-size : 35px; 
                                        font-family : Ricks American NF; 
                                        font-weight : bold;
                                    ''')
        header_text_3.setGeometry(240, 0, 200, 50)

        # ============================= Create detail for check in FITs [P030] =============================
        x_move = 0
        y_move = 60

        fram_user_info_P030 = QFrame(self)
        fram_user_info_P030.setStyleSheet('background-color : #222840; border: 1px solid black; border-radius : 5px')
        fram_user_info_P030.setGeometry(x_move + 10, y_move - 10, 300, 330)

        label_header_P030 = QLabel('P030 : EBT', self)
        label_header_P030.setStyleSheet('background-color : transparent; font-weight : bold; color : red; font-size : 15px;text-decoration: underline;')
        label_header_P030.setGeometry(x_move + 20, y_move - 10, 100,30)

        label_SN_Text_P030 = QLabel('SERIAL NUMBER', self)
        label_SN_Text_P030.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_SN_Text_P030.move(x_move + 20, y_move + 16)
        self.SN_Text_P030 = QLineEdit('', self)
        self.SN_Text_P030.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.SN_Text_P030.setAlignment(Qt.AlignCenter)
        self.SN_Text_P030.setMaxLength(12)
        self.SN_Text_P030.setGeometry(x_move + 120, y_move + 20, 100, 25)

        label_EN_Text_P030 = QLabel('EN', self)
        label_EN_Text_P030.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_EN_Text_P030.move(x_move + 95, y_move + 46)
        self.EN_Text_P030 = QLineEdit('', self)
        self.EN_Text_P030.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.EN_Text_P030.setAlignment(Qt.AlignCenter)
        self.EN_Text_P030.setMaxLength(6)
        self.EN_Text_P030.setGeometry(x_move + 120, y_move + 50, 70, 25)
        
        group_ration_bt_P030 = QButtonGroup(self)
        label_send_to_P030 = QLabel('Send to', self)
        label_send_to_P030.setStyleSheet('background-color : #222840; font-weight : bold; color : white')
        label_send_to_P030.move(x_move + 120, y_move + 80)

        send_to_P025 = QRadioButton('P025 : MDIO EBT Screening', self)
        send_to_P025.setStyleSheet('background-color : #222840; color : white;')
        send_to_P025.setGeometry(x_move + 120, y_move + 110, 150, 15)
        send_to_P030 = QRadioButton('P030 : EBT', self)
        send_to_P030.setStyleSheet('background-color : #222840; color : white;')
        send_to_P030.setGeometry(x_move + 120, y_move + 130, 150, 15)
        send_to_P031 = QRadioButton('P031 : Baking#1', self)
        send_to_P031.setStyleSheet('background-color : #222840; color : white;')
        send_to_P031.setGeometry(x_move + 120, y_move + 150, 150, 15)
        send_to_P040 = QRadioButton('P040 : EBS (EBT Manual)', self)
        send_to_P040.setStyleSheet('background-color : #222840; color : white;')
        send_to_P040.setGeometry(x_move + 120, y_move + 170, 150, 15)
        send_to_P060 = QRadioButton('P060 : OQA Inspection', self)
        send_to_P060.setStyleSheet('background-color : #222840; color : white;')
        send_to_P060.setGeometry(x_move + 120, y_move + 190, 150, 15)
        send_to_P064 = QRadioButton('P064 : SMT Test Disposition', self)
        send_to_P064.setStyleSheet('background-color : #222840; color : white;')
        send_to_P064.setGeometry(x_move + 120, y_move + 210, 150, 15)
        send_to_P065 = QRadioButton('P065 : SMT Process Disposition', self)
        send_to_P065.setStyleSheet('background-color : #222840; color : white;')
        send_to_P065.setGeometry(x_move + 120, y_move + 230, 150, 15)
        send_to_P080 = QRadioButton('P080 : Debug', self)
        send_to_P080.setStyleSheet('background-color : #222840; color : white;')
        send_to_P080.setGeometry(x_move + 120, y_move + 250, 150, 15)
        send_to_P092 = QRadioButton('P092 : Bake', self)
        send_to_P092.setStyleSheet('background-color : #222840; color : white;')
        send_to_P092.setGeometry(x_move + 120, y_move + 270, 150, 15)
        send_to_PCBC = QRadioButton('PCBC : PCBA Coationg', self)
        send_to_PCBC.setStyleSheet('background-color : #222840; color : white;')
        send_to_PCBC.setGeometry(x_move + 120, y_move + 290, 150, 15)

        group_ration_bt_P030.addButton(send_to_P025)
        group_ration_bt_P030.addButton(send_to_P030)
        group_ration_bt_P030.addButton(send_to_P031)
        group_ration_bt_P030.addButton(send_to_P040)
        group_ration_bt_P030.addButton(send_to_P060)
        group_ration_bt_P030.addButton(send_to_P064)
        group_ration_bt_P030.addButton(send_to_P065)
        group_ration_bt_P030.addButton(send_to_P080)
        group_ration_bt_P030.addButton(send_to_P092)
        group_ration_bt_P030.addButton(send_to_PCBC)

        group_ration_bt_P030.buttonClicked.connect(self.send_to_selected_for_P030)

        submit_button_P030 = QPushButton('Submit [P030]', self)
        submit_button_P030.setStyleSheet('''
                                        QPushButton {
                                            background-color : #00C689;
                                            border-radius : 5px;
                                            font-weight : bold;
                                            font-family : MV Boli;
                                            font-size : 13px;
                                        }
                                        QPushButton:hover {
                                            background-color : #00E6A0;
                                        } 
                                        QPushButton:pressed {
                                            background-color : #008A60;
                                        }                                       
                                    ''')
        submit_button_P030.clicked.connect(self.keys_FITs_P030)                                            
        submit_button_P030.setGeometry(x_move + 10, y_move + 330, 300, 30)

        # ============================= Create detail for check in FITs [P025] =============================
        x_move_P025 = 320
        y_move_P025 = 60

        fram_user_info_P025 = QFrame(self)
        fram_user_info_P025.setStyleSheet('background-color : #222840; border: 1px solid black; border-radius : 5px')
        fram_user_info_P025.setGeometry(x_move_P025 + 10, y_move_P025 - 10, 250, 170)

        label_header_P025 = QLabel('P025 : MDIO EBT Screening', self)
        label_header_P025.setStyleSheet('background-color : transparent; font-weight : bold; color : red; font-size : 15px;text-decoration: underline;')
        label_header_P025.setGeometry(x_move_P025 + 20, y_move_P025 - 10, 240,30)

        label_SN_Text_P025 = QLabel('SERIAL NUMBER', self)
        label_SN_Text_P025.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_SN_Text_P025.move(x_move_P025 + 20, y_move_P025 + 16)
        self.SN_Text_P025 = QLineEdit('', self)
        self.SN_Text_P025.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.SN_Text_P025.setAlignment(Qt.AlignCenter)
        self.SN_Text_P025.setMaxLength(12)
        self.SN_Text_P025.setGeometry(x_move_P025 + 120, y_move_P025 + 20, 100, 25)

        label_EN_Text_P025 = QLabel('EN', self)
        label_EN_Text_P025.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_EN_Text_P025.move(x_move_P025 + 95, y_move_P025 + 46)
        self.EN_Text_P025 = QLineEdit('', self)
        self.EN_Text_P025.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.EN_Text_P025.setAlignment(Qt.AlignCenter)
        self.EN_Text_P025.setMaxLength(6)
        self.EN_Text_P025.setGeometry(x_move_P025 + 120, y_move_P025 + 50, 70, 25)

        group_ration_bt_P025 = QButtonGroup(self)
        label_send_to_P025 = QLabel('Send to', self)
        label_send_to_P025.setStyleSheet('background-color : #222840; font-weight : bold; color : white')
        label_send_to_P025.move(x_move_P025 + 120, y_move_P025 + 80)

        send_to_P031_for_P025 = QRadioButton('P031 : Baking#1', self)
        send_to_P031_for_P025.setStyleSheet('background-color : #222840; color : white;')
        send_to_P031_for_P025.setGeometry(x_move_P025 + 120, y_move_P025 + 110, 100, 15)
        send_to_P060_for_P025 = QRadioButton('P060 : OQA Inspection', self)
        send_to_P060_for_P025.setStyleSheet('background-color : #222840; color : white;')
        send_to_P060_for_P025.setGeometry(x_move_P025 + 120, y_move_P025 + 130, 130, 15)

        group_ration_bt_P025.addButton(send_to_P031_for_P025)
        group_ration_bt_P025.addButton(send_to_P060_for_P025)

        group_ration_bt_P025.buttonClicked.connect(self.send_to_selected_for_P025)

        submit_button_P025 = QPushButton('Submit [P025]', self)
        submit_button_P025.setStyleSheet('''
                                        QPushButton {
                                            background-color : #00C689;
                                            border-radius : 5px;
                                            font-weight : bold;
                                            font-family : MV Boli;
                                            font-size : 13px;
                                        }
                                        QPushButton:hover {
                                            background-color : #00E6A0;
                                        } 
                                        QPushButton:pressed {
                                            background-color : #008A60;
                                        }                                       
                                    ''')
        submit_button_P025.clicked.connect(self.keys_FITs_P025)                                            
        submit_button_P025.setGeometry(x_move_P025 + 10, y_move_P025 + 170, 250, 30)

        # ============================= Create detail for check in FITs [P020] =============================
        x_move_P020 = 590
        y_move_P020 = 60
        fram_user_info_P020 = QFrame(self)
        fram_user_info_P020.setStyleSheet('background-color : #222840; border: 1px solid black; border-radius : 5px')
        fram_user_info_P020.setGeometry(x_move_P020 + 10, y_move_P020 - 10, 250, 750)

        label_header_P020 = QLabel('P020 : VMI Pre EBT', self)
        label_header_P020.setStyleSheet('background-color : transparent; font-weight : bold; color : red; font-size : 15px;text-decoration: underline;')
        label_header_P020.setGeometry(x_move_P020 + 20, y_move_P020 - 10, 240,30)

        label_SN_Text_P020 = QLabel('SERIAL NUMBER', self)
        label_SN_Text_P020.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_SN_Text_P020.move(x_move_P020 + 20, y_move_P020 + 16)
        self.SN_Text_P020 = QLineEdit('', self)
        self.SN_Text_P020.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.SN_Text_P020.setAlignment(Qt.AlignCenter)
        self.SN_Text_P020.setMaxLength(12)
        self.SN_Text_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 20, 100, 25)

        label_EN_Text_P020 = QLabel('EN', self)
        label_EN_Text_P020.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_EN_Text_P020.move(x_move_P020 + 95, y_move_P020 + 46)
        self.EN_Text_P020 = QLineEdit('', self)
        self.EN_Text_P020.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.EN_Text_P020.setAlignment(Qt.AlignCenter)
        self.EN_Text_P020.setMaxLength(6)
        self.EN_Text_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 50, 70, 25)

        self.group_ration_bt_P020 = QButtonGroup(self)
        label_send_to_P020 = QLabel('Defect', self)
        label_send_to_P020.setStyleSheet('background-color : #222840; font-weight : bold; color : white')
        label_send_to_P020.move(x_move_P020 + 120, y_move_P020 + 80)

        self.bt_result_P020 = QPushButton('PASS', self)
        self.bt_result_P020.setStyleSheet('background-color : #36FF00;')
        self.bt_result_P020.clicked.connect(self.changeColor_P020)     
        self.bt_result_P020.setGeometry(x_move_P020 + 40, y_move_P020 + 80, 70, 30)

        f1_for_P020 = QRadioButton('Misaligment', self)
        f1_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f1_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 110, 130, 15)
        f2_for_P020 = QRadioButton('Wrong direction', self)
        f2_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f2_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 130, 130, 15)
        f3_for_P020 = QRadioButton('HSP scratch', self)
        f3_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f3_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 150, 130, 15)
        f4_for_P020 = QRadioButton('HSP exposed copper', self)
        f4_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f4_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 170, 130, 15)
        f5_for_P020 = QRadioButton('PCBA damage', self)
        f5_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f5_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 190, 130, 15)
        f6_for_P020 = QRadioButton('PCBA pad lift', self)
        f6_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f6_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 210, 130, 15)
        f7_for_P020 = QRadioButton('PCBA discoloration', self)
        f7_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f7_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 230, 130, 15)
        f8_for_P020 = QRadioButton('Connector scratch', self)
        f8_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f8_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 250, 130, 15)
        f9_for_P020 = QRadioButton('Connector Bending', self)
        f9_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f9_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 270, 130, 15)
        f10_for_P020 = QRadioButton('Connector Broken', self)
        f10_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f10_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 290, 130, 15)
        f11_for_P020 = QRadioButton('Connector Pin Damage', self)
        f11_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f11_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 310, 130, 15)
        f12_for_P020 = QRadioButton('Exposed Copper', self)
        f12_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f12_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 330, 130, 15)
        f13_for_P020 = QRadioButton('Dent', self)
        f13_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f13_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 350, 130, 15)
        f14_for_P020 = QRadioButton('Rusty', self)
        f14_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f14_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 370, 130, 15)
        f15_for_P020 = QRadioButton('Scratch', self)
        f15_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f15_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 390, 130, 15)
        f16_for_P020 = QRadioButton('Blurr', self)
        f16_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f16_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 410, 130, 15)
        f17_for_P020 = QRadioButton('Solder ball', self)
        f17_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f17_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 430, 130, 15)
        f18_for_P020 = QRadioButton('Solder splash', self)
        f18_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f18_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 450, 130, 15)
        f19_for_P020 = QRadioButton('Non wetting', self)
        f19_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f19_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 470, 130, 15)
        f20_for_P020 = QRadioButton('Insufficient Solder', self)
        f20_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f20_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 490, 130, 15)
        f21_for_P020 = QRadioButton('Exceed solder', self)
        f21_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f21_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 510, 130, 15)
        f22_for_P020 = QRadioButton('Poor solder', self)
        f22_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f22_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 530, 130, 15)
        f23_for_P020 = QRadioButton('Missing', self)
        f23_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f23_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 550, 130, 15)
        f24_for_P020 = QRadioButton('Damage', self)
        f24_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f24_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 570, 130, 15)
        f25_for_P020 = QRadioButton('Crack', self)
        f25_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f25_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 590, 130, 15)
        f26_for_P020 = QRadioButton('Knock off', self)
        f26_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f26_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 610, 130, 15)
        f28_for_P020 = QRadioButton('wire deform', self)
        f28_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f28_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 630, 130, 15)
        f29_for_P020 = QRadioButton('Other', self)
        f29_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f29_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 650, 130, 15)
        f30_for_P020 = QRadioButton('Exposed nickel', self)
        f30_for_P020.setStyleSheet('background-color : #222840; color : white;')
        f30_for_P020.setGeometry(x_move_P020 + 120, y_move_P020 + 670, 130, 15)

        self.group_ration_bt_P020.addButton(f1_for_P020)
        self.group_ration_bt_P020.addButton(f2_for_P020)
        self.group_ration_bt_P020.addButton(f3_for_P020)
        self.group_ration_bt_P020.addButton(f4_for_P020)
        self.group_ration_bt_P020.addButton(f5_for_P020)
        self.group_ration_bt_P020.addButton(f6_for_P020)
        self.group_ration_bt_P020.addButton(f7_for_P020)
        self.group_ration_bt_P020.addButton(f8_for_P020)
        self.group_ration_bt_P020.addButton(f9_for_P020)
        self.group_ration_bt_P020.addButton(f10_for_P020)
        self.group_ration_bt_P020.addButton(f11_for_P020)
        self.group_ration_bt_P020.addButton(f12_for_P020)
        self.group_ration_bt_P020.addButton(f13_for_P020)
        self.group_ration_bt_P020.addButton(f14_for_P020)
        self.group_ration_bt_P020.addButton(f15_for_P020)
        self.group_ration_bt_P020.addButton(f16_for_P020)
        self.group_ration_bt_P020.addButton(f17_for_P020)
        self.group_ration_bt_P020.addButton(f18_for_P020)
        self.group_ration_bt_P020.addButton(f19_for_P020)
        self.group_ration_bt_P020.addButton(f20_for_P020)
        self.group_ration_bt_P020.addButton(f21_for_P020)
        self.group_ration_bt_P020.addButton(f22_for_P020)
        self.group_ration_bt_P020.addButton(f23_for_P020)
        self.group_ration_bt_P020.addButton(f24_for_P020)
        self.group_ration_bt_P020.addButton(f25_for_P020)
        self.group_ration_bt_P020.addButton(f26_for_P020)
        self.group_ration_bt_P020.addButton(f28_for_P020)
        self.group_ration_bt_P020.addButton(f29_for_P020)
        self.group_ration_bt_P020.addButton(f30_for_P020)

        self.group_ration_bt_P020.setExclusive(False)

        self.group_ration_bt_P020.buttonClicked.connect(self.fail_defect_P020_selected)

        self.camera_dialog = CameraDialog()

        self.button_on_camera_P020 = QCheckBox('Use Camera', self)
        self.button_on_camera_P020.setStyleSheet('background-color : #222840; color : white;')
        self.button_on_camera_P020.setGeometry(x_move_P020 + 30, y_move_P020 + 701, 130, 15)

        camera_button = QPushButton('Open Camera', self)
        camera_button.clicked.connect(self.open_camera)
        camera_button.setStyleSheet('background-color : #BAFFFC; font-weight: bold;')
        camera_button.setGeometry(x_move_P020 + 120, y_move_P020 + 695, 120, 30)

        submit_button_P020 = QPushButton('Submit [P020]', self)
        submit_button_P020.setStyleSheet('''
                                        QPushButton {
                                            background-color : #00C689;
                                            border-radius : 5px;
                                            font-weight : bold;
                                            font-family : MV Boli;
                                            font-size : 13px;
                                        }
                                        QPushButton:hover {
                                            background-color : #00E6A0;
                                        } 
                                        QPushButton:pressed {
                                            background-color : #008A60;
                                        }                                       
                                    ''')
        submit_button_P020.clicked.connect(self.keys_FITs_P020)                                            
        submit_button_P020.setGeometry(x_move_P020 + 10, y_move_P020 + 750, 250, 30)

        # ============================= Create detail for check in FITs [P021] =============================
        x_move_P021 = 860
        y_move_P021 = 60
        fram_user_info_P021 = QFrame(self)
        fram_user_info_P021.setStyleSheet('background-color : #222840; border: 1px solid black; border-radius : 5px')
        fram_user_info_P021.setGeometry(x_move_P021 + 10, y_move_P021 - 10, 400, 750)

        label_header_P021 = QLabel('P021 : VMI After EBT', self)
        label_header_P021.setStyleSheet('background-color : transparent; font-weight : bold; color : red; font-size : 15px;text-decoration: underline;')
        label_header_P021.setGeometry(x_move_P021 + 20, y_move_P021 - 10, 240,30)

        label_SN_Text_P021 = QLabel('SERIAL NUMBER', self)
        label_SN_Text_P021.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_SN_Text_P021.move(x_move_P021 + 20, y_move_P021 + 16)
        self.SN_Text_P021 = QLineEdit('', self)
        self.SN_Text_P021.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.SN_Text_P021.setAlignment(Qt.AlignCenter)
        self.SN_Text_P021.setMaxLength(12)
        self.SN_Text_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 20, 100, 25)

        label_EN_Text_P021 = QLabel('EN', self)
        label_EN_Text_P021.setStyleSheet('background-color : transparent; font-weight : bold; color : white;')
        label_EN_Text_P021.move(x_move_P021 + 95, y_move_P021 + 46)
        self.EN_Text_P021 = QLineEdit('', self)
        self.EN_Text_P021.setStyleSheet('background-color : #3DA5F4; border: 1px solid black; border-radius : 5px; font-weight : bold; color : white;')
        self.EN_Text_P021.setAlignment(Qt.AlignCenter)
        self.EN_Text_P021.setMaxLength(6)
        self.EN_Text_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 50, 70, 25)

        self.group_ration_bt_P021 = QButtonGroup(self)
        label_send_to_P021 = QLabel('Defect', self)
        label_send_to_P021.setStyleSheet('background-color : #222840; font-weight : bold; color : white')
        label_send_to_P021.move(x_move_P021 + 120, y_move_P021 + 80)

        self.bt_result_P021 = QPushButton('PASS', self)
        self.bt_result_P021.setStyleSheet('background-color : #36FF00;')
        self.bt_result_P021.clicked.connect(self.changeColor_P021)     
        self.bt_result_P021.setGeometry(x_move_P021 + 40, y_move_P021 + 80, 70, 30)

        f1_for_P021 = QRadioButton('Misaligment', self)
        f1_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f1_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 110, 130, 15)
        f2_for_P021 = QRadioButton('Wrong direction', self)
        f2_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f2_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 130, 130, 15)
        f3_for_P021 = QRadioButton('HSP scratch', self)
        f3_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f3_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 150, 130, 15)
        f4_for_P021 = QRadioButton('HSP exposed copper', self)
        f4_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f4_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 170, 130, 15)
        f5_for_P021 = QRadioButton('PCBA damage', self)
        f5_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f5_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 190, 130, 15)
        f6_for_P021 = QRadioButton('PCBA pad lift', self)
        f6_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f6_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 210, 130, 15)
        f7_for_P021 = QRadioButton('PCBA discoloration', self)
        f7_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f7_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 230, 130, 15)
        f8_for_P021 = QRadioButton('Connector scratch', self)
        f8_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f8_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 250, 130, 15)
        f9_for_P021 = QRadioButton('Connector Bending', self)
        f9_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f9_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 270, 130, 15)
        f10_for_P021 = QRadioButton('Connector Broken', self)
        f10_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f10_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 290, 130, 15)
        f11_for_P021 = QRadioButton('Connector Pin Damage', self)
        f11_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f11_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 310, 130, 15)
        f12_for_P021 = QRadioButton('Exposed Copper', self)
        f12_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f12_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 330, 130, 15)
        f13_for_P021 = QRadioButton('Dent', self)
        f13_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f13_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 350, 130, 15)
        f14_for_P021 = QRadioButton('Rusty', self)
        f14_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f14_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 370, 130, 15)
        f15_for_P021 = QRadioButton('Scratch', self)
        f15_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f15_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 390, 130, 15)
        f16_for_P021 = QRadioButton('Blurr', self)
        f16_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f16_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 410, 130, 15)
        f17_for_P021 = QRadioButton('Solder ball', self)
        f17_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f17_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 430, 130, 15)
        f18_for_P021 = QRadioButton('Solder splash', self)
        f18_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f18_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 450, 130, 15)
        f19_for_P021 = QRadioButton('Non wetting', self)
        f19_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f19_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 470, 130, 15)
        f20_for_P021 = QRadioButton('Insufficient Solder', self)
        f20_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f20_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 490, 130, 15)
        f21_for_P021 = QRadioButton('Exceed solder', self)
        f21_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f21_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 510, 130, 15)
        f22_for_P021 = QRadioButton('Poor solder', self)
        f22_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f22_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 530, 130, 15)
        f23_for_P021 = QRadioButton('Missing', self)
        f23_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f23_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 550, 130, 15)
        f24_for_P021 = QRadioButton('Damage', self)
        f24_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f24_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 570, 130, 15)
        f25_for_P021 = QRadioButton('Crack', self)
        f25_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f25_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 590, 130, 15)
        f26_for_P021 = QRadioButton('Knock off', self)
        f26_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f26_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 610, 130, 15)
        f28_for_P021 = QRadioButton('wire deform', self)
        f28_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f28_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 630, 130, 15)
        f29_for_P021 = QRadioButton('Other', self)
        f29_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f29_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 650, 130, 15)
        f30_for_P021 = QRadioButton('Exposed nickel', self)
        f30_for_P021.setStyleSheet('background-color : #222840; color : white;')
        f30_for_P021.setGeometry(x_move_P021 + 120, y_move_P021 + 670, 130, 15)

        self.group_ration_bt_P021.addButton(f1_for_P021)
        self.group_ration_bt_P021.addButton(f2_for_P021)
        self.group_ration_bt_P021.addButton(f3_for_P021)
        self.group_ration_bt_P021.addButton(f4_for_P021)
        self.group_ration_bt_P021.addButton(f5_for_P021)
        self.group_ration_bt_P021.addButton(f6_for_P021)
        self.group_ration_bt_P021.addButton(f7_for_P021)
        self.group_ration_bt_P021.addButton(f8_for_P021)
        self.group_ration_bt_P021.addButton(f9_for_P021)
        self.group_ration_bt_P021.addButton(f10_for_P021)
        self.group_ration_bt_P021.addButton(f11_for_P021)
        self.group_ration_bt_P021.addButton(f12_for_P021)
        self.group_ration_bt_P021.addButton(f13_for_P021)
        self.group_ration_bt_P021.addButton(f14_for_P021)
        self.group_ration_bt_P021.addButton(f15_for_P021)
        self.group_ration_bt_P021.addButton(f16_for_P021)
        self.group_ration_bt_P021.addButton(f17_for_P021)
        self.group_ration_bt_P021.addButton(f18_for_P021)
        self.group_ration_bt_P021.addButton(f19_for_P021)
        self.group_ration_bt_P021.addButton(f20_for_P021)
        self.group_ration_bt_P021.addButton(f21_for_P021)
        self.group_ration_bt_P021.addButton(f22_for_P021)
        self.group_ration_bt_P021.addButton(f23_for_P021)
        self.group_ration_bt_P021.addButton(f24_for_P021)
        self.group_ration_bt_P021.addButton(f25_for_P021)
        self.group_ration_bt_P021.addButton(f26_for_P021)
        self.group_ration_bt_P021.addButton(f28_for_P021)
        self.group_ration_bt_P021.addButton(f29_for_P021)
        self.group_ration_bt_P021.addButton(f30_for_P021)

        self.group_ration_bt_P021.setExclusive(False)

        self.group_ration_bt_P021.buttonClicked.connect(self.fail_defect_P021_selected)

        group_ration_bt_P021 = QButtonGroup(self)
        label_send_to_P021 = QLabel('Send to', self)
        label_send_to_P021.setStyleSheet('background-color : #222840; font-weight : bold; color : white')
        label_send_to_P021.move(x_move_P021 + 270, y_move_P021 + 80)

        send_to_P031_for_P021 = QRadioButton('P031 : Baking#1', self)
        send_to_P031_for_P021.setStyleSheet('background-color : #222840; color : white;')
        send_to_P031_for_P021.setGeometry(x_move_P021 + 270, y_move_P021 + 110, 100, 15)
        send_to_P060_for_P021 = QRadioButton('P060 : OQA Inspection', self)
        send_to_P060_for_P021.setStyleSheet('background-color : #222840; color : white;')
        send_to_P060_for_P021.setGeometry(x_move_P021 + 270, y_move_P021 + 130, 130, 15)
        send_to_P064_for_P021 = QRadioButton('P064 : SMT Test Disposition', self)
        send_to_P064_for_P021.setStyleSheet('background-color : #222840; color : white;')
        send_to_P064_for_P021.setGeometry(x_move_P021 + 270, y_move_P021 + 150, 130, 15)

        group_ration_bt_P021.addButton(send_to_P031_for_P021)
        group_ration_bt_P021.addButton(send_to_P060_for_P021)
        group_ration_bt_P021.addButton(send_to_P064_for_P021)

        group_ration_bt_P021.buttonClicked.connect(self.send_to_selected_for_P021)

        self.camera_dialog = CameraDialog()

        self.button_on_camera_P021 = QRadioButton('Use Camera', self)
        self.button_on_camera_P021.setStyleSheet('background-color : #222840; color : white;')
        self.button_on_camera_P021.setGeometry(x_move_P021 + 30, y_move_P021 + 701, 130, 15)

        camera_button = QCheckBox('Open Camera', self)
        camera_button.clicked.connect(self.open_camera)
        camera_button.setStyleSheet('background-color : #BAFFFC; font-weight: bold;')
        camera_button.setGeometry(x_move_P021 + 120, y_move_P021 + 695, 120, 30)

        submit_button_P021 = QPushButton('Submit [P021]', self)
        submit_button_P021.setStyleSheet('''
                                        QPushButton {
                                            background-color : #00C689;
                                            border-radius : 5px;
                                            font-weight : bold;
                                            font-family : MV Boli;
                                            font-size : 13px;
                                        }
                                        QPushButton:hover {
                                            background-color : #00E6A0;
                                        } 
                                        QPushButton:pressed {
                                            background-color : #008A60;
                                        }                                       
                                    ''')
        submit_button_P021.clicked.connect(self.keys_FITs_P021)                                            
        submit_button_P021.setGeometry(x_move_P021 + 10, y_move_P021 + 750, 400, 30)

        # =======================================================================================

        self.send_to_for_P030 = ''
        self.send_to_for_P025 = ''
        self.send_to_for_P021 = ''
        self.defectCode_P020 = ''
        self.defectCode_P021 = ''
        self.active_defect_P020 = True
        self.active_defect_P021 = True

    def open_camera(self):
        self.start_camera()
        self.camera_dialog.show()
        
    def start_camera(self):
        self.camera_dialog.video_capture = cv2.VideoCapture(0)
        self.camera_dialog.timer.start(30)  # Update every 30 milliseconds

    def send_to_selected_for_P030(self, button):
        self.send_to_for_P030 = button.text()

    def send_to_selected_for_P025(self, button):
        self.send_to_for_P025 = button.text()
    
    def send_to_selected_for_P021(self, button):
        self.send_to_for_P021 = button.text()

    def fail_defect_P020_selected(self, button):
        indexBT = self.group_ration_bt_P020.buttons().index(button) + 1
        if len(str(indexBT)) == 1:
            self.defectCode_P020 = f'0000{str(indexBT)}'
        elif len(str(indexBT)) == 2:
            self.defectCode_P020 = f'000{str(indexBT)}'

    def fail_defect_P021_selected(self, button):
        indexBT = self.group_ration_bt_P020.buttons().index(button) + 1
        if len(str(indexBT)) == 1:
            self.defectCode_P020 = f'0000{str(indexBT)}'
        elif len(str(indexBT)) == 2:
            self.defectCode_P020 = f'000{str(indexBT)}'

    def changeColor_P020(self):
        if self.bt_result_P020.text() == 'PASS':
            self.bt_result_P020.setText('FAIL')
            self.bt_result_P020.setStyleSheet('background-color: red; color: white')
        else:
            self.bt_result_P020.setText('PASS')

            self.bt_result_P020.setStyleSheet('background-color: #36FF00; color: black')
    def changeColor_P021(self):
        if self.bt_result_P021.text() == 'PASS':
            self.bt_result_P021.setText('FAIL')
            self.bt_result_P021.setStyleSheet('background-color: red; color: white')
        else:
            self.bt_result_P021.setText('PASS')
            self.bt_result_P021.setStyleSheet('background-color: #36FF00; color: black')

    def keys_FITs_P020(self):           
        try:
            if self.EN_Text_P020.text() != '':
                if self.SN_Text_P020.text() != '':
                    if self.button_on_camera_P020.isChecked():
                        if os.path.exists('captured_image_1.png'): 
                            if self.bt_result_P020.text() == 'PASS':
                                self.defectCode_P020 = ''

                            objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")
                            FITs_Init = objFITS.fn_InitDB('*', 'P020', '1', 'dbAcacia') 
                            FITs_Log_Check_In = ''    
                            if FITs_Init == 'True':
                                dst_path_1 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P020\\{self.SN_Text_P020.text()} (1).png'
                                dst_path_2 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P020\\{self.SN_Text_P020.text()} (2).png'
                                dst_path_3 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P020\\{self.SN_Text_P020.text()} (3).png'
                                if not os.path.exists(f'{self.SN_Text_P020.text()} (1).png'):
                                    if os.path.exists('captured_image_1.png'):
                                        os.rename('captured_image_1.png', f'{self.SN_Text_P020.text()} (1).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P020.text()} (1).png', dst_path_1)

                                if not os.path.exists(f'{self.SN_Text_P020.text()} (2).png'):
                                    if os.path.exists('captured_image_2.png'):
                                        os.rename('captured_image_2.png', f'{self.SN_Text_P020.text()} (2).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P020.text()} (2).png', dst_path_2)
                                    else:
                                        dst_path_2 = ''

                                if not os.path.exists(f'{self.SN_Text_P020.text()} (3).png'):
                                    if os.path.exists('captured_image_3.png'):
                                        os.rename('captured_image_3.png', f'{self.SN_Text_P020.text()} (3).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P020.text()} (3).png', dst_path_3)
                                    else:
                                        dst_path_3 = ''

                                time.sleep(0.2)
                                parameter = 'EN,PCBA Serial Number,Final VMI Result,Defect,Remark,Attach File #1,Attach File #2,Attach File #3'
                                value = f"{self.EN_Text_P020.text()},{self.SN_Text_P020.text()},{self.bt_result_P020.text()},{self.defectCode_P020},N/A,{dst_path_1},{dst_path_2},{dst_path_3}"
                                FITs_Log_Check_In = objFITS.fn_Log('*', 'P020', '1', parameter, value, ',')

                            objFITS.closeDB()  
                            for button in self.group_ration_bt_P020.buttons():
                                if button.isChecked() == True:                
                                    button.setChecked(False)

                            if FITs_Log_Check_In == 'True':
                                self.SN_Text_P020.setText('')
                                
                            else:
                                msg_box = MessageBox(self)
                                msg_box.setIcon(QMessageBox.Critical) 
                                msg_box.setWindowTitle('Failed')
                                msg_box.setText(f"{FITs_Log_Check_In}")
                                msg_box.exec_()
                                self.SN_Text_P020.setText('')
                        else:
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Information) 
                            msg_box.setWindowTitle('Reminder')
                            msg_box.setText('Please take a picture!')
                            msg_box.exec_() 
                    else:
                        if self.bt_result_P020.text() == 'PASS':
                            self.defectCode_P020 = ''

                        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")
                        FITs_Init = objFITS.fn_InitDB('*', 'P020', '1', 'dbAcacia') 
                        FITs_Log_Check_In = ''    
                        if FITs_Init == 'True':

                            time.sleep(0.2)
                            parameter = 'EN,PCBA Serial Number,Final VMI Result,Defect,Remark,Attach File #1,Attach File #2,Attach File #3'
                            value = f"{self.EN_Text_P020.text()},{self.SN_Text_P020.text()},{self.bt_result_P020.text()},{self.defectCode_P020},N/A,'','',''"
                            FITs_Log_Check_In = objFITS.fn_Log('*', 'P020', '1', parameter, value, ',')

                        objFITS.closeDB()  
                        for button in self.group_ration_bt_P020.buttons():
                            if button.isChecked() == True:                
                                button.setChecked(False)

                        if FITs_Log_Check_In == 'True':
                            self.SN_Text_P020.setText('')
                            
                        else:
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Critical) 
                            msg_box.setWindowTitle('Failed')
                            msg_box.setText(f"{FITs_Log_Check_In}")
                            msg_box.exec_()
                            self.SN_Text_P020.setText('')
                else:
                    msg_box = MessageBox(self)
                    msg_box.setIcon(QMessageBox.Information) 
                    msg_box.setWindowTitle('Reminder')
                    msg_box.setText('Please enter SERIAL NUMBER')
                    msg_box.exec_() 
            else:
                msg_box = MessageBox(self)
                msg_box.setIcon(QMessageBox.Information) 
                msg_box.setWindowTitle('Reminder')
                msg_box.setText('Please EN')
                msg_box.exec_()
            
        except Exception as e:
            msg_box = MessageBox(self)
            msg_box.setIcon(QMessageBox.Critical) 
            msg_box.setWindowTitle('Failed')
            msg_box.setText(e)
            msg_box.exec_()
    
    def keys_FITs_P021(self):
        try:
            if self.EN_Text_P021.text() != '':
                if self.SN_Text_P021.text() != '':
                    if self.button_on_camera_P021.isChecked():
                        if os.path.exists('captured_image_1.png'): 
                            if self.bt_result_P021.text() == 'PASS':
                                self.defectCode_P021 = ''

                            objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")
                            FITs_Init = objFITS.fn_InitDB('*', 'P021', '1', 'dbAcacia') 
                            FITs_Log_Check_In = ''    
                            if FITs_Init == 'True':
                                dst_path_1 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P021\\{self.SN_Text_P021.text()} (1).png'
                                dst_path_2 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P021\\{self.SN_Text_P021.text()} (2).png'
                                dst_path_3 = f'\\\\fbn-fs-bu5\\acacia$\\ACACIA\EBT_VMI\\P021\\{self.SN_Text_P021.text()} (3).png'
                                if not os.path.exists(f'{self.SN_Text_P021.text()} (1).png'):
                                    if os.path.exists('captured_image_1.png'):
                                        os.rename('captured_image_1.png', f'{self.SN_Text_P021.text()} (1).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P021.text()} (1).png', dst_path_1)

                                if not os.path.exists(f'{self.SN_Text_P021.text()} (2).png'):
                                    if os.path.exists('captured_image_2.png'):
                                        os.rename('captured_image_2.png', f'{self.SN_Text_P021.text()} (2).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P021.text()} (2).png', dst_path_2)
                                    else:
                                        dst_path_2 = ''

                                if not os.path.exists(f'{self.SN_Text_P021.text()} (3).png'):
                                    if os.path.exists('captured_image_3.png'):
                                        os.rename('captured_image_3.png', f'{self.SN_Text_P021.text()} (3).png')
                                        time.sleep(0.2)
                                        shutil.move(f'{self.SN_Text_P021.text()} (3).png', dst_path_3)  
                                    else:
                                        dst_path_3 = ''

                                time.sleep(0.2)
                                parameter = 'EN,PCBA Serial Number,Final VMI Result,Defect,Remark,Attach File #1,Attach File #2,Attach File #3,send to'
                                value = f"{self.EN_Text_P021.text()},{self.SN_Text_P021.text()},{self.bt_result_P021.text()},{self.defectCode_P021},N/A,{dst_path_1},{dst_path_2},{dst_path_3},{self.send_to_for_P021}"
                                FITs_Log_Check_In = objFITS.fn_Log('*', 'P021', '1', parameter, value, ',')

                            objFITS.closeDB()  
                            for button in self.group_ration_bt_P021.buttons():
                                if button.isChecked() == True:                
                                    button.setChecked(False)

                            if FITs_Log_Check_In == 'True':
                                self.SN_Text_P021.setText('')
                                
                            else:
                                msg_box = MessageBox(self)
                                msg_box.setIcon(QMessageBox.Critical) 
                                msg_box.setWindowTitle('Failed')
                                msg_box.setText(f"{FITs_Log_Check_In}")
                                msg_box.exec_()
                                self.SN_Text_P021.setText('')
                        else:
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Information) 
                            msg_box.setWindowTitle('Reminder')
                            msg_box.setText('Please take a picture!')
                            msg_box.exec_() 
                    else:
                        if self.bt_result_P021.text() == 'PASS':
                            self.defectCode_P021 = ''

                        objFITS = win32.gencache.EnsureDispatch("FITSDLL.clsDB")
                        FITs_Init = objFITS.fn_InitDB('*', 'P021', '1', 'dbAcacia') 
                        FITs_Log_Check_In = ''    
                        if FITs_Init == 'True':
                            time.sleep(0.2)
                            parameter = 'EN,PCBA Serial Number,Final VMI Result,Defect,Remark,Attach File #1,Attach File #2,Attach File #3,send to'
                            value = f"{self.EN_Text_P021.text()},{self.SN_Text_P021.text()},{self.bt_result_P021.text()},{self.defectCode_P021},N/A,'','','',{self.send_to_for_P021}"
                            FITs_Log_Check_In = objFITS.fn_Log('*', 'P021', '1', parameter, value, ',')

                        objFITS.closeDB()  
                        for button in self.group_ration_bt_P021.buttons():
                            if button.isChecked() == True:                
                                button.setChecked(False)

                        if FITs_Log_Check_In == 'True':
                            self.SN_Text_P021.setText('')
                            
                        else:
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Critical) 
                            msg_box.setWindowTitle('Failed')
                            msg_box.setText(f"{FITs_Log_Check_In}")
                            msg_box.exec_()
                            self.SN_Text_P021.setText('')
                else:
                    msg_box = MessageBox(self)
                    msg_box.setIcon(QMessageBox.Information) 
                    msg_box.setWindowTitle('Reminder')
                    msg_box.setText('Please enter SERIAL NUMBER')
                    msg_box.exec_() 
            else:
                msg_box = MessageBox(self)
                msg_box.setIcon(QMessageBox.Information) 
                msg_box.setWindowTitle('Reminder')
                msg_box.setText('Please EN')
                msg_box.exec_()
            
        except Exception as e:
            msg_box = MessageBox(self)
            msg_box.setIcon(QMessageBox.Critical) 
            msg_box.setWindowTitle('Failed')
            msg_box.setText(e)
            msg_box.exec_()

    def keys_FITs_P030(self):
        try:
            if self.SN_Text_P030.text() != '' or self.EN_Text_P030.text() != '':
                if self.SN_Text_P030.text() != '':
                    if len(self.send_to_for_P030) > 0:
                        data = QueryATS().input_data(self.SN_Text_P030.text())
                        if self.send_to_for_P030 == 'P025 : MDIO EBT Screening' and data[0][14] != 'PASS':
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Critical) 
                            msg_box.setWindowTitle('Failed')
                            msg_box.setText(f"Result is {data[0][14]} not allow to send to {self.send_to_for_P030}")
                            msg_box.exec_()
                        elif self.send_to_for_P030 == 'P060 : OQA Inspection' and data[0][14] != 'PASS':
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Critical) 
                            msg_box.setWindowTitle('Failed')
                            msg_box.setText(f"Result is {data[0][14]} not allow to send to {self.send_to_for_P030}")
                            msg_box.exec_()
                        else:
                            if len(data) > 0:
                                linecard_count = QueryLineCardCount().input_detail(data[0][4])
                                if len(linecard_count) > 0:
                                    payload_check_in = CheckInFITs().input_data(data[0][1], data[0][2], data[0][0])
                                    
                                    time.sleep(0.2)
                                    payload_check_out = CheckOutFITs().input_data(
                                                                                    self.EN_Text_P030.text(), 
                                                                                    data[0][1],
                                                                                    data[0][2],
                                                                                    data[0][3],
                                                                                    data[0][4],
                                                                                    data[0][5],
                                                                                    data[0][6],
                                                                                    data[0][7],
                                                                                    data[0][8],
                                                                                    data[0][9],
                                                                                    data[0][10],
                                                                                    data[0][11],
                                                                                    data[0][12],
                                                                                    data[0][13],
                                                                                    data[0][14],
                                                                                    self.send_to_for_P030,
                                                                                    linecard_count[0][0],
                                                                                    'P030'
                                                                                )
                                    if payload_check_in == 'True' and payload_check_out == 'True':
                                        # msg_box = MessageBox(self)
                                        # msg_box.setIcon(QMessageBox.Information) 
                                        # msg_box.setWindowTitle('Passed')
                                        # msg_box.setText('Recorde data success!')
                                        # msg_box.exec_()
                                        self.SN_Text_P030.setText('')
                                    else:
                                        msg_box = MessageBox(self)
                                        msg_box.setIcon(QMessageBox.Critical) 
                                        msg_box.setWindowTitle('Failed')
                                        msg_box.setText(f"Check In = {payload_check_in} \n\nCheck Out = {payload_check_out}")
                                        msg_box.exec_()
                                        self.SN_Text_P025.setText('')
                                else:
                                    msg_box = MessageBox(self)
                                    msg_box.setIcon(QMessageBox.Information) 
                                    msg_box.setWindowTitle('Reminder')
                                    msg_box.setText('Can not found Line Card Count')
                                    msg_box.exec_()
                            else:
                                msg_box = MessageBox(self)
                                msg_box.setIcon(QMessageBox.Information) 
                                msg_box.setWindowTitle('Reminder')
                                msg_box.setText('Have no data in ATS')
                                msg_box.exec_() 
                    else:
                        msg_box = MessageBox(self)
                        msg_box.setIcon(QMessageBox.Information) 
                        msg_box.setWindowTitle('Reminder')
                        msg_box.setText('Please select [send to]')
                        msg_box.exec_() 
                else:
                    msg_box = MessageBox(self)
                    msg_box.setIcon(QMessageBox.Information) 
                    msg_box.setWindowTitle('Reminder')
                    msg_box.setText('Please enter SERIAL NUMBER')
                    msg_box.exec_() 
            else:
                msg_box = MessageBox(self)
                msg_box.setIcon(QMessageBox.Information) 
                msg_box.setWindowTitle('Reminder')
                msg_box.setText('Please enter data')
                msg_box.exec_()

        except Exception as e:
            msg_box = MessageBox(self)
            msg_box.setIcon(QMessageBox.Critical) 
            msg_box.setWindowTitle('Failed')
            msg_box.setText(e)
            msg_box.exec_()

    def keys_FITs_P025(self):
        try:
            if self.SN_Text_P025.text() != '' or self.EN_Text_P025.text() != '':
                if self.SN_Text_P025.text() != '':
                    if len(self.send_to_for_P025) > 0:
                        payload_check_out = CheckOutFITs().input_data(self.EN_Text_P025.text(), self.SN_Text_P025.text(),'','','','','','','','','','','','','',self.send_to_for_P025,'','P025')

                        if payload_check_out == 'True':
                            # msg_box = MessageBox(self)
                            # msg_box.setIcon(QMessageBox.Information) 
                            # msg_box.setWindowTitle('Passed')
                            # msg_box.setText('Recorde data success!')
                            # msg_box.exec_()
                            self.SN_Text_P025.setText('')
                        else:
                            msg_box = MessageBox(self)
                            msg_box.setIcon(QMessageBox.Critical) 
                            msg_box.setWindowTitle('Failed')
                            msg_box.setText(f"Check Out = {payload_check_out}")
                            msg_box.exec_()
                            self.SN_Text_P025.setText('')
                    else:
                        msg_box = MessageBox(self)
                        msg_box.setIcon(QMessageBox.Information) 
                        msg_box.setWindowTitle('Reminder')
                        msg_box.setText('Please select [send to]')
                        msg_box.exec_() 
                else:
                    msg_box = MessageBox(self)
                    msg_box.setIcon(QMessageBox.Information) 
                    msg_box.setWindowTitle('Reminder')
                    msg_box.setText('Please enter SERIAL NUMBER')
                    msg_box.exec_() 
            else:
                msg_box = MessageBox(self)
                msg_box.setIcon(QMessageBox.Information) 
                msg_box.setWindowTitle('Reminder')
                msg_box.setText('Please enter data')
                msg_box.exec_() 

        except Exception as e:
            msg_box = MessageBox(self)
            msg_box.setIcon(QMessageBox.Critical) 
            msg_box.setWindowTitle('Failed')
            msg_box.setText(e)
            msg_box.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = Main_UI()
    gui.show()
    app.exec_()