from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QButtonGroup, QProgressBar, QWidget, QTabWidget, QRadioButton ,QPushButton, QLineEdit, QLabel, QTableWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import os
import subprocess
from Query_LINECARD import QueryLINECARD

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        main_layout = QtWidgets.QVBoxLayout()
        
        self.tab = QTabWidget(self)
        page_1 = QWidget()
        self.tab.addTab(page_1, "PAGE 1")
        page_2 = QWidget()
        self.tab.addTab(page_2, "PAGE 2")
        self.tab.tabBar().setTabVisible(0, False)
        self.tab.tabBar().setTabVisible(1, False)
        self.tab.setCurrentIndex(1)
        self.tab.setGeometry(5, 5, 1340, 630)

        self.progress_bar = QProgressBar(page_2)
        self.progress_bar.setGeometry(120, 32, 210, 20)

        # Create radio button to select page
        # radio_group = QButtonGroup(page_2)
        # switch_to_page_1 = QRadioButton("By UUT", self)
        # switch_to_page_2 = QRadioButton("By Date", self)
        # radio_group.addButton(switch_to_page_1)
        # radio_group.addButton(switch_to_page_2)
        # switch_to_page_1.setChecked(True)
        # switch_to_page_1.move(1200, 15)
        # switch_to_page_2.move(1275, 15)
        # switch_to_page_1.toggled.connect(self.To_Page_1)
        # switch_to_page_2.toggled.connect(self.To_Page_2)

        # Create radio button to select < 70%
        # self.less_than_70 = QRadioButton("< 70%", page_2)
        # self.less_than_70.setChecked(True)
        # self.less_than_70.move(160, 160)
        # self.greater_than_70 = QRadioButton("All Percent", page_2)
        # self.greater_than_70.move(225, 160)
        # self.less_than_70.toggled.connect(self.less_than_70_condition)
        # self.greater_than_70.toggled.connect(self.greater_than_70_condition)
        # self.condition = "Less than 70 %"

        # Creat refresh button
        font_P1 = QFont()
        font_P1.setBold(True)
        button_P1 = QPushButton("Refresh", page_1)
        button_P1.setGeometry(10, 10, 100, 30)
        button_P1.setStyleSheet("background-color: #98FDFF; color: black;")
        button_P1.setFont(font_P1)
        button_P1.clicked.connect(self.query_data)

        font_P2 = QFont()
        font_P2.setBold(True)
        button_P2 = QPushButton("Refresh", page_2)
        button_P2.setGeometry(10, 27, 100, 30)
        button_P2.setStyleSheet("background-color: #98FDFF; color: black;")
        button_P2.setFont(font_P2)
        button_P2.clicked.connect(self.query_data)
        
        # Creat dropdown day (Page_1)
        day_label_P1 = QLabel("Select Day", page_1)
        day_label_P1.move(265,18)
        self.day_dropbox_P1 = QComboBox(page_1)
        self.day_dropbox_P1.addItem("1")
        self.day_dropbox_P1.addItem("2")
        self.day_dropbox_P1.addItem("3")
        self.day_dropbox_P1.addItem("5")
        self.day_dropbox_P1.addItem("7")
        self.day_dropbox_P1.addItem("14")
        self.day_dropbox_P1.addItem("30")
        self.day_dropbox_P1.addItem("60")
        self.day_dropbox_P1.addItem("90")
        self.day_dropbox_P1.addItem("180")
        self.day_dropbox_P1.setGeometry(320,10,50,30)

         # Creat dropdown day (Page_2)
        # day_label_P2 = QLabel("Select Last UUT", page_2)
        # day_label_P2.move(502,10)
        # self.day_dropbox_P2 = QComboBox(page_2)
        # self.day_dropbox_P2.addItem("Last 10 UUTs")
        # self.day_dropbox_P2.addItem("Last 30 UUTs")
        # self.day_dropbox_P2.addItem("Last 50 UUTs")
        # self.day_dropbox_P2.addItem("Last 100 UUTs")
        # self.day_dropbox_P2.addItem("Last 300 UUTs")
        # self.day_dropbox_P2.addItem("Last 500 UUTs")
        # self.day_dropbox_P2.addItem("Last 1000 UUTs")
        # self.day_dropbox_P2.setGeometry(490,25,100,30)

        # Creat dropdown process (Page_1)
        process_label_P1 = QLabel("Select Process", page_1)
        process_label_P1.move(395,18)
        self.process_dropbox_P1 = QComboBox(page_1)
        Array_Process = ['OIT', 'PCAL', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5']
        for i in Array_Process:
            self.process_dropbox_P1.addItem(i)
        self.process_dropbox_P1.setGeometry(470, 10, 50, 30)

        # Creat dropdown process (Page_2)
        # process_label_P2 = QLabel("Select Process", page_2)
        # process_label_P2.move(307,78)
        # self.process_dropbox_P2 = QComboBox(page_2)
        # Array_Process = ['OIT', 'PCAL', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5']
        # for i in Array_Process:
        #     self.process_dropbox_P2.addItem(i)
        # self.process_dropbox_P2.setGeometry(382, 70, 50, 30)

        # Creat dropdown STATION (Page_1)
        station_lable = QLabel("Select Station", page_1)
        station_lable.move(545, 18)
        self.station_lable_P1 = QComboBox(page_1)
        with open('temp/STATION_ID.txt', 'r') as f:
            file_read = f.read()
        file_read = file_read.split('\n')
        for i in file_read:
            self.station_lable_P1.addItem(i)
        self.station_lable_P1.currentIndexChanged.connect(self.map_process)
        self.station_lable_P1.setGeometry(618, 10, 120, 30)

        # Creat dropdown STATION (Page_2)
        # station_lable_P2 = QLabel("Select Station", page_2)
        # station_lable_P2.move(330, 10)
        # self.station_lable_P2 = QComboBox(page_2)
        # with open('temp/STATION_ID.txt', 'r') as f:
        #     file_read = f.read()
        # file_read = file_read.split('\n')
        # for i in file_read:
        #     self.station_lable_P2.addItem(i)
        # self.station_lable_P2.currentIndexChanged.connect(self.map_process)
        # self.station_lable_P2.setGeometry(305, 25, 127, 30)

        # Create text box to insert yield value
        font_LC_CH = QFont("Arial", 10)
        font_LC_CH.setBold(True)
        LC_text_lable = QLabel("LINECARD SN :", page_1)
        LC_text_lable.move(765, 56)
        self.LC_text = QLineEdit(page_1)
        self.LC_text.setAlignment(Qt.AlignCenter)
        self.LC_text.setFont(font_LC_CH)
        self.LC_text.setGeometry(840, 50, 80, 30)

        CH_text_lable = QLabel("CHASSIS SN :", page_1)
        CH_text_lable.move(771, 96)
        self.CH_text = QLineEdit(page_1)
        self.CH_text.setAlignment(Qt.AlignCenter)
        self.CH_text.setFont(font_LC_CH)
        self.CH_text.setGeometry(840, 90, 80, 30)

        # Create Table
        self.table =  QTableWidget(page_2)
        self.table.setGeometry(600, 100, 730, 500)   

        # Create table yield LINECARD (Page_1)
        label_table_yield_LC_P1 = QLabel(" Table Yield LINECARD", page_1)
        label_table_yield_LC_P1.setGeometry(745, 280, 115, 20)
        self.table_yield_LC_P1 = QTableWidget(page_1)
        self.table_yield_LC_P1.setGeometry(745, 300, 287, 320)
        # Create table yield CHASSIS (Page_1)
        label_table_yield_CH_P1 = QLabel(" Table Yield CHASSIS", page_1)
        label_table_yield_CH_P1.setGeometry(1040, 280, 115, 20)
        self.table_yield_CH_P1 = QTableWidget(page_1)
        self.table_yield_CH_P1.setGeometry(1040, 300, 287, 320)
        # Create table yield per SLOTs (Page_1)
        label_table_yield_slot_P1 = QLabel(" Table Yield each SLOTs", page_1)
        label_table_yield_slot_P1.setGeometry(745, 130, 115, 20)
        self.table_yield_slot_P1 = QTableWidget(page_1)
        self.table_yield_slot_P1.setGeometry(745, 150, 247 , 120) 

        # Create table yield LINECARD (Page_2)
        label_table_yield_LC_P2 = QLabel(" Table Yield LINECARD", page_2)
        label_table_yield_LC_P2.setGeometry(10, 80, 115, 20)
        self.table_yield_LC_P2 = QTableWidget(page_2)
        self.table_yield_LC_P2.setGeometry(10, 100, 287, 320)
        # Create table yield CHASSIS (Page_2)
        label_table_yield_CH = QLabel(" Table Yield CHASSIS", page_2)
        label_table_yield_CH.setGeometry(302, 80, 115, 20)
        self.table_yield_CH_P2 = QTableWidget(page_2)
        self.table_yield_CH_P2.setGeometry(305, 100, 287, 320)    
        # # Create table yield per SLOTs (Page_2)
        # label_table_yield_slot_P2 = QLabel(" Table Yield each SLOTs", page_2)
        # label_table_yield_slot_P2.setGeometry(10, 10, 115, 20)
        # self.table_yield_slot_P2 = QTableWidget(page_2)
        # self.table_yield_slot_P2.setGeometry(10, 30, 247 , 120)

        self.setGeometry(200, 50, 1345, 635)

    def To_Page_1 (self):
        self.tab.setCurrentIndex(1)
    def To_Page_2 (self):
        self.tab.setCurrentIndex(0)

    def less_than_70_condition (self):
        self.condition = "Less than 70 %"
        self.query_data()
    def greater_than_70_condition (self):
        self.condition = "Greater than 70 %"
        self.query_data()

    def map_process (self):
        if self.tab.currentIndex() == 0:
            self.position = self.process_dropbox_P1.currentIndex()
            self.process_dropbox_P1.clear()
            station = str(self.station_lable_P1.currentText())
            station = station.split('_')
            if station[1] == 'AC1200' or station[1] == 'AX1200':
                Array_Process = ['OIT', 'PCAL', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5'] 
                self.LC_text.setText('')
                self.CH_text.setText('')
            elif station[1] == 'AC100M' or station[1] == 'AC200' or station[1] == 'AC400':
                Array_Process = ['OBS', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS']
                self.LC_text.setText('')
                self.CH_text.setText('')
            elif station[1] == '400ZR':
                Array_Process = ['FCAL', 'OPM', 'OPMP', 'OPMT', 'EXP', 'EXS']
                self.LC_text.setText('')
                self.CH_text.setText('')
            
            for i in Array_Process:
                self.process_dropbox_P1.addItem(i)
            self.process_dropbox_P1.setCurrentIndex(self.position)
        
        elif self.tab.currentIndex() == 1:
            self.position = self.process_dropbox_P2.currentIndex()
            self.process_dropbox_P2.clear()
            station = str(self.station_lable_P2.currentText())
            station = station.split('_')
            if station[1] == 'AC1200' or station[1] == 'AX1200':
                Array_Process = ['OIT', 'PCAL', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5'] 
                self.LC_text.setText('')
                self.CH_text.setText('')
            elif station[1] == 'AC100M' or station[1] == 'AC200' or station[1] == 'AC400':
                Array_Process = ['OBS', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS']
                self.LC_text.setText('')
                self.CH_text.setText('')
            elif station[1] == '400ZR':
                Array_Process = ['FCAL', 'OPM', 'OPMP', 'OPMT', 'EXP', 'EXS']
                self.LC_text.setText('')
                self.CH_text.setText('')
            
            for i in Array_Process:
                self.process_dropbox_P2.addItem(i)
            self.process_dropbox_P2.setCurrentIndex(self.position)
    
    def query_data (self):
        with open('temp/STATION_ID.txt', 'r') as f:
            file_read = f.read()
        Array_Station = file_read.split('\n')
        self.progress_bar.setMaximum(len(Array_Station) - 1)

        Array_LC_Row_Data_Yield = []
        Array_CH_Row_Data_Yield = []
        self.Station_ID_LC = []
        self.Station_ID_CH = []
        for loop ,i in enumerate(Array_Station):
            self.progress_bar.setValue(loop)
            Query_LINECARD = QueryLINECARD()
            Data = Query_LINECARD.input_data("1", i, "", "", "", "By Date")  

            LC_Row_Data_Yield = []
            station_LC = []
            for LINECARD in Data:
                DATA_Top_10 = Query_LINECARD.input_data("10", i, "", str(LINECARD[5]), "", "By UUT")
                Fail = []              
                for result in DATA_Top_10:
                    if result[4] != 'PASS':
                        Fail.append(result)                  
                if len(Fail) >= 3:
                    Percent_Yield = ((10 - len(Fail)) / 10) * 100
                    Percent_Yield = f"{Percent_Yield: .2f}"
                    Row_Data = [str(LINECARD[5]), str(10 - len(Fail)), str(len(Fail)), (str(Percent_Yield) + " %")]
                    LC_Row_Data_Yield.append(Row_Data)
                    station_LC.append(i)            
            Array_LC_Row_Data_Yield.extend(LC_Row_Data_Yield)
            self.Station_ID_LC.extend(station_LC)
            
            CH_Row_Data_Yield = []
            station_CH = []
            for CHASSIS in Data:
                if i.split("_")[1] != "AC100M" or i.split("_")[1] != "AC200" or i.split("_")[1] != "AC400":
                    DATA_Top_10 = Query_LINECARD.input_data("10", i, "", "", str(CHASSIS[6]), "By UUT")
                Fail = []          
                for result in DATA_Top_10:
                    if result[4] != 'PASS':
                        Fail.append(result)
                if len(Fail) >= 3:
                    Percent_Yield = ((10 - len(Fail)) / 10) * 100
                    Percent_Yield = f"{Percent_Yield: .2f}"
                    Row_Data = [str(CHASSIS[6]), str(10 - len(Fail)), str(len(Fail)), (str(Percent_Yield) + " %")]
                    CH_Row_Data_Yield.append(Row_Data)
                    station_CH.append(i)
            Array_CH_Row_Data_Yield.extend(CH_Row_Data_Yield)
            self.Station_ID_CH.extend(station_CH)

        self.Station_ID_LC = list(set(self.Station_ID_LC))
        self.Station_ID_CH = list(set(self.Station_ID_CH))

        Array_LC_Row_Data_Yield = sorted(Array_LC_Row_Data_Yield, key=lambda x: float(x[3].strip('%')), reverse=False)
        Array_CH_Row_Data_Yield = sorted(Array_CH_Row_Data_Yield, key=lambda x: float(x[3].strip('%')), reverse=False)
        Array_LC_Row_Data_Yield = list(set(tuple(row) for row in Array_LC_Row_Data_Yield))
        Array_CH_Row_Data_Yield = list(set(tuple(row) for row in Array_CH_Row_Data_Yield))

        header_table_yield = ['LINECARD_SN', 'PASS', 'FAIL', 'Yield']
        self.table_yield_LC_P2.setColumnCount(len(header_table_yield))
        self.table_yield_LC_P2.setHorizontalHeaderLabels(header_table_yield)
        self.table_yield_LC_P2.setRowCount(len(Array_LC_Row_Data_Yield))

        for i, row in enumerate(Array_LC_Row_Data_Yield):
            for j, value in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(value))
                self.table_yield_LC_P2.setItem(i, j, table_item)   
                self.table_yield_LC_P2.resizeColumnToContents(j)        
                self.table_yield_LC_P2.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed)
        
        self.table_yield_LC_P2.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #DCFFA1}")
        self.table_yield_LC_P2.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        self.table_yield_LC_P2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table_yield_LC_P2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_yield_LC_P2.verticalHeader().setVisible(True)
        self.table_yield_LC_P2.cellClicked.connect(self.get_data_LC)

        header_table_yield = ['LINECARD_SN', 'PASS', 'FAIL', 'Yield']
        self.table_yield_CH_P2.setColumnCount(len(header_table_yield))
        self.table_yield_CH_P2.setHorizontalHeaderLabels(header_table_yield)
        self.table_yield_CH_P2.setRowCount(len(Array_CH_Row_Data_Yield))

        for i, row in enumerate(Array_CH_Row_Data_Yield):
            for j, value in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(value))
                self.table_yield_CH_P2.setItem(i, j, table_item)   
                self.table_yield_CH_P2.resizeColumnToContents(j)        
                self.table_yield_CH_P2.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed)
        
        self.table_yield_CH_P2.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #DCFFA1}")
        self.table_yield_CH_P2.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        self.table_yield_CH_P2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table_yield_CH_P2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_yield_CH_P2.verticalHeader().setVisible(True)
        self.table_yield_CH_P2.cellClicked.connect(self.get_data_CH)









        # with open('temp/trigger.txt', 'w') as f:
        #     f.write("1")
        # file_path = "temp\\Loading.exe"
        # os.startfile(file_path)
        # file_path = "temp\\Loading.py"
        # CREATE_NO_WINDOW = 0x08000000
        # subprocess.Popen(["python", file_path], creationflags=CREATE_NO_WINDOW)

        # self.table.clear()
        # day = str(self.day_dropbox_P1.currentText())
        # station = str(self.station_lable_P1.currentText())
        # process = str(self.process_dropbox_P1.currentText())
        # LINECARD_SN = str(self.LC_text.text())
        # CHASSIS_SN = str(self.CH_text.text())

        # Query_LINECARD = QueryLINECARD()
        # Data = Query_LINECARD.input_data(day, station, process, LINECARD_SN, CHASSIS_SN, "By Date")       
        
        # # Set table histoy******************************************************************************
        # self.table.setRowCount(len(Data))
        # header_label = ['STATION_ID', 'SLOT', 'UUT_SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'LINECARD', 'CHASSIS', 'PROCEE', 'MODE']
        # self.table.setColumnCount(len(header_label))
        # self.table.setHorizontalHeaderLabels(header_label)

        # for i, row in enumerate(Data):
        #     for j, value in enumerate(row):
        #         table_item = QtWidgets.QTableWidgetItem(str(value))
        #         self.table.setItem(i, j, table_item)
        #         if j == 4:
        #             if value == 'PASS':
        #                 table_item.setBackground(QtGui.QColor(0,255,0))
        #             else:
        #                 table_item.setBackground(QtGui.QColor(255,0,0))
        #         self.table.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed) # Disable rezeable column width
        
        # self.table.setColumnWidth(1, 12)    # Width column SLOT
        # self.table.setColumnWidth(2, 130)   # Width column UUT_SERIAL_NUMBER
        # self.table.setColumnWidth(3, 110)   # Width column START_DATE_TIME
        # self.table.setColumnWidth(4, 60)    # Width column RESULT
        # self.table.setColumnWidth(5, 75)    # Width column LINECARD
        # self.table.setColumnWidth(6, 75)    # Width column CHASSIS
        # self.table.setColumnWidth(7, 60)    # Width column PROCESS
        # self.table.setColumnWidth(8, 60)    # Width column MODE
        # self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #A1B0FF}")
        # self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        # self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.table.verticalHeader().setVisible(False)
        # self.table.cellClicked.connect(self.get_data_in_cell)

        # if self.tab.currentIndex() == 0:
        #     table_LC = self.table_yield_LC_P1
        #     table_CH = self.table_yield_CH_P1
        #     table_slot = self.table_yield_slot_P1
        # elif self.tab.currentIndex() == 1:
        #     station = str(self.station_lable_P2.currentText())
        #     process = str(self.process_dropbox_P2.currentText())
        #     table_LC = self.table_yield_LC_P2
        #     table_CH = self.table_yield_CH_P2
        #     table_slot = self.table_yield_slot_P2
        #     day = self.day_dropbox_P2.currentText()
        #     day = day.split(" ")
        #     Data = Query_LINECARD.input_data(day[1], station, process, LINECARD_SN, CHASSIS_SN, "By UUT")
        
            
        # # Set table LINECARD yield******************************************************************************
        # SN_LINECARD_Pack = []
        # for i in Data:
        #     if i[5] != '':
        #         SN_LINECARD_Pack.append(i[5])
        # SN_LINECARD_Pack = list(set(SN_LINECARD_Pack))
        
        # SN_LINECARD_Dict = {}
        # pass_LC = 0
        # fail_LC = 0
        # for SN_LC in SN_LINECARD_Pack:
        #     pass_LC = 0
        #     fail_LC = 0
        #     total = 0
        #     percent = 0.00
        #     for group in Data:
        #         if group[5] == SN_LC:
        #             if group[4] == 'PASS':
        #                 pass_LC += 1
        #             else:
        #                 fail_LC += 1
        #             total = pass_LC + fail_LC
        #             percent = (pass_LC/total) * 100
        #             percent = f"{percent: .2f}"
        #         SN_LINECARD_Dict[str(SN_LC)] = (str(total), str(pass_LC), str(fail_LC), str(percent) + " %")

        # if self.condition == "Greater than 70 %":
        #     SN_LINECARD_Array = []
        #     for SN_LC, value in SN_LINECARD_Dict.items():
        #         SN_LINECARD_Array.append((SN_LC, value[0], value[1], value[2], value[3]))
        #     SN_LINECARD_Array = sorted(SN_LINECARD_Array, key=lambda x: float(x[4].strip('%')), reverse=False)
        # elif self.condition == "Less than 70 %":
        #     SN_LINECARD_Dict = {k: v for k, v in SN_LINECARD_Dict.items() if float(v[3].strip('%')) <= 70.00}
        #     SN_LINECARD_Array = []
        #     for SN_LC, value in SN_LINECARD_Dict.items():
        #         SN_LINECARD_Array.append((SN_LC, value[0], value[1], value[2], value[3]))
        
        # header_table_yield = ['LINECARD', 'Input', 'PASS', 'FAIL', 'Yield']
        # table_LC.setColumnCount(len(header_table_yield))
        # table_LC.setHorizontalHeaderLabels(header_table_yield)
        # table_LC.setRowCount(len(SN_LINECARD_Array))

        # for i, row in enumerate(SN_LINECARD_Array):
        #     for j, value in enumerate(row):
        #         table_item = QtWidgets.QTableWidgetItem(str(value))
        #         table_LC.setItem(i, j, table_item)   
        #         table_LC.resizeColumnToContents(j)        
        #         table_LC.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed)
        
        # table_LC.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #DCFFA1}")
        # table_LC.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        # table_LC.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # table_LC.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # table_LC.verticalHeader().setVisible(True)

        # # Set table CHASSSIS yield******************************************************************************
        # product = self.station_lable_P1.currentText().split('_')
        # if product[1] == 'AC100M' or product[1] == 'AC200' or product[1] == 'AC400':
        #     table_CH.clear()
        # else:
        #     SN_CHASSIS_Pack = []
        #     for i in Data:
        #         if i[6] != '':
        #             SN_CHASSIS_Pack.append(i[6])
        #     SN_CHASSIS_Pack = list(set(SN_CHASSIS_Pack))
            
        #     SN_CHASSIS_Dict = {}
        #     pass_CH = 0
        #     fail_CH = 0
        #     for SN_CH in SN_CHASSIS_Pack:
        #         pass_CH = 0
        #         fail_CH = 0
        #         total = 0
        #         percent = 0.00
        #         for group in Data:
        #             if group[6] == SN_CH:
        #                 if group[4] == 'PASS':
        #                     pass_CH += 1
        #                 else:
        #                     fail_CH += 1
        #                 total = pass_CH + fail_CH
        #                 percent = (pass_CH/total) * 100
        #                 percent = f"{percent: .2f}"
        #             SN_CHASSIS_Dict[str(SN_CH)] = (str(total), str(pass_CH), str(fail_CH), str(percent) + " %")

        #     if self.condition == "Greater than 70 %":
        #         SN_CHASSIS_Array = []
        #         for SN_CH, value in SN_CHASSIS_Dict.items():
        #             SN_CHASSIS_Array.append((SN_CH, value[0], value[1], value[2], value[3]))
        #         SN_CHASSIS_Array = sorted(SN_CHASSIS_Array, key=lambda x: float(x[4].strip('%')), reverse=False)
        #     elif self.condition == "Less than 70 %":
        #         SN_CHASSIS_Dict = {k: v for k, v in SN_CHASSIS_Dict.items() if float(v[3].strip('%')) <= 70.00}
        #         SN_CHASSIS_Array = []
        #         for SN_CH, value in SN_CHASSIS_Dict.items():
        #             SN_CHASSIS_Array.append((SN_CH, value[0], value[1], value[2], value[3]))
            
        #     header_table_yield = ['LINECARD', 'Input', 'PASS', 'FAIL', 'Yield']
        #     table_CH.setColumnCount(len(header_table_yield))
        #     table_CH.setHorizontalHeaderLabels(header_table_yield)
        #     table_CH.setRowCount(len(SN_CHASSIS_Array))

        #     for i, row in enumerate(SN_CHASSIS_Array):
        #         for j, value in enumerate(row):
        #             table_item = QtWidgets.QTableWidgetItem(str(value))
        #             table_CH.setItem(i, j, table_item)   
        #             table_CH.resizeColumnToContents(j)        
        #             table_CH.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed)
            
        #     table_CH.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #DCFFA1}")
        #     table_CH.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        #     table_CH.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #     table_CH.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #     table_CH.verticalHeader().setVisible(True)

        # # Set table yield per SLOTs******************************************************************************
        # SLOTs_Array = []
        # for i in Data:
        #     SLOTs_Array.append(i[1])
        # SLOTs_Array = list(set(SLOTs_Array)) # Remove duplice data in array
        # group_slot = []
        # for SLOT in SLOTs_Array:
        #     array = []
        #     for i in Data:
        #         if i[1] == SLOT:
        #             array.append(i)
        #     group_slot.append(array)
        # pass_slot = 0
        # fail_slot = 0
        # percent_slot = 0
        # loop = 0
        # array_yield_per_SLOTs = []
        # for i in group_slot:
        #     pass_slot = 0
        #     fail_slot = 0
        #     percent_slot = 0.00
        #     for val in i:
        #         if val[4] == 'PASS':
        #             pass_slot += 1
        #         else:
        #             fail_slot += 1
        #     total_slot = pass_slot + fail_slot
        #     percent_slot = (pass_slot/total_slot) * 100
        #     percent_slot = f"{percent_slot: .2f}"
            
        #     array_yield_per_SLOTs.append((str(total_slot), str(pass_slot), str(fail_slot), str(percent_slot) + ' %'))
        # array_yield_per_SLOTs_NEW = []   
        # for index, val in enumerate(array_yield_per_SLOTs):
        #     array_yield_per_SLOTs_NEW.append((('SLOT' + str(SLOTs_Array[index])),) + val)

        # table_slot.setRowCount(len(array_yield_per_SLOTs))
        # table_slot.setColumnCount(5)
        # table_slot.setHorizontalHeaderLabels(['SLOT', 'Total', 'Paseed', 'Failed', 'Yield'])

        # for i, row in enumerate(array_yield_per_SLOTs_NEW):
        #     for j, val in enumerate(row):
        #         item_table = QtWidgets.QTableWidgetItem(str(val))
        #         table_slot.setItem(i, j, item_table)

        # table_slot.resizeColumnsToContents()
        # table_slot.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFEBBE}")
        # table_slot.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
        # table_slot.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # table_slot.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # table_slot.verticalHeader().setVisible(False)
        # table_slot.horizontalHeader().setVisible(True)

        # with open('temp/trigger.txt', 'w') as f:
        #     f.write("0")

    def get_data_LC(self, row, column):
        item = self.table_yield_LC_P2.item(row, column)
        if item is not None:
            if column == 0:
                data = item.text()

                Query_LINECARD = QueryLINECARD()
                Get_Data = Query_LINECARD.input_data("10", self.Station_ID_LC[row], "", str(data), "", "By UUT") # Need to define station name to get product type (such as "ATE_AC1200_132", pruduct type is "AC1200")
                self.table.setRowCount(len(Get_Data))
                header_label = ['STATION_ID', 'SLOT', 'UUT_SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'LINECARD', 'CHASSIS', 'PROCEE', 'MODE']
                self.table.setColumnCount(len(header_label))
                self.table.setHorizontalHeaderLabels(header_label)

                for i, row in enumerate(Get_Data):
                    for j, value in enumerate(row):
                        table_item = QtWidgets.QTableWidgetItem(str(value))
                        self.table.setItem(i, j, table_item)
                        if j == 4:
                            if value == 'PASS':
                                table_item.setBackground(QtGui.QColor(0,255,0))
                            else:
                                table_item.setBackground(QtGui.QColor(255,0,0))
                        self.table.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed) # Disable rezeable column width
                
                self.table.setColumnWidth(1, 12)    # Width column SLOT
                self.table.setColumnWidth(2, 130)   # Width column UUT_SERIAL_NUMBER
                self.table.setColumnWidth(3, 110)   # Width column START_DATE_TIME
                self.table.setColumnWidth(4, 60)    # Width column RESULT
                self.table.setColumnWidth(5, 75)    # Width column LINECARD
                self.table.setColumnWidth(6, 75)    # Width column CHASSIS
                self.table.setColumnWidth(7, 60)    # Width column PROCESS
                self.table.setColumnWidth(8, 60)    # Width column MODE
                self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #A1B0FF}")
                self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
                self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.table.verticalHeader().setVisible(False)

    def get_data_CH(self, row, column):
        item = self.table_yield_CH_P2.item(row, column)
        if item is not None:
            if column == 0:
                data = item.text()

                Query_LINECARD = QueryLINECARD()
                Get_Data = Query_LINECARD.input_data("10", self.Station_ID_CH[row], "", "", str(data), "By UUT")
                self.table.setRowCount(len(Get_Data))
                header_label = ['STATION_ID', 'SLOT', 'UUT_SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'LINECARD', 'CHASSIS', 'PROCEE', 'MODE']
                self.table.setColumnCount(len(header_label))
                self.table.setHorizontalHeaderLabels(header_label)

                for i, row in enumerate(Get_Data):
                    for j, value in enumerate(row):
                        table_item = QtWidgets.QTableWidgetItem(str(value))
                        self.table.setItem(i, j, table_item)
                        if j == 4:
                            if value == 'PASS':
                                table_item.setBackground(QtGui.QColor(0,255,0))
                            else:
                                table_item.setBackground(QtGui.QColor(255,0,0))
                        self.table.horizontalHeader().setSectionResizeMode(j, QtWidgets.QHeaderView.Fixed) # Disable rezeable column width
                
                self.table.setColumnWidth(1, 12)    # Width column SLOT
                self.table.setColumnWidth(2, 130)   # Width column UUT_SERIAL_NUMBER
                self.table.setColumnWidth(3, 110)   # Width column START_DATE_TIME
                self.table.setColumnWidth(4, 60)    # Width column RESULT
                self.table.setColumnWidth(5, 75)    # Width column LINECARD
                self.table.setColumnWidth(6, 75)    # Width column CHASSIS
                self.table.setColumnWidth(7, 60)    # Width column PROCESS
                self.table.setColumnWidth(8, 60)    # Width column MODE
                self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #A1B0FF}")
                self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")   
                self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                self.table.verticalHeader().setVisible(False)
        # if item is not None:
        #     if column == 5:
        #         data = item.text()
        #         self.LC_text.setText(data)
        #         self.CH_text.setText('')
        #     elif column == 6:
        #         data = item.text()
        #         self.CH_text.setText(data)
        #         self.LC_text.setText('')
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()