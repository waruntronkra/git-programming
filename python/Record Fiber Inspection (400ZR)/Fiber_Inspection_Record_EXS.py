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
            self.setWindowTitle('Record Fiber Inspection (EXP) V3.8')

            note_1 = QLabel("! หมายเหตุ !", self)
            note_1.setStyleSheet('color : red; font-size : 17px; font-weight : bold')
            note_1.move(10,60)

            note_2 = QLabel("กรณี Enaface งานแล้วต้องการคีย์ FAIL ให้ทำการ Check in แบบ Manual แทน", self)
            note_2.setStyleSheet('color : black; font-size : 15px; font-weight : bold')
            note_2.setGeometry(120,67,550,20)

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
                     
            font = QFont()
            font.setBold(True)
            self.button = QPushButton(icon_save, "   บันทึก", self)
            self.button.setGeometry(900, 65, 120, 50)
            self.button.setFont(font)
            self.button.clicked.connect(self.window_BT_option)

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
            proces_arr = ['EndFace EXP', "EXP"]
            for i in proces_arr:
                self.process.addItem(i)
            self.process.currentIndexChanged.connect(self.process_change)
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

            self.path_box.setText("\\\\fbn-fs-bu5\\acacia$\\Test\\LoopBack Record")

            self.Dict_Data = {}

            self.file_type_selected = '.pdf'  
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

            self.PI_Location_Scaned.setText("BAY6.FBER.01.A")

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

    def process_change(self):
        if self.process.currentText() == "EndFace EXP":
            for idx, (x, y) in enumerate(zip(self.Array_UUT_BOX, self.Array_LoopBack_SN_Box)):
                y.setReadOnly(False)
                if idx != 59:
                    y.textChanged.connect(lambda text, widget_in = self.Array_UUT_BOX[idx]: self.text_LoopBack_change(text, widget_in)) 
                    x.textChanged.connect(lambda text, widget_in = self.Array_LoopBack_SN_Box[idx + 1]: self.text_UUT_change(text, widget_in)) 
                elif idx == 59:
                    y.textChanged.connect(lambda text, widget_in = self.Array_UUT_BOX[idx]: self.text_LoopBack_change(text, widget_in))
        elif self.process.currentText() == "EXP":
            for idx, (x, y) in enumerate(zip(self.Array_UUT_BOX, self.Array_LoopBack_SN_Box)):
                y.setReadOnly(False)
                if idx != 59:
                    x.textChanged.connect(lambda text, widget_in = self.Array_UUT_BOX[idx + 1]: self.text_UUT_change(text, widget_in)) 

    def text_UUT_change(self, text, widget):
        if len(text) == 9:
            widget.setFocus(Qt.OtherFocusReason)
    def text_LoopBack_change(self, text, widget):
        if len(text) == 14:
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
    
    def ensure_FITs(self):
        try:
            if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':
                arr_active = [True]
                arr_LB = []
                arr_UUT = []
                duplicate_arr_LB = []
                duplicate_arr_UUT = []
                if self.process.currentText() == "EndFace EXP": # Check in only Endface
                    arr_list_files = []
                    for i in os.listdir(self.path_box.text()):
                        arr_list_files.append(i)

                    for j in self.Array_LoopBack_SN_Box:
                        if j.text() != '':
                            arr_LB.append(j.text() + self.file_type_selected)
                    
                    for uut in self.Array_UUT_BOX:
                        if uut.text() != '':
                            arr_UUT.append(uut.text())
                    
                    msg_alert = ''               
                    for k in arr_LB:
                        if k not in arr_list_files: 
                            msg_alert += f"LoopBack SN [{k}] ไม่อยู่ใน folder ที่เก็บไฟล์กล้อง กรุณาส่องใหม่\n"
                            arr_active.append(False)
                        elif k in arr_list_files:
                            arr_active.append(True)

                    duplicate_arr_LB = list(set(arr_LB))          
                    duplicate_arr_UUT = list(set(arr_UUT))        
                
                if False not in arr_active:
                    if len(arr_LB) == len(duplicate_arr_LB):
                        if len(arr_UUT) == len(duplicate_arr_UUT):
                            self.frame_box.setVisible(False)
                            self.click_option_1.setVisible(False)
                            self.click_option_2.setVisible(False)
                            self.close_BT.setVisible(False)               
                                                
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
                                    if self.process.currentText() == "EndFace EXP":
                                        self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), "EndFace EXP")))
                                    elif self.process.currentText() == "EXP":
                                        self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), "EXP")))

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
                            QMessageBox.information(self, "Error", "ตรวจพบ SN งาน ซ้ำ")
                    else:
                        QMessageBox.information(self, "Error", "ตรวจพบ สาย ซ้ำ")  
                else:
                    QMessageBox.information(self, "Error", msg_alert)  
            else:
                QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน")  

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def submit_FITs(self):
        try:
            Check_In_FITs_EXS = CheckInFITsEXS()
            Query_FITs = QueryFITs()
            self.progress_bar.setVisible(True)
            
            LoopBack = []
            if self.process.currentText() == "EndFace EXP":
                for i in self.Array_LoopBack_SN_Box:
                    if i.text() != '':
                        LoopBack.append(i.text())
            elif self.process.currentText() == "EXP":  
                for x in self.Array_UUT_BOX: 
                    if x.text() != '':
                        Queried_FITs = Query_FITs.input_data(str(x.text()), 'EndFace EXP', False)    
                        LoopBack.append(Queried_FITs[1])

            self.progress_bar.setMaximum(len(self.output))

            Check_In_Arr = []
            out = ''
            SN_Arr = []       
            for index, i in enumerate(self.output):
                if self.check_in_FITs_way == "1" and self.process.currentText() == "EndFace EXP":
                    out = Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EndFace EXP")
                    self.progress_bar.setValue(int(index + 1))
                    Check_In_Arr.append(out)
                    SN_Arr.append(i[0])
                elif self.check_in_FITs_way == "2" and self.process.currentText() == "EndFace EXP":
                    out = Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EndFace EXP")
                    time.sleep(0.1)
                    Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EXP")                   
                    self.progress_bar.setValue(int(index + 1))  
                    Check_In_Arr.append(out)  
                    SN_Arr.append(i[0])
                elif self.process.currentText() == "EXP":      
                    out = Check_In_FITs_EXS.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), LoopBack[index].replace(self.file_type_selected,''), self.PI_Location_Scaned.text(), '', 'PASS', 'NO',f'\\\\fabrinet\\files\\Acacia\\Test\\Endface inspect EXP\\{str(i[0]) + self.file_type_selected}','',self.file_type_selected, "EXP")                     
                    self.progress_bar.setValue(int(index + 1))     
                    Check_In_Arr.append(out)
                    SN_Arr.append(i[0])

            CheckIn_OK = []
            for i in Check_In_Arr:
                CheckIn_OK.append(i.split("|")[0])
            CheckIn_OK = list(set(CheckIn_OK))

            if len(CheckIn_OK) == 1 and CheckIn_OK[0] == 'True':
                if self.check_in_FITs_way == "1" and self.process.currentText() == "EndFace EXP":
                    self.save_file()
                else:
                    # Reset Value
                    for i in range(60):
                        self.Array_LoopBack_SN_Box[i].setText('')
                        self.Array_UUT_BOX[i].setText('')
            else:
                msg_check_in = ''
                for i,j in zip(SN_Arr, Check_In_Arr):
                    msg_check_in += f"[{i}] : {j}\n"
                QMessageBox.information(self,"Error",f"บันทึกไม่สำเร็จ!\n\n{msg_check_in}")                  
          
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def refresh_FITs(self):
        try:
            HandShake_FITs_EXS = HandShakeFITsEXS()
            self.output = []
            for i in self.Array_UUT_BOX:
                if i.text() != '':
                    if self.process.currentText() == "EndFace EXP":
                        self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), "EndFace EXP")))
                    elif self.process.currentText() == "EXP":
                        self.output.append((str(i.text()), HandShake_FITs_EXS.input_data(str(i.text()), "EXP")))

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

    def save_file(self):
        try:
            date_today = datetime.now()
            month = date_today.strftime("%b")
            month_upper = month.upper()
            year = date_today.strftime("'%y")

            Full_Date = date_today.strftime(f"%d {month_upper} %Y")
    
            path_for_throw = f"\\\\fbn-fs-bu5\\acacia$\\Test\\Endface inspect Loopback\\{month_upper + year}\\{Full_Date}" # Path for throw LoopBack files
            if not os.path.exists(path_for_throw): # Check folder SN exists or not
                os.makedirs(path_for_throw)

            SN_Enter = []
            for i in self.Array_UUT_BOX:
                if i.text() != '':
                    SN_Enter.append(i.text())    

            LoopBack_SN_Enter = []
            for j in self.Array_LoopBack_SN_Box:
                if j.text() != '':
                    LoopBack_SN_Enter.append(j.text())                        
            
            for UUT_SN, LB_SN in zip(SN_Enter, LoopBack_SN_Enter):                                                    
                if os.path.exists(path_for_throw + "\\" + LB_SN + self.file_type_selected):  # Check file exists or not
                    os.remove(path_for_throw + "\\" + LB_SN + self.file_type_selected) # If exists, remove it
                shutil.copy(self.path_box.text() + "\\" + LB_SN + self.file_type_selected, path_for_throw)   

                dst = "\\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\EXP"                           
                folder_path_FBN_created = os.path.join(dst, UUT_SN) # Join path for create folder SN
                
                if not os.path.exists(folder_path_FBN_created): # Check folder SN exists or not
                    os.makedirs(folder_path_FBN_created) # If not exists, create it

                if os.path.exists(folder_path_FBN_created + "\\" + LB_SN + self.file_type_selected):
                    os.remove(folder_path_FBN_created + "\\" + LB_SN + self.file_type_selected) 
                shutil.copy(self.path_box.text() + "\\" + LB_SN + self.file_type_selected, folder_path_FBN_created)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()