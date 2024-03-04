from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QButtonGroup, QProgressBar, QWidget, QTabWidget, QRadioButton ,QPushButton, QLineEdit, QLabel, QTableWidget, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
import os
import sys
from Query_LINECARD import QueryLINECARD

class MyGUI_First(QtWidgets.QMainWindow):
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

        # Creat dropdown process (Page_1)
        process_label_P1 = QLabel("Select Process", page_1)
        process_label_P1.move(395,18)
        self.process_dropbox_P1 = QComboBox(page_1)
        Array_Process = ['OIT', 'PCAL', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5']
        for i in Array_Process:
            self.process_dropbox_P1.addItem(i)
        self.process_dropbox_P1.setGeometry(470, 10, 50, 30)

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

        self.setGeometry(200, 50, 0, 0)
        self.setFixedSize(1345,635)

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
            station_LC = list(set(station_LC))
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
            station_CH = list(set(station_CH))
            self.Station_ID_CH.extend(station_CH)

        seen_LC = set()
        unique_arrays_LC = []
        for array in Array_LC_Row_Data_Yield:
            array_tuple = tuple(array)  # Convert array to tuple since lists are unhashable
            if array_tuple not in seen_LC:
                seen_LC.add(array_tuple)
                unique_arrays_LC.append(tuple(array))

        seen_CH = set()
        unique_arrays_CH = []
        for array in Array_CH_Row_Data_Yield:
            array_tuple = tuple(array)  # Convert array to tuple since lists are unhashable
            if array_tuple not in seen_CH:
                seen_CH.add(array_tuple)
                unique_arrays_CH.append(tuple(array))

        Array_LC_Row_Data_Yield = unique_arrays_LC
        Array_CH_Row_Data_Yield = unique_arrays_CH

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
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = MyGUI_First()
    gui.show()
    app.exec_()