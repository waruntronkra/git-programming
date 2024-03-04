from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QAction, QFrame, QMenu, QLabel, QLineEdit, QToolTip, QVBoxLayout, QComboBox, QMessageBox, QFileDialog, QFrame, QTableWidget, QDialog, QProgressBar, QRadioButton
import os
from datetime import datetime
import shutil
import sys
import glob
from Create_Slot_EXS import CreateSlotEXS
from Check_In_FITs_EXS import CheckInFITsEXS
from HandShake_FITs_EXS import HandShakeFITsEXS
from Query_FITs import QueryFITs
from Check_Out_FITs import CheckOutFITs
from Query_Last_Result_Test import QueryLastResultTest
from Connect_WinSCP import ConnectWinSCP_GET
import time
import netifaces

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle('Record Fiber Inspection (EXP) V2.0')

            font_BT = QFont()
            font_BT.setBold(True)

            this_file_path = os.path.abspath(sys.argv[0])
            self.this_file_path = os.path.dirname(this_file_path)

            icon_path_browse = "temp\\icon\\browse.ico"
            icon_browse = QIcon(icon_path_browse)
            icon_path_save = "temp\\icon\\save.ico"
            icon_save = QIcon(icon_path_save)
            icon_path_window = "temp\\icon\\ui.ico"
            icon_window = QIcon(icon_path_window)
            icon_path_read = "temp\\icon\\read.ico"
            icon_read = QIcon(icon_path_read)
            icon_path_fits = "temp\\icon\\FITs.jpg"
            icon_fits = QIcon(icon_path_fits)

            self.Main_Layout = QtWidgets.QVBoxLayout()
            self.setWindowIcon(icon_window)

            label_file_type = QLabel('เลือกประเภทไฟล์จากการส่องกล้อง', self)
            label_file_type.setGeometry(900,5,170,20)
            self.file_type_pdf = QRadioButton('PDF',self)
            self.file_type_pdf.setChecked(True)
            self.file_type_pdf.move(900,17)
            self.file_type_html= QRadioButton('HTML',self)
            self.file_type_html.move(950,17)

            self.file_type_pdf.clicked.connect(lambda : self.file_type_check('.pdf'))
            self.file_type_html.clicked.connect(lambda : self.file_type_check('.html'))

            self.button_browse = QPushButton(icon_browse, "  เลือกโฟรเดอร์ที่เก็บไฟล์จากการส่องกล้อง", self)
            self.button_browse.setGeometry(10, 5, 230, 30)
            self.button_browse.clicked.connect(self.Browse_Path)

            self.path_box = QLineEdit('', self)
            self.path_box.setGeometry(245, 10, 460, 20)
            self.path_box.setReadOnly(True)

            self.button_store = QPushButton(icon_browse, "  เลือกโฟรเดอร์ที่จะเก็บบันทึก", self)
            self.button_store.setGeometry(10, 40, 230, 30)
            self.button_store.clicked.connect(self.Store_Path)

            self.path_box_store = QLineEdit('', self)
            self.path_box_store.setGeometry(245, 45, 460, 20)
            self.path_box_store.setReadOnly(True)
                     
            font = QFont()
            font.setBold(True)
            self.button = QPushButton(icon_save, "   บันทึก", self)
            self.button.setGeometry(900, 65, 120, 50)
            self.button.setFont(font)
            self.button.clicked.connect(self.window_BT_option)

            BT_Mapping = QPushButton(icon_read, " อ่านข้อมูล", self)
            icon_read_size = QSize(25,20)
            BT_Mapping.setIconSize(icon_read_size)
            BT_Mapping.setGeometry(10, 85, 696, 30)
            BT_Mapping.clicked.connect(self.getData)

            # Detail to Save FITs
            frame = QFrame(self)
            frame.setGeometry(710, 10, 180, 105)
            frame.setStyleSheet("background-color: #5CFF5D;")
            frame.setFrameShape(QFrame.Box)

            PI_Location_Label = QLabel("PI Location", self)
            PI_Location_Label.setGeometry(720, 64, 100, 20)
            self.PI_Location_Scaned = QLineEdit(self)
            self.PI_Location_Scaned.setAlignment(Qt.AlignCenter)
            self.PI_Location_Scaned.setGeometry(780, 65, 100, 20)

            EN_Label = QLabel("EN", self)
            EN_Label.setGeometry(760, 39, 100, 20)
            self.EN_Scaned = QLineEdit(self)
            self.EN_Scaned.setAlignment(Qt.AlignCenter)
            self.EN_Scaned.setGeometry(780, 40, 50, 20)
            self.EN_Scaned.textChanged.connect(lambda text, widget_in = self.PI_Location_Scaned: self.text_EN_change(text, widget_in))

            STATION_Scaned_Label = QLabel("STATION ID", self)
            STATION_Scaned_Label.setGeometry(720, 14, 100, 20)
            self.STATION_Scaned = QLineEdit(self)
            self.STATION_Scaned.setText('-')
            self.STATION_Scaned.setAlignment(Qt.AlignCenter)
            self.STATION_Scaned.textChanged.connect(lambda text, widget_in = self.EN_Scaned: self.text_STATION_change(text, widget_in))
            self.STATION_Scaned.setGeometry(780, 15, 100, 20)   

            self.process = QComboBox(self)
            proces_arr = ['EndFace EXP']
            for i in proces_arr:
                self.process.addItem(i)
            self.process.setGeometry(780,90,85,20)

            Create_Slot_EXS = CreateSlotEXS()
            
            x_move = 10
            y_move = 120
            self.Array_UUT_BOX = []
            self.Array_LoopBack_SN_Box = []
            for i in range(60):
                if i == 12 :
                    x_move = 10
                    y_move += 60
                elif i == 24 :
                    x_move = 10
                    y_move += 60
                elif i == 36 :
                    x_move = 10
                    y_move += 60
                elif i == 48 :
                    x_move = 10
                    y_move += 60
                elif i == 60 :
                    x_move = 10
                    y_move += 60

                var = Create_Slot_EXS.input_data(self, x_move, y_move)
                self.Array_UUT_BOX.append(var[0])
                self.Array_LoopBack_SN_Box.append(var[1])
                x_move += 140          
            
            for idx, (x, y) in enumerate(zip(self.Array_UUT_BOX, self.Array_LoopBack_SN_Box)):
                if idx != 59:
                    y.textChanged.connect(lambda text, widget_in = self.Array_UUT_BOX[idx]: self.text_LoopBack_change(text, widget_in)) 
                    x.textChanged.connect(lambda text, widget_in = self.Array_LoopBack_SN_Box[idx + 1]: self.text_UUT_change(text, widget_in)) 
                elif idx == 59:
                    y.textChanged.connect(lambda text, widget_in = self.Array_UUT_BOX[idx]: self.text_LoopBack_change(text, widget_in)) 

            with open('setting/Path Files Location.txt', 'r') as f:
                file_read_1 = f.read()       
            file_read_1 = file_read_1.replace("\\", '/')
            self.path_box.setText(file_read_1)

            with open('setting/Path for Store.txt', 'r') as f:
                file_read_2 = f.read()
            file_read_2 = file_read_2.replace("\\", '/')
            self.path_box_store.setText(file_read_2)

            self.Dict_Data = {}

            self.file_type_selected = '.pdf'

            self.q_1 = QPushButton("งานรอ Check in EXP กลุ่มที่ 1", self)
            self.q_1.clicked.connect(lambda : self.get_wait_file("1", self.q_1))
            self.q_1.setGeometry(1129,10,150,30)

            self.q_2 = QPushButton("งานรอ Check in EXP กลุ่มที่ 2", self)
            self.q_2.clicked.connect(lambda : self.get_wait_file("2", self.q_2))
            self.q_2.setGeometry(1129,45,150,30)

            self.q_3 = QPushButton("งานรอ Check in EXP กลุ่มที่ 3", self)
            self.q_3.clicked.connect(lambda : self.get_wait_file("3", self.q_3))
            self.q_3.setGeometry(1129,80,150,30)

            self.q_4 = QPushButton("งานรอ Check in EXP กลุ่มที่ 4", self)
            self.q_4.clicked.connect(lambda : self.get_wait_file("4", self.q_4))
            self.q_4.setGeometry(1289,10,150,30)

            self.q_5 = QPushButton("งานรอ Check in EXP กลุ่มที่ 5", self)
            self.q_5.clicked.connect(lambda : self.get_wait_file("5", self.q_5))
            self.q_5.setGeometry(1289,45,150,30)

            self.q_6 = QPushButton("งานรอ Check in EXP กลุ่มที่ 6", self)
            self.q_6.clicked.connect(lambda : self.get_wait_file("6", self.q_6))
            self.q_6.setGeometry(1289,80,150,30)

            self.q_7 = QPushButton("งานรอ Check in EXP กลุ่มที่ 8", self)
            self.q_7.clicked.connect(lambda : self.get_wait_file("8", self.q_7))
            self.q_7.setGeometry(1449,10,150,30)

            self.q_8 = QPushButton("งานรอ Check in EXP กลุ่มที่ 8", self)
            self.q_8.clicked.connect(lambda : self.get_wait_file("8", self.q_8))
            self.q_8.setGeometry(1449,45,150,30)

            self.q_9 = QPushButton("งานรอ Check in EXP กลุ่มที่ 9", self)
            self.q_9.clicked.connect(lambda : self.get_wait_file("9", self.q_9))
            self.q_9.setGeometry(1449,80,150,30)

            self.array_q = [self.q_1, self.q_2, self.q_3, self.q_4, self.q_5, self.q_6, self.q_7, self.q_8, self.q_9]

            for i in range(9):
                self.array_q[i].setVisible(False)

            for i, txt in enumerate(os.listdir("temp\\log")):
                txt_name = txt.split("_")[1].split(".")[0]
                self.array_q[i].setText(f"งานรอ Check in EXP กลุ่มที่ {str(txt_name)}")
                self.array_q[i].setVisible(True)
            
            self.check_in_FITs_way = "1"       

            self.frame_box = QFrame(self)
            self.frame_box.setStyleSheet("background-color: #FFE7EB;")
            self.frame_box.setFrameShape(QFrame.Box)
            self.frame_box.setGeometry(785,40,350,95)
            self.frame_box.setVisible(False)

            self.click_option_1 = QPushButton("Check-in แค่ EndFace EXP กรณีงานรอเข้าเทส EXP", self)
            self.click_option_1.setFont(font_BT)  
            self.click_option_1.setStyleSheet("background-color: #7182FF;")    
            self.click_option_1.setGeometry(825,55,270,30)
            self.click_option_1.clicked.connect(self.select_option_1)
            self.click_option_1.setVisible(False)

            self.click_option_2 = QPushButton("Check-in ทั้ง EndFace EXP และ EXP กรณีงานเทส EXP ได้เลย", self)           
            self.click_option_2.setFont(font_BT)              
            self.click_option_2.setStyleSheet("background-color: #FFC100;")           
            self.click_option_2.setGeometry(800,90,320,30)
            self.click_option_2.clicked.connect(self.select_option_2)
            self.click_option_2.setVisible(False)   

            self.close_BT = QPushButton("X", self)           
            self.close_BT.setStyleSheet("background-color: red;")  
            self.close_BT.setGeometry(1110,45,20,20)
            self.close_BT.clicked.connect(self.close_option)
            self.close_BT.setVisible(False)

            self.group_name_no = "0"

            self.setGeometry(50, 50, 0, 0) 
            self.setFixedSize(1695, 420)

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def file_type_check(self, file_type):
        self.file_type_selected = file_type
    
    def Browse_Path(self):
        self.path_name_file_located = QFileDialog.getExistingDirectory(self, "Select Directory")     

        if self.path_name_file_located != '':
            self.path_box.setText(self.path_name_file_located)
            with open('setting\\Path Files Location.txt', 'w') as f:
                f.write(self.path_name_file_located)

    def Store_Path(self):
        self.path_name_file_located_store = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if self.path_name_file_located_store != '':
            self.path_box_store.setText(self.path_name_file_located_store)
            with open('setting\\Path for Store.txt', 'w') as f:
                f.write(self.path_name_file_located_store)

    def text_UUT_change(self, text, widget):
        if len(text) == 9:
            widget.setFocus(Qt.OtherFocusReason)
    def text_LoopBack_change(self, text, widget):
        if len(text) == 6:
            widget.setFocus(Qt.OtherFocusReason)

    def text_STATION_change(self, text, widget):
        if len(text) == 13:
            widget.setFocus(Qt.OtherFocusReason)
    def text_EN_change(self, text, widget):
        if len(text) == 6:
            widget.setFocus(Qt.OtherFocusReason)

    def window_BT_option(self):
        if self.process.currentText() == "EndFace EXP":
            self.frame_box.setVisible(True)
            self.click_option_1.setVisible(True)
            self.click_option_2.setVisible(True)
            self.close_BT.setVisible(True)
        else:
            self.ensure_FITs()
        
    def select_option_1(self):
        self.check_in_FITs_way = "1"     
        self.ensure_FITs()
        
    def select_option_2(self):
        self.check_in_FITs_way = "2"
        self.ensure_FITs()       

    def close_option(self):
        self.frame_box.setVisible(False)
        self.click_option_1.setVisible(False)
        self.click_option_2.setVisible(False)
        self.close_BT.setVisible(False)
    
    def save_to_log_temp(self):
        try:
            msg_log = ''
            for x,y in zip(self.Array_UUT_BOX, self.Array_LoopBack_SN_Box):
                if x.text() != '' and y.text() != '':
                    msg_log += str(x.text()) + " " + str(y.text()) + "\n"
            
            if len(msg_log) != 0:
                list_log_folder = os.listdir("temp\\log")   

                if len(list_log_folder) > 0:
                    max_arr = []
                    for i in list_log_folder:
                        max_arr.append(i.split("_")[1].split(".")[0])

                    with open(f"temp\\log\\group_{str(int(max(max_arr)) + 1)}.txt",'w') as f:
                        f.write(msg_log)
                elif len(list_log_folder) < 1:
                    with open('temp/log/group_1.txt','w') as f:
                        f.write(msg_log)
                return True
            else:
                QMessageBox.information(self,"Error","กรุณากรอก SN")
                return False

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")               

    def get_wait_file(self, group_name, widget_in):
        try:
            if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':
                num_wid = str(widget_in.text().split(" ")[5])
                if os.path.exists(f"temp/log/group_{num_wid}.txt"):
                    with open(f"temp/log/group_{num_wid}.txt", 'r') as f:
                        self.file_read = f.read()
                self.group_name_no = num_wid
                
                self.frame_box.setVisible(False)
                self.click_option_1.setVisible(False)
                self.click_option_2.setVisible(False)
                self.close_BT.setVisible(False)

                self.check_in_FITs_way = "3"

                for i in range(9):
                    self.array_q[i].setVisible(False)

                for i, txt in enumerate(os.listdir("temp\\log")):
                    txt_name = txt.split("_")[1].split(".")[0]
                    self.array_q[i].setText(f"งานรอ Check in EXP กลุ่มที่ {str(txt_name)}")
                    self.array_q[i].setVisible(True)
                            
                dialog = QDialog(self)

                self.progress_bar = QProgressBar(dialog)
                self.progress_bar.setMinimum(0)
                self.progress_bar.setValue(0)
                self.progress_bar.setGeometry(120,11,450,28)
                self.progress_bar.setVisible(False)

                self.table_FITs = QTableWidget(dialog)
                self.table_FITs.setGeometry(10, 45, 552, 381)

                icon_path_refresh = "temp\\icon\\refresh.ico"
                icon_refresh = QIcon(icon_path_refresh) 
                refresh_BT = QPushButton(icon_refresh, ' Refresh', dialog)
                icon_refresh_size = QSize(25,20)
                refresh_BT.setIconSize(icon_refresh_size)
                refresh_BT.clicked.connect(self.refresh_FITs)
                refresh_BT.setGeometry(10, 10, 102, 30)

                icon_path_submit = "temp\\icon\\submit.ico"
                icon_submit = QIcon(icon_path_submit)
                button = QPushButton(icon_submit, ' ยืนยัน', dialog)
                icon_submit_size = QSize(25,20)
                button.setIconSize(icon_submit_size)
                button.clicked.connect(self.submit_FITs)
                button.clicked.connect(lambda: dialog.close())
                button.setGeometry(10, 430, 552, 30)

                arr_read_txt = []
                split_file_read = self.file_read.split('\n')
                for i in split_file_read:
                    arr_read_txt.append(i.split(" "))

                HandShake_FITs_EXS = HandShakeFITsEXS()
                self.output = []
                for i in arr_read_txt:
                    if i[0] != '':
                        self.output.append((str(i[0]), HandShake_FITs_EXS.input_data(str(i[0]), "EXP")))
                
                self.LoopBack_in_txt = []
                if self.check_in_FITs_way == "3":
                    for i in arr_read_txt:
                        if i[0] != '':
                            self.LoopBack_in_txt.append(i[1])

                self.table_FITs.setColumnCount(2)
                self.table_FITs.setRowCount(len(self.output))
                self.table_FITs.setHorizontalHeaderLabels(["Serial Number", "Description"])
                for i, row in enumerate(self.output):
                    for j, col in enumerate(row):
                        table_item = QtWidgets.QTableWidgetItem(str(col))
                        self.table_FITs.setItem(i, j, table_item)
                        if j == 1:
                            if col == 'True':
                                table_item.setBackground(QtGui.QColor(0,255,0))
                            else:
                                table_item.setBackground(QtGui.QColor(255,0,0))

                self.table_FITs.setColumnWidth(1, 450)
                self.table_FITs.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #96CE84}")
                self.table_FITs.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
                self.table_FITs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.table_FITs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.table_FITs.verticalHeader().setVisible(False)

                dialog.show()
                dialog.setGeometry(650, 300, 0, 0)
                dialog.setFixedSize(572, 465)
            else:
                QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน") 

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
                
    def ensure_FITs(self):
        try:
            if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':  
                self.frame_box.setVisible(False)
                self.click_option_1.setVisible(False)
                self.click_option_2.setVisible(False)
                self.close_BT.setVisible(False)
                
                CHECK = self.getData()

                if CHECK == True:               
                    for i in range(9):
                        self.array_q[i].setVisible(False)

                    for i, txt in enumerate(os.listdir("temp\\log")):
                        txt_name = txt.split("_")[1].split(".")[0]
                        self.array_q[i].setText(f"งานรอ Check in EXP กลุ่มที่ {str(txt_name)}")
                        self.array_q[i].setVisible(True)
                                        
                    dialog = QDialog(self)

                    self.progress_bar = QProgressBar(dialog)
                    self.progress_bar.setMinimum(0)
                    self.progress_bar.setValue(0)
                    self.progress_bar.setGeometry(120,11,450,28)
                    self.progress_bar.setVisible(False)

                    self.table_FITs = QTableWidget(dialog)
                    self.table_FITs.setGeometry(10, 45, 552, 381)

                    icon_path_refresh = "temp\\icon\\refresh.ico"
                    icon_refresh = QIcon(icon_path_refresh) 
                    refresh_BT = QPushButton(icon_refresh, ' Refresh', dialog)
                    icon_refresh_size = QSize(25,20)
                    refresh_BT.setIconSize(icon_refresh_size)
                    refresh_BT.clicked.connect(self.refresh_FITs)
                    refresh_BT.setGeometry(10, 10, 102, 30)

                    icon_path_submit = "temp\\icon\\submit.ico"
                    icon_submit = QIcon(icon_path_submit)
                    button = QPushButton(icon_submit, ' ยืนยัน', dialog)
                    icon_submit_size = QSize(25,20)
                    button.setIconSize(icon_submit_size)
                    button.clicked.connect(self.submit_FITs)
                    button.clicked.connect(lambda: dialog.close())
                    button.setGeometry(10, 430, 552, 30)

                    HandShake_FITs_EXS = HandShakeFITsEXS()
                    self.output = []
                    for i in self.Array_UUT_BOX:
                        if i.text() != '':
                            self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), self.process.currentText())))

                    self.table_FITs.setColumnCount(2)
                    self.table_FITs.setRowCount(len(self.output))
                    self.table_FITs.setHorizontalHeaderLabels(["Serial Number", "Description"])
                    for i, row in enumerate(self.output):
                        for j, col in enumerate(row):
                            table_item = QtWidgets.QTableWidgetItem(str(col))
                            self.table_FITs.setItem(i, j, table_item)
                            if j == 1:
                                if col == 'True':
                                    table_item.setBackground(QtGui.QColor(0,255,0))
                                else:
                                    table_item.setBackground(QtGui.QColor(255,0,0))

                    self.table_FITs.setColumnWidth(1, 450)
                    self.table_FITs.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #96CE84}")
                    self.table_FITs.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
                    self.table_FITs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                    self.table_FITs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                    self.table_FITs.verticalHeader().setVisible(False)

                    dialog.show()
                    dialog.setGeometry(650, 300, 0, 0)
                    dialog.setFixedSize(572, 465)
            else:
                QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน")  

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def submit_FITs(self):
        try:
            if self.check_in_FITs_way == "1" and self.process.currentText() == "EndFace EXP":
                self.save_to_log_temp()
            for i in range(9):
                self.array_q[i].setVisible(False)

            for i, txt in enumerate(os.listdir("temp\\log")):
                txt_name = txt.split("_")[1].split(".")[0]
                self.array_q[i].setText(f"งานรอ Check in EXP กลุ่มที่ {str(txt_name)}")
                self.array_q[i].setVisible(True)

            Check_In_FITs_EXS = CheckInFITsEXS()
            self.progress_bar.setVisible(True)
            
            if self.check_in_FITs_way != "3":
                LoopBack = self.LoopBack_for_FITs
            else:
                LoopBack = self.LoopBack_in_txt

            self.progress_bar.setMaximum(len(self.output))

            HandCheck_Arr = []
            for index, i in enumerate(self.output):
                HandCheck = i[1].split('|')[0]
                # HandCheck = 'True'
                if HandCheck == 'True':
                    if self.check_in_FITs_way == "1" and self.process.currentText() == "EndFace EXP":
                        Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EndFace EXP")
                        self.progress_bar.setValue(int(index + 1))
                    elif self.check_in_FITs_way == "2" and self.process.currentText() == "EndFace EXP":
                        Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EndFace EXP")
                        Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EXP")                   
                        self.progress_bar.setValue(int(index + 1))   
                    elif self.check_in_FITs_way == "3":
                        Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EXP")                    
                        self.progress_bar.setValue(int(index + 1))      
                    elif self.process.currentText() == "EXP":      
                        Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EXP")                     
                        self.progress_bar.setValue(int(index + 1))      

                HandCheck_Arr.append(HandCheck)

            if 'False' not in HandCheck_Arr:
                if self.process.currentText() == "EXP" or self.check_in_FITs_way == "3":
                    if self.check_in_FITs_way == "3":
                        self.array_q[int(self.group_name_no) - 1].setVisible(False)

                        os.remove(os.path.join("temp\\log", f"group_{self.group_name_no}.txt"))

                        for i in range(9):
                            self.array_q[i].setVisible(False)

                        for i, txt in enumerate(os.listdir("temp\\log")):
                            txt_name = txt.split("_")[1].split(".")[0]
                            self.array_q[i].setText(f"งานรอ Check in EXP กลุ่มที่ {str(txt_name)}")
                            self.array_q[i].setVisible(True)

                elif self.check_in_FITs_way != "3": 
                    self.save_file()    

                for i in range(60):
                    self.Array_LoopBack_SN_Box[i].setText('')
                    self.Array_UUT_BOX[i].setText('')
                    
            elif 'False' in HandCheck_Arr:
                QMessageBox.information(self,"Error",f"บันทึกไม่สำเร็จ!")
                # Reset Value
                for i in range(60):
                    self.Array_LoopBack_SN_Box[i].setText('')
                    self.Array_UUT_BOX[i].setText('')
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def refresh_FITs(self):
        try:
            if self.check_in_FITs_way != "3":
                HandShake_FITs_EXS = HandShakeFITsEXS()
                self.output = []
                for i in self.Array_UUT_BOX: 
                    if i.text() != '':
                        self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), self.process.currentText())))
            else:
                arr_read_txt = []
                split_file_read = self.file_read.split('\n')
                for i in split_file_read:
                    arr_read_txt.append(i.split(" "))

                HandShake_FITs_EXS = HandShakeFITsEXS()
                self.output = []
                for i in arr_read_txt:
                    if i[0] != '':
                        self.output.append((str(i[0]), HandShake_FITs_EXS.input_data(str(i[0]), self.process.currentText())))

            self.table_FITs.setColumnCount(2)
            self.table_FITs.setRowCount(len(self.output))
            self.table_FITs.setHorizontalHeaderLabels(["Serial Number", "Description"])
            for i, row in enumerate(self.output):
                for j, col in enumerate(row):
                    table_item = QtWidgets.QTableWidgetItem(str(col))
                    self.table_FITs.setItem(i, j, table_item)
                    if j == 1:
                        if col == 'True':
                            table_item.setBackground(QtGui.QColor(0,255,0))
                        else:
                            table_item.setBackground(QtGui.QColor(255,0,0))

            self.table_FITs.setColumnWidth(1, 450)
            self.table_FITs.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #96CE84}")
            self.table_FITs.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
            self.table_FITs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.table_FITs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.table_FITs.verticalHeader().setVisible(False)

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def getData(self):
        try:  
            # value_retest = self.retest_mode()
            # print(value_retest)

            if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':                 
                for filename in os.listdir('temp'):
                    if filename.endswith(self.file_type_selected):
                        file_path = os.path.join('temp', filename)
                        os.remove(file_path)
                list_data = [f for f in os.listdir(self.path_box.text()) if f.endswith(self.file_type_selected)] # Path file generated from Fiber Inspection
                list_data.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_box.text(), x)), reverse=True)
                SN_Entered = []
                for x in self.Array_UUT_BOX: # Get SN
                    if x.text() != '':
                        SN_Entered.append(x.text())

                if len(SN_Entered) != len(set(SN_Entered)):
                    QMessageBox.information(self, "Error", "มี SN งานซ้ำ") 
                    return False
                else:
                    list_data = list_data[:len(SN_Entered)]
                    list_data = list_data[::-1]
                    LoopBack_SN = list_data # Reverse   

                    if len(SN_Entered) == len(LoopBack_SN): 
                        self.Dict_Data = {}
                        index = 0
                        for i, val in enumerate(self.Array_UUT_BOX):
                            if val.text() != '':
                                self.Array_LoopBack_SN_Box[i].setText(LoopBack_SN[index].replace(self.file_type_selected, ''))
                                shutil.copy(self.path_box.text() + "/" + LoopBack_SN[index], 'temp')
                                self.Dict_Data[str(val.text())] = (LoopBack_SN[index])
                                index += 1
                            else:
                                self.Array_LoopBack_SN_Box[i].setText('')
                
                        self.UUT_SN_all = list(self.Dict_Data.keys())  
                        self.LoopBack_for_FITs = list(self.Dict_Data.values())  
                        return True
                    else:
                        QMessageBox.information(self, "Error", "จำนวน SN งาน ไม่ตรงกับจำนวนไฟล์ที่ได้จากการส่องกล้อง") 
                    return False
            else:
                QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน")    
                return False
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def save_file(self):
        try:
            date_today = datetime.now()
            month = date_today.strftime("%b")
            month_upper = month.upper()
            year = date_today.strftime("'%y")

            Full_Date = date_today.strftime(f"%d {month_upper} %Y")
    
            path_for_throw = f"\\\\fbn-fs-bu5\\acacia$\\Test\\Endface inspect Loopback\\{month_upper + year}\\{Full_Date}"
            if not os.path.exists(path_for_throw):
                os.makedirs(path_for_throw)

            now = datetime.now()
            current_date = now.strftime("%d %b %Y %H_%M_%S")
            New_Folder = os.path.join(self.path_box_store.text() , current_date)
            os.makedirs(New_Folder)

            SN_Enter = []
            for i in self.Array_UUT_BOX:
                SN_Enter.append(i.text())               
            
            for key, value in self.Dict_Data.items():   
                shutil.copy(self.path_box.text() + "/" + value, 'temp')
                Folder_SN = os.path.join(New_Folder, key) # Join path for create folder SN inside folder DateTime
                os.makedirs(Folder_SN) # \\{DateTime}\\{SN}
                        
                if os.path.exists(path_for_throw + "\\" + value):
                    os.remove(path_for_throw + "\\" + value)  
                shutil.copy('temp/' + value, path_for_throw)             

                shutil.move('temp/' + value, Folder_SN)

                dst = "\\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\EXP"                           
                folder_path_FBN_created = os.path.join(dst, key) # Join path for create folder SN

                if os.path.exists(folder_path_FBN_created):
                    shutil.rmtree(folder_path_FBN_created) 
        
                os.makedirs(folder_path_FBN_created) # \\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\EXS\\{SN}

                for file_name in os.listdir(Folder_SN):
                    source = os.path.join(Folder_SN, file_name) # \\{DateTime}\\{SN}\\{Files}                        
                    shutil.copy(source, folder_path_FBN_created)

                time.sleep(0.1)  
 
            for i, var in enumerate(self.Array_LoopBack_SN_Box + self.Array_UUT_BOX):
                var.setText('')

            QMessageBox.information(self, 'แจ้งเตือน', 'บันทึกสำเร็จ')
            self.check_in_FITs_way = "1"

            # Reset Value
            for i in range(60):
                self.Array_LoopBack_SN_Box[i].setText('')
                self.Array_UUT_BOX[i].setText('')
        
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")    

    def retest_mode(self):
        try:
            UUT_SN_Enter = []
            for i in self.Array_UUT_BOX:
                UUT_SN_Enter.append(i.text())

            Query_Last_Result_Test = QueryLastResultTest()
            Query_FITs = QueryFITs()
            index = 0
            LoopBack_SN_Retest = []
            Shim_retest = []
            slot_retest = []
            SN_retest = []
            self.SN_for_re_run = []

            # ==================== Per all codition below need to endface after there are moment of UUT every time ============================
            for index, k in enumerate(UUT_SN_Enter):
                # ************************************ Get detail EXP ************************************
                if k != '': # There are data in array
                    last_result_test_EXP = Query_Last_Result_Test.input_data(str(k), 'EXP')
                    # Case retest
                    if last_result_test_EXP != 0:
                        if last_result_test_EXP[0] != 'PASS' and last_result_test_EXP[1] == index and last_result_test_EXP[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            FITs_Out = Query_FITs.input_data(str(k), 'EXP', True) # Get TX,RX value from last check in EXP
                            LoopBack_SN_Retest.append(FITs_Out[1])
                            Shim_retest.append(FITs_Out[2])
                            if FITs_Out != 9999:
                                slot_retest.append(index)
                                SN_retest.append(str(k))

            self.SN_for_re_run = SN_retest
            return slot_retest, LoopBack_SN_Retest, SN_retest, Shim_retest

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()