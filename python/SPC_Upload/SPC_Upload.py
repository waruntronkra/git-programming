from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont, QMovie, QIcon, QColor
from PyQt5.QtCore import QTimer, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QDialog, QMessageBox, QFrame, QTableWidget, QGraphicsDropShadowEffect, QProgressBar, QPlainTextEdit
from Query_SPC_400ZR import QuerySPC400ZR
from Check_In_FIT import CheckInFITs
from Insert_Data_To_Table import InsertDataToTable
from Create_Indicator_Check_Run import CreateIndicatorCheckRun
import time
from datetime import datetime
import numpy as np

class SPC_Upload(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto Upload SPC Data')
        self.setWindowIcon(QIcon('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\auto_SPC_upload.gif'))
        self.setStyleSheet('background-color : #28283c;')

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setStyleSheet('color : white; font-weight : bold;')
        self.progress_bar.setValue(0)
        self.progress_bar.setGeometry(1195,460,360,25)
        self.progress_bar.setVisible(False)

        self.text_payload = QPlainTextEdit('', self)
        self.text_payload.setStyleSheet('background-color : #50a0ff; color : black; font-size : 10px;')
        self.text_payload.setGeometry(1195, 490, 350, 200)
        self.text_payload.setReadOnly(True)

        label_title_1 = QLabel('SPC', self)
        label_title_1.setStyleSheet('''
                                    font-family : Arial; 
                                    font-size : 20px; 
                                    color : #8EE432;
                                    font-weight : bold;
                                ''')
        label_title_1.setGeometry(200,17,100,20)

        label_title_2 = QLabel('Auto Collection', self)
        label_title_2.setStyleSheet('''
                                    font-family : Arial; 
                                    font-size : 20px; 
                                    color : #DFDFDF;
                                    font-weight : bold;
                                ''')
        label_title_2.setGeometry(250,17,150,20)
        
        label = QLabel(self)
        label.setGeometry(150,0,50,50)
        GIF = QMovie('\\\\fbn-fs-bu5\\acacia$\\Test Module\\Utility for FIR Program\\icon\\auto_SPC_upload.gif')
        GIF.setScaledSize(QSize(45,45))
        label.setMovie(GIF)
        GIF.start()

        button = QPushButton('Query', self)
        button.setStyleSheet('''
                                QPushButton {
                                    border-radius: 5px;
                                    font-weight : bold;
                                    background-color: #50a0ff;
                                }
                                QPushButton:hover {
                                    background-color: #00F7FF;
                                }
                            ''')
        button.clicked.connect(self.timer)
        button.setGeometry(10,10,100,30)

        font = QFont()
        font.setFamily('Century Gothic')
        font.setPixelSize(10)
        font.setBold(True)
        self.table = QTableWidget(self)
        self.table.setGeometry(10,50,1540,400)
        self.table.setFont(font)
        self.table.setColumnCount(20)
        self.table.setHorizontalHeaderLabels(['SERIAL_NUMBER','HW_PART_NUMBER','MODEL','MC_SLOT','MODE','START_DATE_TIME','STATUS','ID','TX OSNR In-Band','Rx Power Monitor','Temperature - Laser','Temperature - ASIC','Tx Power','PROCESS','Operation','UUT_Turnup_Tx_Max','ITLA_Frequency','OSNR','STATION','ACTIVE'])
        self.table.setColumnWidth(0,90)
        self.table.setColumnWidth(1,100)
        self.table.setColumnWidth(2,70)
        self.table.setColumnWidth(3,60)
        self.table.setColumnWidth(4,40)
        self.table.setColumnWidth(5,120)
        self.table.setColumnWidth(6,50)
        self.table.setColumnWidth(7,50)
        self.table.setColumnWidth(8,90)
        self.table.setColumnWidth(9,90)
        self.table.setColumnWidth(10,110)
        self.table.setColumnWidth(11,110)
        self.table.setColumnWidth(12,60)
        self.table.setColumnWidth(13,60)
        self.table.setColumnWidth(14,60)
        self.table.setColumnWidth(15,110)
        self.table.setColumnWidth(16,80)
        self.table.setColumnWidth(17,50)
        self.table.setColumnWidth(18,60)
        self.table.setColumnWidth(19,60)

        self.table.horizontalHeader().setStyleSheet('''
                                                    QHeaderView::section {
                                                        background-color : #50a0ff; 
                                                        font-family : Century Gothic;
                                                        font-size : 10px;
                                                        font-weight : bold;
                                                        border : True;
                                                        }                                                 
                                                    ''')
        self.table.setStyleSheet('''
                                QTableView {
                                    gridline-color : #3c3c3c; 
                                    color : #DFDFDF; 
                                    background-color : #14283c; 
                                    border-radius: 5px;
                                    }
                                ''')

        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.verticalHeader().setVisible(False)
        
        label_FCAL = QLabel('FCAL', self)
        label_FCAL.setStyleSheet('font-size : 20px; color : white; font-family : Arial Rounded MT Bold; font-weight : bold;')
        label_FCAL.setGeometry(10, 470,100,25)

        self.button_242 = CreateIndicatorCheckRun()
        self.button_247 = CreateIndicatorCheckRun()
        self.button_251 = CreateIndicatorCheckRun()
        self.button_272 = CreateIndicatorCheckRun()
        self.button_278 = CreateIndicatorCheckRun()

        self.button_242.input_detail('ATE_400ZR_242', self, 10, 510, 130, 40)
        self.button_247.input_detail('ATE_400ZR_247', self, 150, 510, 130, 40)
        self.button_251.input_detail('ATE_400ZR_251', self, 290, 510, 130, 40)
        self.button_272.input_detail('ATE_400ZR_272', self, 430, 510, 130, 40)
        self.button_278.input_detail('ATE_400ZR_278', self, 570, 510, 130, 40)

        label_OPM = QLabel('OPM', self)
        label_OPM.setStyleSheet('font-size : 20px; color : white; font-family : Arial Rounded MT Boldc; font-weight : bold;')
        label_OPM.setGeometry(10,580,100,25)

        self.button_243 = CreateIndicatorCheckRun()
        self.button_249 = CreateIndicatorCheckRun()
        self.button_271 = CreateIndicatorCheckRun()
        self.button_273 = CreateIndicatorCheckRun()
        self.button_293 = CreateIndicatorCheckRun()
        self.button_294 = CreateIndicatorCheckRun()
        self.button_297 = CreateIndicatorCheckRun()
        self.button_298 = CreateIndicatorCheckRun()
        self.button_302 = CreateIndicatorCheckRun()
        self.button_319 = CreateIndicatorCheckRun()
        self.button_314 = CreateIndicatorCheckRun()
        self.button_267 = CreateIndicatorCheckRun()

        self.button_243.input_detail('ATE_400ZR_243', self, 10, 620, 130, 40)
        self.button_249.input_detail('ATE_400ZR_249', self, 150, 620, 130, 40)
        self.button_271.input_detail('ATE_400ZR_271', self, 290, 620, 130, 40)
        self.button_273.input_detail('ATE_400ZR_273', self, 430, 620, 130, 40)
        self.button_293.input_detail('ATE_400ZR_293', self, 570, 620, 130, 40)
        self.button_294.input_detail('ATE_400ZR_294', self, 710, 620, 130, 40)
        self.button_297.input_detail('ATE_400ZR_297', self, 10, 670, 130, 40)
        self.button_298.input_detail('ATE_400ZR_298', self, 150, 670, 130, 40)
        self.button_302.input_detail('ATE_400ZR_302', self, 290, 670, 130, 40)
        self.button_319.input_detail('ATE_400ZR_319', self, 430, 670, 130, 40)
        self.button_314.input_detail('ATE_400ZR_314', self, 570, 670, 130, 40)
        self.button_267.input_detail('ATE_400ZR_267', self, 710, 670, 130, 40)

        self.last_refresh = QLabel('', self)
        self.last_refresh.setStyleSheet('font-size : 10px; color : #8EE432; font-family : Arial Rounded MT Bold; font-weight : bold;')
        self.last_refresh.setGeometry(1310,700,250,20)

        label_min = QLabel('Set Time', self)
        label_min.setStyleSheet('color : white; font-weight : bold; font-size : 12px')
        label_min.setGeometry(1385,17,70,20)
        label_min_unit = QLabel('min', self)
        label_min_unit.setStyleSheet('color : white; font-weight : bold; font-size : 12px')
        label_min_unit.setGeometry(1510,17,70,20)
        self.time_refresh = QLineEdit('30', self)   
        self.time_refresh.setStyleSheet('background-color : white; font-weight : bold; font-size : 12px')
        self.time_refresh.setAlignment(Qt.AlignCenter)
        self.time_refresh.setGeometry(1450,15,50,25)

        self.slot_query = 0
        self.loop = 0
        self.station = 'ATE_400ZR_242'
        self.process = 'FCAL'

        self.setFixedSize(1560,730)
        self.move(350,10)

        self.time_loop = QTimer(self)
        self.time_loop_big = QTimer(self)   

        self.active_timer = False  
    
    def timer_big(self):
        self.time_loop_big.timeout.connect(self.timer)
        self.time_loop_big.start(int(int(self.time_refresh.text()) * 60 * 1000))

    def timer(self):
        self.loop = 0
        self.slot_query = 0
        self.station = 'ATE_400ZR_242'
        self.process = 'FCAL'
        self.text_payload.setPlainText('')
        self.table.clearContents()
        self.progress_bar.setMaximum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        time_now = datetime.now()
        current_date = time_now.strftime("%d %B %Y %I:%M:%S")
        self.last_refresh.setText(f'Last time refresh : {current_date}')
       
        self.time_loop.timeout.connect(self.start_run)
        self.time_loop.start(100)    

        self.loop = 0
        self.slot = 204
        
    def start_run(self):    
        self.table.setRowCount(self.slot)
        self.progress_bar.setMaximum(self.slot)
        self.progress_bar.setValue(self.loop)
        
        if self.loop < self.slot:          
            if self.loop == 12:
                self.slot_query = 0
                self.station = 'ATE_400ZR_247'
                self.process = 'FCAL'

                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_242.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_242.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_242.set_color('#FFF000')

            elif self.loop == 24:
                self.slot_query = 0
                self.station = 'ATE_400ZR_251'
                self.process = 'FCAL'

                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 12, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_247.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_247.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_247.set_color('#FFF000')

            elif self.loop == 36:
                self.slot_query = 0
                self.station = 'ATE_400ZR_272'
                self.process = 'FCAL'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 24, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_251.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_251.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_251.set_color('#FFF000')

            elif self.loop == 48:
                self.slot_query = 0
                self.station = 'ATE_400ZR_278'
                self.process = 'FCAL'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 36, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_272.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_272.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_272.set_color('#FFF000')

            elif self.loop == 60:
                self.slot_query = 0
                self.station = 'ATE_400ZR_243'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 48, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_278.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_278.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_278.set_color('#FFF000')

            elif self.loop == 72:
                self.slot_query = 0
                self.station = 'ATE_400ZR_249'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 60, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_243.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_243.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_243.set_color('#FFF000')

            elif self.loop == 84:
                self.slot_query = 0
                self.station = 'ATE_400ZR_271'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 72, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_249.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_249.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_249.set_color('#FFF000')

            elif self.loop == 96:
                self.slot_query = 0
                self.station = 'ATE_400ZR_273'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 84, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_271.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_271.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_271.set_color('#FFF000')

            elif self.loop == 108:
                self.slot_query = 0
                self.station = 'ATE_400ZR_293'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 96, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_273.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_273.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_273.set_color('#FFF000')

            elif self.loop == 120:
                self.slot_query = 0
                self.station = 'ATE_400ZR_294'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 108, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_293.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_293.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_293.set_color('#FFF000')

            elif self.loop == 132:
                self.slot_query = 0
                self.station = 'ATE_400ZR_297'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 120, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_294.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_294.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_294.set_color('#FFF000')

            elif self.loop == 144:
                self.slot_query = 0
                self.station = 'ATE_400ZR_298'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 132, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_297.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_297.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_297.set_color('#FFF000')

            elif self.loop == 156:
                self.slot_query = 0
                self.station = 'ATE_400ZR_302'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 144, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_298.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_298.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_298.set_color('#FFF000')

            elif self.loop == 168:
                self.slot_query = 0
                self.station = 'ATE_400ZR_319'
                self.process = 'OPM'
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 156, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_302.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_302.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_302.set_color('#FFF000')

            elif self.loop == 180:
                self.slot_query = 0
                self.station = 'ATE_400ZR_314'
                self.process = 'OPM'    
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 168, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_319.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_319.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_319.set_color('#FFF000')
            
            elif self.loop == 192:
                self.slot_query = 0
                self.station = 'ATE_400ZR_267'
                self.process = 'OPM'    
                
                column_ACTIVE = []
                for row in range(12):
                    item = self.table.item(row + 180, 19)
                    column_ACTIVE.append(str(item.text()))
                column_ACTIVE = list(set(column_ACTIVE))

                if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                    self.button_314.set_color('#0CD16F')
                elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                    self.button_314.set_color('#FF0000')
                elif len(column_ACTIVE) > 1:
                    self.button_314.set_color('#FFF000')

            data = QuerySPC400ZR().input_data(f"{self.station}", str(self.slot_query), self.process) 

            InsertDataToTable().input_detail(data, self.table, self.loop, self.slot_query, self.station)

            if len(data) > 0:
                FITs_Payload = CheckInFITs().input_data(data[0][0], data[0][1], data[0][2], data[0][3], data[0][4], data[0][5], data[0][6], data[0][7], data[0][8], data[0][9], data[0][10], data[0][11], data[0][12], data[0][13], data[0][15], data[0][16], data[0][17], self.process) 
                cursor = self.text_payload.textCursor()
                cursor.movePosition(cursor.End)
                cursor.insertText(FITs_Payload + '\n')
                self.text_payload.setTextCursor(cursor)
            else:
                None

            self.loop += 1
            self.slot_query += 1

        else:           
            column_ACTIVE = []
            for row in range(12):
                item = self.table.item(row + 192, 19)
                column_ACTIVE.append(str(item.text()))
            column_ACTIVE = list(set(column_ACTIVE))

            if column_ACTIVE[0] == 'True' and len(column_ACTIVE) == 1:
                self.button_267.set_color('#0CD16F')
            elif column_ACTIVE[0] == 'False' and len(column_ACTIVE) == 1:
                self.button_267.set_color('#FF0000')
            elif len(column_ACTIVE) > 1:
                self.button_267.set_color('#FFF000')

            if self.active_timer == False:
                self.time_loop.stop()
                self.timer_big()
                self.active_timer = True

            elif self.active_timer == True:
                self.time_loop.stop()
            
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = SPC_Upload()
    gui.show()
    app.exec_()
