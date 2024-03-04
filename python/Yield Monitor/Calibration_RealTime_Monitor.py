import pyodbc
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QAbstractItemView, QScrollArea, QProgressBar, QTabWidget, QAction, QHeaderView, QLabel, QComboBox, QPushButton, QWidget, QButtonGroup, QRadioButton, QMenu, QDialog, QVBoxLayout, QTableWidget, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtChart import QChart, QLineSeries, QChartView, QBarCategoryAxis, QValueAxis, QCategoryAxis, QBarSeries, QBarSet, QScatterSeries
from PyQt5.QtGui import QColor, QIcon, QFont, QPainter, QBrush, QPalette, QMovie, QPen, QMovie
import os
import time
import numpy as np
import pandas as pd
import math
import csv
import subprocess
import openpyxl
from datetime import datetime, timedelta
from collections import OrderedDict, defaultdict
from Query_Value_ATE_CAL import QueryValueATECAL
from Query_BaseLine import QueryBaseLine
from Slot_Mapping import SlotMapping
from Prepare_Data_To_Graph import PrepareDataToGraph
from Insert_Data_To_Graph import InsertDataToGraph
from Create_Graph import CreateGraph
from Group_SLOT import GroupSLOT
from Check_Empty_Data import CheckEmptyData
from Add_BaseLine_Limit import AddBaseLineLimit
from Send_Email import SendEmail
from Save_To_Excel import SaveToExcel

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.Main_Tab_Dis = QTabWidget(self)      
        self.Loss_Factor_Page = QWidget()
        self.Main_Tab_Dis.addTab(self.Loss_Factor_Page, "Loss Factor")
        self.Base_Line_Page = QWidget()
        self.Main_Tab_Dis.addTab(self.Base_Line_Page, "Base Line")
        self.LF_Page_400ZR = QWidget()
        for i in range(2):
            self.Main_Tab_Dis.tabBar().setTabVisible(i, False)
        
        self.TAB_Graph_LF = QTabWidget(self.Loss_Factor_Page)
        self.Page_AC1200_LF = QWidget()
        self.TAB_Graph_LF.addTab(self.Page_AC1200_LF, "AC1200 LF")
        self.Page_400ZR_LF = QWidget()
        self.TAB_Graph_LF.addTab(self.Page_400ZR_LF, "400ZR LF")
        for i in range(2):
            self.TAB_Graph_LF.tabBar().setTabVisible(i, False)
        self.TAB_Graph_LF.setGeometry(0, 0, 1805, 985)
        self.TAB_Graph_LF.setCurrentIndex(0)

        self.TAB_Graph_BL = QTabWidget(self.Base_Line_Page)
        self.Page_AC1200_BL = QWidget()
        self.TAB_Graph_BL.addTab(self.Page_AC1200_BL, "AC1200 BL")
        self.Page_400ZR_BL = QWidget()
        self.TAB_Graph_BL.addTab(self.Page_400ZR_BL, "400ZR BL")
        for i in range(2):
            self.TAB_Graph_BL.tabBar().setTabVisible(i, False)
        self.TAB_Graph_BL.setGeometry(0, 0, 1805, 985)
        self.TAB_Graph_BL.setCurrentIndex(0)

        # Create ratio button
        self.button_group_LF_BL = QButtonGroup()
        self.button_group_LF_BL.setExclusive(True)

        self.LF_Page = QRadioButton("Loss Factor Page", self)
        self.LF_Page.setGeometry(560,30,150,20)
        self.BL_Page = QRadioButton("Base Line Page", self)
        self.BL_Page.setChecked(True)
        self.BL_Page.setGeometry(720,30,150,20)

        self.button_group_LF_BL.addButton(self.LF_Page)
        self.button_group_LF_BL.addButton(self.BL_Page)

        self.LF_Page.clicked.connect(lambda: self.radio_update(page=0))
        self.BL_Page.clicked.connect(lambda: self.radio_update(page=1))
        self.Main_Tab_Dis.setCurrentIndex(1)

        # Creat Ratio button to send email
        self.button_group_email = QButtonGroup()
        self.button_group_email.setExclusive(True)

        self.email = QRadioButton("Send Email", self)
        self.email.setVisible(False) # Hide
        self.email.setGeometry(1010,30,160,20)      
        self.not_email = QRadioButton("NOT Send Email", self)
        self.not_email.setChecked(True)
        self.not_email.setVisible(False) # Hide
        self.not_email.setGeometry(1160,30,190,20)

        self.email.clicked.connect(self.Plot_Graph)
        self.not_email.clicked.connect(self.Plot_Graph)

        self.button_group_email.addButton(self.email)
        self.button_group_email.addButton(self.not_email)

        # Create ratio button for page LOSS_FACTOR, TAB_POWER, UUT_POWER
        self.button_group_page = QButtonGroup()
        self.button_group_page.setExclusive(True)

        self.loss_factor_page = QRadioButton("Loss Factor Page", self)
        self.loss_factor_page.setChecked(True)
        self.loss_factor_page.move(25, 60)
        self.tap_power_page = QRadioButton("Tab Power Page", self)
        self.tap_power_page.move(145, 60)    
        self.uut_power_page = QRadioButton("UUT Power Page", self)
        self.uut_power_page.move(260, 60)

        self.button_group_page.addButton(self.loss_factor_page)
        self.button_group_page.addButton(self.tap_power_page)
        self.button_group_page.addButton(self.uut_power_page)

        self.loss_factor_page.clicked.connect(self.Plot_Graph)
        self.tap_power_page.clicked.connect(self.Plot_Graph)
        self.uut_power_page.clicked.connect(self.Plot_Graph)

        # Creat Text Box shown last Base Line changed
        font_L = QFont()
        font_L.setBold(True)
        last_BL_changed = QLabel("Date last Base Line changed", self)
        last_BL_changed.setGeometry(1390, 31, 240, 20)
        last_BL_changed.setFont(font_L)

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.data_last_BL_changed = QLineEdit("", self)
        self.data_last_BL_changed.setGeometry(1626, 27, 170, 30)
        self.data_last_BL_changed.setAlignment(Qt.AlignCenter)
        self.data_last_BL_changed.setFont(font)
        self.data_last_BL_changed.setStyleSheet("background-color: red; color: yellow")

        # Creat dropdown day
        day_label = QLabel("Select Day", self)
        day_label.move(23,22)
        self.day_dropbox_dis = QComboBox(self)
        self.day_dropbox_dis.addItem("1")
        self.day_dropbox_dis.addItem("2")
        self.day_dropbox_dis.addItem("3")
        self.day_dropbox_dis.addItem("5")
        self.day_dropbox_dis.addItem("7")
        self.day_dropbox_dis.addItem("14")
        self.day_dropbox_dis.addItem("30")
        self.day_dropbox_dis.addItem("60")
        self.day_dropbox_dis.addItem("90")
        self.day_dropbox_dis.addItem("180")
        self.day_dropbox_dis.move(110,24)
        self.day_dropbox_dis.setFixedSize(50,30)

        self.day_dropbox_dis.currentTextChanged.connect(self.Plot_Graph)

        file = open("temp/STATION_ID (for CAL).txt", "r")
        file_read = file.read()
        All_STATION_Array = file_read.split('\n')
        self.STATION_Label = QLabel("Select STATION", self)
        self.STATION_Label.setGeometry(170,30,160,20)
        self.STATION_dropbox = QComboBox(self)
        self.STATION_dropbox.move(290,24)
        self.STATION_dropbox.setFixedSize(160,30)  
        for i in All_STATION_Array:
            self.STATION_dropbox.addItem(i)   
        self.STATION_dropbox.currentIndexChanged.connect(self.Station_Mapping)

        # Create button
        self.query_button = QPushButton("Refresh", self)     
        self.query_button.move(465,23)
        self.query_button.setFixedSize(80, 32)
        self.query_button.clicked.connect(self.Plot_Graph)

        # Create Graph Loss Factor (AC1200)*******************************************************
        Create_Graph = CreateGraph()
        self.SL0_AC1200_LF = Create_Graph.input_detail(10, 65, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT0_LF = self.SL0_AC1200_LF[0]
        self.Graph_AC1200_SLOT0_View_LF = self.SL0_AC1200_LF[1]
        self.SL1_AC1200_LF = Create_Graph.input_detail(615, 65, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT1_LF = self.SL1_AC1200_LF[0]
        self.Graph_AC1200_SLOT1_View_LF = self.SL1_AC1200_LF[1]
        self.SL2_AC1200_LF = Create_Graph.input_detail(1220, 65, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT2_LF = self.SL2_AC1200_LF[0]
        self.Graph_AC1200_SLOT2_View_LF = self.SL2_AC1200_LF[1]
        self.SL3_AC1200_LF = Create_Graph.input_detail(10, 370, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT3_LF = self.SL3_AC1200_LF[0]
        self.Graph_AC1200_SLOT3_View_LF = self.SL3_AC1200_LF[1]
        self.SL4_AC1200_LF = Create_Graph.input_detail(615, 370, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT4_LF = self.SL4_AC1200_LF[0]
        self.Graph_AC1200_SLOT4_View_LF = self.SL4_AC1200_LF[1]
        self.SL5_AC1200_LF = Create_Graph.input_detail(1220, 370, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT5_LF = self.SL5_AC1200_LF[0]
        self.Graph_AC1200_SLOT5_View_LF = self.SL5_AC1200_LF[1]
        self.SL6_AC1200_LF = Create_Graph.input_detail(10, 665, 600, 300, self.Page_AC1200_LF, False)
        self.Graph_AC1200_SLOT6_LF = self.SL6_AC1200_LF[0]
        self.Graph_AC1200_SLOT6_View_LF = self.SL6_AC1200_LF[1]

        # Create Graph Loss Factor (400ZR)*******************************************************
        self.SL0_400ZR_LF = Create_Graph.input_detail(10, 55, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT0_LF = self.SL0_400ZR_LF[0]
        self.Graph_400ZR_SLOT0_View_LF = self.SL0_400ZR_LF[1]
        self.SL1_400ZR_LF = Create_Graph.input_detail(455, 55, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT1_LF = self.SL1_400ZR_LF[0]
        self.Graph_400ZR_SLOT1_View_LF = self.SL1_400ZR_LF[1]
        self.SL2_400ZR_LF = Create_Graph.input_detail(900, 55, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT2_LF = self.SL2_400ZR_LF[0]
        self.Graph_400ZR_SLOT2_View_LF = self.SL2_400ZR_LF[1]
        self.SL3_400ZR_LF = Create_Graph.input_detail(1345, 55, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT3_LF = self.SL3_400ZR_LF[0]
        self.Graph_400ZR_SLOT3_View_LF = self.SL3_400ZR_LF[1]
        self.SL4_400ZR_LF = Create_Graph.input_detail(10, 360, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT4_LF = self.SL4_400ZR_LF[0]
        self.Graph_400ZR_SLOT4_View_LF = self.SL4_400ZR_LF[1]
        self.SL5_400ZR_LF = Create_Graph.input_detail(455, 360, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT5_LF = self.SL5_400ZR_LF[0]
        self.Graph_400ZR_SLOT5_View_LF = self.SL5_400ZR_LF[1]
        self.SL6_400ZR_LF = Create_Graph.input_detail(900, 360, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT6_LF = self.SL6_400ZR_LF[0]
        self.Graph_400ZR_SLOT6_View_LF = self.SL6_400ZR_LF[1]
        self.SL7_400ZR_LF = Create_Graph.input_detail(1345, 360, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT7_LF = self.SL7_400ZR_LF[0]
        self.Graph_400ZR_SLOT7_View_LF = self.SL7_400ZR_LF[1]
        self.SL8_400ZR_LF = Create_Graph.input_detail(10, 675, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT8_LF = self.SL8_400ZR_LF[0]
        self.Graph_400ZR_SLOT8_View_LF = self.SL8_400ZR_LF[1]
        self.SL9_400ZR_LF = Create_Graph.input_detail(455, 675, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT9_LF = self.SL9_400ZR_LF[0]
        self.Graph_400ZR_SLOT9_View_LF = self.SL9_400ZR_LF[1]
        self.SL10_400ZR_LF = Create_Graph.input_detail(900, 675, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT10_LF = self.SL10_400ZR_LF[0]
        self.Graph_400ZR_SLOT10_View_LF = self.SL10_400ZR_LF[1]
        self.SL11_400ZR_LF = Create_Graph.input_detail(1345, 675, 440, 300, self.Page_400ZR_LF, False)
        self.Graph_400ZR_SLOT11_LF = self.SL11_400ZR_LF[0]
        self.Graph_400ZR_SLOT11_View_LF = self.SL11_400ZR_LF[1]
            
        # Create Graph Base Line (AC1200)*******************************************************
        Create_Graph = CreateGraph()
        self.SL0_AC1200_BL = Create_Graph.input_detail(10, 55, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT0_BL = self.SL0_AC1200_BL[0]
        self.Graph_AC1200_SLOT0_View_BL = self.SL0_AC1200_BL[1]
        self.SL1_AC1200_BL = Create_Graph.input_detail(615, 55, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT1_BL = self.SL1_AC1200_BL[0]
        self.Graph_AC1200_SLOT1_View_BL = self.SL1_AC1200_BL[1]
        self.SL2_AC1200_BL = Create_Graph.input_detail(1220, 55, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT2_BL = self.SL2_AC1200_BL[0]
        self.Graph_AC1200_SLOT2_View_BL = self.SL2_AC1200_BL[1]
        self.SL3_AC1200_BL = Create_Graph.input_detail(10, 360, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT3_BL = self.SL3_AC1200_BL[0]
        self.Graph_AC1200_SLOT3_View_BL = self.SL3_AC1200_BL[1]
        self.SL4_AC1200_BL = Create_Graph.input_detail(615, 360, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT4_BL = self.SL4_AC1200_BL[0]
        self.Graph_AC1200_SLOT4_View_BL = self.SL4_AC1200_BL[1]
        self.SL5_AC1200_BL = Create_Graph.input_detail(1220, 360, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT5_BL = self.SL5_AC1200_BL[0]
        self.Graph_AC1200_SLOT5_View_BL = self.SL5_AC1200_BL[1]
        self.SL6_AC1200_BL = Create_Graph.input_detail(10, 675, 600, 300, self.Page_AC1200_BL, False)
        self.Graph_AC1200_SLOT6_BL = self.SL6_AC1200_BL[0]
        self.Graph_AC1200_SLOT6_View_BL = self.SL6_AC1200_BL[1]

        # Create Graph Base Line (400ZR)*******************************************************
        self.SL0_400ZR_BL = Create_Graph.input_detail(10, 55, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT0_BL = self.SL0_400ZR_BL[0]
        self.Graph_400ZR_SLOT0_View_BL = self.SL0_400ZR_BL[1]
        self.SL1_400ZR_BL = Create_Graph.input_detail(455, 55, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT1_BL = self.SL1_400ZR_BL[0]
        self.Graph_400ZR_SLOT1_View_BL = self.SL1_400ZR_BL[1]
        self.SL2_400ZR_BL = Create_Graph.input_detail(900, 55, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT2_BL = self.SL2_400ZR_BL[0]
        self.Graph_400ZR_SLOT2_View_BL = self.SL2_400ZR_BL[1]
        self.SL3_400ZR_BL = Create_Graph.input_detail(1345, 55, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT3_BL = self.SL3_400ZR_BL[0]
        self.Graph_400ZR_SLOT3_View_BL = self.SL3_400ZR_BL[1]
        self.SL4_400ZR_BL = Create_Graph.input_detail(10, 360, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT4_BL = self.SL4_400ZR_BL[0]
        self.Graph_400ZR_SLOT4_View_BL = self.SL4_400ZR_BL[1]
        self.SL5_400ZR_BL = Create_Graph.input_detail(455, 360, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT5_BL = self.SL5_400ZR_BL[0]
        self.Graph_400ZR_SLOT5_View_BL = self.SL5_400ZR_BL[1]
        self.SL6_400ZR_BL = Create_Graph.input_detail(900, 360, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT6_BL = self.SL6_400ZR_BL[0]
        self.Graph_400ZR_SLOT6_View_BL = self.SL6_400ZR_BL[1]
        self.SL7_400ZR_BL = Create_Graph.input_detail(1345, 360, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT7_BL = self.SL7_400ZR_BL[0]
        self.Graph_400ZR_SLOT7_View_BL = self.SL7_400ZR_BL[1]
        self.SL8_400ZR_BL = Create_Graph.input_detail(10, 675, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT8_BL = self.SL8_400ZR_BL[0]
        self.Graph_400ZR_SLOT8_View_BL = self.SL8_400ZR_BL[1]
        self.SL9_400ZR_BL = Create_Graph.input_detail(455, 675, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT9_BL = self.SL9_400ZR_BL[0]
        self.Graph_400ZR_SLOT9_View_BL = self.SL9_400ZR_BL[1]
        self.SL10_400ZR_BL = Create_Graph.input_detail(900, 675, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT10_BL = self.SL10_400ZR_BL[0]
        self.Graph_400ZR_SLOT10_View_BL = self.SL10_400ZR_BL[1]
        self.SL11_400ZR_BL = Create_Graph.input_detail(1345, 675, 440, 300, self.Page_400ZR_BL, False)
        self.Graph_400ZR_SLOT11_BL = self.SL11_400ZR_BL[0]
        self.Graph_400ZR_SLOT11_View_BL = self.SL11_400ZR_BL[1]

        self.distribute_plot = QPushButton("Plot Distribute", self)
        self.distribute_plot.setGeometry(870,25,130,30)
        self.distribute_plot.clicked.connect(self.plot_distribution)     

        # Create Graph Right-Click Loss Factor (AC1200)*******************************************************
        self.Array_Graph_AC1200_LF = [self.Graph_AC1200_SLOT0_LF,self.Graph_AC1200_SLOT1_LF,self.Graph_AC1200_SLOT2_LF,self.Graph_AC1200_SLOT3_LF,self.Graph_AC1200_SLOT4_LF,self.Graph_AC1200_SLOT5_LF,self.Graph_AC1200_SLOT6_LF]
        self.Array_Graph_AC1200_View_LF = [self.Graph_AC1200_SLOT0_View_LF,self.Graph_AC1200_SLOT1_View_LF,self.Graph_AC1200_SLOT2_View_LF,self.Graph_AC1200_SLOT3_View_LF,self.Graph_AC1200_SLOT4_View_LF,self.Graph_AC1200_SLOT5_View_LF,self.Graph_AC1200_SLOT6_View_LF]
        self.Array_Graph_400ZR_LF = [self.Graph_400ZR_SLOT0_LF,self.Graph_400ZR_SLOT1_LF,self.Graph_400ZR_SLOT2_LF,self.Graph_400ZR_SLOT3_LF,self.Graph_400ZR_SLOT4_LF,self.Graph_400ZR_SLOT5_LF,self.Graph_400ZR_SLOT6_LF,self.Graph_400ZR_SLOT7_LF,self.Graph_400ZR_SLOT8_LF,self.Graph_400ZR_SLOT9_LF,self.Graph_400ZR_SLOT10_LF,self.Graph_400ZR_SLOT11_LF]
        self.Array_Graph_400ZR_View_LF = [self.Graph_400ZR_SLOT0_View_LF,self.Graph_400ZR_SLOT1_View_LF,self.Graph_400ZR_SLOT2_View_LF,self.Graph_400ZR_SLOT3_View_LF,self.Graph_400ZR_SLOT4_View_LF,self.Graph_400ZR_SLOT5_View_LF,self.Graph_400ZR_SLOT6_View_LF,self.Graph_400ZR_SLOT7_View_LF,self.Graph_400ZR_SLOT8_View_LF,self.Graph_400ZR_SLOT9_View_LF,self.Graph_400ZR_SLOT10_View_LF,self.Graph_400ZR_SLOT11_View_LF]
        
        for i, j in zip(self.Array_Graph_AC1200_LF, self.Array_Graph_AC1200_View_LF):
            j.setContextMenuPolicy(Qt.CustomContextMenu)
            j.customContextMenuRequested.connect(lambda pos, chart_view_in=j, chart_in=i, menu=['See Raw Data','Expand Graph']: self.right_clicked(pos, chart_view_in, chart_in, menu))
        for i, j in zip(self.Array_Graph_400ZR_LF, self.Array_Graph_400ZR_View_LF):
            j.setContextMenuPolicy(Qt.CustomContextMenu)
            j.customContextMenuRequested.connect(lambda pos, chart_view_in=j, chart_in=i, menu=['See Raw Data','Expand Graph']: self.right_clicked(pos, chart_view_in, chart_in, menu))

        # Create Graph Right-Click Loss Factor (400ZR)*******************************************************
        self.Array_Graph_AC1200_BL = [self.Graph_AC1200_SLOT0_BL,self.Graph_AC1200_SLOT1_BL,self.Graph_AC1200_SLOT2_BL,self.Graph_AC1200_SLOT3_BL,self.Graph_AC1200_SLOT4_BL,self.Graph_AC1200_SLOT5_BL,self.Graph_AC1200_SLOT6_BL]
        self.Array_Graph_AC1200_View_BL = [self.Graph_AC1200_SLOT0_View_BL,self.Graph_AC1200_SLOT1_View_BL,self.Graph_AC1200_SLOT2_View_BL,self.Graph_AC1200_SLOT3_View_BL,self.Graph_AC1200_SLOT4_View_BL,self.Graph_AC1200_SLOT5_View_BL,self.Graph_AC1200_SLOT6_View_BL]
        self.Array_Graph_400ZR_BL = [self.Graph_400ZR_SLOT0_BL,self.Graph_400ZR_SLOT1_BL,self.Graph_400ZR_SLOT2_BL,self.Graph_400ZR_SLOT3_BL,self.Graph_400ZR_SLOT4_BL,self.Graph_400ZR_SLOT5_BL,self.Graph_400ZR_SLOT6_BL,self.Graph_400ZR_SLOT7_BL,self.Graph_400ZR_SLOT8_BL,self.Graph_400ZR_SLOT9_BL,self.Graph_400ZR_SLOT10_BL,self.Graph_400ZR_SLOT11_BL]
        self.Array_Graph_400ZR_View_BL = [self.Graph_400ZR_SLOT0_View_BL,self.Graph_400ZR_SLOT1_View_BL,self.Graph_400ZR_SLOT2_View_BL,self.Graph_400ZR_SLOT3_View_BL,self.Graph_400ZR_SLOT4_View_BL,self.Graph_400ZR_SLOT5_View_BL,self.Graph_400ZR_SLOT6_View_BL,self.Graph_400ZR_SLOT7_View_BL,self.Graph_400ZR_SLOT8_View_BL,self.Graph_400ZR_SLOT9_View_BL,self.Graph_400ZR_SLOT10_View_BL,self.Graph_400ZR_SLOT11_View_BL]

        for i, j in zip(self.Array_Graph_AC1200_BL, self.Array_Graph_AC1200_View_BL):
            j.setContextMenuPolicy(Qt.CustomContextMenu)
            j.customContextMenuRequested.connect(lambda pos, chart_view_in=j, chart_in=i, menu=['See Raw Data','Expand Graph','Setting Limit']: self.right_clicked(pos, chart_view_in, chart_in, menu))
        for i, j in zip(self.Array_Graph_400ZR_BL, self.Array_Graph_400ZR_View_BL):
            j.setContextMenuPolicy(Qt.CustomContextMenu)
            j.customContextMenuRequested.connect(lambda pos, chart_view_in=j, chart_in=i, menu=['See Raw Data','Expand Graph','Setting Limit']: self.right_clicked(pos, chart_view_in, chart_in, menu))
        
        self.email_active = False
        self.loss_factor_page.setVisible(False)
        self.tap_power_page.setVisible(False)  
        self.uut_power_page.setVisible(False)
        self.TAB_Graph_LF.setCurrentIndex(1)
        self.TAB_Graph_BL.setCurrentIndex(1)
        self.station_id = ['ATE','400ZR','242']
        self.x_axis_graph = []
        self.Main_Tab_Dis.setGeometry(10,10,1840,990)
        self.setGeometry(30,40,0,0)
        self.setFixedSize(1820,1005)
    
    def plot_distribution(self):
        if len(self.x_axis_graph) > 0:
            dialog = QDialog(self)

            self.dis_chart = QChart()
            self.dis_chart_view = QChartView(self.dis_chart, dialog)
            self.dis_chart.removeAllSeries()

            Dis_LF_Page = QRadioButton("Loss Factor Page", dialog)
            Dis_LF_Page.setChecked(True)
            Dis_LF_Page.move(25, 25)
            Dis_BL_Page = QRadioButton("Base Line Page", dialog)
            Dis_BL_Page.move(150, 25)

            Dis_LF_Page.clicked.connect(lambda: self.LF_BL_Data(self.data_for_dis_plot_LF))
            Dis_BL_Page.clicked.connect(lambda: self.LF_BL_Data(self.data_for_dis_plot_BL))

            self.table = QtWidgets.QTableWidget(dialog)

            if self.station_id[1] == 'AC1200' or self.station_id[1] == 'AX1200':
                row_header = ['','', 'TX_LANE0', 'RX_LANE0', 'TX_LANE1', 'RX_LANE0']
                if self.station_id[2] == '132' or self.station_id[1] == '182' or self.station_id[1] == '256' or self.station_id[1] == '266':
                    Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2']
                else:
                    Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2','SLOT3', 'SLOT4', 'SLOT5', 'SLOT6']
            elif self.station_id[1] == '400ZR':
                row_header = ['','', 'TX_LANE0', 'RX_LANE0']
                Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2','SLOT3', 'SLOT4', 'SLOT5', 'SLOT6', 'SLOT7', 'SLOT8','SLOT9', 'SLOT10', 'SLOT11']

            serie_dict = {}
            group_data = []
            loop = 0
            x_index = 0
            run_num = 0

            for data_dict in self.data_for_dis_plot_LF:
                series_name = data_dict['name'] # Serie name
                series = QScatterSeries()
                series.setMarkerSize(11)               
                for point in data_dict['data']:   
                    if loop == len(self.x_axis_graph):
                        loop = 0
                        x_index += 1  
                    if run_num == len(data_dict['data']):
                        x_index = 0
                        run_num = 0       
                    if point != '':                     
                        series.append(x_index, float(point))
                        group_data.append(float(point))  
                    else:
                        series.append(x_index, np.nan) 
                    loop += 1     
                    run_num += 1
                series.setName(series_name)
                self.dis_chart.addSeries(series)
                serie_dict[series_name] = series         

            self.dis_chart.createDefaultAxes()
            self.dis_chart.axisX().hide()

            self.dis_chart.setTitle("Distribution Plot (" + str(self.STATION_dropbox.currentText()) + ")")
            self.y_axis = self.dis_chart.axisY()
            self.y_axis.setRange((min(group_data)-0.25), (max(group_data)+0.25))

            self.x_axis = QCategoryAxis()
            for i, name in enumerate(Array_X_Axis_Name):
                self.x_axis.setLabelsPosition(i+1) 
                self.x_axis.append(name, i+1)
            self.x_axis.setRange(-0.25, len(Array_X_Axis_Name) - 0.75)
            self.dis_chart.addAxis(self.x_axis, Qt.AlignBottom)
            for i in serie_dict.values():          
                i.attachAxis(self.x_axis)

            self.table.clearContents()
            self.table.setRowCount(len(row_header))
            self.table.setVerticalHeaderLabels(row_header)

            index = 0
            column_header = []
            for i in range(len(self.x_axis_graph) * len(Array_X_Axis_Name)):
                if index == len(self.x_axis_graph):
                    index = 0
                column_header.append(self.x_axis_graph[index])
                index += 1

            self.table.setColumnCount(len(column_header))
            cell = 0
            for col in range(len(Array_X_Axis_Name)):        
                self.table.setItem(0, cell, QtWidgets.QTableWidgetItem(str(Array_X_Axis_Name[col])))
                self.table.item(0, cell).setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.item(0, cell).setBackground(QtGui.QColor(245, 255, 0))
                self.table.setSpan(0, cell, 1, len(self.x_axis_graph))
                cell += len(self.x_axis_graph)

            for col in range(len(column_header)):
                self.table.setItem(1, col, QtWidgets.QTableWidgetItem(str(column_header[col])))
                self.table.item(1, col).setForeground(QtGui.QColor(255, 255, 255))
                self.table.item(1, col).setBackground(QtGui.QColor(0, 39, 255))

            for row, item in enumerate(self.data_for_dis_plot_LF):
                for col, value in enumerate(item['data']):                  
                    self.table.setItem(row + 2, col, QtWidgets.QTableWidgetItem(str(value)))

            self.table.horizontalHeader().setVisible(False)
            self.table.verticalHeader().setStyleSheet("QHeaderView::section{background-color: #00FF06}")
            self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")

            self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.table.customContextMenuRequested.connect(self.export)
            
            self.dis_chart_view.move(10,10)
            self.dis_chart_view.setFixedSize(1780,680)
            self.table.move(10,690)
            self.table.setFixedSize(1780,200)
            dialog.setGeometry(30,70,1800,900)
            dialog.show()

        else:
            QMessageBox.information(self, "Notify", "Have no any data found")
            
    def LF_BL_Data(self, data_in):
        self.dis_chart.removeAllSeries()
        if self.station_id[1] == 'AC1200' or self.station_id[1] == 'AX1200':
            row_header = ['','', 'TX_LANE0', 'RX_LANE0', 'TX_LANE1', 'RX_LANE0']
            if self.station_id[2] == '132' or self.station_id[1] == '182' or self.station_id[1] == '256' or self.station_id[1] == '266':
                Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2']
            else:
                Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2','SLOT3', 'SLOT4', 'SLOT5', 'SLOT6']
        elif self.station_id[1] == '400ZR':
            row_header = ['','', 'TX_LANE0', 'RX_LANE0']
            Array_X_Axis_Name = ['SLOT0', 'SLOT1', 'SLOT2','SLOT3', 'SLOT4', 'SLOT5', 'SLOT6', 'SLOT7', 'SLOT8','SLOT9', 'SLOT10', 'SLOT11']

        serie_dict = {}
        group_data = []
        loop = 0
        x_index = 0
        run_num = 0
        for data_dict in data_in:
            series_name = data_dict['name'] # Serie name
            series = QScatterSeries()
            series.setMarkerSize(11)               
            for point in data_dict['data']:   
                if loop == len(self.x_axis_graph):
                    loop = 0
                    x_index += 1  
                if run_num == len(data_dict['data']):
                    x_index = 0
                    run_num = 0       
                if point != '':                     
                    series.append(x_index, float(point))
                    group_data.append(float(point))  
                else:
                    series.append(x_index, np.nan) 
                loop += 1     
                run_num += 1
            series.setName(series_name)
            self.dis_chart.addSeries(series)
            serie_dict[series_name] = series         

        self.dis_chart.createDefaultAxes()
        self.dis_chart.axisX().hide()

        self.dis_chart.setTitle("Distribution Plot (" + str(self.STATION_dropbox.currentText()) + ")")
        self.y_axis = self.dis_chart.axisY()
        self.y_axis.setRange((min(group_data)-0.25), (max(group_data)+0.25))

        self.x_axis = QCategoryAxis()
        for i, name in enumerate(Array_X_Axis_Name):
            self.x_axis.setLabelsPosition(i+1) 
            self.x_axis.append(name, i+1)
        self.x_axis.setRange(-0.25, len(Array_X_Axis_Name) - 0.75)
        self.dis_chart.addAxis(self.x_axis, Qt.AlignBottom)
        for i in serie_dict.values():          
            i.attachAxis(self.x_axis)

        self.table.clearContents()
        self.table.setRowCount(len(row_header))
        self.table.setVerticalHeaderLabels(row_header)

        index = 0
        column_header = []
        for i in range(len(self.x_axis_graph) * len(Array_X_Axis_Name)):
            if index == len(self.x_axis_graph):
                index = 0
            column_header.append(self.x_axis_graph[index])
            index += 1

        self.table.setColumnCount(len(column_header))
        cell = 0
        for col in range(len(Array_X_Axis_Name)):        
            self.table.setItem(0, cell, QtWidgets.QTableWidgetItem(str(Array_X_Axis_Name[col])))
            self.table.item(0, cell).setTextAlignment(QtCore.Qt.AlignCenter)
            self.table.item(0, cell).setBackground(QtGui.QColor(245, 255, 0))
            self.table.setSpan(0, cell, 1, len(self.x_axis_graph))
            cell += len(self.x_axis_graph)

        for col in range(len(column_header)):
            self.table.setItem(1, col, QtWidgets.QTableWidgetItem(str(column_header[col])))
            self.table.item(1, col).setForeground(QtGui.QColor(255, 255, 255))
            self.table.item(1, col).setBackground(QtGui.QColor(0, 39, 255))

        for row, item in enumerate(data_in):
            for col, value in enumerate(item['data']):                  
                self.table.setItem(row + 2, col, QtWidgets.QTableWidgetItem(str(value)))

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setStyleSheet("QHeaderView::section{background-color: #00FF06}")
        self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")

        self.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.export)
        
    def export(self, position):
        menu = QtWidgets.QMenu(self)
        export_action = menu.addAction("Export to Excel")
        action = menu.exec_(self.table.mapToGlobal(position))
        if action == export_action:
            rows = self.table.rowCount()
            columns = self.table.columnCount()

            data = []
            for row in range(rows):
                row_data = []
                row_header = self.table.verticalHeaderItem(row).text()
                row_data.append(row_header)
                for column in range(columns):
                    item = self.table.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                data.append(row_data)

            df = pd.DataFrame(data)
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', 'Excel Files (*.xlsx)')

            if file_path:
                try:
                    df.to_excel(file_path, index=False, header=False)

                    # Open file self after saving
                    QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
                except Exception as e:
                    QtWidgets.QMessageBox.warning(self, 'Export Error', f'An error occurred during export: {str(e)}')

    def Station_Mapping (self):       
        for i in (self.Array_Graph_AC1200_LF + self.Array_Graph_AC1200_BL + self.Array_Graph_400ZR_LF + self.Array_Graph_400ZR_BL):
            i.removeAllSeries()

        self.station_id = self.STATION_dropbox.currentText()
        self.station_id = self.station_id.split('_')
        if self.station_id[1] == 'AC1200':
            self.loss_factor_page.setVisible(True)
            self.tap_power_page.setVisible(True)  
            self.uut_power_page.setVisible(True)
            self.TAB_Graph_LF.setCurrentIndex(0)
            self.TAB_Graph_BL.setCurrentIndex(0)
            
        elif self.station_id[1] == '400ZR':
            self.loss_factor_page.setVisible(False)
            self.tap_power_page.setVisible(False)  
            self.uut_power_page.setVisible(False)
            self.TAB_Graph_LF.setCurrentIndex(1)
            self.TAB_Graph_BL.setCurrentIndex(1)
        
        self.Plot_Graph()
    
    def right_clicked(self, pos, chart_view_in, chart_in, menu_in):
        menu = QMenu()
        menu_array = []
        for i in menu_in:
            menu_index = QAction(i, menu)
            menu.addAction(menu_index)
            menu_array.append(menu_index)
        action = menu.exec_(chart_view_in.mapToGlobal(pos))

        if action is not None:
            if action == menu_array[0]:
                data = {}
                for series in chart_in.series():
                    series_data = ()
                    for point in series.pointsVector():
                        x = point.x()
                        y = point.y()
                        series_data = series_data + (y,)
                    data[series.name()] = series_data
                self.Table_Raw_Data(data, self.x_axis_graph)
            elif action == menu_array[1]:
                data = {}
                for series in chart_in.series():
                    series_data = ()
                    for point in series.pointsVector():
                        x = point.x()
                        y = point.y()
                        series_data = series_data + (y,)
                    data[series.name()] = series_data
                self.Expand_Graph(data, chart_in)
            elif action == menu_array[2]:
                self.limit_setting()

    def Table_Raw_Data(self, data_in, row_header):
        if len(self.x_axis_graph) > 0:
            self = QDialog(self)
            layout = QVBoxLayout()
            table = QtWidgets.QTableWidget()
            row_header = row_header[::-1]

            table.setColumnCount(len(list(data_in.keys())))
            table.setRowCount(len(row_header))       
            table.setHorizontalHeaderLabels(list(data_in.keys()))
            table.setVerticalHeaderLabels(row_header)

            for i, (name, val) in enumerate(data_in.items()):
                val = val[::-1]
                for j, values in enumerate(val):
                    item = QtWidgets.QTableWidgetItem(str(values))
                    table.setItem(j, i, item)

            table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #00A6FF}")
            table.verticalHeader().setStyleSheet("QHeaderView::section{background-color: #EDFF00}")
            table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

            layout.addWidget(table)
            self.setLayout(layout)
            self.setWindowTitle("Raw Data")
            self.setGeometry(300,150,0,0)
            self.setFixedSize(740,400)
            self.show()
        else:
            QMessageBox.information(self, "Notify", "Have no any data found")

    def Expand_Graph(self, data_in, graph_in):
        if len(self.x_axis_graph) > 0:
            dialog = QDialog(self)

            layout = QVBoxLayout()
            chart = QChart()
            chart.setTitle(graph_in.title())
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)

            array_val = []
            serie_dict = {}
            serie_index = 0
            for key, values in data_in.items():
                series = QLineSeries()
                series.setName(key)
                series.setPointsVisible(True)
                if len(graph_in.title()) > 10:
                    if self.station_id[1] == 'AC1200':
                        if serie_index == 4 or serie_index == 5:
                            pen = QPen(Qt.black, 2, Qt.DotLine)
                            series.setPen(pen)
                    elif self.station_id[1] == '400ZR':
                        if serie_index == 2 or serie_index == 3:
                            pen = QPen(Qt.black, 2, Qt.DotLine)
                            series.setPen(pen)
                for i in range(len(values)):
                    series.append(i, values[i])
                    array_val.append(values[i])
                chart.addSeries(series)
                serie_dict["series_name"] = series
                serie_index += 1

            chart.createDefaultAxes()
            chart.axisX().hide()
            chart.axisY().hide()       

            x_axis = QCategoryAxis()
            x_axis.setLabelsAngle(-90)
            y_axis = QValueAxis()

            tuple_group = ()
            for index, val in enumerate(data_in["TX_LANE0"]):
                    tuple_group = tuple_group + ((index, val),)
            x = 0    
            for point in tuple_group:  
                if len(self.x_axis_graph) == 1:
                    x_val = point[0]
                else:
                    x_val = point[0]+1
                x_axis.setLabelsPosition(x_val) 
                x_axis.append(self.x_axis_graph[x], x_val)              
                x += 1

            font = QFont()
            font.setPointSize(10)  # Set font size to 10 points

            x_axis.setLabelsFont(font)
            y_axis.setLabelsFont(QFont("Arial", 10))

            x_axis.setRange(-0.5, len(self.x_axis_graph) -0.5)
            if array_val:
                y_axis.setRange((min(array_val)) - 0.2, (max(array_val)) + 0.2)  

            chart.addAxis(x_axis, Qt.AlignBottom)
            chart.addAxis(y_axis, Qt.AlignLeft)
            for i in serie_dict.values():                   
                i.attachAxis(x_axis)
            series.attachAxis(y_axis)            
            
            layout.addWidget(chart_view)
            dialog.setLayout(layout)
            dialog.setGeometry(100,150,1700,800)
            dialog.show()
        else:
            QMessageBox.information(self, "Notify", "Have no any data found")

    def limit_setting(self):
        if len(self.x_axis_graph) > 0:
            dialog = QDialog(self)
            dialog.setWindowTitle('Limit Setting')
            dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
            dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

            font_limit = QFont()
            font_limit.setBold(True)

            label_UCL = QLabel('UCL :', dialog)
            label_UCL.setFont(font_limit)
            label_UCL.move(15, 10)

            label_LCL = QLabel('LCL :', dialog)
            label_LCL.setFont(font_limit)
            label_LCL.move(15, 40)

            file_limit = open('temp/LIMIT.txt', 'r')
            limit_read = file_limit.read()
            limit_read = limit_read.split('\n')

            self.UCL = QLineEdit(str(limit_read[0]), dialog)
            self.UCL.setGeometry(47,7,60,20)
            self.UCL.setAlignment(Qt.AlignCenter)

            self.LCL = QLineEdit(str(limit_read[1]), dialog)
            self.LCL.setGeometry(47,37,60,20)
            self.LCL.setAlignment(Qt.AlignCenter)

            BT = QPushButton("Save", dialog)
            BT.setGeometry(47,67,60,20)
            BT.clicked.connect(self.save_limit)

            dialog.setFixedSize(140,100)
            dialog.show()
        else:
            QMessageBox.information(self, "Notify", "Have no any data found")
            
    def save_limit (self):
        with open('temp/LIMIT.txt', 'w') as f:
            f.write(str(self.UCL.text()) + '\n' + str(self.LCL.text()))
        QMessageBox.information(self, "Notify", "Saved!")

    def radio_update(self, page):
        self.Main_Tab_Dis.setCurrentIndex(page)

    def Plot_Graph(self):
        self.day_selected = self.day_dropbox_dis.currentText()
        self.station_selected = self.STATION_dropbox.currentText()

        if self.email.isChecked():
            self.email_active = True
        elif self.not_email.isChecked():
            self.email_active = False

        Query_Value_ATE_CAL = QueryValueATECAL()
        Query_BaseLine = QueryBaseLine()
        Slot_Mapping = SlotMapping()
        Group_SLOT = GroupSLOT()
        Prepare_Data_To_Graph = PrepareDataToGraph()
        Check_Empty_Data = CheckEmptyData()
        Insert_Data_To_Graph = InsertDataToGraph()
        Add_BaseLine_Limit = AddBaseLineLimit()

        if self.station_id[1] == 'AC1200' or self.station_id[1] == 'AX1200':   
            parameter = 'Loss Factor'
            if self.loss_factor_page.isChecked():
                parameter = 'Loss Factor'
            elif self.tap_power_page.isChecked():
                parameter = 'Tap Power'
            elif self.uut_power_page.isChecked():
                parameter = 'UUT Power' 
            
            DATA_Loss_Factor = Query_Value_ATE_CAL.input_detai(self.day_selected, self.station_selected, parameter)      
            DATA_BaseLine = Query_BaseLine.input_detai(self.station_selected, parameter)

            Array_DateTime_LossFactor = []
            for i in DATA_Loss_Factor:
                Array_DateTime_LossFactor.append(i[1])
            Array_DateTime_LossFactor = list(OrderedDict.fromkeys(Array_DateTime_LossFactor)) # Delete duplicate data in array
            self.x_axis_graph = Array_DateTime_LossFactor

            Array_DateTime_BaseLine = []
            for i in DATA_BaseLine:
                Array_DateTime_BaseLine.append(i[1])
            Array_DateTime_BaseLine = list(OrderedDict.fromkeys(Array_DateTime_BaseLine)) # Delete duplicate data in array
            self.data_last_BL_changed.setText(str(Array_DateTime_BaseLine[0]))       

            if len(Array_DateTime_LossFactor) > 0:        
                Array_SLOT0 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=1, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT1 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=3, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT2 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=5, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)     
                Array_SLOT3 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=7, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT4 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=9, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT5 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=11, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)     
                Array_SLOT6 = Slot_Mapping.input_data(LANE_Quantity=2, Start_From=13, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)

                Array_SLOT = []
                for i in range(2):
                        i += 1
                        Array_SLOT.append("Baseline Calibrate Port" + str(i) + "TX")
                        Array_SLOT.append("Baseline Calibrate Port" + str(i) + "RX")
                Array_BaseLine = []
                for i in DATA_BaseLine:
                    Array_BaseLine.append(i[4])  

                BaseLine_SLOT0 = Array_BaseLine[:4]
                BaseLine_SLOT1 = Array_BaseLine[4:8]
                BaseLine_SLOT2 = Array_BaseLine[8:12] 
                BaseLine_SLOT3 = Array_BaseLine[12:16] 
                BaseLine_SLOT4 = Array_BaseLine[16:20] 
                BaseLine_SLOT5 = Array_BaseLine[20:24]
                BaseLine_SLOT6 = Array_BaseLine[24:28] 
        
                Array_to_Graph_SLOT0 = Group_SLOT.Input(Array_SLOT0, "Calibrate Port PORT1TX", "Calibrate Port PORT1RX", "Calibrate Port PORT2TX", "Calibrate Port PORT2RX", self.station_id[1])
                Array_to_Graph_SLOT1 = Group_SLOT.Input(Array_SLOT1, "Calibrate Port PORT3TX", "Calibrate Port PORT3RX", "Calibrate Port PORT4TX", "Calibrate Port PORT4RX", self.station_id[1])
                Array_to_Graph_SLOT2 = Group_SLOT.Input(Array_SLOT2, "Calibrate Port PORT5TX", "Calibrate Port PORT5RX", "Calibrate Port PORT6TX", "Calibrate Port PORT6RX", self.station_id[1])
                Array_to_Graph_SLOT3 = Group_SLOT.Input(Array_SLOT3, "Calibrate Port PORT7TX", "Calibrate Port PORT7RX", "Calibrate Port PORT8TX", "Calibrate Port PORT8RX", self.station_id[1])
                Array_to_Graph_SLOT4 = Group_SLOT.Input(Array_SLOT4, "Calibrate Port PORT9TX", "Calibrate Port PORT9RX", "Calibrate Port PORT10TX", "Calibrate Port PORT10RX", self.station_id[1])
                Array_to_Graph_SLOT5 = Group_SLOT.Input(Array_SLOT5, "Calibrate Port PORT11TX", "Calibrate Port PORT11RX", "Calibrate Port PORT12TX", "Calibrate Port PORT12RX", self.station_id[1])
                Array_to_Graph_SLOT6 = Group_SLOT.Input(Array_SLOT6, "Calibrate Port PORT13TX", "Calibrate Port PORT13RX", "Calibrate Port PORT14TX", "Calibrate Port PORT14RX", self.station_id[1])

                Dict_SLOT0_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT0_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT0_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT0_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT1_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT1_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT1_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT1_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT2_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT2_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT2_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT2_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT3_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT3_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT3_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT3_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT4_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT4_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT4_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT4_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT5_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT5_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT5_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT5_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                Dict_SLOT6_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT6_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]
                Dict_SLOT6_TX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[2]
                Dict_SLOT6_RX_LANE1 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT0_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT0_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT0_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT0_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT1_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT1_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT1_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT1_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT2_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT2_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT2_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT2_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT3_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT3_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT3_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT3_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT4_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT4_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT4_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT4_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_SLOT5_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT5_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT5_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT5_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[3]
                
                BL_SLOT6_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT6_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                BL_SLOT6_TX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[2]
                BL_SLOT6_RX_L1 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[3]

                BL_Dict_SLOT0_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT0_TX_L0)
                BL_Dict_SLOT0_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT0_RX_L0)
                BL_Dict_SLOT0_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT0_TX_L1)
                BL_Dict_SLOT0_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT0_RX_L1)

                BL_Dict_SLOT1_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT1_TX_L0)
                BL_Dict_SLOT1_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT1_RX_L0)
                BL_Dict_SLOT1_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT1_TX_L1)
                BL_Dict_SLOT1_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT1_RX_L1)

                BL_Dict_SLOT2_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT2_TX_L0)
                BL_Dict_SLOT2_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT2_RX_L0)
                BL_Dict_SLOT2_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT2_TX_L1)
                BL_Dict_SLOT2_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT2_RX_L1)

                BL_Dict_SLOT3_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT3_TX_L0)
                BL_Dict_SLOT3_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT3_RX_L0)
                BL_Dict_SLOT3_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT3_TX_L1)
                BL_Dict_SLOT3_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT3_RX_L1)

                BL_Dict_SLOT4_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT4_TX_L0)
                BL_Dict_SLOT4_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT4_RX_L0)
                BL_Dict_SLOT4_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT4_TX_L1)
                BL_Dict_SLOT4_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT4_RX_L1)

                BL_Dict_SLOT5_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT5_TX_L0)
                BL_Dict_SLOT5_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT5_RX_L0)
                BL_Dict_SLOT5_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT5_TX_L1)
                BL_Dict_SLOT5_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT5_RX_L1)

                BL_Dict_SLOT6_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT6_TX_L0)
                BL_Dict_SLOT6_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT6_RX_L0)
                BL_Dict_SLOT6_TX_LANE1 = Prepare_Data_To_Graph.input_value("TX_LANE1", BL_SLOT6_TX_L1)
                BL_Dict_SLOT6_RX_LANE1 = Prepare_Data_To_Graph.input_value("RX_LANE1", BL_SLOT6_RX_L1)

                Series_Graph_SLOT0 = [Dict_SLOT0_TX_LANE0,Dict_SLOT0_RX_LANE0,Dict_SLOT0_TX_LANE1,Dict_SLOT0_RX_LANE1]
                Series_Graph_SLOT1 = [Dict_SLOT1_TX_LANE0,Dict_SLOT1_RX_LANE0,Dict_SLOT1_TX_LANE1,Dict_SLOT1_RX_LANE1]
                Series_Graph_SLOT2 = [Dict_SLOT2_TX_LANE0,Dict_SLOT2_RX_LANE0,Dict_SLOT2_TX_LANE1,Dict_SLOT2_RX_LANE1]
                Series_Graph_SLOT3 = [Dict_SLOT3_TX_LANE0,Dict_SLOT3_RX_LANE0,Dict_SLOT3_TX_LANE1,Dict_SLOT3_RX_LANE1]
                Series_Graph_SLOT4 = [Dict_SLOT4_TX_LANE0,Dict_SLOT4_RX_LANE0,Dict_SLOT4_TX_LANE1,Dict_SLOT4_RX_LANE1]
                Series_Graph_SLOT5 = [Dict_SLOT5_TX_LANE0,Dict_SLOT5_RX_LANE0,Dict_SLOT5_TX_LANE1,Dict_SLOT5_RX_LANE1]
                Series_Graph_SLOT6 = [Dict_SLOT6_TX_LANE0,Dict_SLOT6_RX_LANE0,Dict_SLOT6_TX_LANE1,Dict_SLOT6_RX_LANE1]

                All_Data_LF = Series_Graph_SLOT0 + Series_Graph_SLOT1 + Series_Graph_SLOT2 + Series_Graph_SLOT3 + Series_Graph_SLOT4 + Series_Graph_SLOT5 + Series_Graph_SLOT6

                TX_LANE0_Dict_LF = {'name': 'TX_LANE0', 'data': []}
                RX_LANE0_Dict_LF = {'name': 'RX_LANE0', 'data': []}
                TX_LANE1_Dict_LF = {'name': 'TX_LANE1', 'data': []}
                RX_LANE1_Dict_LF = {'name': 'RX_LANE1', 'data': []}

                for data in All_Data_LF:
                    if data['name'] == 'TX_LANE0':  
                        for val in data['data']:
                            TX_LANE0_Dict_LF['data'].append(val[1])   
                    if data['name'] == 'RX_LANE0':  
                        for val in data['data']:
                            RX_LANE0_Dict_LF['data'].append(val[1])  
                    if data['name'] == 'TX_LANE1':  
                        for val in data['data']:
                            TX_LANE1_Dict_LF['data'].append(val[1])  
                    if data['name'] == 'RX_LANE1':  
                        for val in data['data']:
                            RX_LANE1_Dict_LF['data'].append(val[1]) 
                self.data_for_dis_plot_LF = [TX_LANE0_Dict_LF,RX_LANE0_Dict_LF,TX_LANE1_Dict_LF,RX_LANE1_Dict_LF]
                
                Series_BL_Graph_SLOT0 = [BL_Dict_SLOT0_TX_LANE0,BL_Dict_SLOT0_RX_LANE0,BL_Dict_SLOT0_TX_LANE1,BL_Dict_SLOT0_RX_LANE1]
                Series_BL_Graph_SLOT1 = [BL_Dict_SLOT1_TX_LANE0,BL_Dict_SLOT1_RX_LANE0,BL_Dict_SLOT1_TX_LANE1,BL_Dict_SLOT1_RX_LANE1]
                Series_BL_Graph_SLOT2 = [BL_Dict_SLOT2_TX_LANE0,BL_Dict_SLOT2_RX_LANE0,BL_Dict_SLOT2_TX_LANE1,BL_Dict_SLOT2_RX_LANE1]
                Series_BL_Graph_SLOT3 = [BL_Dict_SLOT3_TX_LANE0,BL_Dict_SLOT3_RX_LANE0,BL_Dict_SLOT3_TX_LANE1,BL_Dict_SLOT3_RX_LANE1]
                Series_BL_Graph_SLOT4 = [BL_Dict_SLOT4_TX_LANE0,BL_Dict_SLOT4_RX_LANE0,BL_Dict_SLOT4_TX_LANE1,BL_Dict_SLOT4_RX_LANE1]
                Series_BL_Graph_SLOT5 = [BL_Dict_SLOT5_TX_LANE0,BL_Dict_SLOT5_RX_LANE0,BL_Dict_SLOT5_TX_LANE1,BL_Dict_SLOT5_RX_LANE1]
                Series_BL_Graph_SLOT6 = [BL_Dict_SLOT6_TX_LANE0,BL_Dict_SLOT6_RX_LANE0,BL_Dict_SLOT6_TX_LANE1,BL_Dict_SLOT6_RX_LANE1]
                
                All_Data_BL = Series_BL_Graph_SLOT0 + Series_BL_Graph_SLOT1 + Series_BL_Graph_SLOT2 + Series_BL_Graph_SLOT3 + Series_BL_Graph_SLOT4 + Series_BL_Graph_SLOT5 + Series_BL_Graph_SLOT6

                TX_LANE0_Dict_BL = {'name': 'TX_LANE0', 'data': []}
                RX_LANE0_Dict_BL = {'name': 'RX_LANE0', 'data': []}
                TX_LANE1_Dict_BL = {'name': 'TX_LANE1', 'data': []}
                RX_LANE1_Dict_BL = {'name': 'RX_LANE1', 'data': []}

                for data in All_Data_BL:
                    if data['name'] == 'TX_LANE0':  
                        for val in data['data']:
                            TX_LANE0_Dict_BL['data'].append(val[1])   
                    if data['name'] == 'RX_LANE0':  
                        for val in data['data']:
                            RX_LANE0_Dict_BL['data'].append(val[1])  
                    if data['name'] == 'TX_LANE1':  
                        for val in data['data']:
                            TX_LANE1_Dict_BL['data'].append(val[1])  
                    if data['name'] == 'RX_LANE1':  
                        for val in data['data']:
                            RX_LANE1_Dict_BL['data'].append(val[1])  

                self.data_for_dis_plot_BL = [TX_LANE0_Dict_BL,RX_LANE0_Dict_BL,TX_LANE1_Dict_BL,RX_LANE1_Dict_BL]
                
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT0, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT0_LF, "SLOT0", BaseLine_SLOT0, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT1, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT1_LF, "SLOT1", BaseLine_SLOT1, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT2, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT2_LF, "SLOT2", BaseLine_SLOT2, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT3, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT3_LF, "SLOT3", BaseLine_SLOT3, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT4, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT4_LF, "SLOT4", BaseLine_SLOT4, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT5, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT5_LF, "SLOT5", BaseLine_SLOT5, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT6, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT6_LF, "SLOT6", BaseLine_SLOT6, "Loss Factor", self.station_id[1])
                
                Series_BL_Graph_SLOT0 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT0)
                Series_BL_Graph_SLOT1 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT1)
                Series_BL_Graph_SLOT2 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT2)
                Series_BL_Graph_SLOT3 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT3)
                Series_BL_Graph_SLOT4 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT4)
                Series_BL_Graph_SLOT5 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT5)
                Series_BL_Graph_SLOT6 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT6)

                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT0, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT0_BL, "Base Line SLOT0", BaseLine_SLOT0, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT1, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT1_BL, "Base Line SLOT1", BaseLine_SLOT1, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT2, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT2_BL, "Base Line SLOT2", BaseLine_SLOT2, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT3, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT3_BL, "Base Line SLOT3", BaseLine_SLOT3, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT4, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT4_BL, "Base Line SLOT4", BaseLine_SLOT4, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT5, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT5_BL, "Base Line SLOT5", BaseLine_SLOT5, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT6, Array_DateTime_LossFactor, self.Graph_AC1200_SLOT6_BL, "Base Line SLOT6", BaseLine_SLOT6, "Base Line", self.station_id[1])
            else:
                QMessageBox.information(self, "Notify", "Have no any data found")

        elif self.station_id[1] == '400ZR':
            self.loss_factor_page.setChecked(True)
            parameter = 'Loss Factor'

            DATA_Loss_Factor = Query_Value_ATE_CAL.input_detai(self.day_selected, self.station_selected, parameter)
            DATA_BaseLine = Query_BaseLine.input_detai(self.station_selected, parameter)
                       
            Array_DateTime_LossFactor = []
            for i in DATA_Loss_Factor:
                Array_DateTime_LossFactor.append(i[1])
            Array_DateTime_LossFactor = list(OrderedDict.fromkeys(Array_DateTime_LossFactor)) # Delete duplicate data in array
            self.x_axis_graph = Array_DateTime_LossFactor
            self.x_axis_graph_for_save = Array_DateTime_LossFactor

            Array_DateTime_BaseLine = []
            for i in DATA_BaseLine:
                Array_DateTime_BaseLine.append(i[1])
            Array_DateTime_BaseLine = list(OrderedDict.fromkeys(Array_DateTime_BaseLine)) # Delete duplicate data in array
            self.data_last_BL_changed.setText(str(Array_DateTime_BaseLine[0]))

            if len(Array_DateTime_LossFactor) > 0: 
                Array_SLOT0 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=1, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT1 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=2, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT2 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=3, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT3 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=4, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT4 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=5, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT5 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=6, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT6 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=7, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT7 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=8, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT8 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=9, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT9 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=10, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT10 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=11, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)
                Array_SLOT11 = Slot_Mapping.input_data(LANE_Quantity=1, Start_From=12, Data_in=DATA_Loss_Factor, Array_DateTime_in=Array_DateTime_LossFactor)

                Array_SLOT = []
                for i in range(1):
                        i += 1
                        Array_SLOT.append("Baseline Calibrate Port" + str(i) + "TX")
                        Array_SLOT.append("Baseline Calibrate Port" + str(i) + "RX")
                Array_BaseLine = []
                for i in DATA_BaseLine:
                    Array_BaseLine.append(i[4]) 

                BaseLine_SLOT0 = Array_BaseLine[:2]
                BaseLine_SLOT1 = Array_BaseLine[2:4]
                BaseLine_SLOT2 = Array_BaseLine[4:6] 
                BaseLine_SLOT3 = Array_BaseLine[6:8] 
                BaseLine_SLOT4 = Array_BaseLine[8:10] 
                BaseLine_SLOT5 = Array_BaseLine[10:12]
                BaseLine_SLOT6 = Array_BaseLine[12:14]
                BaseLine_SLOT7 = Array_BaseLine[14:16]
                BaseLine_SLOT8 = Array_BaseLine[16:18]
                BaseLine_SLOT9 = Array_BaseLine[18:20] 
                BaseLine_SLOT10 = Array_BaseLine[20:22] 
                BaseLine_SLOT11 = Array_BaseLine[22:24] 

                Array_to_Graph_SLOT0 = Group_SLOT.Input(Array_SLOT0, "Calibrate Port PORT1TX", "Calibrate Port PORT1RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT1 = Group_SLOT.Input(Array_SLOT1, "Calibrate Port PORT2TX", "Calibrate Port PORT2RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT2 = Group_SLOT.Input(Array_SLOT2, "Calibrate Port PORT3TX", "Calibrate Port PORT3RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT3 = Group_SLOT.Input(Array_SLOT3, "Calibrate Port PORT4TX", "Calibrate Port PORT4RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT4 = Group_SLOT.Input(Array_SLOT4, "Calibrate Port PORT5TX", "Calibrate Port PORT5RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT5 = Group_SLOT.Input(Array_SLOT5, "Calibrate Port PORT6TX", "Calibrate Port PORT6RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT6 = Group_SLOT.Input(Array_SLOT6, "Calibrate Port PORT7TX", "Calibrate Port PORT7RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT7 = Group_SLOT.Input(Array_SLOT7, "Calibrate Port PORT8TX", "Calibrate Port PORT8RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT8 = Group_SLOT.Input(Array_SLOT8, "Calibrate Port PORT9TX", "Calibrate Port PORT9RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT9 = Group_SLOT.Input(Array_SLOT9, "Calibrate Port PORT10TX", "Calibrate Port PORT10RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT10 = Group_SLOT.Input(Array_SLOT10, "Calibrate Port PORT11TX", "Calibrate Port PORT11RX", "", "", self.station_id[1])
                Array_to_Graph_SLOT11 = Group_SLOT.Input(Array_SLOT11, "Calibrate Port PORT12TX", "Calibrate Port PORT12RX", "", "", self.station_id[1])

                Dict_SLOT0_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT0_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT0, Array_to_Graph_SLOT0, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT1_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT1_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT1, Array_to_Graph_SLOT1, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT2_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT2_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT2, Array_to_Graph_SLOT2, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT3_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT3_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT3, Array_to_Graph_SLOT3, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT4_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT4_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT4, Array_to_Graph_SLOT4, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT5_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT5_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT5, Array_to_Graph_SLOT5, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT6_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT6_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT6, Array_to_Graph_SLOT6, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT7_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT7, Array_to_Graph_SLOT7, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT7_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT7, Array_to_Graph_SLOT7, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT8_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT8, Array_to_Graph_SLOT8, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT8_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT8, Array_to_Graph_SLOT8, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT9_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT9, Array_to_Graph_SLOT9, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT9_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT9, Array_to_Graph_SLOT9, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT10_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT10, Array_to_Graph_SLOT10, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT10_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT10, Array_to_Graph_SLOT10, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                Dict_SLOT11_TX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT11, Array_to_Graph_SLOT11, "Loss Factor", self.station_id[1], Mode_In='CAL')[0]
                Dict_SLOT11_RX_LANE0 = Check_Empty_Data.array_in(Array_to_Graph_SLOT11, Array_to_Graph_SLOT11, "Loss Factor", self.station_id[1], Mode_In='CAL')[1]

                # Base Line Calculate
                BL_SLOT0_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT0_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT0, Array_to_Graph_SLOT0, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT1_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT1_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT1, Array_to_Graph_SLOT1, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT2_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT2_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT2, Array_to_Graph_SLOT2, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT3_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT3_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT3, Array_to_Graph_SLOT3, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT4_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT4_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT4, Array_to_Graph_SLOT4, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT5_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT5_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT5, Array_to_Graph_SLOT5, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                
                BL_SLOT6_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT6_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT6, Array_to_Graph_SLOT6, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT7_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT7, Array_to_Graph_SLOT7, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT7_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT7, Array_to_Graph_SLOT7, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT8_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT8, Array_to_Graph_SLOT8, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT8_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT8, Array_to_Graph_SLOT8, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT9_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT9, Array_to_Graph_SLOT9, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT9_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT9, Array_to_Graph_SLOT9, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                BL_SLOT10_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT10, Array_to_Graph_SLOT10, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT10_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT10, Array_to_Graph_SLOT10, "Base Line", self.station_id[1], Mode_In='CAL')[1]
                
                BL_SLOT11_TX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT11, Array_to_Graph_SLOT11, "Base Line", self.station_id[1], Mode_In='CAL')[0]
                BL_SLOT11_RX_L0 = Check_Empty_Data.array_in(BaseLine_SLOT11, Array_to_Graph_SLOT11, "Base Line", self.station_id[1], Mode_In='CAL')[1]

                # Prepare Base Line value calculated to Graph
                BL_Dict_SLOT0_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT0_TX_L0)
                BL_Dict_SLOT0_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT0_RX_L0)

                BL_Dict_SLOT1_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT1_TX_L0)
                BL_Dict_SLOT1_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT1_RX_L0)

                BL_Dict_SLOT2_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT2_TX_L0)
                BL_Dict_SLOT2_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT2_RX_L0)

                BL_Dict_SLOT3_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT3_TX_L0)
                BL_Dict_SLOT3_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT3_RX_L0)

                BL_Dict_SLOT4_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT4_TX_L0)
                BL_Dict_SLOT4_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT4_RX_L0)

                BL_Dict_SLOT5_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT5_TX_L0)
                BL_Dict_SLOT5_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT5_RX_L0)

                BL_Dict_SLOT6_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT6_TX_L0)
                BL_Dict_SLOT6_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT6_RX_L0)

                BL_Dict_SLOT7_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT7_TX_L0)
                BL_Dict_SLOT7_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT7_RX_L0)

                BL_Dict_SLOT8_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT8_TX_L0)
                BL_Dict_SLOT8_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT8_RX_L0)

                BL_Dict_SLOT9_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT9_TX_L0)
                BL_Dict_SLOT9_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT9_RX_L0)

                BL_Dict_SLOT10_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT10_TX_L0)
                BL_Dict_SLOT10_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT10_RX_L0)

                BL_Dict_SLOT11_TX_LANE0 = Prepare_Data_To_Graph.input_value("TX_LANE0", BL_SLOT11_TX_L0)
                BL_Dict_SLOT11_RX_LANE0 = Prepare_Data_To_Graph.input_value("RX_LANE0", BL_SLOT11_RX_L0)
                    
                Series_Graph_SLOT0 = [Dict_SLOT0_TX_LANE0,Dict_SLOT0_RX_LANE0]
                Series_Graph_SLOT1 = [Dict_SLOT1_TX_LANE0,Dict_SLOT1_RX_LANE0]
                Series_Graph_SLOT2 = [Dict_SLOT2_TX_LANE0,Dict_SLOT2_RX_LANE0]
                Series_Graph_SLOT3 = [Dict_SLOT3_TX_LANE0,Dict_SLOT3_RX_LANE0]
                Series_Graph_SLOT4 = [Dict_SLOT4_TX_LANE0,Dict_SLOT4_RX_LANE0]
                Series_Graph_SLOT5 = [Dict_SLOT5_TX_LANE0,Dict_SLOT5_RX_LANE0]
                Series_Graph_SLOT6 = [Dict_SLOT6_TX_LANE0,Dict_SLOT6_RX_LANE0]
                Series_Graph_SLOT7 = [Dict_SLOT7_TX_LANE0,Dict_SLOT7_RX_LANE0]
                Series_Graph_SLOT8 = [Dict_SLOT8_TX_LANE0,Dict_SLOT8_RX_LANE0]
                Series_Graph_SLOT9 = [Dict_SLOT9_TX_LANE0,Dict_SLOT9_RX_LANE0]
                Series_Graph_SLOT10 = [Dict_SLOT10_TX_LANE0,Dict_SLOT10_RX_LANE0]
                Series_Graph_SLOT11 = [Dict_SLOT11_TX_LANE0,Dict_SLOT11_RX_LANE0]

                All_Data_LF = Series_Graph_SLOT0 + Series_Graph_SLOT1 + Series_Graph_SLOT2 + Series_Graph_SLOT3 + Series_Graph_SLOT4 + Series_Graph_SLOT5 + Series_Graph_SLOT6 + Series_Graph_SLOT7 + Series_Graph_SLOT8 + Series_Graph_SLOT9 + Series_Graph_SLOT10 + Series_Graph_SLOT11

                TX_LANE0_Dict_LF = {'name': 'TX_LANE0', 'data': []}
                RX_LANE0_Dict_LF = {'name': 'RX_LANE0', 'data': []}

                for data in All_Data_LF:
                    if data['name'] == 'TX_LANE0':  
                        for val in data['data']:
                            TX_LANE0_Dict_LF['data'].append(val[1])   
                    if data['name'] == 'RX_LANE0':  
                        for val in data['data']:
                            RX_LANE0_Dict_LF['data'].append(val[1])  

                self.data_for_dis_plot_LF = [TX_LANE0_Dict_LF,RX_LANE0_Dict_LF]

                # Insert Array BaseLine calculated
                Series_BL_Graph_SLOT0 = [BL_Dict_SLOT0_TX_LANE0,BL_Dict_SLOT0_RX_LANE0]
                Series_BL_Graph_SLOT1 = [BL_Dict_SLOT1_TX_LANE0,BL_Dict_SLOT1_RX_LANE0]
                Series_BL_Graph_SLOT2 = [BL_Dict_SLOT2_TX_LANE0,BL_Dict_SLOT2_RX_LANE0]
                Series_BL_Graph_SLOT3 = [BL_Dict_SLOT3_TX_LANE0,BL_Dict_SLOT3_RX_LANE0]
                Series_BL_Graph_SLOT4 = [BL_Dict_SLOT4_TX_LANE0,BL_Dict_SLOT4_RX_LANE0]
                Series_BL_Graph_SLOT5 = [BL_Dict_SLOT5_TX_LANE0,BL_Dict_SLOT5_RX_LANE0]
                Series_BL_Graph_SLOT6 = [BL_Dict_SLOT6_TX_LANE0,BL_Dict_SLOT6_RX_LANE0]
                Series_BL_Graph_SLOT7 = [BL_Dict_SLOT7_TX_LANE0,BL_Dict_SLOT7_RX_LANE0]
                Series_BL_Graph_SLOT8 = [BL_Dict_SLOT8_TX_LANE0,BL_Dict_SLOT8_RX_LANE0]
                Series_BL_Graph_SLOT9 = [BL_Dict_SLOT9_TX_LANE0,BL_Dict_SLOT9_RX_LANE0]
                Series_BL_Graph_SLOT10 = [BL_Dict_SLOT10_TX_LANE0,BL_Dict_SLOT10_RX_LANE0]
                Series_BL_Graph_SLOT11 = [BL_Dict_SLOT11_TX_LANE0,BL_Dict_SLOT11_RX_LANE0]

                All_Data_BL = Series_BL_Graph_SLOT0 + Series_BL_Graph_SLOT1 + Series_BL_Graph_SLOT2 + Series_BL_Graph_SLOT3 + Series_BL_Graph_SLOT4 + Series_BL_Graph_SLOT5 + Series_BL_Graph_SLOT6 + Series_BL_Graph_SLOT7 + Series_BL_Graph_SLOT8 + Series_BL_Graph_SLOT9 + Series_BL_Graph_SLOT10 + Series_BL_Graph_SLOT11

                TX_LANE0_Dict_BL = {'name': 'TX_LANE0', 'data': []}
                RX_LANE0_Dict_BL = {'name': 'RX_LANE0', 'data': []}

                for data in All_Data_BL:
                    if data['name'] == 'TX_LANE0':  
                        for val in data['data']:
                            TX_LANE0_Dict_BL['data'].append(val[1])   
                    if data['name'] == 'RX_LANE0':  
                        for val in data['data']:
                            RX_LANE0_Dict_BL['data'].append(val[1])  

                self.data_for_dis_plot_BL = [TX_LANE0_Dict_BL,RX_LANE0_Dict_BL]

                # Create graph LossFactor
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT0, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT0_LF, "SLOT0", BaseLine_SLOT0, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT1, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT1_LF, "SLOT1", BaseLine_SLOT1, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT2, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT2_LF, "SLOT2", BaseLine_SLOT2, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT3, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT3_LF, "SLOT3", BaseLine_SLOT3, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT4, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT4_LF, "SLOT4", BaseLine_SLOT4, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT5, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT5_LF, "SLOT5", BaseLine_SLOT5, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT6, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT6_LF, "SLOT6", BaseLine_SLOT6, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT7, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT7_LF, "SLOT7", BaseLine_SLOT7, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT8, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT8_LF, "SLOT8", BaseLine_SLOT8, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT9, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT9_LF, "SLOT9", BaseLine_SLOT9, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT10, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT10_LF, "SLOT10", BaseLine_SLOT10, "Loss Factor", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_Graph_SLOT11, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT11_LF, "SLOT11", BaseLine_SLOT11, "Loss Factor", self.station_id[1])
                
                # Create graph Baseline
                Series_BL_Graph_SLOT0 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT0)
                Series_BL_Graph_SLOT1 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT1)
                Series_BL_Graph_SLOT2 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT2)
                Series_BL_Graph_SLOT3 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT3)
                Series_BL_Graph_SLOT4 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT4)
                Series_BL_Graph_SLOT5 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT5)
                Series_BL_Graph_SLOT6 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT6)
                Series_BL_Graph_SLOT7 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT7)
                Series_BL_Graph_SLOT8 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT8)
                Series_BL_Graph_SLOT9 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT9)
                Series_BL_Graph_SLOT10 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT10)
                Series_BL_Graph_SLOT11 = Add_BaseLine_Limit.input(Series_BL_Graph_SLOT11)
           
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT0, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT0_BL, "Base Line SLOT0", BaseLine_SLOT0, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT1, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT1_BL, "Base Line SLOT1", BaseLine_SLOT1, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT2, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT2_BL, "Base Line SLOT2", BaseLine_SLOT2, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT3, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT3_BL, "Base Line SLOT3", BaseLine_SLOT3, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT4, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT4_BL, "Base Line SLOT4", BaseLine_SLOT4, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT5, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT5_BL, "Base Line SLOT5", BaseLine_SLOT5, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT6, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT6_BL, "Base Line SLOT6", BaseLine_SLOT6, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT7, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT7_BL, "Base Line SLOT7", BaseLine_SLOT7, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT8, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT8_BL, "Base Line SLOT8", BaseLine_SLOT8, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT9, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT9_BL, "Base Line SLOT9", BaseLine_SLOT9, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT10, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT10_BL, "Base Line SLOT10", BaseLine_SLOT10, "Base Line", self.station_id[1])
                Insert_Data_To_Graph.detail_in(Series_BL_Graph_SLOT11, Array_DateTime_LossFactor, self.Graph_400ZR_SLOT11_BL, "Base Line SLOT11", BaseLine_SLOT11, "Base Line", self.station_id[1])
    
                self.array_data_for_check = [Series_BL_Graph_SLOT0,Series_BL_Graph_SLOT1,Series_BL_Graph_SLOT2,Series_BL_Graph_SLOT3,Series_BL_Graph_SLOT4,Series_BL_Graph_SLOT5,Series_BL_Graph_SLOT6,Series_BL_Graph_SLOT7,Series_BL_Graph_SLOT8,Series_BL_Graph_SLOT9,Series_BL_Graph_SLOT10,Series_BL_Graph_SLOT11]
                self.clear_file()
                self.save_xlsx()

                self.check_out()
            else:
                QMessageBox.information(self, "Notify", "Have no any data found")

    def check_out(self):
        file_limit = open('temp/LIMIT.txt', 'r')
        limit_read = file_limit.read()
        limit_read = limit_read.split('\n')
        usl = limit_read[0]
        lsl = limit_read[1]
        text_TX = ''
        text_RX = ''
        SLOT_Failed = []
        for idx, i in enumerate(self.array_data_for_check):
            if float(i[0]['data'][-1][1]) > float(usl):
                text_TX += f"SLOT {idx} TX, Out of Upper Spec\n"
                SLOT_Failed.append(idx)
            elif float(i[0]['data'][-1][1]) < float(lsl):
                text_TX += f"SLOT {idx} TX, Out of Lower Spec\n"
                SLOT_Failed.append(idx)
        for idx, i in enumerate(self.array_data_for_check):
            if float(i[1]['data'][-1][1]) > float(usl):
                text_RX += f"SLOT {idx} RX, Out of Upper Spec\n"
                SLOT_Failed.append(idx)
            elif float(i[1]['data'][-1][1]) < float(lsl):
                text_RX += f"SLOT {idx} RX, Out of Lower Spec\n"
                SLOT_Failed.append(idx)

        SLOT_Failed = list(set(SLOT_Failed))      

        list_files = os.listdir(f'log_files/{self.STATION_dropbox.currentText()}')
        list_files = sorted(list_files, key=lambda x: int(x.split('SLOT')[1].split('.')[0]))

        directory = os.getcwd()

        if list_files:
            if len(SLOT_Failed) > 0:
                files_failed = []       
                for i in SLOT_Failed:
                    files_failed.append(directory + f'\\log_files\\{self.STATION_dropbox.currentText()}\\' + list_files[i])

        print(directory + f'\\log_files\\{self.STATION_dropbox.currentText()}\\' + list_files[0])

        # Read csv
        with open('temp/temp_email.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if rows:
                arr = []
                for row in rows:
                    arr.append(row)

        send_email = False
        if self.x_axis_graph in arr:
            send_email = False
        else:
            send_email = True
        
        if len(text_TX) > 0 or len(text_RX) > 0:
            # =========================== Sending Email ===========================
            # if self.email_active == True:
            if send_email == True:
                Send_Email = SendEmail()
                Send_Email.data_in(text_in="========== Don't reply this email back, just reminder dataof Calibration out of Base Line ==========\n\n" + f"{self.STATION_dropbox.currentText()}\n\n"+ "*** TX Detail ***\n" + text_TX + "\n*** RX Detail ***\n" + text_RX, attachments=files_failed)
                time.sleep(1)
                
                # Write to csv
                with open('temp/temp_email.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(self.x_axis_graph)

                self.not_email.setChecked(True)
                QMessageBox.information(self, "Notify", "Send Email Successfully!\n\n" + text_TX + "\n" + text_RX)

            elif send_email == False:
                QMessageBox.information(self, "Notify", "Email already send, can't send duplicate!\n\n" + text_TX + "\n" + text_RX)
        else: 
            self.not_email.setChecked(True)
            QMessageBox.information(self, "Notify", "No any data out of control !")     

    def clear_file(self):
        if not os.path.exists(f"log_files/{self.STATION_dropbox.currentText()}"):
            os.makedirs(f"log_files/{self.STATION_dropbox.currentText()}")
        else:
            print(f"Folder is already exists.")

        list_f = os.listdir(f"log_files/{self.STATION_dropbox.currentText()}")
        arr = []
        for i in list_f:
            arr.append(os.path.join(f"log_files/{self.STATION_dropbox.currentText()}", i))
        for j in arr:
            os.remove(j)

    def save_xlsx(self):            
        x_cat = self.x_axis_graph_for_save
        x_cat.insert(0, 'Date_Time')
        for idx in range(len(self.array_data_for_check)):
            tx_array = []
            rx_array = []
            limit_usl = []
            limit_lsl = []
            for tx in self.array_data_for_check[idx][0]['data']: # First index in SLOTs locate
                tx_array.append(tx[1])
            for rx in self.array_data_for_check[idx][1]['data']: # First index in SLOTs locate
                rx_array.append(rx[1])
            for lm_u in self.array_data_for_check[idx][2]['data']: # First index in SLOTs locate
                limit_usl.append(lm_u[1])
            for lm_l in self.array_data_for_check[idx][3]['data']: # First index in SLOTs locate
                limit_lsl.append(lm_l[1])

            tx_array.insert(0,'TX')
            rx_array.insert(0,'RX')
            limit_usl.insert(0,'USL')
            limit_lsl.insert(0,'LSL')  

            array = zip(*(x_cat, tx_array, rx_array, limit_usl, limit_lsl)) 

            Save_To_Excel = SaveToExcel()
            Save_To_Excel.save(array_in=array, filename=f'log_files/{self.STATION_dropbox.currentText()}/SLOT{idx}.xlsx', title_chart=self.STATION_dropbox.currentText() + f" | SLOT{idx}", row_range=len(tx_array))  

        self.x_axis_graph.pop(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()
