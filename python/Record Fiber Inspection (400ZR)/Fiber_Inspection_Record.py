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
from Query_FITs_HW import QueryFITsHW
import time
import netifaces
import csv

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle('Record Fiber Inspection V4.5')

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
            # proces_arr = ['FCAL','OPM','LCT1', 'LCT2', 'LCTT']
            proces_arr = ['FCAL','OPM']
            for i in proces_arr:
                self.process.addItem(i)
            self.process.setGeometry(742,220,55,20)

            Create_Slot = CreateSlot()

            # variable_11 = Create_Slot.input_data(self, "SLOT11", 490, 350)
            # self.UUT_SN_Box_11 = variable_11[0]
            # self.TX_SN_11 = variable_11[1]
            # self.RX_SN_11 = variable_11[2]
            # self.Test_Count_11 = variable_11[3]
            # self.Shim_SN_11 = variable_11[4]
            # self.Shim_SN_11.textChanged.connect(lambda text, widget_in = self.STATION_Scaned: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_11.textChanged.connect(lambda text, widget_in = self.Shim_SN_11: self.text_UUT_change(text, widget_in))  

            # variable_10 = Create_Slot.input_data(self, "SLOT10", 330, 350)
            # self.UUT_SN_Box_10 = variable_10[0]
            # self.TX_SN_10 = variable_10[1]
            # self.RX_SN_10 = variable_10[2]
            # self.Test_Count_10 = variable_10[3]
            # self.Shim_SN_10 = variable_10[4]
            # self.Shim_SN_10.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_11: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_10.textChanged.connect(lambda text, widget_in = self.Shim_SN_10: self.text_UUT_change(text, widget_in))  

            # variable_9 = Create_Slot.input_data(self, "SLOT9", 170, 350)
            # self.UUT_SN_Box_9 = variable_9[0]
            # self.TX_SN_9 = variable_9[1]
            # self.RX_SN_9 = variable_9[2]
            # self.Test_Count_9 = variable_9[3]
            # self.Shim_SN_9 = variable_9[4]
            # self.Shim_SN_9.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_10: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_9.textChanged.connect(lambda text, widget_in = self.Shim_SN_9: self.text_UUT_change(text, widget_in))  

            # variable_8 = Create_Slot.input_data(self, "SLOT8", 10, 350)
            # self.UUT_SN_Box_8 = variable_8[0]
            # self.TX_SN_8 = variable_8[1]
            # self.RX_SN_8 = variable_8[2]
            # self.Test_Count_8 = variable_8[3]
            # self.Shim_SN_8 = variable_8[4]
            # self.Shim_SN_8.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_9: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_8.textChanged.connect(lambda text, widget_in = self.Shim_SN_8: self.text_UUT_change(text, widget_in))  
            
            # variable_7 = Create_Slot.input_data(self, "SLOT7", 490, 235)
            # self.UUT_SN_Box_7 = variable_7[0]
            # self.TX_SN_7 = variable_7[1]
            # self.RX_SN_7 = variable_7[2]
            # self.Test_Count_7 = variable_7[3]
            # self.Shim_SN_7 = variable_7[4]
            # self.Shim_SN_7.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_8: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_7.textChanged.connect(lambda text, widget_in = self.Shim_SN_7: self.text_UUT_change(text, widget_in))  

            # variable_6 = Create_Slot.input_data(self, "SLOT6", 330, 235)
            # self.UUT_SN_Box_6 = variable_6[0]
            # self.TX_SN_6 = variable_6[1]
            # self.RX_SN_6 = variable_6[2]
            # self.Test_Count_6 = variable_6[3]
            # self.Shim_SN_6 = variable_6[4]
            # self.Shim_SN_6.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_7: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_6.textChanged.connect(lambda text, widget_in = self.Shim_SN_6: self.text_UUT_change(text, widget_in))  

            # variable_5 = Create_Slot.input_data(self, "SLOT5", 170, 235)
            # self.UUT_SN_Box_5 = variable_5[0]
            # self.TX_SN_5 = variable_5[1]
            # self.RX_SN_5 = variable_5[2]
            # self.Test_Count_5 = variable_5[3]
            # self.Shim_SN_5 = variable_5[4]
            # self.Shim_SN_5.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_6: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_5.textChanged.connect(lambda text, widget_in = self.Shim_SN_5: self.text_UUT_change(text, widget_in))  

            # variable_4 = Create_Slot.input_data(self, "SLOT4", 10, 235)
            # self.UUT_SN_Box_4 = variable_4[0]
            # self.TX_SN_4 = variable_4[1]
            # self.RX_SN_4 = variable_4[2]
            # self.Test_Count_4 = variable_4[3]
            # self.Shim_SN_4 = variable_4[4]
            # self.Shim_SN_4.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_5: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_4.textChanged.connect(lambda text, widget_in = self.Shim_SN_4: self.text_UUT_change(text, widget_in))  

            # variable_3 = Create_Slot.input_data(self, "SLOT3", 490, 120)
            # self.UUT_SN_Box_3 = variable_3[0]
            # self.TX_SN_3 = variable_3[1]
            # self.RX_SN_3 = variable_3[2]
            # self.Test_Count_3 = variable_3[3]
            # self.Shim_SN_3 = variable_3[4]
            # self.Shim_SN_3.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_4: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_3.textChanged.connect(lambda text, widget_in = self.Shim_SN_3: self.text_UUT_change(text, widget_in))  

            # variable_2 = Create_Slot.input_data(self, "SLOT2", 330, 120)
            # self.UUT_SN_Box_2 = variable_2[0]
            # self.TX_SN_2 = variable_2[1]
            # self.RX_SN_2 = variable_2[2]
            # self.Test_Count_2 = variable_2[3]
            # self.Shim_SN_2 = variable_2[4]
            # self.Shim_SN_2.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_3: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_2.textChanged.connect(lambda text, widget_in = self.Shim_SN_2: self.text_UUT_change(text, widget_in))  

            # variable_1 = Create_Slot.input_data(self, "SLOT1", 170, 120)
            # self.UUT_SN_Box_1 = variable_1[0]
            # self.TX_SN_1 = variable_1[1]
            # self.RX_SN_1 = variable_1[2]
            # self.Test_Count_1 = variable_1[3]
            # self.Shim_SN_1 = variable_1[4]
            # self.Shim_SN_1.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_2: self.shim_SN_change(text, widget_in))  
            # self.UUT_SN_Box_1.textChanged.connect(lambda text, widget_in = self.Shim_SN_1: self.text_UUT_change(text, widget_in))  

            # variable_0 = Create_Slot.input_data(self, "SLOT0", 10, 120)
            # self.UUT_SN_Box_0 = variable_0[0]
            # self.TX_SN_0 = variable_0[1]
            # self.RX_SN_0 = variable_0[2]
            # self.Test_Count_0 = variable_0[3]
            # self.Shim_SN_0 = variable_0[4]
            # self.Shim_SN_0.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_1: self.shim_SN_change(text, widget_in))
            # self.UUT_SN_Box_0.textChanged.connect(lambda text, widget_in = self.Shim_SN_0: self.text_UUT_change(text, widget_in))   

            variable_11 = Create_Slot.input_data(self, "SLOT11", 490, 350)
            self.UUT_SN_Box_11 = variable_11[0]
            self.TX_SN_11 = variable_11[1]
            self.RX_SN_11 = variable_11[2]
            self.Test_Count_11 = variable_11[3]
            self.Shim_SN_11 = variable_11[4]
            self.UUT_SN_Box_11.textChanged.connect(lambda text, widget_in = self.STATION_Scaned: self.text_UUT_change(text, widget_in))  

            variable_10 = Create_Slot.input_data(self, "SLOT10", 330, 350)
            self.UUT_SN_Box_10 = variable_10[0]
            self.TX_SN_10 = variable_10[1]
            self.RX_SN_10 = variable_10[2]
            self.Test_Count_10 = variable_10[3]
            self.Shim_SN_10 = variable_10[4]
            self.UUT_SN_Box_10.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_11: self.text_UUT_change(text, widget_in))  

            variable_9 = Create_Slot.input_data(self, "SLOT9", 170, 350)
            self.UUT_SN_Box_9 = variable_9[0]
            self.TX_SN_9 = variable_9[1]
            self.RX_SN_9 = variable_9[2]
            self.Test_Count_9 = variable_9[3]
            self.Shim_SN_9 = variable_9[4]
            self.UUT_SN_Box_9.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_10: self.text_UUT_change(text, widget_in))  

            variable_8 = Create_Slot.input_data(self, "SLOT8", 10, 350)
            self.UUT_SN_Box_8 = variable_8[0]
            self.TX_SN_8 = variable_8[1]
            self.RX_SN_8 = variable_8[2]
            self.Test_Count_8 = variable_8[3]
            self.Shim_SN_8 = variable_8[4]
            self.UUT_SN_Box_8.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_9: self.text_UUT_change(text, widget_in))  
            
            variable_7 = Create_Slot.input_data(self, "SLOT7", 490, 235)
            self.UUT_SN_Box_7 = variable_7[0]
            self.TX_SN_7 = variable_7[1]
            self.RX_SN_7 = variable_7[2]
            self.Test_Count_7 = variable_7[3]
            self.Shim_SN_7 = variable_7[4]
            self.UUT_SN_Box_7.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_8: self.text_UUT_change(text, widget_in))  

            variable_6 = Create_Slot.input_data(self, "SLOT6", 330, 235)
            self.UUT_SN_Box_6 = variable_6[0]
            self.TX_SN_6 = variable_6[1]
            self.RX_SN_6 = variable_6[2]
            self.Test_Count_6 = variable_6[3]
            self.Shim_SN_6 = variable_6[4]
            self.UUT_SN_Box_6.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_7: self.text_UUT_change(text, widget_in))  

            variable_5 = Create_Slot.input_data(self, "SLOT5", 170, 235)
            self.UUT_SN_Box_5 = variable_5[0]
            self.TX_SN_5 = variable_5[1]
            self.RX_SN_5 = variable_5[2]
            self.Test_Count_5 = variable_5[3]
            self.Shim_SN_5 = variable_5[4]
            self.UUT_SN_Box_5.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_6: self.text_UUT_change(text, widget_in))  

            variable_4 = Create_Slot.input_data(self, "SLOT4", 10, 235)
            self.UUT_SN_Box_4 = variable_4[0]
            self.TX_SN_4 = variable_4[1]
            self.RX_SN_4 = variable_4[2]
            self.Test_Count_4 = variable_4[3]
            self.Shim_SN_4 = variable_4[4]
            self.UUT_SN_Box_4.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_5: self.text_UUT_change(text, widget_in))  

            variable_3 = Create_Slot.input_data(self, "SLOT3", 490, 120)
            self.UUT_SN_Box_3 = variable_3[0]
            self.TX_SN_3 = variable_3[1]
            self.RX_SN_3 = variable_3[2]
            self.Test_Count_3 = variable_3[3]
            self.Shim_SN_3 = variable_3[4]
            self.UUT_SN_Box_3.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_4: self.text_UUT_change(text, widget_in))  

            variable_2 = Create_Slot.input_data(self, "SLOT2", 330, 120)
            self.UUT_SN_Box_2 = variable_2[0]
            self.TX_SN_2 = variable_2[1]
            self.RX_SN_2 = variable_2[2]
            self.Test_Count_2 = variable_2[3]
            self.Shim_SN_2 = variable_2[4]
            self.UUT_SN_Box_2.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_3: self.text_UUT_change(text, widget_in))  

            variable_1 = Create_Slot.input_data(self, "SLOT1", 170, 120)
            self.UUT_SN_Box_1 = variable_1[0]
            self.TX_SN_1 = variable_1[1]
            self.RX_SN_1 = variable_1[2]
            self.Test_Count_1 = variable_1[3]
            self.Shim_SN_1 = variable_1[4]
            self.UUT_SN_Box_1.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_2: self.text_UUT_change(text, widget_in))  

            variable_0 = Create_Slot.input_data(self, "SLOT0", 10, 120)
            self.UUT_SN_Box_0 = variable_0[0]
            self.TX_SN_0 = variable_0[1]
            self.RX_SN_0 = variable_0[2]
            self.Test_Count_0 = variable_0[3]
            self.Shim_SN_0 = variable_0[4]
            self.UUT_SN_Box_0.textChanged.connect(lambda text, widget_in = self.UUT_SN_Box_1: self.text_UUT_change(text, widget_in)) 

            with open('setting/Path Files Location.txt', 'r') as f:
                file_read_1 = f.read()       
            file_read_1 = file_read_1.replace("\\", '/')
            self.path_box.setText(file_read_1)

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

            BT_Show_HW_Table = QPushButton(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\table_HW_PN.ico'), '  Show Table HW_PN \n  that able to mix', self)
            BT_Show_HW_Table.setIconSize(QSize(24,24))
            BT_Show_HW_Table.setGeometry(670, 50, 180, 40)
            BT_Show_HW_Table.clicked.connect(self.show_table_HW_PN)

            self.setGeometry(500, 340, 0, 0) 
            self.setFixedSize(860, 500)
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def show_table_HW_PN(self):
        dialog = QDialog(self)

        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        label_header_FCAL = QLabel('Table HW_PN that able to run mix for process FCAL', dialog)
        label_header_FCAL.setStyleSheet('font-size : 13px; font-weight : bold; font-family : Century Gothic; color: #00C114;')
        label_header_FCAL.setGeometry(10,10,350,20)

        label_header_OPM = QLabel('Table HW_PN that able to run mix for process OPM', dialog)
        label_header_OPM.setStyleSheet('font-size : 13px; font-weight : bold; font-family : Century Gothic; color: #0013FF;')
        label_header_OPM.setGeometry(360,10,350,20)

        # =========== Create for show HW PN that able to run mix for process FCAL ===========
        self.table_FCAL = QTableWidget(dialog)
        self.table_FCAL.setGeometry(10,35,310,400)
        self.table_FCAL.setColumnCount(3)
        self.table_FCAL.setHorizontalHeaderLabels(['HW_PART_NUMBER','Module Type','Group'])
        self.table_FCAL.setColumnWidth(0, 120)
        self.table_FCAL.setColumnWidth(1, 120)
        self.table_FCAL.setColumnWidth(2, 50)

        self.table_FCAL.horizontalHeader().setStyleSheet('''
                                                        QHeaderView::section {
                                                            background-color: #B1FFB3;
                                                            font-family : Century Gothic;
                                                            font-size : 11px;
                                                            font-weight : bold;
                                                            }
                                                    ''')
        self.table_FCAL.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        self.table_FCAL.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table_FCAL.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_FCAL.verticalHeader().setVisible(False)

        # =========== Create for show HW PN that able to run mix for process OPM ===========
        self.table_OPM = QTableWidget(dialog)
        self.table_OPM.setGeometry(360,35,310,400)
        self.table_OPM.setColumnCount(3)
        self.table_OPM.setHorizontalHeaderLabels(['HW_PART_NUMBER','Module Type','Group'])
        self.table_OPM.setColumnWidth(0, 120)
        self.table_OPM.setColumnWidth(1, 120)
        self.table_OPM.setColumnWidth(2, 50)

        self.table_OPM.horizontalHeader().setStyleSheet('''
                                                        QHeaderView::section {
                                                            background-color: #B1DFFF;
                                                            font-family : Century Gothic;
                                                            font-size : 11px;
                                                            font-weight : bold;
                                                            }
                                                    ''')
        self.table_OPM.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        self.table_OPM.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table_OPM.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_OPM.verticalHeader().setVisible(False)

        
        # =========== Read CSV mixing HW PN of process FCAL ===========
        csv_path_FCAL = '\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_FCAL.csv'
        data_FCAL = []
        with open(csv_path_FCAL, 'r') as f:
            for row in csv.reader(f):
                data_FCAL.append(row)
        data_FCAL.pop(0)
        self.table_FCAL.setRowCount(len(data_FCAL))

        for i, row in enumerate(data_FCAL):
            for j, col in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(col))
                self.table_FCAL.setItem(i, j, table_item)

        # =========== Read CSV mixing HW PN of process OPM ===========
        csv_path_OPM = '\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_OPM.csv'
        data_OPM = []
        with open(csv_path_OPM, 'r') as f:
            for row in csv.reader(f):
                data_OPM.append(row)
        data_OPM.pop(0)
        self.table_OPM.setRowCount(len(data_OPM))

        for i, row in enumerate(data_OPM):
            for j, col in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(col))
                self.table_OPM.setItem(i, j, table_item)

        # =========== Create button to add more HW PN ===========
        text_empty = QPushButton('', dialog)
        text_empty.clicked.connect(self.nothing)
        text_empty.setVisible(False)

        BT_add_HW_FCAL = QPushButton(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\add_HW.ico'), ' Add more HW PN [FCAL]', dialog)
        BT_add_HW_FCAL.setGeometry(680,34,150,30)
        BT_add_HW_FCAL.clicked.connect(self.add_more_HW_FCAL)
        BT_add_HW_OPM = QPushButton(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\add_HW.ico'), ' Add more HW PN [OPM]', dialog)
        BT_add_HW_OPM.clicked.connect(self.add_more_HW_OPM)
        BT_add_HW_OPM.setGeometry(680,74,150,30)
              
        dialog.setFixedSize(840,450)
        dialog.show()

    def nothing(self):
        None
    
    def add_more_HW_FCAL(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add More HW for FCAL')

        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        label_enter_HW = QLabel('Enter HW_PART_NUMBER :', dialog)
        label_enter_HW.setGeometry(10,11,150,20)
        enter_HW = QLineEdit('', dialog)
        enter_HW.setAlignment(Qt.AlignCenter)
        enter_HW.setGeometry(145,10,100,25)

        label_enter_module_type = QLabel('Enter Module Type :', dialog)
        label_enter_module_type.setGeometry(45,46,150,20)
        enter_module_type = QLineEdit('', dialog)
        enter_module_type.setAlignment(Qt.AlignCenter)
        enter_module_type.setGeometry(145,45,100,25)

        label_enter_group = QLabel('Enter Group :', dialog)
        label_enter_group.setGeometry(77,81,150,20)
        enter_group = QLineEdit('', dialog)
        enter_group.setAlignment(Qt.AlignCenter)
        enter_group.setGeometry(145,80,30,25)

        button_confirm = QPushButton(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\add_button.ico'), '  Submit', dialog)
        button_confirm.clicked.connect(lambda : self.add_new_HW_to_table_FCAL(enter_HW.text(), enter_module_type.text(), enter_group.text()))
        button_confirm.clicked.connect(lambda : dialog.close())
        button_confirm.setGeometry(144,110,120,30)

        dialog.setFixedSize(270,150)
        dialog.show()

    def add_new_HW_to_table_FCAL(self, HW_PN, Module_Type, Group):
        csv_path_FCAL = '\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_FCAL.csv'
        with open(csv_path_FCAL, 'a', newline='') as f:
            csv.writer(f).writerow([HW_PN, Module_Type, Group])

        data_FCAL = []
        with open(csv_path_FCAL, 'r') as f:
            for row in csv.reader(f):
                data_FCAL.append(row)
        data_FCAL.pop(0)
        self.table_FCAL.setRowCount(len(data_FCAL))

        for i, row in enumerate(data_FCAL):
            for j, col in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(col))
                self.table_FCAL.setItem(i, j, table_item)
    
    def add_more_HW_OPM(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Add More HW for OPM')

        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        label_enter_HW = QLabel('Enter HW_PART_NUMBER :', dialog)
        label_enter_HW.setGeometry(10,11,150,20)
        enter_HW = QLineEdit('', dialog)
        enter_HW.setAlignment(Qt.AlignCenter)
        enter_HW.setGeometry(145,10,100,25)

        label_enter_module_type = QLabel('Enter Module Type :', dialog)
        label_enter_module_type.setGeometry(45,46,150,20)
        enter_module_type = QLineEdit('', dialog)
        enter_module_type.setAlignment(Qt.AlignCenter)
        enter_module_type.setGeometry(145,45,100,25)

        label_enter_group = QLabel('Enter Group :', dialog)
        label_enter_group.setGeometry(77,81,150,20)
        enter_group = QLineEdit('', dialog)
        enter_group.setAlignment(Qt.AlignCenter)
        enter_group.setGeometry(145,80,30,25)

        button_confirm = QPushButton(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\add_button.ico'), '  Submit', dialog)
        button_confirm.clicked.connect(lambda : self.add_new_HW_to_table_OPM(enter_HW.text(), enter_module_type.text(), enter_group.text()))
        button_confirm.clicked.connect(lambda : dialog.close())
        button_confirm.setGeometry(144,110,120,30)

        dialog.setFixedSize(270,150)
        dialog.show()

    def add_new_HW_to_table_OPM(self, HW_PN, Module_Type, Group):
        csv_path_OPM = '\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_OPM.csv'
        with open(csv_path_OPM, 'a', newline='') as f:
            csv.writer(f).writerow([HW_PN, Module_Type, Group])

        data_OPM = []
        with open(csv_path_OPM, 'r') as f:
            for row in csv.reader(f):
                data_OPM.append(row)
        data_OPM.pop(0)
        self.table_OPM.setRowCount(len(data_OPM))

        for i, row in enumerate(data_OPM):
            for j, col in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(col))
                self.table_OPM.setItem(i, j, table_item)

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

            # Check In FITs
            Check_In_Arr = []
            out = ''
            SN_Arr = [] 
            for index, i in enumerate(self.output):
                out = Check_In_FITs.input_data(i[0], self.STATION_Scaned.text(), self.EN_Scaned.text(), TX[index], RX[index], self.PI_Location_Scaned.text(), self.process.currentText(), self.Array_Shimp_SN[int(SLOT_Usage[index])].text())
                self.progress_bar.setValue(int(index) + 1)
                Check_In_Arr.append(out)
                SN_Arr.append(i[0])
                time.sleep(0.2)   
            
            CheckIn_OK = []
            for i in Check_In_Arr:
                CheckIn_OK.append(i.split("|")[0])
            CheckIn_OK = list(set(CheckIn_OK))

            if len(CheckIn_OK) == 1 and CheckIn_OK[0] == 'True':                    
                self.save_file()
            else:
                msg_check_in = ''
                for i,j in zip(SN_Arr, Check_In_Arr):
                    msg_check_in += f"[{i}] : {j}\n"
                QMessageBox.information(self,"Error",f"บันทึกไม่สำเร็จ!\n\n{msg_check_in}")

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

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
                    
                    HW_PART_NUMBER = re_run_checking[4]    
                    HW_PART_NUMBER = list(set(HW_PART_NUMBER))

                    csv_path = f'\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\HW_PN_Mixing_400ZR_{self.process.currentText()}.csv'
                    data_HW_from_CSV = []
                    data_Module_type_from_CSV = []
                    data_Group_from_CSV = []
                    with open(csv_path, 'r') as f:
                        for row in csv.reader(f):
                            data_HW_from_CSV.append(row[0])
                            data_Module_type_from_CSV.append(row[1])
                            data_Group_from_CSV.append(row[2])

                    set_group_hw = []
                    set_group_module_type_hw = []
                    for i, j, k in zip(data_HW_from_CSV, data_Module_type_from_CSV, data_Group_from_CSV):
                        for hw_input in HW_PART_NUMBER:
                            if hw_input in i:
                                set_group_hw.append(k)
                                set_group_module_type_hw.append(j)

                    set_group_hw = list(set(set_group_hw))   
                    set_group_module_type_hw = list(set(set_group_module_type_hw))    

                    if len(set_group_hw) == 1:                  
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
                                            self.Array_Shimp_SN[j].setText(re_run_checking[3][index])
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
                        msg = ''
                        for group, module_type in zip(set_group_hw, set_group_module_type_hw):
                            msg += f'Group : {module_type} \n'
   
                        QMessageBox.information(self, "Error", f"มีการรัน mix HW กัน\n\n{msg}" )
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
                                                          
                            self.TX_for_FITs = self.TX_Serial_Array + TX_Re_Run
                            self.RX_for_FITs = self.RX_Serial_Array + RX_Re_Run
                            self.ensure_FITs()     
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
            Shim_Queried = []
            slot_re_run = []
            SN_Using = []
            self.SN_for_re_run = []
            HW_PN = []

            # ==================== Per all codition below need to endface after there are moment of UUT every time ============================
            for index, k in enumerate(UUT_SN_Enter):
                # ************************************ Get detail FCAL ************************************
                if k != '' and self.process.currentText() == 'FCAL': # There are data in array
                    last_result_test_FACL = Query_Last_Result_Test.input_data(str(k), 'FCAL')
                    HW_PN_Queried = QueryFITsHW().input_data(k)
                    HW_PN.append(HW_PN_Queried)
                    # Case retest
                    if last_result_test_FACL != 0:
                        if last_result_test_FACL[0] != 'PASS' and last_result_test_FACL[1] == index and last_result_test_FACL[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_FITs = Query_FITs.input_data(str(k), 'FCAL', True) # Get TX,RX value from last check in FCAL
                            TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                            Shim_Queried.append(TX_RX_Queried_FITs[2])
                            if TX_RX_Queried_FITs != 9999:
                                slot_re_run.append(index)
                                SN_Using.append(str(k))

                # ************************************ Get detail OPM ************************************
                elif k != '' and self.process.currentText() == 'OPM':
                    last_result_test_OPM = Query_Last_Result_Test.input_data(str(k), 'OPM') # This step must wait until ATS transfer done
                    HW_PN_Queried = QueryFITsHW().input_data(k)
                    HW_PN.append(HW_PN_Queried)
                    # Case retest
                    if last_result_test_OPM != 0: # There are data in array
                        if last_result_test_OPM[0] != 'PASS' and last_result_test_OPM[1] == index and last_result_test_OPM[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_FITs = Query_FITs.input_data(str(k), 'OPM', True) # Get TX,RX value from last check in OPM
                            if TX_RX_Queried_FITs != 9999:
                                TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                                Shim_Queried.append(TX_RX_Queried_FITs[2])
                                slot_re_run.append(index)
                                SN_Using.append(str(k))
                            else:
                                QMessageBox.information(self, "Error", "กรุณา Check In OPM ก่อน")    
                
                elif k != '' and self.process.currentText() == 'LCT1':
                    last_result_test_LCT1 = Query_Last_Result_Test.input_data(str(k), 'LCT1') # This step must wait until ATS transfer done
                    
                    # Case retest
                    if last_result_test_LCT1 != 0: # There are data in array
                        if last_result_test_LCT1[0] != 'PASS' and last_result_test_LCT1[1] == index and last_result_test_LCT1[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_LCT1 = Query_FITs.input_data(str(k), 'LCT1', True) # Get TX,RX value from last check in LCT1
                            if TX_RX_Queried_FITs != 9999:
                                TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                                Shim_Queried.append(TX_RX_Queried_FITs[2])
                                slot_re_run.append(index)
                                SN_Using.append(str(k))
                            else:
                                QMessageBox.information(self, "Error", "กรุณา Check In LCT1 ก่อน")
                
                elif k != '' and self.process.currentText() == 'LCT2':
                    last_result_test_LCT2 = Query_Last_Result_Test.input_data(str(k), 'LCT2') # This step must wait until ATS transfer done
                    
                    # Case retest
                    if last_result_test_LCT2 != 0: # There are data in arrayun
                        if last_result_test_LCT2[0] != 'PASS' and last_result_test_LCT2[1] == index and last_result_test_LCT2[2] == self.STATION_Scaned.text(): # Result = FAIL | Retest same slot | Retest station
                            TX_RX_Queried_LCT2 = Query_FITs.input_data(str(k), 'LCT2', True) # Get TX,RX value from last check in LCT2
                            if TX_RX_Queried_FITs != 9999:
                                TX_RX_Queried.append(TX_RX_Queried_FITs[1])
                                Shim_Queried.append(TX_RX_Queried_FITs[2])
                                slot_re_run.append(index)
                                SN_Using.append(str(k))
                                QMessageBox.information(self, "Error", "กรุณา Check In LCT2 ก่อน")
          
            self.SN_for_re_run = SN_Using
            return slot_re_run, TX_RX_Queried, SN_Using, Shim_Queried, HW_PN

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def save_file(self):
        try:
            for key, value in self.Dict_Data.items():   
                dst = f"\\\\fabrinet\\files\\Acacia2\\DataEntry\\Fiber_Inspection_Record\\{self.process.currentText()}"                              
                folder_path_FBN_created = os.path.join(dst, key)

                # If folder not create yet, create it
                if not os.path.exists(folder_path_FBN_created):
                    os.makedirs(folder_path_FBN_created)        

                tx_file = self.path_box.text() + f"\\{value[0]}"
                rx_file = self.path_box.text() + f"\\{value[1]}"
                if os.path.exists(tx_file):
                    if os.path.exists(folder_path_FBN_created + f"\\{value[0]}"):
                        os.remove(folder_path_FBN_created + f"\\{value[0]}")
                    shutil.move(tx_file, folder_path_FBN_created)

                if os.path.exists(rx_file):
                    if os.path.exists(folder_path_FBN_created + f"\\{value[1]}"):
                        os.remove(folder_path_FBN_created + f"\\{value[1]}")
                    shutil.move(rx_file, folder_path_FBN_created)

                time.sleep(0.1) 
            
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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()