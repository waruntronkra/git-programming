from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton, QAction, QFrame, QMenu, QLabel, QLineEdit, QToolTip, QVBoxLayout, QComboBox, QMessageBox, QFileDialog, QFrame, QTableWidget, QDialog, QProgressBar
import os
from datetime import datetime
import shutil
import sys
import glob
from Create_Slot import CreateSlot
from Check_In_FITs import CheckInFITs
from HandShake_FITs import HandShakeFITs
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
            self.setWindowTitle('Record Fiber Inspection V3.8')

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

            self.button_browse = QPushButton(icon_browse, "  เลือกโฟรเดอร์ที่เก็บไฟล์จากการส่องกล้อง", self)
            self.button_browse.setGeometry(10, 5, 230, 30)
            self.button_browse.clicked.connect(self.Browse_Path)

            self.path_box = QLineEdit('', self)
            self.path_box.setGeometry(245, 10, 400, 20)
            self.path_box.setReadOnly(True)

            self.button_store = QPushButton(icon_browse, "  เลือกโฟรเดอร์ที่จะเก็บบันทึก", self)
            self.button_store.setGeometry(10, 40, 230, 30)
            self.button_store.clicked.connect(self.Store_Path)

            self.path_box_store = QLineEdit('', self)
            self.path_box_store.setGeometry(245, 45, 400, 20)
            self.path_box_store.setReadOnly(True)
            
            font = QFont()
            font.setBold(True)
            self.button = QPushButton(icon_save, "   บันทึก", self)
            self.button.setGeometry(268, 465, 120, 30)
            self.button.setFont(font)
            self.button.clicked.connect(self.check_file)

            BT_Mapping = QPushButton(icon_read, " อ่านข้อมูล", self)
            icon_read_size = QSize(25,20)
            BT_Mapping.setIconSize(icon_read_size)
            BT_Mapping.setGeometry(10, 80, 636, 30)
            BT_Mapping.clicked.connect(self.getData)

            frame = QFrame(self)
            frame.setGeometry(670, 120, 180, 130)
            frame.setStyleSheet("background-color: #5CFF5D;")
            frame.setFrameShape(QFrame.Box)

            PI_Location_Label = QLabel("PI Location", self)
            PI_Location_Label.setGeometry(683, 189, 100, 20)
            self.PI_Location_Scaned = QLineEdit(self)
            self.PI_Location_Scaned.setAlignment(Qt.AlignCenter)
            self.PI_Location_Scaned.setGeometry(742, 190, 100, 20)

            EN_Label = QLabel("EN", self)
            EN_Label.setGeometry(723, 159, 100, 20)
            self.EN_Scaned = QLineEdit(self)
            self.EN_Scaned.setAlignment(Qt.AlignCenter)
            self.EN_Scaned.setGeometry(742, 160, 50, 20)
            self.EN_Scaned.textChanged.connect(lambda text, widget_in = self.PI_Location_Scaned: self.text_EN_change(text, widget_in))

            STATION_Scaned_Label = QLabel("STATION ID", self)
            STATION_Scaned_Label.setGeometry(678, 129, 100, 20)
            self.STATION_Scaned = QLineEdit(self)
            self.STATION_Scaned.setAlignment(Qt.AlignCenter)
            self.STATION_Scaned.textChanged.connect(lambda text, widget_in = self.EN_Scaned: self.text_STATION_change(text, widget_in))
            self.STATION_Scaned.setGeometry(742, 130, 100, 20)   

            self.process = QComboBox(self)
            # proces_arr = ['FCAL', 'OPM', 'OPMP', 'OPMT']
            proces_arr = ['FCAL','OPM']
            for i in proces_arr:
                self.process.addItem(i)
            self.process.setGeometry(742,220,55,20)

            Create_Slot = CreateSlot()

            variable_11 = Create_Slot.input_data(self, "SLOT11", 490, 350)
            self.UUT_SN_Box_11 = variable_11[0]
            self.TX_SN_11 = variable_11[1]
            self.RX_SN_11 = variable_11[2]
            self.Test_Count_11 = variable_11[3]
            self.Shim_SN_11 = variable_11[4]
            # self.Shim_SN_11.textChanged.connect(lambda text, widget_in = self.STATION_Scaned: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_11.textChanged.connect(lambda text, widget_in = self.STATION_Scaned: self.text_UUT_change(text, widget_in))  

            variable_10 = Create_Slot.input_data(self, "SLOT10", 330, 350)
            self.UUT_SN_Box_10 = variable_10[0]
            self.TX_SN_10 = variable_10[1]
            self.RX_SN_10 = variable_10[2]
            self.Test_Count_10 = variable_10[3]
            self.Shim_SN_10 = variable_10[4]
            # self.Shim_SN_10.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_11: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_10.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_11: self.text_UUT_change(text, widget_in))  

            variable_9 = Create_Slot.input_data(self, "SLOT9", 170, 350)
            self.UUT_SN_Box_9 = variable_9[0]
            self.TX_SN_9 = variable_9[1]
            self.RX_SN_9 = variable_9[2]
            self.Test_Count_9 = variable_9[3]
            self.Shim_SN_9 = variable_9[4]
            # self.Shim_SN_9.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_10: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_9.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_10: self.text_UUT_change(text, widget_in))  

            variable_8 = Create_Slot.input_data(self, "SLOT8", 10, 350)
            self.UUT_SN_Box_8 = variable_8[0]
            self.TX_SN_8 = variable_8[1]
            self.RX_SN_8 = variable_8[2]
            self.Test_Count_8 = variable_8[3]
            self.Shim_SN_8 = variable_8[4]
            # self.Shim_SN_8.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_9: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_8.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_9: self.text_UUT_change(text, widget_in))  
            
            variable_7 = Create_Slot.input_data(self, "SLOT7", 490, 235)
            self.UUT_SN_Box_7 = variable_7[0]
            self.TX_SN_7 = variable_7[1]
            self.RX_SN_7 = variable_7[2]
            self.Test_Count_7 = variable_7[3]
            self.Shim_SN_7 = variable_7[4]
            # self.Shim_SN_7.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_8: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_7.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_8: self.text_UUT_change(text, widget_in))  

            variable_6 = Create_Slot.input_data(self, "SLOT6", 330, 235)
            self.UUT_SN_Box_6 = variable_6[0]
            self.TX_SN_6 = variable_6[1]
            self.RX_SN_6 = variable_6[2]
            self.Test_Count_6 = variable_6[3]
            self.Shim_SN_6 = variable_6[4]
            # self.Shim_SN_6.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_7: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_6.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_7: self.text_UUT_change(text, widget_in))  

            variable_5 = Create_Slot.input_data(self, "SLOT5", 170, 235)
            self.UUT_SN_Box_5 = variable_5[0]
            self.TX_SN_5 = variable_5[1]
            self.RX_SN_5 = variable_5[2]
            self.Test_Count_5 = variable_5[3]
            self.Shim_SN_5 = variable_5[4]
            # self.Shim_SN_5.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_6: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_5.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_6: self.text_UUT_change(text, widget_in))  

            variable_4 = Create_Slot.input_data(self, "SLOT4", 10, 235)
            self.UUT_SN_Box_4 = variable_4[0]
            self.TX_SN_4 = variable_4[1]
            self.RX_SN_4 = variable_4[2]
            self.Test_Count_4 = variable_4[3]
            self.Shim_SN_4 = variable_4[4]
            # self.Shim_SN_4.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_5: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_4.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_5: self.text_UUT_change(text, widget_in))  

            variable_3 = Create_Slot.input_data(self, "SLOT3", 490, 120)
            self.UUT_SN_Box_3 = variable_3[0]
            self.TX_SN_3 = variable_3[1]
            self.RX_SN_3 = variable_3[2]
            self.Test_Count_3 = variable_3[3]
            self.Shim_SN_3 = variable_3[4]
            # self.Shim_SN_3.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_4: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_3.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_4: self.text_UUT_change(text, widget_in))  

            variable_2 = Create_Slot.input_data(self, "SLOT2", 330, 120)
            self.UUT_SN_Box_2 = variable_2[0]
            self.TX_SN_2 = variable_2[1]
            self.RX_SN_2 = variable_2[2]
            self.Test_Count_2 = variable_2[3]
            self.Shim_SN_2 = variable_2[4]
            # self.Shim_SN_2.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_3: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_2.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_3: self.text_UUT_change(text, widget_in))  

            variable_1 = Create_Slot.input_data(self, "SLOT1", 170, 120)
            self.UUT_SN_Box_1 = variable_1[0]
            self.TX_SN_1 = variable_1[1]
            self.RX_SN_1 = variable_1[2]
            self.Test_Count_1 = variable_1[3]
            self.Shim_SN_1 = variable_1[4]
            # self.Shim_SN_1.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_2: self.shim_SN_change(text, widget_in))  
            self.UUT_SN_Box_1.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_2: self.text_UUT_change(text, widget_in))  

            variable_0 = Create_Slot.input_data(self, "SLOT0", 10, 120)
            self.UUT_SN_Box_0 = variable_0[0]
            self.TX_SN_0 = variable_0[1]
            self.RX_SN_0 = variable_0[2]
            self.Test_Count_0 = variable_0[3]
            self.Shim_SN_0 = variable_0[4]
            # self.Shim_SN_0.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_1: self.shim_SN_change(text, widget_in))
            self.UUT_SN_Box_0.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_1: self.text_UUT_change(text, widget_in)) 

            with open('setting/Path Files Location.txt', 'r') as f:
                file_read_1 = f.read()       
            file_read_1 = file_read_1.replace("\\", '/')
            self.path_box.setText(file_read_1)

            with open('setting/Path for Store.txt', 'r') as f:
                file_read_2 = f.read()
            file_read_2 = file_read_2.replace("\\", '/')
            self.path_box_store.setText(file_read_2)

            self.Dict_Data = {}

            self.Array_TX_SN_Box = (self.TX_SN_0,self.TX_SN_1,self.TX_SN_2,self.TX_SN_3,self.TX_SN_4,self.TX_SN_5,self.TX_SN_6,self.TX_SN_7,self.TX_SN_8,self.TX_SN_9,self.TX_SN_10,self.TX_SN_11)
            self.Array_RX_SN_Box = (self.RX_SN_0,self.RX_SN_1,self.RX_SN_2,self.RX_SN_3,self.RX_SN_4,self.RX_SN_5,self.RX_SN_6,self.RX_SN_7,self.RX_SN_8,self.RX_SN_9,self.RX_SN_10,self.RX_SN_11)
            self.Array_UUT_BOX = (self.UUT_SN_Box_0,self.UUT_SN_Box_1,self.UUT_SN_Box_2,self.UUT_SN_Box_3,self.UUT_SN_Box_4,self.UUT_SN_Box_5,self.UUT_SN_Box_6,self.UUT_SN_Box_7,self.UUT_SN_Box_8,self.UUT_SN_Box_9,self.UUT_SN_Box_10,self.UUT_SN_Box_11)
            self.Test_Count_Box = (self.Test_Count_0,self.Test_Count_1,self.Test_Count_2,self.Test_Count_3,self.Test_Count_4,self.Test_Count_5,self.Test_Count_6,self.Test_Count_7,self.Test_Count_8,self.Test_Count_9,self.Test_Count_10,self.Test_Count_11)
            self.Array_Shimp_SN = (self.Shim_SN_0,self.Shim_SN_1,self.Shim_SN_2,self.Shim_SN_3,self.Shim_SN_4,self.Shim_SN_5,self.Shim_SN_6,self.Shim_SN_7,self.Shim_SN_8,self.Shim_SN_9,self.Shim_SN_10,self.Shim_SN_11)

            for x in self.Array_UUT_BOX:
                x.setContextMenuPolicy(Qt.CustomContextMenu)
                x.customContextMenuRequested.connect(lambda pos, widget=x: self.show_value(pos, widget))

            BT_Show_log = QPushButton('แสดงไฟล์ .html ทั้งหมดใน path', self)
            BT_Show_log.setGeometry(670, 10, 180, 30)
            BT_Show_log.clicked.connect(self.shown_all_file)

            self.setGeometry(500, 340, 0, 0) 
            self.setFixedSize(860, 500)
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def show_value(self, pos, widget):
        try:
            HandShake_FITs = HandShakeFITs()
            result = HandShake_FITs.input_data(str(widget.text()), self.process.currentText())      

            menu = QMenu()
            menu_index = QAction(result, menu)
            menu.addAction(menu_index)
            action = menu.exec_(widget.mapToGlobal(pos)) 

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def text_UUT_change(self, text, widget):
        if len(text) == 9:
            widget.setFocus(Qt.OtherFocusReason)
    def shim_SN_change(self, text, widget):
        if len(text) == 5:
            widget.setFocus(Qt.OtherFocusReason)
    def text_STATION_change(self, text, widget):
        if len(text) == 13:
            widget.setFocus(Qt.OtherFocusReason)
    def text_EN_change(self, text, widget):
        if len(text) == 6:
            widget.setFocus(Qt.OtherFocusReason)

    def ensure_FITs(self):
        try:
            self.getData()
            self.trigger = 0
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

            HandShake_FITs = HandShakeFITs()
            self.output = []
            for i in self.UUT_SN_all:
                self.output.append((str(i), HandShake_FITs.input_data(str(i), self.process.currentText())))

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

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def submit_FITs(self):
        try:
            Check_In_FITs = CheckInFITs()
            self.progress_bar.setVisible(True)
            
            TX = []
            for x in self.TX_for_FITs:
                if '.' in x:
                    val = x.split('.')
                    TX.append(val[0])
                else:
                    TX.append(x)
            RX = []
            for x in self.RX_for_FITs:
                if '.' in x:
                    val = x.split('.')
                    RX.append(val[0])
                else:
                    RX.append(x)

            result_message_1 = []
            result_message_2 = []
            self.progress_bar.setMaximum(len(self.output))

            SLOT_Usage = []
            for idx, j in enumerate(self.Array_UUT_BOX):
                if j.text() != '':
                    SLOT_Usage.append(idx)                

            for index, i in enumerate(self.output):
                if i[1] == 'True':
                    Check_In_FITs.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), TX[index], RX[index], self.PI_Location_Scaned.text(), self.process.currentText(), self.Array_Shimp_SN[int(SLOT_Usage[index])].text())
                    self.progress_bar.setValue(int(index) + 1)
                    time.sleep(0.2)           
            self.save_file()

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def window_FITs_result(self, array_in, msg_1, msg_2):
        dialog = QDialog()
        table = QTableWidget(dialog)
        table.setGeometry(10,10,301,276)

        sn = []
        for i in array_in:
            sn.append(str(i[0]))

        description = "Check In 'OPM'"
        array = []
        for x, y in zip(sn, msg_1):
            array.append((x, description, y))

        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['SN งาน', 'รายละเอียด', 'ผลลัพธ์'])
        table.setRowCount(len(sn[0]))

        for i, row in enumerate(array):
            for j, val in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(val))
                table.setItem(i, j, table_item)
                table.setRowHeight(i, 20)
                if j == 2:
                    if val == "True":
                        table_item.setBackground(QtGui.QColor(0, 255, 0))
                    else:
                        table_item.setBackground(QtGui.QColor(255, 0, 0))   
 
        table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #00E8FF}")
        table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table.verticalHeader().setVisible(False)

    def refresh_FITs(self):
        try:
            HandShake_FITs = HandShakeFITs()
            self.output = []
            for i in self.UUT_SN_all:
                self.output.append((str(i), HandShake_FITs.input_data(str(i), self.process.currentText())))

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

    def shown_all_file(self):
        try:
            dialog = QDialog(self)
            table = QTableWidget(dialog)
            table.setGeometry(10, 10, 300, 500)
            list_file = [f for f in os.listdir(self.path_box.text()) if f.endswith(".html")] 
            list_file.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_box.text(), x)), reverse=True)
            path_list_file = []
            for i in list_file:
                path_list_file.append(os.path.join(self.path_box.text(), i))

            date_from_list_file = []
            for j in path_list_file:
                with open(j, 'r') as file:
                    html_content = file.read()
                start_index = html_content.find('<td class="HeaderField" style="width:75%">') + len('<td class="HeaderField" style="width:75%">')
                end_index = html_content.find('</td>', start_index)
                value = html_content[start_index:end_index]
                date_from_list_file.append(value)

            detail_file_list = []
            for x, y in zip(list_file, date_from_list_file):
                detail_file_list.append((x, y))
            
            table.setColumnCount(2)
            table.setHorizontalHeaderLabels(["SN สายไฟเบอร์", "วันที่ ที่บันทึกไฟล์"])
            table.setRowCount(len(detail_file_list))
            for i, row in enumerate(detail_file_list):
                for j, col in enumerate(row):
                    table_item = QtWidgets.QTableWidgetItem(str(col))
                    table.setItem(i, j, table_item)
                    table.resizeColumnToContents(j) 

            table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #DCFFA1}")
            table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            table.verticalHeader().setVisible(True)

            dialog.show()

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def Browse_Path(self):
        self.path_name_file_located = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.path_box.setText(self.path_name_file_located)

    def Store_Path(self):
        self.path_name_file_located_store = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.path_box_store.setText(self.path_name_file_located_store)

    def get_slot(self):
        return True

    def getData(self):
        try:  
            # SLOT_Check = self.get_slot() 
            SLOT_Check = True
            if SLOT_Check == True:
                if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':
                    re_run_checking = self.check_re_run_UUT()
                    if re_run_checking is not None:
                        self.position_slot_re_run = re_run_checking[0]   
                        self.re_run_SN = re_run_checking[2]
                    
                    list_data = [f for f in os.listdir(self.path_box.text()) if f.endswith(".html")] # Path file generated from Fiber Inspection
                    list_data.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_box.text(), x)), reverse=True)
                    array_1 = [self.UUT_SN_Box_0.text(),self.UUT_SN_Box_1.text(),self.UUT_SN_Box_2.text(),self.UUT_SN_Box_3.text()]
                    array_2 = [self.UUT_SN_Box_4.text(),self.UUT_SN_Box_5.text(),self.UUT_SN_Box_6.text(),self.UUT_SN_Box_7.text()]
                    array_3 = [self.UUT_SN_Box_8.text(),self.UUT_SN_Box_9.text(),self.UUT_SN_Box_10.text(),self.UUT_SN_Box_11.text()]
                    qty = 0

                    SN_Enter = array_1 + array_2 + array_3

                    Query_FITs = QueryFITs()
                    for index, i in enumerate(SN_Enter):
                        self.Test_Count_Box[index].setText('')

                    for index, i in enumerate(SN_Enter):
                        if i != '' and len(i) == 9:
                            test_count = Query_FITs.input_data(str(i), self.process.currentText(), True)
                            if test_count != 9999:
                                self.Test_Count_Box[index].setText(str(test_count[0]))
                            else:
                                self.Test_Count_Box[index].setText('')

                    for idx, i in enumerate(SN_Enter):
                        self.Array_UUT_BOX[idx].setStyleSheet("background-color: #FFFFFF;")

                    HandShake_FITs = HandShakeFITs()
                    for idx, i in enumerate(SN_Enter):
                        if i != '':
                            HandShake_SN = HandShake_FITs.input_data(str(i), self.process.currentText())
                            if HandShake_SN == 'True':
                                self.Array_UUT_BOX[idx].setStyleSheet("background-color: #46FF00;")
                            else:
                                self.Array_UUT_BOX[idx].setStyleSheet("background-color: #FF0000;")

                    if re_run_checking is not None:
                        if len(re_run_checking[0]) > 0:
                            for j in re_run_checking[0]:
                                SN_Enter[j] = ''
                    for i in SN_Enter:
                        if i != '':
                            qty += 1
                    
                    self.array_fiber_SN = list_data[:qty*2]
                    self.array_fiber_SN = self.array_fiber_SN[::-1]
                    if qty*2 <= len(list_data):
                        array_TX = []
                        array_RX = []
                        loop = 0
                        for i in self.array_fiber_SN:
                            if i[0] == 'R':
                                array_TX.append(i)
                            elif i[0] == 'W':   
                                array_RX.append(i)

                        if len(array_TX) == len(array_RX): #even number           
                            index = 0
                            self.Dict_Data = {}
                            for i, val in enumerate(SN_Enter):
                                if val != '':
                                    self.Array_TX_SN_Box[i].setText(array_TX[index].replace('.html', ''))
                                    self.Array_RX_SN_Box[i].setText(array_RX[index].replace('.html', ''))
                                    shutil.copy(self.path_box.text() + "/" + array_TX[index], 'temp')
                                    shutil.copy(self.path_box.text() + "/" + array_RX[index], 'temp')
                                    self.Dict_Data[str(val)] = (array_TX[index],array_RX[index])
                                    index += 1
                                else:
                                    self.Array_TX_SN_Box[i].setText('')
                                    self.Array_RX_SN_Box[i].setText('')     

                            if re_run_checking is not None:              
                                if len(re_run_checking[0]) > 0:
                                    for index, j in enumerate(re_run_checking[0]):
                                        self.Array_TX_SN_Box[j].setText(re_run_checking[1][index][0])
                                        self.Array_RX_SN_Box[j].setText(re_run_checking[1][index][1])
                                        self.Dict_Data[str(re_run_checking[2][index])] = re_run_checking[1][index]                
                            self.UUT_SN_all = list(self.Dict_Data.keys())  
                            self.Fiber_Check_Corrective()       
                            return True
                        else:
                            QMessageBox.information(self, "Error", "มีจำนวนไฟล์ R หรือ W ไม่เท่ากัน")
                            return False            
                    else:
                        QMessageBox.information(self, "Error", "จำนวน SN งาน ไม่ตรงกับจำนวนไฟล์ที่ได้จากการส่องกล้อง")
                        return False
                else:
                    QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน")    
                    return False

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def Fiber_Check_Corrective(self):
        try:
            Dict_TX_Get = {}
            for slot, tx in enumerate(self.Array_TX_SN_Box):
                Dict_TX_Get['SLOT' + str(slot)] = tx.text()[-4:]

            Dict_RX_Get = {}
            for slot, rx in enumerate(self.Array_RX_SN_Box):
                Dict_RX_Get['SLOT' + str(slot)] = rx.text()[-4:]

            msg = ''
            for (key_tx, value_tx), (key_rx, value_rx) in zip(Dict_TX_Get.items(), Dict_RX_Get.items()):
                if value_tx == value_rx:
                    None
                else:
                    msg += msg + f"ตรวจพบสายของ {key_tx} ไม่ครบ\n"

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def check_file(self):  
        try:
            self.check_re_run_UUT() 
            CHECK = self.getData()  
            if CHECK == True:    
                if self.Dict_Data != {}:    
                    if self.STATION_Scaned.text() != '' and self.EN_Scaned.text() != '' and self.PI_Location_Scaned.text() != '':
                        UUT_SN_input = []
                        for i in self.Array_UUT_BOX:
                            if i.text() != '':
                                UUT_SN_input.append(i.text())
                        Check_UUT_SN_input = list(set(UUT_SN_input))

                        if len(Check_UUT_SN_input) == len(UUT_SN_input):         
                            self.TX_Serial_Array = []
                            self.RX_Serial_Array = []    
                            TX_Re_Run = []
                            RX_Re_Run = []     
                            
                            for key, i in self.Dict_Data.items():
                                if key not in self.SN_for_re_run:
                                    self.TX_Serial_Array.append(i[0])
                                    self.RX_Serial_Array.append(i[1])

                                elif key in self.SN_for_re_run:
                                    TX_Re_Run.append(i[0])
                                    RX_Re_Run.append(i[1])

                            path_list_file_TX = []
                            for i in self.TX_Serial_Array:
                                path_list_file_TX.append(os.path.join(self.path_box.text(), i))

                            date_from_list_file_TX = []
                            for j in path_list_file_TX:
                                with open(j, 'r') as file:
                                    html_content = file.read()
                                start_index = html_content.find('<td class="HeaderField" style="width:75%">') + len('<td class="HeaderField" style="width:75%">')
                                end_index = html_content.find('</td>', start_index)
                                value = html_content[start_index:end_index]
                                date_from_list_file_TX.append(value)

                            path_list_file_RX = []
                            for i in self.RX_Serial_Array:
                                path_list_file_RX.append(os.path.join(self.path_box.text(), i))

                            date_from_list_file_RX = []
                            for j in path_list_file_RX:
                                with open(j, 'r') as file:
                                    html_content = file.read()
                                start_index = html_content.find('<td class="HeaderField" style="width:75%">') + len('<td class="HeaderField" style="width:75%">')
                                end_index = html_content.find('</td>', start_index)
                                value = html_content[start_index:end_index]
                                date_from_list_file_RX.append(value)

                            check_duplicate_date_from_list_file_TX = list(set(date_from_list_file_TX))
                            check_duplicate_date_from_list_file_RX = list(set(date_from_list_file_RX))
                                                
                            if len(check_duplicate_date_from_list_file_TX) == len(date_from_list_file_TX) and len(check_duplicate_date_from_list_file_RX) == len(date_from_list_file_RX):     
                                # Get (last) date of .html (fiber inspection file)
                                list_data = [f for f in os.listdir(self.path_box_store.text())]
                                list_data.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_box_store.text(), x)), reverse=True)                           
                                if len(list_data) > 0:                                             
                                        list_data_inside = [f for f in os.listdir(os.path.join(self.path_box_store.text(), list_data[0]))]
                                        Array_Date_html_last = []
                                        for i in list_data_inside:
                                            if i not in self.re_run_SN:
                                                list_data_html_inside = [f for f in os.listdir(self.path_box_store.text() + '/' + list_data[0] + '/' + i)]
                                                for j in list_data_html_inside:
                                                    html_joined = os.path.join(self.path_box_store.text() + '/' + list_data[0] + '/' + i, j)
                                                    Array_Date_html_last.append(self.read_html_dt(html_joined))
                                        
                                        # Get (current) date of .html (fiber inspection file) in path storaged
                                        Array_Date_html = []
                                        for i in self.array_fiber_SN:
                                            Array_Date_html.append(self.read_html_dt(os.path.join(self.path_box.text(), i)))
                                        count = 0                                      

                                        for i in Array_Date_html:
                                            if i in Array_Date_html_last:
                                                count += 1
                                            else:
                                                count = 0
                                        if count > 0:
                                            QMessageBox.information(self, "Error", "ตรวจพบมีไฟล์ซ้ำ")
                                            for filename in os.listdir('temp'):
                                                if filename.endswith(".html"):
                                                    file_path = os.path.join('temp', filename)
                                                    os.remove(file_path)       
                                        else:             
                                            self.TX_for_FITs = self.TX_Serial_Array + TX_Re_Run
                                            self.RX_for_FITs = self.RX_Serial_Array + RX_Re_Run
                                            self.ensure_FITs()     
                                else: 
                                    self.TX_for_FITs = self.TX_Serial_Array + TX_Re_Run
                                    self.RX_for_FITs = self.RX_Serial_Array + RX_Re_Run
                                    self.ensure_FITs()  
                            else:
                                QMessageBox.information(self, "Error", "ตรวจพบมีไฟล์ปัจจุบันมีวันที่ซ้ำ")
                                for filename in os.listdir('temp'):
                                    if filename.endswith(".html"):
                                        file_path = os.path.join('temp', filename)
                                        os.remove(file_path)  
                        else:
                            QMessageBox.information(self, "Error", "ตรวจพบมี SN งานซ้ำ")
                            for filename in os.listdir('temp'):
                                if filename.endswith(".html"):
                                    file_path = os.path.join('temp', filename)
                                    os.remove(file_path)
                    else:
                        QMessageBox.information(self, "Error", "โปรดป้อน EN , STATION ID , PI Location ให้ครบถ้วน")
                else:
                    QMessageBox.information(self, "Error", "ไม่พบข้อมูลที่จะบันทึก")
                    for filename in os.listdir('temp'):
                        if filename.endswith(".html"):
                            file_path = os.path.join('temp', filename)
                            os.remove(file_path)

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def check_re_run_UUT(self):
        try:
            UUT_SN_Enter = []
            for i in self.Array_UUT_BOX:
                UUT_SN_Enter.append(i.text())

            Query_Last_Result_Test = QueryLastResultTest()
            Query_FITs = QueryFITs()
            index = 0
            TX_RX_Queried = []
            slot_re_run = []
            SN_Using = []
            self.SN_for_re_run = []

            # ==================== Per all codition below need to endface after there are moment of UUT every time ============================
            for index, k in enumerate(UUT_SN_Enter):
                # ************************************ Get detail FCAL ************************************
                if k != '' and self.process.currentText() == 'FCAL': # There are data in array
                    last_result_test_FACL = Query_Last_Result_Test.input_data(str(k), 'FCAL')
                    # Case retest
                    if last_result_test_FACL != 0:
                        if last_result_test_FACL[0] != 'PASS' and last_result_test_FACL[1] == index and last_result_test_FACL[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_FITs = Query_FITs.input_data(str(k), 'FCAL', True) # Get TX,RX value from last check in FCAL
                            TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                            if TX_RX_Queried_FITs != 9999:
                                slot_re_run.append(index)
                                SN_Using.append(str(k))

                # ************************************ Get detail OPM ************************************
                elif k != '' and self.process.currentText() == 'OPM':
                    last_result_test_OPM = Query_Last_Result_Test.input_data(str(k), 'OPM') # This step must wait until ATS transfer done
                    # Case retest
                    if last_result_test_OPM != 0: # There are data in array
                        if last_result_test_OPM[0] != 'PASS' and last_result_test_OPM[1] == index and last_result_test_OPM[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_FITs = Query_FITs.input_data(str(k), 'OPM', True) # Get TX,RX value from last check in OPM
                            if TX_RX_Queried_FITs != 9999:
                                TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                                slot_re_run.append(index)
                                SN_Using.append(str(k))
                            else:
                                QMessageBox.information(self, "Error", "กรุณา Check In OPM ก่อน")    

            self.SN_for_re_run = SN_Using
            return slot_re_run, TX_RX_Queried, SN_Using

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def save_file(self):
        try:
            self.clear_empty_folder()
            now = datetime.now()
            current_date = now.strftime("%d %b %Y %H_%M_%S")
            New_Folder = os.path.join(self.path_box_store.text() , current_date)
            os.makedirs(New_Folder)

            SN_Enter = []
            for i in self.Array_UUT_BOX:
                SN_Enter.append(i.text())
            
            for key, value in self.Dict_Data.items():   
                Folder_SN = os.path.join(New_Folder, key)
                os.makedirs(Folder_SN)

                if key not in self.re_run_SN:                      
                    shutil.move('temp/' + value[0], Folder_SN) # Tx
                    shutil.move('temp/' + value[1], Folder_SN) # Rx

                    dst = f"\\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\{self.process.currentText()}"                              
                    folder_path_FBN_created = os.path.join(dst, key)

                    if os.path.exists(folder_path_FBN_created):
                        shutil.rmtree(folder_path_FBN_created)

                    os.makedirs(folder_path_FBN_created)

                    for file_name in os.listdir(Folder_SN):
                        source = os.path.join(Folder_SN, file_name)                                
                        shutil.copy(source, folder_path_FBN_created)
            
                    time.sleep(0.1) 

                elif key in self.re_run_SN: # Key is (retest) SN entered
                    all_folder_in_store_path = os.listdir(self.path_box_store.text())
                    all_folder_in_store_path.sort(key=lambda x: os.path.getmtime(os.path.join(self.path_box_store.text(), x)), reverse=True) # Get all folder (Batch test) [sort desc by Date]
                    all_folder_in_store_path.pop(0)
                    for j in all_folder_in_store_path:
                        list_SN_folder = os.listdir(os.path.join(self.path_box_store.text(), j)) # Get Folder SN inside Batch folder
                        if key in list_SN_folder:
                            for k in list_SN_folder:

                                if key == k:
                                    list_html = os.listdir(os.path.join(os.path.join(self.path_box_store.text(),j), k))
                                    shutil.copy(os.path.join(os.path.join(os.path.join(self.path_box_store.text(),j), k), list_html[0]), Folder_SN)
                                    shutil.copy(os.path.join(os.path.join(os.path.join(self.path_box_store.text(),j), k), list_html[1]), Folder_SN)

                                    dst = f"\\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\{self.process.currentText()}"                           
                                    folder_path_FBN_created = os.path.join(dst, key)
                
                                    if os.path.exists(folder_path_FBN_created):
                                        shutil.rmtree(folder_path_FBN_created)
                            
                                    os.makedirs(folder_path_FBN_created)

                                    for file_name in os.listdir(Folder_SN):
                                        source = os.path.join(Folder_SN, file_name)                              
                                        shutil.copy(source, folder_path_FBN_created)
                            
                                    time.sleep(0.1)  
                        break
            
            for filename in os.listdir('temp'):
                if filename.endswith(".html"):
                    file_path = os.path.join('temp', filename)
                    os.remove(file_path)   
            for i, var in enumerate(self.Array_TX_SN_Box + self.Array_RX_SN_Box + self.Array_UUT_BOX + self.Test_Count_Box + self.Array_Shimp_SN):
                var.setText('')
            QMessageBox.information(self, 'แจ้งเตือน', 'บันทึกสำเร็จ')
        
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error to Save Files : {e}")

    def read_html_dt (self, file_in):
        try:
            with open(file_in, 'r') as file:
                html_content = file.read()
            start_index = html_content.find('<td class="HeaderField" style="width:75%">') + len('<td class="HeaderField" style="width:75%">')
            end_index = html_content.find('</td>', start_index)
            value = html_content[start_index:end_index]
            return value
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def clear_empty_folder(self):
        try:
            list_folder_store = os.listdir(self.path_box_store.text())
            if len(list_folder_store) > 0:
                for i in list_folder_store:
                    list_folder_sn = os.listdir(os.path.join(self.path_box_store.text(), i))
                    if list_folder_sn:
                        for j in list_folder_sn:
                            list_file_html = os.listdir(os.path.join(os.path.join(self.path_box_store.text(), i), j))
                            if list_file_html == []:
                                shutil.rmtree(os.path.join(self.path_box_store.text(), i))
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()