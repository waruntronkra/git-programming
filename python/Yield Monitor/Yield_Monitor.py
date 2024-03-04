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
import subprocess
import openpyxl
from datetime import datetime, timedelta
from Query_Value_Test import QueryValueTest
from Query_Result_Test import QueryResultTest
from Query_Result_Test_SN import QueryResultTestSN
from Query_FITs_History import QueryFITsHistory
from Query_FITs_Operation import QueryFITsOperation
from Query_LastResult_Test import QueryLastResultTest
from Query_LINECARD_CHASSIS import QueryLINECARDCHASSIS
from Query_Value_LINE_CHAS import QueryValueLINECHAS
from Create_Table import CreateTable
from Cal_Yield import CalYield
from Insert_Yield_to_Table import InsertYieldtoTable
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

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()

        self.Main_TAB = QTabWidget(self)
        
        self.process = ""
        self.day = ""

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setGeometry(470,1,500,18)
        self.progress_bar.setVisible(False)
        
        # Create main TAB
        self.AC1200_Page = QWidget()      
        self.Main_TAB.addTab(self.AC1200_Page, "AC1200")
        self.AC100M_Page = QWidget()
        self.Main_TAB.addTab(self.AC100M_Page, "AC100M")
        self.AC200_Page = QWidget()
        self.Main_TAB.addTab(self.AC200_Page, "AC200")
        self.AC400_Page = QWidget()
        self.Main_TAB.addTab(self.AC400_Page, "AC400")
        self.ZEPHYR_Page = QWidget()
        self.Main_TAB.addTab(self.ZEPHYR_Page, "ZEPHYR")
        self.ODB_Page = QWidget()
        self.Main_TAB.addTab(self.ODB_Page, "ODB")
        self.NITLA_Page = QWidget()
        self.Main_TAB.addTab(self.NITLA_Page, "NITLA")
        self.AX1200_Page = QWidget()
        self.Main_TAB.addTab(self.AX1200_Page, "AX1200")

        self.Main_TAB.tabBarClicked.connect(self.force_run)

        # Create process tab (AC1200) inside main tab
        self.TAB_PROCESS_AC1200 = QTabWidget(self.AC1200_Page)
        self.TAB_OIT_AC1200 = QWidget()
        self.TAB_PROCESS_AC1200.addTab(self.TAB_OIT_AC1200, "OIT")
        self.TAB_CAL_AC1200 = QWidget()
        self.TAB_PROCESS_AC1200.addTab(self.TAB_CAL_AC1200, "CAL")
        self.TAB_FVT_AC1200 = QWidget()
        self.TAB_PROCESS_AC1200.addTab(self.TAB_FVT_AC1200, "FVT")
        self.TAB_EXS5_AC1200 = QWidget()
        self.TAB_PROCESS_AC1200.addTab(self.TAB_EXS5_AC1200, "EXS")
        for i in range(4):
            self.TAB_PROCESS_AC1200.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_AC1200.resize(1880, 940)
        self.TAB_PROCESS_AC1200.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (AC100M) inside main tab
        self.TAB_PROCESS_AC100M = QTabWidget(self.AC100M_Page)
        self.TAB_OBS_AC100M = QWidget()
        self.TAB_PROCESS_AC100M.addTab(self.TAB_OBS_AC100M, "OBS")
        self.TAB_FVT_AC100M = QWidget()
        self.TAB_PROCESS_AC100M.addTab(self.TAB_FVT_AC100M, "FVT")
        self.TAB_EXS_AC100M = QWidget()
        self.TAB_PROCESS_AC100M.addTab(self.TAB_EXS_AC100M, "EXS")
        for i in range(3):
            self.TAB_PROCESS_AC100M.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_AC100M.resize(1880, 940) 
        self.TAB_PROCESS_AC100M.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (AC200) inside main tab
        self.TAB_PROCESS_AC200 = QTabWidget(self.AC200_Page)
        self.TAB_OBS_AC200 = QWidget()
        self.TAB_PROCESS_AC200.addTab(self.TAB_OBS_AC200, "OBS")
        self.TAB_FVT_AC200 = QWidget()
        self.TAB_PROCESS_AC200.addTab(self.TAB_FVT_AC200, "FVT")
        self.TAB_EXS_AC200 = QWidget()
        self.TAB_PROCESS_AC200.addTab(self.TAB_EXS_AC200, "EXS")
        for i in range(3):
            self.TAB_PROCESS_AC200.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_AC200.resize(1880, 940)      
        self.TAB_PROCESS_AC200.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (AC400) inside main tab
        self.TAB_PROCESS_AC400 = QTabWidget(self.AC400_Page)
        self.TAB_OBS_AC400 = QWidget()
        self.TAB_PROCESS_AC400.addTab(self.TAB_OBS_AC400, "OBS")
        self.TAB_FVT_AC400 = QWidget()
        self.TAB_PROCESS_AC400.addTab(self.TAB_FVT_AC400, "FVT")
        self.TAB_EXS_AC400 = QWidget()
        self.TAB_PROCESS_AC400.addTab(self.TAB_EXS_AC400, "EXS")
        for i in range(3):
            self.TAB_PROCESS_AC400.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_AC400.resize(1880, 940)   
        self.TAB_PROCESS_AC400.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (ZEPHYR) inside main tab
        self.TAB_PROCESS_ZEPHYR = QTabWidget(self.ZEPHYR_Page)
        self.TAB_FCAL_ZEPHYR = QWidget()
        self.TAB_PROCESS_ZEPHYR.addTab(self.TAB_FCAL_ZEPHYR, "FCAL")
        self.TAB_OPM_ZEPHYR = QWidget()
        self.TAB_PROCESS_ZEPHYR.addTab(self.TAB_OPM_ZEPHYR, "OPM")
        self.TAB_EXS_ZEPHYR = QWidget()
        self.TAB_PROCESS_ZEPHYR.addTab(self.TAB_EXS_ZEPHYR, "EXS")
        self.TAB_EBT_OEM = QWidget()
        self.TAB_PROCESS_ZEPHYR.addTab(self.TAB_EBT_OEM, "EBT")
        for i in range(4):
            self.TAB_PROCESS_ZEPHYR.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_ZEPHYR.resize(1880, 940)  
        self.TAB_PROCESS_ZEPHYR.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (ODB) inside main tab
        self.TAB_PROCESS_ODB = QTabWidget(self.ODB_Page)
        self.TAB_CAL_ODB = QWidget()
        self.TAB_PROCESS_ODB.addTab(self.TAB_CAL_ODB, "CAL")
        for i in range(1):
            self.TAB_PROCESS_ODB.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_ODB.resize(1880, 940)  
        self.TAB_PROCESS_ODB.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (NITLA) inside main tab
        self.TAB_PROCESS_NITLA = QTabWidget(self.NITLA_Page)
        self.TAB_CAL_NITLA = QWidget()
        self.TAB_PROCESS_NITLA.addTab(self.TAB_CAL_NITLA, "CAL")
        for i in range(1):
            self.TAB_PROCESS_NITLA.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_NITLA.resize(1880, 940)
        self.TAB_PROCESS_NITLA.setStyleSheet("background-color: #D8FFFA;")

        # Create process tab (AX1200) inside main tab
        self.TAB_PROCESS_AX1200 = QTabWidget(self.AX1200_Page)
        self.TAB_PCAL_AX1200 = QWidget()
        self.TAB_PROCESS_AX1200.addTab(self.TAB_PCAL_AX1200, "PCAL")
        self.TAB_FVT_AX1200 = QWidget()
        self.TAB_PROCESS_AX1200.addTab(self.TAB_FVT_AX1200, "FVT")
        self.TAB_EXS_AX1200 = QWidget()
        self.TAB_PROCESS_AX1200.addTab(self.TAB_EXS_AX1200, "EXS")
        for i in range(3):
            self.TAB_PROCESS_AX1200.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_AX1200.resize(1880, 940)
        self.TAB_PROCESS_AX1200.setStyleSheet("background-color: #D8FFFA;")
        
        # Config Windowapp
        self.setWindowTitle("Result Test and Yield Monitor V2.1")

        # Ratio button slect fresh unit
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)

        self.all_unit_button = QRadioButton("All", self.Main_TAB)
        self.all_unit_button.setChecked(True)
        self.all_unit_button.move(187, 45)
        self.fresh_unit_button = QRadioButton("Fresh Unit", self.Main_TAB)
        self.fresh_unit_button.move(237, 45)
        self.all_unit_button.clicked.connect(self.fresh_selector)
        self.fresh_unit_button.clicked.connect(self.fresh_selector)

        self.button_group.addButton(self.all_unit_button)
        self.button_group.addButton(self.fresh_unit_button)

        icon_plot_dis = QIcon("temp/icon/plot_dis.ico")
        icon_plot_dis_size = icon_plot_dis.actualSize(QSize(30, 30))
        ate_cal = QPushButton(icon_plot_dis,"Chart Station Calibration", self)
        ate_cal.setIconSize(icon_plot_dis_size)
        ate_cal.setGeometry(520,25,180,30)
        ate_cal.clicked.connect(self.load_plot_cal_file)

        # icon_LC_CH_Yield = QIcon("temp/icon/icon_LC_CH_Yield.ico")
        # icon_LC_CH_Yield_size = icon_LC_CH_Yield.actualSize(QSize(30, 30))
        # LC_CH_Yield = QPushButton(icon_LC_CH_Yield,"Calculation LINECARD/CHASSIS Yield", self)
        # LC_CH_Yield.setIconSize(icon_LC_CH_Yield_size)
        # LC_CH_Yield.setGeometry(720,25,230,30)
        # LC_CH_Yield.clicked.connect(self.LC_CH_Yield)

        icon_pareto = QIcon("temp/icon/pareto.ico")
        icon_pareto_size = icon_pareto.actualSize(QSize(30, 30))
        pareto = QPushButton(icon_pareto,"Pareto", self)
        pareto.setIconSize(icon_pareto_size)
        pareto.setGeometry(2000,25,100,30) # Wait for update ######################################################################################################################################
        pareto.clicked.connect(self.pareto_chart)  

        # Create ration button (AC1200)
        self.process_ratio_AC1200 = QLabel("Select Process", self.TAB_PROCESS_AC1200)
        self.process_ratio_AC1200.move(10, 48)  
        self.oit_button_AC1200 = QRadioButton("OIT", self.TAB_PROCESS_AC1200)
        self.oit_button_AC1200.setChecked(True)
        self.oit_button_AC1200.move(85, 47)
        self.cal_button_AC1200 = QRadioButton("CAL", self.TAB_PROCESS_AC1200)
        self.cal_button_AC1200.move(135, 47)
        self.fst_button_AC1200 = QRadioButton("FST", self.TAB_PROCESS_AC1200)
        self.fst_button_AC1200.move(185, 47)
        self.fvt_button_AC1200 = QRadioButton("FVT", self.TAB_PROCESS_AC1200)
        self.fvt_button_AC1200.move(235, 47)
        self.ept_button_AC1200 = QRadioButton("EPT", self.TAB_PROCESS_AC1200)
        self.ept_button_AC1200.move(285, 47)
        self.ess_button_AC1200 = QRadioButton("ESS", self.TAB_PROCESS_AC1200)
        self.ess_button_AC1200.move(335, 47)
        self.exp_button_AC1200 = QRadioButton("EXP", self.TAB_PROCESS_AC1200)
        self.exp_button_AC1200.move(385, 47)
        self.exs5_button_AC1200 = QRadioButton("EXS5", self.TAB_PROCESS_AC1200)
        self.exs5_button_AC1200.move(435, 47)    

        self.oit_button_AC1200.clicked.connect(self.force_run)
        self.cal_button_AC1200.clicked.connect(self.force_run)
        self.fst_button_AC1200.clicked.connect(self.force_run)
        self.fvt_button_AC1200.clicked.connect(self.force_run)
        self.ept_button_AC1200.clicked.connect(self.force_run)
        self.ess_button_AC1200.clicked.connect(self.force_run)
        self.exp_button_AC1200.clicked.connect(self.force_run)
        self.exs5_button_AC1200.clicked.connect(self.force_run)

        # Create ration button (AC100M)
        self.process_ratio_AC100M = QLabel("Select Process", self.TAB_PROCESS_AC100M)
        self.process_ratio_AC100M.move(10, 48)  
        self.obs_button_AC100M = QRadioButton("OBS", self.TAB_PROCESS_AC100M)
        self.obs_button_AC100M.setChecked(True)
        self.obs_button_AC100M.move(85, 47)
        self.fst_button_AC100M = QRadioButton("FST", self.TAB_PROCESS_AC100M)
        self.fst_button_AC100M.move(135, 47)
        self.fvt_button_AC100M = QRadioButton("FVT", self.TAB_PROCESS_AC100M)
        self.fvt_button_AC100M.move(185, 47)
        self.ept_button_AC100M = QRadioButton("EPT", self.TAB_PROCESS_AC100M)
        self.ept_button_AC100M.move(235, 47)
        self.ess_button_AC100M = QRadioButton("ESS", self.TAB_PROCESS_AC100M)
        self.ess_button_AC100M.move(285, 47)
        self.exp_button_AC100M = QRadioButton("EXP", self.TAB_PROCESS_AC100M)
        self.exp_button_AC100M.move(335, 47)
        self.exs_button_AC100M = QRadioButton("EXS", self.TAB_PROCESS_AC100M)
        self.exs_button_AC100M.move(385, 47)

        self.obs_button_AC100M.clicked.connect(self.force_run)
        self.fst_button_AC100M.clicked.connect(self.force_run)
        self.fvt_button_AC100M.clicked.connect(self.force_run)
        self.ept_button_AC100M.clicked.connect(self.force_run)
        self.ess_button_AC100M.clicked.connect(self.force_run)
        self.exp_button_AC100M.clicked.connect(self.force_run)
        self.exs_button_AC100M.clicked.connect(self.force_run)

        # Create ration button (AC200)
        self.process_ratio_AC200 = QLabel("Select Process", self.TAB_PROCESS_AC200)
        self.process_ratio_AC200.move(10, 48)  
        self.obs_button_AC200 = QRadioButton("OBS", self.TAB_PROCESS_AC200)
        self.obs_button_AC200.setChecked(True)
        self.obs_button_AC200.move(85, 47)
        self.fst_button_AC200 = QRadioButton("FST", self.TAB_PROCESS_AC200)
        self.fst_button_AC200.move(135, 47)
        self.fvt_button_AC200 = QRadioButton("FVT", self.TAB_PROCESS_AC200)
        self.fvt_button_AC200.move(185, 47)
        self.ept_button_AC200 = QRadioButton("EPT", self.TAB_PROCESS_AC200)
        self.ept_button_AC200.move(235, 47)
        self.ess_button_AC200 = QRadioButton("ESS", self.TAB_PROCESS_AC200)
        self.ess_button_AC200.move(285, 47)
        self.exp_button_AC200 = QRadioButton("EXP", self.TAB_PROCESS_AC200)
        self.exp_button_AC200.move(335, 47)
        self.exs_button_AC200 = QRadioButton("EXS", self.TAB_PROCESS_AC200)
        self.exs_button_AC200.move(385, 47)

        self.obs_button_AC200.clicked.connect(self.force_run)
        self.fst_button_AC200.clicked.connect(self.force_run)
        self.fvt_button_AC200.clicked.connect(self.force_run)
        self.ept_button_AC200.clicked.connect(self.force_run)
        self.ess_button_AC200.clicked.connect(self.force_run)
        self.exp_button_AC200.clicked.connect(self.force_run)
        self.exs_button_AC200.clicked.connect(self.force_run)

        # Create ration button (AC400)
        self.process_ratio_AC400 = QLabel("Select Process", self.TAB_PROCESS_AC400)
        self.process_ratio_AC400.move(10, 48)  
        self.obs_button_AC400 = QRadioButton("OBS", self.TAB_PROCESS_AC400)
        self.obs_button_AC400.setChecked(True)
        self.obs_button_AC400.move(85, 47)
        self.fst_button_AC400 = QRadioButton("FST", self.TAB_PROCESS_AC400)
        self.fst_button_AC400.move(135, 47)
        self.fvt_button_AC400 = QRadioButton("FVT", self.TAB_PROCESS_AC400)
        self.fvt_button_AC400.move(185, 47)
        self.ept_button_AC400 = QRadioButton("EPT", self.TAB_PROCESS_AC400)
        self.ept_button_AC400.move(235, 47)
        self.ess_button_AC400 = QRadioButton("ESS", self.TAB_PROCESS_AC400)
        self.ess_button_AC400.move(285, 47)
        self.exp_button_AC400 = QRadioButton("EXP", self.TAB_PROCESS_AC400)
        self.exp_button_AC400.move(335, 47)
        self.exs_button_AC400 = QRadioButton("EXS", self.TAB_PROCESS_AC400)
        self.exs_button_AC400.move(385, 47)

        self.obs_button_AC400.clicked.connect(self.force_run)
        self.fst_button_AC400.clicked.connect(self.force_run)
        self.fst_button_AC400.clicked.connect(self.force_run)
        self.ept_button_AC400.clicked.connect(self.force_run)
        self.ess_button_AC400.clicked.connect(self.force_run)
        self.exp_button_AC400.clicked.connect(self.force_run)
        self.exs_button_AC400.clicked.connect(self.force_run)

        # Create ration button (ZEPHYR)
        self.process_ratio_ZEPHYR = QLabel("Select Process", self.TAB_PROCESS_ZEPHYR)
        self.process_ratio_ZEPHYR.move(10, 48)  
        self.fcal_button_ZEPHYR = QRadioButton("FCAL", self.TAB_PROCESS_ZEPHYR)
        self.fcal_button_ZEPHYR.setChecked(True)
        self.fcal_button_ZEPHYR.move(85, 47)
        self.opm_button_ZEPHYR = QRadioButton("OPM", self.TAB_PROCESS_ZEPHYR)
        self.opm_button_ZEPHYR.move(135, 47)
        self.opmp_button_ZEPHYR = QRadioButton("OPMP", self.TAB_PROCESS_ZEPHYR)
        self.opmp_button_ZEPHYR.move(185, 47)
        self.opmt_button_ZEPHYR = QRadioButton("OPMT", self.TAB_PROCESS_ZEPHYR)
        self.opmt_button_ZEPHYR.move(235, 47)
        self.exp_button_ZEPHYR = QRadioButton("EXP", self.TAB_PROCESS_ZEPHYR)
        self.exp_button_ZEPHYR.move(285, 47)
        self.exs_button_ZEPHYR = QRadioButton("EXS", self.TAB_PROCESS_ZEPHYR)
        self.exs_button_ZEPHYR.move(335, 47)
        self.rebt_button_OEM = QRadioButton("OE-MCM (REBT)", self.TAB_PROCESS_ZEPHYR)
        self.rebt_button_OEM.move(385, 47)
        self.ebt_button_OEM = QRadioButton("OE-MCM (EBT)", self.TAB_PROCESS_ZEPHYR)
        self.ebt_button_OEM.move(495, 47)

        self.fcal_button_ZEPHYR.clicked.connect(self.force_run)
        self.opm_button_ZEPHYR.clicked.connect(self.force_run)
        self.opmp_button_ZEPHYR.clicked.connect(self.force_run)
        self.opmt_button_ZEPHYR.clicked.connect(self.force_run)
        self.exp_button_ZEPHYR.clicked.connect(self.force_run)
        self.exs_button_ZEPHYR.clicked.connect(self.force_run)
        self.rebt_button_OEM.clicked.connect(self.force_run)
        self.ebt_button_OEM.clicked.connect(self.force_run)

        # Create ration button (ODB)
        self.process_ratio_ODB = QLabel("Select Process", self.TAB_PROCESS_ODB)
        self.process_ratio_ODB.move(10, 48)  
        self.cal_button_ODB = QRadioButton("CAL", self.TAB_PROCESS_ODB)
        self.cal_button_ODB.setChecked(True)
        self.cal_button_ODB.move(85, 47)

        self.cal_button_ODB.clicked.connect(self.force_run)

        # Create ration button (NITLA)
        self.process_ratio_NITLA = QLabel("Select Process", self.TAB_PROCESS_NITLA)
        self.process_ratio_NITLA.move(10, 48)  
        self.mcn_button_NITLA = QRadioButton("MCN", self.TAB_PROCESS_NITLA)
        self.mcn_button_NITLA.setChecked(True)
        self.mcn_button_NITLA.move(85, 47)
        self.cal_button_NITLA = QRadioButton("CAL", self.TAB_PROCESS_NITLA)
        self.cal_button_NITLA.move(135, 47)
        self.fvt_button_NITLA = QRadioButton("FVT", self.TAB_PROCESS_NITLA)
        self.fvt_button_NITLA.move(185, 47)

        self.mcn_button_NITLA.clicked.connect(self.force_run)
        self.cal_button_NITLA.clicked.connect(self.force_run)
        self.fvt_button_NITLA.clicked.connect(self.force_run)

        # Create ration button (AX1200)
        self.process_ratio_AX1200 = QLabel("Select Process", self.TAB_PROCESS_AX1200)
        self.process_ratio_AX1200.move(10, 48)
        self.pcal_button_AX1200 = QRadioButton("PCAL", self.TAB_PROCESS_AX1200)
        self.pcal_button_AX1200.setChecked(True)
        self.pcal_button_AX1200.move(85, 47)
        self.cal_button_AX1200 = QRadioButton("CAL", self.TAB_PROCESS_AX1200)
        self.cal_button_AX1200.move(135, 47)
        self.fvt_button_AX1200 = QRadioButton("FVT", self.TAB_PROCESS_AX1200)
        self.fvt_button_AX1200.move(185, 47)
        self.fept_button_AX1200 = QRadioButton("FEPT", self.TAB_PROCESS_AX1200)
        self.fept_button_AX1200.move(235, 47)
        self.fst_button_AX1200 = QRadioButton("FST", self.TAB_PROCESS_AX1200)
        self.fst_button_AX1200.move(285, 47)
        self.ess_button_AX1200 = QRadioButton("ESS", self.TAB_PROCESS_AX1200)
        self.ess_button_AX1200.move(335, 47)
        self.exp_button_AX1200 = QRadioButton("EXP", self.TAB_PROCESS_AX1200)
        self.exp_button_AX1200.move(385, 47)
        self.exs_button_AX1200 = QRadioButton("EXS", self.TAB_PROCESS_AX1200)
        self.exs_button_AX1200.move(435, 47)

        self.pcal_button_AX1200.clicked.connect(self.force_run)
        self.cal_button_AX1200.clicked.connect(self.force_run)
        self.fvt_button_AX1200.clicked.connect(self.force_run)
        self.fept_button_AX1200.clicked.connect(self.force_run)
        self.fst_button_AX1200.clicked.connect(self.force_run)
        self.ess_button_AX1200.clicked.connect(self.force_run)
        self.exp_button_AX1200.clicked.connect(self.force_run)
        self.exs_button_AX1200.clicked.connect(self.force_run)

        # Creat Dropbox
        self.day_label_AC1200 = QLabel("Select Day", self.Main_TAB)
        self.day_label_AC1200.move(12, 38)
        self.day_dropbbox = QComboBox(self.Main_TAB)
        self.day_dropbbox.addItem("1")
        self.day_dropbbox.addItem("2")
        self.day_dropbbox.addItem("3")
        self.day_dropbbox.addItem("5")
        self.day_dropbbox.addItem("7")
        self.day_dropbbox.addItem("14")
        self.day_dropbbox.addItem("30")
        self.day_dropbbox.addItem("90")
        self.day_dropbbox.move(70, 30)
        self.day_dropbbox.setFixedSize(40, 30)
        self.day_dropbbox.currentTextChanged.connect(self.force_run)

        # Create Button
        self.run_button = QPushButton("Refresh", self.Main_TAB)
        self.run_button.move(10, 90)
        self.run_button.setFixedSize(70, 35)
        self.run_button.clicked.connect(self.Query_SQL)

        Create_Table = CreateTable()
        # Create table AC1200 ********************************************************************************
        self.table_ATE_132 = Create_Table.Table_Detail("ATE_AC1200_132", self.TAB_OIT_AC1200, 10, 115, 10, 130, 500, 111)
        self.table_ATE_182 = Create_Table.Table_Detail("ATE_AC1200_182", self.TAB_OIT_AC1200, 520, 115, 520, 130, 500, 111)
        self.table_ATE_256 = Create_Table.Table_Detail("ATE_AC1200_256", self.TAB_OIT_AC1200, 10, 250, 10, 265, 500, 111)
        self.table_ATE_266 = Create_Table.Table_Detail("ATE_AC1200_266", self.TAB_OIT_AC1200, 520, 250, 520, 265, 500, 111)
        self.table_ATE_309 = Create_Table.Table_Detail("ATE_AC1200_309", self.TAB_CAL_AC1200, 10, 115, 10, 130, 1000, 180)
        self.table_ATE_169 = Create_Table.Table_Detail("ATE_AC1200_169", self.TAB_FVT_AC1200, 10, 115, 10, 130, 400, 203)
        self.table_ATE_170 = Create_Table.Table_Detail("ATE_AC1200_170", self.TAB_FVT_AC1200, 420, 115, 420, 130, 400, 203)
        self.table_ATE_183 = Create_Table.Table_Detail("ATE_AC1200_183", self.TAB_FVT_AC1200, 830, 115, 830, 130, 400, 203)
        self.table_ATE_187 = Create_Table.Table_Detail("ATE_AC1200_187", self.TAB_FVT_AC1200, 1240, 115, 1240, 130, 400, 203)
        self.table_ATE_188 = Create_Table.Table_Detail("ATE_AC1200_188", self.TAB_FVT_AC1200, 10, 340, 10, 355, 400, 203)
        self.table_ATE_210 = Create_Table.Table_Detail("ATE_AC1200_210", self.TAB_FVT_AC1200, 420, 340, 420, 355, 400, 203)
        self.table_ATE_215 = Create_Table.Table_Detail("ATE_AC1200_215", self.TAB_FVT_AC1200, 830, 340, 830, 355, 400, 203)
        self.table_ATE_223 = Create_Table.Table_Detail("ATE_AC1200_223", self.TAB_FVT_AC1200, 1240, 340, 1240, 355, 400, 203)
        self.table_ATE_257 = Create_Table.Table_Detail("ATE_AC1200_257", self.TAB_FVT_AC1200, 10, 565, 10, 580, 400, 203)
        self.table_ATE_259 = Create_Table.Table_Detail("ATE_AC1200_259", self.TAB_FVT_AC1200, 420, 565, 420, 580, 400, 203)
        self.table_ATE_265 = Create_Table.Table_Detail("ATE_AC1200_265", self.TAB_FVT_AC1200, 830, 565, 830, 580, 400, 203)
        self.table_ATE_270 = Create_Table.Table_Detail("ATE_AC1200_270", self.TAB_FVT_AC1200, 1240, 565, 1240, 580, 400, 203)
        self.table_ATE_154 = Create_Table.Table_Detail("ATE_AC1200_154", self.TAB_EXS5_AC1200, 10, 115, 10, 130, 530, 387)
        self.table_ATE_195 = Create_Table.Table_Detail("ATE_AC1200_195", self.TAB_EXS5_AC1200, 550, 115, 550, 130, 530, 387)
        self.table_ATE_211 = Create_Table.Table_Detail("ATE_AC1200_211", self.TAB_EXS5_AC1200, 1090, 115, 1090, 130, 530, 387)
        self.table_ATE_213 = Create_Table.Table_Detail("ATE_AC1200_213", self.TAB_EXS5_AC1200, 10, 525, 10, 540, 530, 387)
        self.table_ATE_252 = Create_Table.Table_Detail("ATE_AC1200_252", self.TAB_EXS5_AC1200, 550, 525, 550, 540, 530, 387)
        self.table_ATE_254 = Create_Table.Table_Detail("ATE_AC1200_254", self.TAB_EXS5_AC1200, 1090, 525, 1090, 540, 530, 387)

        # Create table AC100M ********************************************************************************
        self.table_ATE_100 = Create_Table.Table_Detail("ATE_AC100M_100", self.TAB_OBS_AC100M, 10, 115, 10, 130, 500, 180)
        self.table_ATE_149 = Create_Table.Table_Detail("ATE_AC100M_149", self.TAB_OBS_AC100M, 520, 115, 520, 130, 500, 180)
        self.table_ATE_044 = Create_Table.Table_Detail("ATE_AC100M_044", self.TAB_FVT_AC100M, 10, 115, 10, 130, 500, 226)
        self.table_ATE_046 = Create_Table.Table_Detail("ATE_AC100M_046", self.TAB_FVT_AC100M, 520, 115, 520, 130, 500, 226)
        self.table_ATE_060 = Create_Table.Table_Detail("ATE_AC100M_060", self.TAB_FVT_AC100M, 1030, 115, 1030, 130, 500, 226)
        self.table_ATE_061 = Create_Table.Table_Detail("ATE_AC100M_061", self.TAB_FVT_AC100M, 10, 365, 10, 380, 500, 226)
        self.table_ATE_067 = Create_Table.Table_Detail("ATE_AC100M_067", self.TAB_FVT_AC100M, 520, 365, 520, 380, 500, 226)
        self.table_ATE_110 = Create_Table.Table_Detail("ATE_AC100M_110", self.TAB_EXS_AC100M, 10, 115, 10, 130, 600, 687)
        self.table_ATE_128 = Create_Table.Table_Detail("ATE_AC100M_128", self.TAB_EXS_AC100M, 620, 115, 620, 130, 600, 687)

        # Create table AC200 ********************************************************************************
        self.table_ATE_103 = Create_Table.Table_Detail("ATE_AC200_103", self.TAB_OBS_AC200, 10, 115, 10, 130, 500, 180)
        self.table_ATE_035 = Create_Table.Table_Detail("ATE_AC200_035", self.TAB_FVT_AC200, 10, 115, 10, 130, 500, 226)
        self.table_ATE_067_2 = Create_Table.Table_Detail("ATE_AC200_067", self.TAB_FVT_AC200, 520, 115, 520, 130, 500, 226)
        self.table_ATE_083 = Create_Table.Table_Detail("ATE_AC200_083", self.TAB_FVT_AC200, 10, 365, 10, 380, 500, 226)
        self.table_ATE_104 = Create_Table.Table_Detail("ATE_AC200_104", self.TAB_FVT_AC200, 520, 365, 520, 380, 500, 226)
        self.table_ATE_131 = Create_Table.Table_Detail("ATE_AC200_131", self.TAB_EXS_AC200, 10, 115, 10, 130, 600, 687)
        self.table_ATE_155 = Create_Table.Table_Detail("ATE_AC200_155", self.TAB_EXS_AC200, 620, 115, 620, 130, 600, 687)

        # Create table AC400 ********************************************************************************
        self.table_ATE_063 = Create_Table.Table_Detail("ATE_AC400_063", self.TAB_OBS_AC400, 10, 115, 10, 130, 500, 111)
        self.table_ATE_136 = Create_Table.Table_Detail("ATE_AC400_136", self.TAB_FVT_AC400, 10, 115, 10, 130, 500, 203)
        self.table_ATE_125 = Create_Table.Table_Detail("ATE_AC400_125", self.TAB_EXS_AC400, 10, 115, 10, 130, 500, 203)

        # Create table ZEPHYR ********************************************************************************
        self.table_ATE_242 = Create_Table.Table_Detail("ATE_400ZR_242", self.TAB_FCAL_ZEPHYR, 10, 115, 10, 130, 500, 319)
        self.table_ATE_247 = Create_Table.Table_Detail("ATE_400ZR_247", self.TAB_FCAL_ZEPHYR, 520, 115, 520, 130, 500, 319)
        self.table_ATE_251 = Create_Table.Table_Detail("ATE_400ZR_251", self.TAB_FCAL_ZEPHYR, 1030, 115, 1030, 130, 500, 319)
        self.table_ATE_272 = Create_Table.Table_Detail("ATE_400ZR_272", self.TAB_FCAL_ZEPHYR, 10, 460, 10, 475, 500, 319)
        self.table_ATE_278 = Create_Table.Table_Detail("ATE_400ZR_278", self.TAB_FCAL_ZEPHYR, 520, 460, 520, 475, 500, 319)
        self.table_ATE_242_2 = Create_Table.Table_Detail("ATE_400ZR_242", self.TAB_OPM_ZEPHYR, 10, 115, 10, 130, 200, 319)
        self.table_ATE_243 = Create_Table.Table_Detail("ATE_400ZR_243", self.TAB_OPM_ZEPHYR, 220, 115, 220, 130, 200, 319)
        self.table_ATE_249 = Create_Table.Table_Detail("ATE_400ZR_249", self.TAB_OPM_ZEPHYR, 430, 115, 430, 130, 200, 319)
        self.table_ATE_267 = Create_Table.Table_Detail("ATE_400ZR_267", self.TAB_OPM_ZEPHYR, 640, 115, 640, 130, 200, 319)
        self.table_ATE_271 = Create_Table.Table_Detail("ATE_400ZR_271", self.TAB_OPM_ZEPHYR, 850, 115, 850, 130, 200, 319)
        self.table_ATE_273 = Create_Table.Table_Detail("ATE_400ZR_273", self.TAB_OPM_ZEPHYR, 1060, 115, 1060, 130, 200, 319)
        self.table_ATE_293 = Create_Table.Table_Detail("ATE_400ZR_293", self.TAB_OPM_ZEPHYR, 1270, 115, 1270, 130, 200, 319)
        self.table_ATE_294 = Create_Table.Table_Detail("ATE_400ZR_294", self.TAB_OPM_ZEPHYR, 10, 460, 10, 475, 200, 319)
        self.table_ATE_297 = Create_Table.Table_Detail("ATE_400ZR_297", self.TAB_OPM_ZEPHYR, 220, 460, 220, 475, 200, 319)
        self.table_ATE_298 = Create_Table.Table_Detail("ATE_400ZR_298", self.TAB_OPM_ZEPHYR, 430, 460, 430, 475, 200, 319)
        self.table_ATE_302 = Create_Table.Table_Detail("ATE_400ZR_302", self.TAB_OPM_ZEPHYR, 640, 460, 640, 475, 200, 319)
        self.table_ATE_304 = Create_Table.Table_Detail("ATE_400ZR_304", self.TAB_OPM_ZEPHYR, 850, 460, 850, 475, 200, 319)
        self.table_ATE_319 = Create_Table.Table_Detail("ATE_400ZR_319", self.TAB_OPM_ZEPHYR, 1060, 460, 1060, 475, 200, 319)
        self.table_ATE_262 = Create_Table.Table_Detail("ATE_400ZR_262", self.TAB_EXS_ZEPHYR, 10, 115, 10, 130, 400, 319)
        self.table_ATE_280 = Create_Table.Table_Detail("ATE_400ZR_280", self.TAB_EXS_ZEPHYR, 420, 115, 420, 130, 400, 319)
        self.table_ATE_305 = Create_Table.Table_Detail("ATE_400ZR_305", self.TAB_EXS_ZEPHYR, 830, 115, 830, 130, 400, 319)
        self.table_ATE_306 = Create_Table.Table_Detail("ATE_400ZR_306", self.TAB_EXS_ZEPHYR, 1240, 115, 1240, 130, 400, 319)
        self.table_ATE_316 = Create_Table.Table_Detail("ATE_400ZR_316", self.TAB_EXS_ZEPHYR, 10, 460, 10, 475, 400, 319)
        self.table_ATE_330 = Create_Table.Table_Detail("ATE_400ZR_330", self.TAB_EXS_ZEPHYR, 420, 460, 420, 475, 400, 319)
        self.table_ATE_345 = Create_Table.Table_Detail("ATE_400ZR_345", self.TAB_EXS_ZEPHYR, 830, 460, 830, 475, 400, 319)
        self.table_ATE_358 = Create_Table.Table_Detail("ATE_400ZR_358", self.TAB_EXS_ZEPHYR, 1240, 460, 1240, 475, 400, 319)
        self.table_ATE_233 = Create_Table.Table_Detail("ATE_400ZR_233", self.TAB_EBT_OEM, 10, 115, 10, 130, 400, 273)
        self.table_ATE_275 = Create_Table.Table_Detail("ATE_400ZR_275", self.TAB_EBT_OEM, 420, 115, 420, 130, 400, 273)
        self.table_ATE_310 = Create_Table.Table_Detail("ATE_400ZR_310", self.TAB_EBT_OEM, 830, 115, 830, 130, 400, 273)
        self.table_ATE_328 = Create_Table.Table_Detail("ATE_400ZR_328", self.TAB_EBT_OEM, 1240, 115, 1240, 130, 400, 273)

        # Create table ODB ********************************************************************************
        self.table_ATE_239 = Create_Table.Table_Detail("ATE_ODB_239", self.TAB_CAL_ODB, 10, 115, 10, 130, 1000, 134)
        self.table_ATE_261 = Create_Table.Table_Detail("ATE_ODB_261", self.TAB_CAL_ODB, 10, 275, 10, 290, 1000, 134)
        self.table_ATE_349 = Create_Table.Table_Detail("ATE_ODB_349", self.TAB_CAL_ODB, 10, 435, 10, 450, 1000, 134)

        # Create table NITLA ********************************************************************************
        self.table_ATE_261_2 = Create_Table.Table_Detail("ATE_NITLA_261", self.TAB_CAL_NITLA, 10, 115, 10, 130, 1000, 134)
        self.table_ATE_303 = Create_Table.Table_Detail("ATE_NITLA_303", self.TAB_CAL_NITLA, 10, 275, 10, 290, 1000, 134)

        # Create table AX1200 ********************************************************************************
        self.table_ATE_331 = Create_Table.Table_Detail("ATE_AX1200_331", self.TAB_PCAL_AX1200, 10, 115, 10, 130, 1000, 319)
        self.table_ATE_362 = Create_Table.Table_Detail("ATE_AX1200_362", self.TAB_FVT_AX1200, 10, 470, 10, 130, 1000, 319)
        self.table_ATE_356 = Create_Table.Table_Detail("ATE_AX1200_356", self.TAB_FVT_AX1200, 10, 115, 10, 130, 1000, 319)
        self.table_ATE_195_2 = Create_Table.Table_Detail("ATE_AX1200_195", self.TAB_EXS_AX1200, 10, 115, 10, 130, 1000, 319)

        # Create Table Yield *********************************************************************************  
        Header_Yield = ["Process","Input","PASS","FAIL","YIELD"] 
        self.table_yield = QtWidgets.QTableWidget(self)
        self.table_yield.move(1390, 5)
        self.table_yield.setFixedSize(266, 140)
        self.table_yield.setColumnCount(len(Header_Yield))
        self.table_yield.setHorizontalHeaderLabels(Header_Yield)
        self.table_yield.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_yield.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for i in range(self.table_yield.columnCount()): # Resize column
                self.table_yield.setColumnWidth(i, 53)

        self.CY = "00.00"
        self.Cumulative_Yield = QLabel("Cumulative Yield : " + self.CY, self.Main_TAB)
        self.Cumulative_Yield.move(1270, 80)
    
        #*****************************************************************************************************      
        self.setCentralWidget(self.Main_TAB)
        self.setGeometry(250,40,1660,965)
        self.setFixedSize(1660,965)
        self.Main_TAB.setCurrentIndex(0) # Choose Page in TAB
        self.TAB_PROCESS_AC1200.setCurrentIndex(0)
        self.TAB_PROCESS_AC100M.setCurrentIndex(0) 
        self.TAB_PROCESS_AC200.setCurrentIndex(0) 
        self.TAB_PROCESS_AC400.setCurrentIndex(0) 
        self.TAB_PROCESS_ZEPHYR.setCurrentIndex(0)
        self.TAB_PROCESS_AX1200.setCurrentIndex(0)
        self.Main_TAB.currentChanged.connect(self.updateLabel)
        self.TAB_Name = "AC1200"    
        
        Table_Array_1 = [self.table_ATE_132, self.table_ATE_182, self.table_ATE_256, self.table_ATE_266, self.table_ATE_309, self.table_ATE_331, self.table_ATE_362, self.table_ATE_356,  self.table_ATE_195_2]
        Table_Array_2 = [self.table_ATE_169, self.table_ATE_170, self.table_ATE_183, self.table_ATE_187, self.table_ATE_188, self.table_ATE_210, self.table_ATE_215, self.table_ATE_223, self.table_ATE_257, self.table_ATE_259, self.table_ATE_265, self.table_ATE_270]
        Table_Array_3 = [self.table_ATE_154, self.table_ATE_195, self.table_ATE_211, self.table_ATE_213, self.table_ATE_252, self.table_ATE_254]
        Table_Array_4 = [self.table_ATE_100, self.table_ATE_149, self.table_ATE_044, self.table_ATE_046, self.table_ATE_060, self.table_ATE_061, self.table_ATE_067, self.table_ATE_110, self.table_ATE_128]
        Table_Array_5 = [self.table_ATE_103, self.table_ATE_035, self.table_ATE_067_2, self.table_ATE_083, self.table_ATE_104,self.table_ATE_131, self.table_ATE_155]
        Table_Array_6 = [self.table_ATE_063,self.table_ATE_136, self.table_ATE_125, self.table_ATE_239, self.table_ATE_261, self.table_ATE_349, self.table_ATE_261_2, self.table_ATE_303]
        Table_Array_7 = [self.table_ATE_242, self.table_ATE_247, self.table_ATE_251, self.table_ATE_272, self.table_ATE_278]
        Table_Array_8 = [self.table_ATE_242_2, self.table_ATE_243, self.table_ATE_249, self.table_ATE_267, self.table_ATE_271, self.table_ATE_273, self.table_ATE_293, self.table_ATE_294, self.table_ATE_297, self.table_ATE_298, self.table_ATE_302, self.table_ATE_304, self.table_ATE_319]
        Table_Array_9 = [self.table_ATE_262, self.table_ATE_280, self.table_ATE_305, self.table_ATE_306, self.table_ATE_316, self.table_ATE_330, self.table_ATE_345, self.table_ATE_358, self.table_ATE_233, self.table_ATE_275, self.table_ATE_310, self.table_ATE_328]   
        
        for table_station in Table_Array_1 + Table_Array_2 + Table_Array_3 + Table_Array_4 + Table_Array_5 + Table_Array_6 + Table_Array_7 + Table_Array_8 + Table_Array_9:
            table_station.setContextMenuPolicy(Qt.CustomContextMenu)
            table_station.customContextMenuRequested.connect(lambda pos, table=table_station: self.showMenu(pos, table))
        
        self.text_time = QLabel('', self)
        self.text_time.setGeometry(10,930,250,20)

        self.timer = QTimer()
        self.timer.timeout.connect(self.Query_SQL)
        self.timer.start(60000)
    
    def force_run(self):
        self.Query_SQL()

    def fresh_selector(self):
        if self.all_unit_button.isChecked():
            self.fresh = "\n--and TEST_COUNT in ('1')"
        elif self.fresh_unit_button.isChecked():
            self.fresh = "\nand TEST_COUNT in ('1')"
            
        self.Query_SQL()

    def pareto_chart(self):
        dialog = QDialog(self)    

        lable_station = QLabel("Select STATION_ID", dialog)
        lable_station.move(14, 5)
        self.pareto_station = QComboBox(dialog)
        with open('temp/STATION_ID.txt', 'r') as f:
            file_read = f.read()
        file_read = file_read.split('\n')
        for i in file_read:
            self.pareto_station.addItem(i)
        self.pareto_station.currentIndexChanged.connect(self.station_mapping_process)
        self.pareto_station.setGeometry(14,20,150,30)
        
        lable_day = QLabel("Select Day", dialog)
        lable_day.move(180, 5)
        self.day_pareto = QComboBox(dialog)
        self.day_pareto.addItem("1")
        self.day_pareto.addItem("2")
        self.day_pareto.addItem("3")
        self.day_pareto.addItem("5")
        self.day_pareto.addItem("7")
        self.day_pareto.addItem("14")
        self.day_pareto.addItem("30")
        self.day_pareto.addItem("90")
        self.day_pareto.setGeometry(180,20,50,30)

        process_label = QLabel("Select Process", dialog)
        process_label.move(250,5)
        self.process_dropbox = QComboBox(dialog)
        Array_Process = ['OIT', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5']
        for i in Array_Process:
            self.process_dropbox.addItem(i)
        self.process_dropbox.setGeometry(250, 20, 50, 30)

        font = QFont()
        font.setBold(True)
        button_pareto = QPushButton("Refresh", dialog)
        button_pareto.setGeometry(400, 20, 100, 30)
        button_pareto.setStyleSheet("background-color: #FFF2C9; color: black;")
        button_pareto.setFont(font)
        button_pareto.clicked.connect(self.query_pareto)

        self.Graph = QChart()
        self.Graph.setAnimationOptions(QChart.SeriesAnimations)
        self.series = QBarSeries()

        Graph_View = QChartView(self.Graph, dialog)
        Graph_View.setRenderHint(QPainter.Antialiasing)
                    
        Graph_View.setGeometry(5,50,1200,780)
        dialog.setGeometry(100,100,1600,830)
        dialog.show()
    
    def station_mapping_process(self):
        self.position = self.process_dropbox.currentIndex()
        self.process_dropbox.clear()
        station = str(self.pareto_station.currentText())
        station = station.split('_')
        if station[1] == 'AC1200':
            Array_Process = ['OIT', 'CAL', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS5'] 
        elif station[1] == 'AC100M' or station[1] == 'AC200' or station[1] == 'AC400':
            Array_Process = ['OBS', 'FST', 'FVT', 'EPT', 'ESS', 'EXP', 'EXS']
        elif station[1] == '400ZR':
            Array_Process = ['FCAL', 'OPM', 'OPMP', 'OPMT', 'EXP', 'EXS']
            
        for i in Array_Process:
            self.process_dropbox.addItem(i)
        self.process_dropbox.setCurrentIndex(self.position)
    
    def query_pareto(self):
        process = "('" + self.process_dropbox.currentText() + "')" + "\nand MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')"
        Query_Result_Test = QueryResultTest()
        self.DATA_All = Query_Result_Test.Receive_Data([self.pareto_station.currentText()], self.day_pareto.currentText(), process, "\nand TEST_COUNT in ('1')", self.TAB_Name)    
        
        if self.DATA_All != [[]]:   
            self.series.clear()     
            array_result = []
            for i in self.DATA_All[0]:
                array_result.append(i[3])
            array_result = list(set(array_result))
            
            group_dict = {}
            count = 0
            for i in array_result:
                count = 0
                for j in self.DATA_All[0]:
                    if i != 'PASS':
                        if j[3] == i:
                            count += 1
                        group_dict[str(i)] = str(count)
            group_dict = {k: v for k, v in sorted(group_dict.items(), key=lambda item: int(item[1]), reverse=True)}
            group_val = [int(count) for count in group_dict.values()]
            bar_set = QBarSet('All Failure')
            for key, value in group_dict.items():
                bar_set.append(int(value))
                bar_set.setColor(Qt.red)
                self.series.append(bar_set)

            self.Graph.addSeries(self.series)
            self.Graph.createDefaultAxes()

            axisY = QValueAxis()
            axisY.hide()
            axisY.setRange(0, max(group_val) + 0.5)

            self.Graph.addAxis(axisY, Qt.AlignLeft)
            self.series.attachAxis(axisY)

            self.axis_x = QBarCategoryAxis()
            self.axis_x.setLabelsAngle(-90)
            self.axis_x.append(list(group_dict.keys()))
            self.Graph.setAxisX(self.axis_x, self.series)  
     
    def load_plot_cal_file(self):
        # file_path = "temp\\Calibration_Monitor.exe"
        # os.startfile(file_path)
        # CREATE_NO_WINDOW = 0x08000000
        # subprocess.Popen(["python", file_path], creationflags=CREATE_NO_WINDOW)

        dialog = QDialog(self)

        self.Main_Tab_Dis = QTabWidget(dialog)      
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
        self.TAB_Graph_LF.setGeometry(0, 0, 1835, 985)
        self.TAB_Graph_LF.setCurrentIndex(0)

        self.TAB_Graph_BL = QTabWidget(self.Base_Line_Page)
        self.Page_AC1200_BL = QWidget()
        self.TAB_Graph_BL.addTab(self.Page_AC1200_BL, "AC1200 BL")
        self.Page_400ZR_BL = QWidget()
        self.TAB_Graph_BL.addTab(self.Page_400ZR_BL, "400ZR BL")
        for i in range(2):
            self.TAB_Graph_BL.tabBar().setTabVisible(i, False)
        self.TAB_Graph_BL.setGeometry(0, 0, 1835, 985)
        self.TAB_Graph_BL.setCurrentIndex(0)

        # Create ratio button
        self.button_group_LF_BL = QButtonGroup()
        self.button_group_LF_BL.setExclusive(True)

        self.LF_Page = QRadioButton("Loss Factor Page", dialog)
        self.LF_Page.setChecked(True)
        self.LF_Page.move(550, 30)
        self.BL_Page = QRadioButton("Base Line Page", dialog)
        self.BL_Page.move(660, 30)

        self.button_group_LF_BL.addButton(self.LF_Page)
        self.button_group_LF_BL.addButton(self.BL_Page)

        self.LF_Page.clicked.connect(lambda: self.radio_update(page=0))
        self.BL_Page.clicked.connect(lambda: self.radio_update(page=1))
        self.Main_Tab_Dis.setCurrentIndex(0)

        # Create ratio Mode
        self.button_group_mode = QButtonGroup()
        self.button_group_mode.setExclusive(True)

        self.mode_slot = QRadioButton("Mode By SLOTs", dialog)
        self.mode_slot.setChecked(True)
        self.mode_slot.move(950, 30)
        self.mode_ate = QRadioButton("Mode Merge SLOT", dialog)
        self.mode_ate.move(1060, 30)

        self.button_group_mode.addButton(self.mode_slot)
        self.button_group_mode.addButton(self.mode_ate)

        self.mode_slot.clicked.connect(lambda: self.hide_graph(active=False))
        self.mode_ate.clicked.connect(lambda: self.hide_graph(active=True))

        self.graph_by_station = QChart()
        self.graph_by_station_view = QChartView(self.graph_by_station, dialog)
        self.graph_by_station_view.setRenderHint(QPainter.Antialiasing)
        self.graph_by_station_view.setGeometry(25,80,1810,900)
        self.graph_by_station_view.setVisible(False)

        # Create ratio button for page LOSS_FACTOR, TAB_POWER, UUT_POWER
        self.button_group_page = QButtonGroup()
        self.button_group_page.setExclusive(True)

        self.loss_factor_page = QRadioButton("Loss Factor Page", dialog)
        self.loss_factor_page.setChecked(True)
        self.loss_factor_page.move(25, 60)
        self.tap_power_page = QRadioButton("Tab Power Page", dialog)
        self.tap_power_page.move(145, 60)    
        self.uut_power_page = QRadioButton("UUT Power Page", dialog)
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
        last_BL_changed = QLabel("Timestamp of last Base Line changed", dialog)
        last_BL_changed.setGeometry(1450, 31, 220, 20)
        last_BL_changed.setFont(font_L)

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.data_last_BL_changed = QLineEdit("", dialog)
        self.data_last_BL_changed.setGeometry(1666, 27, 170, 30)
        self.data_last_BL_changed.setAlignment(Qt.AlignCenter)
        self.data_last_BL_changed.setFont(font)
        self.data_last_BL_changed.setStyleSheet("background-color: red; color: yellow")

        # Creat dropdown day
        day_label = QLabel("Select Day", dialog)
        day_label.move(23,30)
        self.day_dropbox_dis = QComboBox(dialog)
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
        self.day_dropbox_dis.move(80,24)
        self.day_dropbox_dis.setFixedSize(50,30)

        self.day_dropbox_dis.currentTextChanged.connect(self.Plot_Graph)

        file = open("temp/STATION_ID.txt", "r")
        file_read = file.read()
        All_STATION_Array = file_read.split('\n')
        self.STATION_Label = QLabel("Select STATION", dialog)
        self.STATION_Label.move(150,32)
        self.STATION_dropbox = QComboBox(dialog)
        self.STATION_dropbox.move(230,24)
        self.STATION_dropbox.setFixedSize(140,30)  
        for i in All_STATION_Array:
            self.STATION_dropbox.addItem(i)   
        self.STATION_dropbox.currentIndexChanged.connect(self.Station_Mapping)

        # Create button
        self.query_button = QPushButton("Refresh", dialog)     
        self.query_button.move(400,24)
        self.query_button.setFixedSize(100, 30)
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

        self.distribute_plot = QPushButton("Plot Distribute", dialog)
        self.distribute_plot.setGeometry(800,25,100,30)
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
        
        self.station_id = ['ATE','AC1200','132']
        self.x_axis_graph = []
        self.Main_Tab_Dis.setGeometry(10,10,1840,990)
        dialog.setGeometry(30,40,0,0)
        dialog.setFixedSize(1850,1005)
        dialog.show()

    def hide_graph(self, active):
        self.graph_by_station_view.setVisible(active)

        if active == True:
            self.Plot_Merge_Slot()
    
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

                    # Open file dialog after saving
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
            dialog = QDialog(self)
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
            dialog.setLayout(layout)
            dialog.setWindowTitle("Raw Data")
            dialog.setGeometry(300,150,0,0)
            dialog.setFixedSize(740,400)
            dialog.show()
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

    def limit_setting (self):
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

    def Plot_Merge_Slot(self):
        parameter_selected = 'Loss Factor'
        if self.loss_factor_page.isChecked():
            parameter_selected = 'Loss Factor'
        elif self.tap_power_page.isChecked():
            parameter_selected = 'Tap Power'
        elif self.uut_power_page.isChecked():
            parameter_selected = 'UUT Power'

        Query_Value_ATE_CAL = QueryValueATECAL()

        Loss_Factor = Query_Value_ATE_CAL.input_detai(self.day_dropbox_dis.currentText(), self.STATION_dropbox.currentText(), parameter_selected)
        Date_Array = []
        Step_Name = []
        Value = []
        for i in Loss_Factor:
            Date_Array.append(i[1])
            Step_Name.append(i[3])
            Value.append(i[4])

        TX_LANE0 = []
        Value_TX_LANE0 = []
        Date_TX_LANE0 = []

        TX_LANE1 = []
        Value_TX_LANE1 = []
        Date_TX_LANE1 = []

        RX_LANE0 = []
        Value_RX_LANE0 = []
        Date_RX_LANE0 = []

        RX_LANE1 = []
        Value_RX_LANE1 = []
        Date_RX_LANE1 = []
        for i,j,k in zip(Step_Name, Value, Date_Array):
            if i[-2] == "T":
                for char in i:
                    if char.isdigit():
                        if int(char) % 2 != 0:
                            TX_LANE0.append(i)
                            Value_TX_LANE0.append(j)
                            Date_TX_LANE0.append(k)
                        elif int(char) % 2 == 0:
                            TX_LANE1.append(i)
                            Value_TX_LANE1.append(j)
                            Date_TX_LANE1.append(k)
            if i[-2] == "R":
                for char in i:
                    if char.isdigit():
                        if int(char) % 2 != 0:
                            RX_LANE0.append(i)
                            Value_RX_LANE0.append(j)
                            Date_RX_LANE0.append(k)
                        elif int(char) % 2 == 0:
                            RX_LANE1.append(i)
                            Value_RX_LANE1.append(j)
                            Date_RX_LANE1.append(k)

        New_Value_TX_LANE0 = []
        for num, i in enumerate(Value_TX_LANE0):
            New_Value_TX_LANE0.append((num, i))

        New_Value_TX_LANE1 = []
        for num, i in enumerate(Value_TX_LANE1):
            New_Value_TX_LANE1.append((num, i))

        New_Value_RX_LANE0 = []
        for num, i in enumerate(Value_RX_LANE0):
            New_Value_RX_LANE0.append((num, i))

        New_Value_RX_LANE1 = []
        for num, i in enumerate(Value_RX_LANE1):
            New_Value_RX_LANE1.append((num, i))

        print(Date_TX_LANE0)    

        Dict_TX_LANE0 = {'name' : 'TX_LANE0', 'data' : New_Value_TX_LANE0}
        Dict_TX_LANE1 = {'name' : 'TX_LANE1', 'data' : New_Value_TX_LANE1}
        Dict_RX_LANE0 = {'name' : 'RX_LANE0', 'data' : New_Value_RX_LANE0}
        Dict_RX_LANE1 = {'name' : 'RX_LANE1', 'data' : New_Value_RX_LANE1}

        Array_Dict_TX = [Dict_TX_LANE0, Dict_TX_LANE1]
        self.graph_by_station.removeAllSeries()
        serie_dict = {}
        group_data = []
        for data_dict in Array_Dict_TX:
            series_name = data_dict['name'] # Serie name
            series = QLineSeries()
            series.setPointsVisible(True) # Show marker point
            for point in data_dict['data']:
                x_val = int(point[0])                   
                y_val = float(point[1])
                series.append(x_val, y_val)
                group_data.append(y_val)  
            series.setName(series_name)
            self.graph_by_station.addSeries(series)
            serie_dict[series_name] = series
        
        self.graph_by_station.createDefaultAxes()
        self.graph_by_station.axisX().hide()
        self.graph_by_station.axisY().hide()

    def Plot_Graph(self):
        self.day_selected = self.day_dropbox_dis.currentText()
        self.station_selected = self.STATION_dropbox.currentText()

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
            
            else:
                QMessageBox.information(self, "Notify", "Have no any data found")

    def LC_CH_Yield(self):
        print("OK")
        # file_path = "temp\\Yield_LINECARD_CHASSIS.exe"
        # os.startfile(file_path)
        # # CREATE_NO_WINDOW = 0x08000000
        # # subprocess.Popen(["python", file_path], creationflags=CREATE_NO_WINDOW)

    def updateLabel(self, index):
        self.TAB_Name = self.Main_TAB.tabText(index)
        self.Query_SQL()

    def Query_SQL(self): 
        try:
            time_now = datetime.now()
            current_date = time_now.strftime("%d/%b/%Y %I:%M:%S")
            self.text_time.setText(f'Last time refresh : {current_date}')

            self.progress_bar.setVisible(True)
            
            # with open('temp/trigger.txt', 'w') as f:
            #     f.write('1')  
            # time.sleep(0.1)
            # self.loading_GIF()
            
            self.day = self.day_dropbbox.currentText()
            if self.all_unit_button.isChecked():
                self.fresh = "\n--and TEST_COUNT in ('1')"
            elif self.fresh_unit_button.isChecked():
                self.fresh = "\nand TEST_COUNT in ('1')"
                
            STATION_ID = []
            SLOT_Quantity = 0
            Table_Array = []
            rows_header = []
            if self.TAB_Name == "AC1200":
                Process_for_Yield = ['OIT', 'CAL', 'FVT', 'ESS', 'EXS5']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "AC1200")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.oit_button_AC1200.isChecked():
                    self.process = "OIT"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(0)
                    STATION_ID = ["ATE_AC1200_132", "ATE_AC1200_182", "ATE_AC1200_256", "ATE_AC1200_266"]
                    Table_Array = [self.table_ATE_132, self.table_ATE_182, self.table_ATE_256, self.table_ATE_266]
                    SLOT_Quantity = 3
                elif self.cal_button_AC1200.isChecked():
                    self.process = "CAL"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(1)
                    STATION_ID = ["ATE_AC1200_309"]
                    Table_Array = [self.table_ATE_309]
                    SLOT_Quantity = 6
                elif self.fst_button_AC1200.isChecked():
                    self.process = "FST"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(2)
                    STATION_ID = ["ATE_AC1200_169", "ATE_AC1200_170", "ATE_AC1200_183", "ATE_AC1200_187", "ATE_AC1200_188", "ATE_AC1200_210", "ATE_AC1200_215", "ATE_AC1200_223", "ATE_AC1200_257", "ATE_AC1200_259", "ATE_AC1200_265", "ATE_AC1200_270"]
                    Table_Array = [self.table_ATE_169, self.table_ATE_170, self.table_ATE_183, self.table_ATE_187, self.table_ATE_188, self.table_ATE_210, self.table_ATE_215, self.table_ATE_223, self.table_ATE_257, self.table_ATE_259, self.table_ATE_265, self.table_ATE_270]
                    SLOT_Quantity = 7
                elif self.fvt_button_AC1200.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(2)
                    STATION_ID = ["ATE_AC1200_169", "ATE_AC1200_170", "ATE_AC1200_183", "ATE_AC1200_187", "ATE_AC1200_188", "ATE_AC1200_210", "ATE_AC1200_215", "ATE_AC1200_223", "ATE_AC1200_257", "ATE_AC1200_259", "ATE_AC1200_265", "ATE_AC1200_270"]
                    Table_Array = [self.table_ATE_169, self.table_ATE_170, self.table_ATE_183, self.table_ATE_187, self.table_ATE_188, self.table_ATE_210, self.table_ATE_215, self.table_ATE_223, self.table_ATE_257, self.table_ATE_259, self.table_ATE_265, self.table_ATE_270]
                    SLOT_Quantity = 7
                elif self.ept_button_AC1200.isChecked():
                    self.process = "EPT"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(2)
                    STATION_ID = ["ATE_AC1200_169", "ATE_AC1200_170", "ATE_AC1200_183", "ATE_AC1200_187", "ATE_AC1200_188", "ATE_AC1200_210", "ATE_AC1200_215", "ATE_AC1200_223", "ATE_AC1200_257", "ATE_AC1200_259", "ATE_AC1200_265", "ATE_AC1200_270"]
                    Table_Array = [self.table_ATE_169, self.table_ATE_170, self.table_ATE_183, self.table_ATE_187, self.table_ATE_188, self.table_ATE_210, self.table_ATE_215, self.table_ATE_223, self.table_ATE_257, self.table_ATE_259, self.table_ATE_265, self.table_ATE_270]
                    SLOT_Quantity = 7
                elif self.ess_button_AC1200.isChecked():
                    self.process = "ESS"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(2)
                    STATION_ID = ["ATE_AC1200_169", "ATE_AC1200_170", "ATE_AC1200_183", "ATE_AC1200_187", "ATE_AC1200_188", "ATE_AC1200_210", "ATE_AC1200_215", "ATE_AC1200_223", "ATE_AC1200_257", "ATE_AC1200_259", "ATE_AC1200_265", "ATE_AC1200_270"]
                    Table_Array = [self.table_ATE_169, self.table_ATE_170, self.table_ATE_183, self.table_ATE_187, self.table_ATE_188, self.table_ATE_210, self.table_ATE_215, self.table_ATE_223, self.table_ATE_257, self.table_ATE_259, self.table_ATE_265, self.table_ATE_270]
                    SLOT_Quantity = 7
                elif self.exp_button_AC1200.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(3)
                    STATION_ID = ["ATE_AC1200_154", "ATE_AC1200_195", "ATE_AC1200_211", "ATE_AC1200_213", "ATE_AC1200_252", "ATE_AC1200_254"]
                    Table_Array = [self.table_ATE_154, self.table_ATE_195, self.table_ATE_211, self.table_ATE_213, self.table_ATE_252, self.table_ATE_254]
                    SLOT_Quantity = 15
                elif self.exs5_button_AC1200.isChecked():
                    self.process = "EXS5"
                    self.TAB_PROCESS_AC1200.setCurrentIndex(3)
                    STATION_ID = ["ATE_AC1200_154", "ATE_AC1200_195", "ATE_AC1200_211", "ATE_AC1200_213", "ATE_AC1200_252", "ATE_AC1200_254"]
                    Table_Array = [self.table_ATE_154, self.table_ATE_195, self.table_ATE_211, self.table_ATE_213, self.table_ATE_252, self.table_ATE_254]
                    SLOT_Quantity = 15
            elif self.TAB_Name == "AC100M":
                Process_for_Yield = ['OBS', 'FVT', 'ESS', 'EXS']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "AC100M")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.obs_button_AC100M.isChecked():
                    self.process = "OBS"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(0) 
                    STATION_ID = ["ATE_AC100M_100", "ATE_AC100M_149"]
                    Table_Array = [self.table_ATE_100, self.table_ATE_149]
                    SLOT_Quantity = 6
                elif self.fst_button_AC100M.isChecked():
                    self.process = "FST"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC100M_044", "ATE_AC100M_046", "ATE_AC100M_060", "ATE_AC100M_061", "ATE_AC100M_067"]
                    Table_Array = [self.table_ATE_044, self.table_ATE_046, self.table_ATE_060, self.table_ATE_061, self.table_ATE_067]
                    SLOT_Quantity = 8
                elif self.fvt_button_AC100M.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC100M_044", "ATE_AC100M_046", "ATE_AC100M_060", "ATE_AC100M_061", "ATE_AC100M_067"]
                    Table_Array = [self.table_ATE_044, self.table_ATE_046, self.table_ATE_060, self.table_ATE_061, self.table_ATE_067]
                    SLOT_Quantity = 8
                elif self.ept_button_AC100M.isChecked():
                    self.process = "EPT"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC100M_044", "ATE_AC100M_046", "ATE_AC100M_060", "ATE_AC100M_061", "ATE_AC100M_067"]
                    Table_Array = [self.table_ATE_044, self.table_ATE_046, self.table_ATE_060, self.table_ATE_061, self.table_ATE_067]
                    SLOT_Quantity = 8
                elif self.ess_button_AC100M.isChecked():
                    self.process = "ESS"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC100M_044", "ATE_AC100M_046", "ATE_AC100M_060", "ATE_AC100M_061", "ATE_AC100M_067"]
                    Table_Array = [self.table_ATE_044, self.table_ATE_046, self.table_ATE_060, self.table_ATE_061, self.table_ATE_067]
                    SLOT_Quantity = 8
                elif self.exp_button_AC100M.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC100M_110", "ATE_AC100M_128"]
                    Table_Array = [self.table_ATE_110, self.table_ATE_128]        
                    SLOT_Quantity = 28
                elif self.exs_button_AC100M.isChecked():
                    self.process = "EXS"
                    self.TAB_PROCESS_AC100M.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC100M_110", "ATE_AC100M_128"]
                    Table_Array = [self.table_ATE_110, self.table_ATE_128]        
                    SLOT_Quantity = 28
            elif self.TAB_Name == "AC200":
                Process_for_Yield = ['OBS', 'FVT', 'ESS', 'EXS']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "AC200")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.obs_button_AC200.isChecked():
                    self.process = "OBS"
                    self.TAB_PROCESS_AC200.setCurrentIndex(0) 
                    STATION_ID = ["ATE_AC200_103",]
                    Table_Array = [self.table_ATE_103]
                    SLOT_Quantity = 6
                elif self.fst_button_AC200.isChecked():
                    self.process = "FST"
                    self.TAB_PROCESS_AC200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC200_035", "ATE_AC200_067", "ATE_AC200_083", "ATE_AC200_104"]
                    Table_Array = [self.table_ATE_035, self.table_ATE_067_2, self.table_ATE_083, self.table_ATE_104]
                    SLOT_Quantity = 8
                elif self.fvt_button_AC200.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_AC200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC200_035", "ATE_AC200_067", "ATE_AC200_083", "ATE_AC200_104"]
                    Table_Array = [self.table_ATE_035, self.table_ATE_067_2, self.table_ATE_083, self.table_ATE_104]
                    SLOT_Quantity = 8
                elif self.ept_button_AC200.isChecked():
                    self.process = "EPT"
                    self.TAB_PROCESS_AC200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC200_035", "ATE_AC200_067", "ATE_AC200_083", "ATE_AC200_104"]
                    Table_Array = [self.table_ATE_035, self.table_ATE_067_2, self.table_ATE_083, self.table_ATE_104]
                    SLOT_Quantity = 8
                elif self.ess_button_AC200.isChecked():
                    self.process = "ESS"
                    self.TAB_PROCESS_AC200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC200_035", "ATE_AC200_067", "ATE_AC200_083", "ATE_AC200_104"]
                    Table_Array = [self.table_ATE_035, self.table_ATE_067_2, self.table_ATE_083, self.table_ATE_104]
                    SLOT_Quantity = 8
                elif self.exp_button_AC200.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_AC200.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC200_131", "ATE_AC200_155"]
                    Table_Array = [self.table_ATE_131, self.table_ATE_155]
                    SLOT_Quantity = 28
                elif self.exs_button_AC200.isChecked():
                    self.process = "EXS"
                    self.TAB_PROCESS_AC200.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC200_131", "ATE_AC200_155"]
                    Table_Array = [self.table_ATE_131, self.table_ATE_155]
                    SLOT_Quantity = 28
            elif self.TAB_Name == "AC400":
                Process_for_Yield = ['OBS', 'FVT', 'ESS', 'EXS']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "AC400")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.obs_button_AC400.isChecked():
                    self.process = "OBS"
                    self.TAB_PROCESS_AC400.setCurrentIndex(0) 
                    STATION_ID = ["ATE_AC400_063"]
                    Table_Array = [self.table_ATE_063]
                    SLOT_Quantity = 3
                elif self.fst_button_AC400.isChecked():
                    self.process = "FST"
                    self.TAB_PROCESS_AC400.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC400_136"]
                    Table_Array = [self.table_ATE_136]
                    SLOT_Quantity = 7
                elif self.fvt_button_AC400.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_AC400.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC400_136"]
                    Table_Array = [self.table_ATE_136]
                    SLOT_Quantity = 7
                elif self.ept_button_AC400.isChecked():
                    self.process = "EPT"
                    self.TAB_PROCESS_AC400.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC400_136"]
                    Table_Array = [self.table_ATE_136]
                    SLOT_Quantity = 7
                elif self.ess_button_AC400.isChecked():
                    self.process = "ESS"
                    self.TAB_PROCESS_AC400.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AC400_136"]
                    Table_Array = [self.table_ATE_136]
                    SLOT_Quantity = 7
                elif self.exp_button_AC400.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_AC400.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC400_125"]
                    Table_Array = [self.table_ATE_125]
                    SLOT_Quantity = 7
                elif self.exs_button_AC400.isChecked():
                    self.process = "EXS"
                    self.TAB_PROCESS_AC400.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AC400_125"]
                    Table_Array = [self.table_ATE_125]
                    SLOT_Quantity = 7
            elif self.TAB_Name == "ZEPHYR":
                Process_for_Yield = ['FCAL', 'OPM', 'OPMT', 'EXS']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "400ZR")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.fcal_button_ZEPHYR.isChecked():
                    self.process = "FCAL"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(0) 
                    STATION_ID = ["ATE_400ZR_242", "ATE_400ZR_247", "ATE_400ZR_251", "ATE_400ZR_272", "ATE_400ZR_278"]
                    Table_Array = [self.table_ATE_242, self.table_ATE_247, self.table_ATE_251, self.table_ATE_272, self.table_ATE_278]
                    SLOT_Quantity = 12
                elif self.opm_button_ZEPHYR.isChecked():
                    self.process = "OPM"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(1) 
                    STATION_ID = ["ATE_400ZR_242", "ATE_400ZR_243", "ATE_400ZR_249", "ATE_400ZR_267", "ATE_400ZR_271", "ATE_400ZR_273", "ATE_400ZR_293", "ATE_400ZR_294", "ATE_400ZR_297", "ATE_400ZR_298", "ATE_400ZR_302", "ATE_400ZR_304", "ATE_400ZR_319"]
                    Table_Array = [self.table_ATE_242_2, self.table_ATE_243, self.table_ATE_249, self.table_ATE_267, self.table_ATE_271, self.table_ATE_273, self.table_ATE_293, self.table_ATE_294, self.table_ATE_297, self.table_ATE_298, self.table_ATE_302, self.table_ATE_304, self.table_ATE_319]
                    SLOT_Quantity = 12
                elif self.opmp_button_ZEPHYR.isChecked():
                    self.process = "OPMP"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(1) 
                    STATION_ID = ["ATE_400ZR_242", "ATE_400ZR_243", "ATE_400ZR_249", "ATE_400ZR_267", "ATE_400ZR_271", "ATE_400ZR_273", "ATE_400ZR_293", "ATE_400ZR_294", "ATE_400ZR_297", "ATE_400ZR_298", "ATE_400ZR_302", "ATE_400ZR_304", "ATE_400ZR_319"]
                    Table_Array = [self.table_ATE_242_2, self.table_ATE_243, self.table_ATE_249, self.table_ATE_267, self.table_ATE_271, self.table_ATE_273, self.table_ATE_293, self.table_ATE_294, self.table_ATE_297, self.table_ATE_298, self.table_ATE_302, self.table_ATE_304, self.table_ATE_319]
                    SLOT_Quantity = 12
                elif self.opmt_button_ZEPHYR.isChecked():
                    self.process = "OPMT"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(1) 
                    STATION_ID = ["ATE_400ZR_242", "ATE_400ZR_243", "ATE_400ZR_249", "ATE_400ZR_267", "ATE_400ZR_271", "ATE_400ZR_273", "ATE_400ZR_293", "ATE_400ZR_294", "ATE_400ZR_297", "ATE_400ZR_298", "ATE_400ZR_302", "ATE_400ZR_304", "ATE_400ZR_319"]
                    Table_Array = [self.table_ATE_242_2, self.table_ATE_243, self.table_ATE_249, self.table_ATE_267, self.table_ATE_271, self.table_ATE_273, self.table_ATE_293, self.table_ATE_294, self.table_ATE_297, self.table_ATE_298, self.table_ATE_302, self.table_ATE_304, self.table_ATE_319]
                    SLOT_Quantity = 12
                elif self.exp_button_ZEPHYR.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(2) 
                    STATION_ID = ["ATE_400ZR_262", "ATE_400ZR_280", "ATE_400ZR_305", "ATE_400ZR_306", "ATE_400ZR_316", "ATE_400ZR_330", "ATE_400ZR_345",  "ATE_400ZR_358"]
                    Table_Array = [self.table_ATE_262, self.table_ATE_280, self.table_ATE_305, self.table_ATE_306, self.table_ATE_316, self.table_ATE_330, self.table_ATE_345, self.table_ATE_358]
                    SLOT_Quantity = 60
                elif self.exs_button_ZEPHYR.isChecked():
                    self.process = "EXS"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(2) 
                    STATION_ID = ["ATE_400ZR_262", "ATE_400ZR_280", "ATE_400ZR_305", "ATE_400ZR_306", "ATE_400ZR_316", "ATE_400ZR_330", "ATE_400ZR_345",  "ATE_400ZR_358"]
                    Table_Array = [self.table_ATE_262, self.table_ATE_280, self.table_ATE_305, self.table_ATE_306, self.table_ATE_316, self.table_ATE_330, self.table_ATE_345, self.table_ATE_358]
                    SLOT_Quantity = 60
                elif self.rebt_button_OEM.isChecked():
                    self.process = "REBT"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(3) 
                    STATION_ID = ["ATE_400ZR_233", "ATE_400ZR_275", "ATE_400ZR_310", "ATE_400ZR_328"]
                    Table_Array = [self.table_ATE_233, self.table_ATE_275, self.table_ATE_310, self.table_ATE_328]
                    SLOT_Quantity = 10
                elif self.ebt_button_OEM.isChecked():
                    self.process = "EBT"
                    self.TAB_PROCESS_ZEPHYR.setCurrentIndex(3) 
                    STATION_ID = ["ATE_400ZR_233", "ATE_400ZR_275", "ATE_400ZR_310", "ATE_400ZR_328"]
                    Table_Array = [self.table_ATE_233, self.table_ATE_275, self.table_ATE_310, self.table_ATE_328]
                    SLOT_Quantity = 10
            elif self.TAB_Name == "ODB":
                Process_for_Yield = ['CAL']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "ODB")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.cal_button_ODB.isChecked():
                    self.process = "CAL"
                    self.TAB_PROCESS_ODB.setCurrentIndex(0) 
                    STATION_ID = ["ATE_ODB_239", "ATE_ODB_261", "ATE_ODB_349"]
                    Table_Array = [self.table_ATE_239, self.table_ATE_261, self.table_ATE_349]
                    SLOT_Quantity = 4
            elif self.TAB_Name == "NITLA":
                Process_for_Yield = ['MCN', 'CAL', 'FVT']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "NITLA")
                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.mcn_button_NITLA.isChecked():
                    self.process = "MCN"
                    self.TAB_PROCESS_NITLA.setCurrentIndex(0) 
                    STATION_ID = ["ATE_NITLA_261", "ATE_NITLA_303"]
                    Table_Array = [self.table_ATE_261_2, self.table_ATE_303]
                    SLOT_Quantity = 4
                elif self.cal_button_NITLA.isChecked():
                    self.process = "CAL"
                    self.TAB_PROCESS_NITLA.setCurrentIndex(0) 
                    STATION_ID = ["ATE_NITLA_261", "ATE_NITLA_303"]
                    Table_Array = [self.table_ATE_261_2, self.table_ATE_303]
                    SLOT_Quantity = 4
                elif self.fvt_button_NITLA.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_NITLA.setCurrentIndex(0) 
                    STATION_ID = ["ATE_NITLA_261", "ATE_NITLA_303"]
                    Table_Array = [self.table_ATE_261_2, self.table_ATE_303]
                    SLOT_Quantity = 4
            elif self.TAB_Name == "AX1200":
                Process_for_Yield = ['PCAL', 'CAL', 'FVT', 'ESS', 'EXS']
                Array_DAta_for_Cal_Yield = []
                for i in Process_for_Yield:
                    Query_LastResult_Test = QueryLastResultTest()
                    val = Query_LastResult_Test.Input_Data(self.day, i, self.fresh, self.TAB_Name, "AX1200")

                    Array_DAta_for_Cal_Yield.append(val)
                Cal_Yield = CalYield()
                Array_Yield = []
                for i, val in enumerate(Process_for_Yield):
                    Yield_OIT = Cal_Yield.input(Array_DAta_for_Cal_Yield[i])
                    Yield_OIT = (val,) + Yield_OIT
                    Array_Yield.append(Yield_OIT)
                Insert_Yield_to_Table = InsertYieldtoTable()
                Insert_Yield_to_Table.Yield_Detail(Process_for_Yield, Array_Yield, self.table_yield)

                Cumulative_Yield_Value = []
                for i in Array_Yield:
                    string_splited = i[4].split(" ")
                    Cumulative_Yield_Value.append(float(string_splited[0])/100)
                CY_New = 1.0
                for val in Cumulative_Yield_Value:
                    if val != 0.0:
                        CY_New *= val
                CY_New = "{:.2f}".format(CY_New*100)
                self.Cumulative_Yield.setText("Cumulative Yield : " + str(CY_New))

                if self.pcal_button_AX1200.isChecked():
                    self.process = "PCAL"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(0) 
                    STATION_ID = ["ATE_AX1200_331","ATE_AX1200_362"]
                    Table_Array = [self.table_ATE_331, self.table_ATE_362]
                    SLOT_Quantity = 12
                elif self.cal_button_AX1200.isChecked():
                    self.process = "CAL"
                    self.TAB_PROCESS_NITLA.setCurrentIndex(0) 
                    STATION_ID = ["ATE_AX1200_331","ATE_AX1200_362"]
                    Table_Array = [self.table_ATE_331, self.table_ATE_362]
                    SLOT_Quantity = 12
                elif self.fvt_button_AX1200.isChecked():
                    self.process = "FVT"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AX1200_356"]
                    Table_Array = [self.table_ATE_356]
                    SLOT_Quantity = 12
                elif self.fept_button_AX1200.isChecked():
                    self.process = "FEPT"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AX1200_356"]
                    Table_Array = [self.table_ATE_356]
                    SLOT_Quantity = 12
                elif self.fst_button_AX1200.isChecked():
                    self.process = "FST"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AX1200_356"]
                    Table_Array = [self.table_ATE_356]
                    SLOT_Quantity = 12
                elif self.ess_button_AX1200.isChecked():
                    self.process = "ESS"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(1) 
                    STATION_ID = ["ATE_AX1200_356"]
                    Table_Array = [self.table_ATE_356]
                    SLOT_Quantity = 12
                elif self.exp_button_AX1200.isChecked():
                    self.process = "EXP"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AX1200_195"]
                    Table_Array = [self.table_ATE_195_2]
                    SLOT_Quantity = 15
                elif self.exs_button_AX1200.isChecked():
                    self.process = "EXS"
                    self.TAB_PROCESS_AX1200.setCurrentIndex(2) 
                    STATION_ID = ["ATE_AX1200_195"]
                    Table_Array = [self.table_ATE_195_2]
                    SLOT_Quantity = 15

            rows_header = []   
            for i in range(SLOT_Quantity):
                str_val = "SLOT" + str(i)
                rows_header.append(str_val)
        
            self.process = "('" + self.process + "','KGB','SPC')"
            index = 0
            Table_Array[index].clearContents()     
    
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(len(STATION_ID) - 1)
            Query_Result_Test = QueryResultTest()
            for x in Query_Result_Test.Receive_Data(STATION_ID, self.day, self.process, self.fresh, self.TAB_Name):
                print(index)
                self.progress_bar.setValue(index)
                #*********************** Group data following date (Get Failure Mode) ***************************#
                Grouped_Data_Status = {}    
                for y in x:
                    if y[2] not in Grouped_Data_Status: # Define column[2] (START_DTE_TIME) to sperate data
                        Grouped_Data_Status[y[2]] = []
                    Grouped_Data_Status[y[2]].append(y[3:4] + y[6:7])
                for key, value in Grouped_Data_Status.items(): # Convert array inside dict to tuple
                    if isinstance(value, list):
                        Grouped_Data_Status[key] = tuple(value)

                # Sort data depend on slot running
                Dict_Status = {}
                for key, value in Grouped_Data_Status.items(): # Pack data, key = {keys}, value = {values}
                    if isinstance(value, tuple): # Check val is tuple or not
                        array = []
                        for i in range(SLOT_Quantity):
                            array.append('')
                        Dict_Status[key] = array
                        for sub_value in value:
                            if isinstance(sub_value, tuple):
                                Dict_Status[key][sub_value[1]] = sub_value[0] # sub_value[1] is index to place in tuple, sub_value[0] is data
                            else:
                                if type(sub_value) == int:
                                    Dict_Status[key][sub_value] = value[0]

                #*********************** Group data following date (Get Mode) ***************************#
                Grouped_Data_Mode = {}    
                for y in x:
                    if y[2] not in Grouped_Data_Mode: # Define column[2] (START_DTE_TIME) to sperate data
                        Grouped_Data_Mode[y[2]] = []
                    Grouped_Data_Mode[y[2]].append(y[5:6] + y[6:7])
                for key, value in Grouped_Data_Mode.items(): # Convert array inside dict to tuple
                    if isinstance(value, list):
                        Grouped_Data_Mode[key] = tuple(value)  

                # Sort data depend on slot running
                Dict_Mode = {}
                for key, value in Grouped_Data_Mode.items(): # Pack data, key = {keys}, value = {values}
                    if isinstance(value, tuple): # Check val is tuple or not
                        array = []
                        for i in range(SLOT_Quantity):
                            array.append('')
                        Dict_Mode[key] = array
                        for sub_value in value:
                            if isinstance(sub_value, tuple):
                                Dict_Mode[key][sub_value[1]] = sub_value[0] # sub_value[1] is index to place in tuple, sub_value[0] is data
                            else:
                                if type(sub_value) == int:
                                    Dict_Mode[key][sub_value] = value[0]     

                #*********************** Group data following date (SN) ***************************#
                Grouped_Data_SN = {}    
                for y in x:
                    if y[2] not in Grouped_Data_SN: # Define column[2] (START_DTE_TIME) to sperate data
                        Grouped_Data_SN[y[2]] = []
                    Grouped_Data_SN[y[2]].append(y[1:2] + y[6:7])
                for key, value in Grouped_Data_SN.items(): # Convert array inside dict to tuple
                    if isinstance(value, list):
                        Grouped_Data_SN[key] = tuple(value)  

                # Sort data depend on slot running
                Dict_SN = {}
                for key, value in Grouped_Data_SN.items(): # Pack data, key = {keys}, value = {values}
                    if isinstance(value, tuple): # Check val is tuple or not
                        array = []
                        for i in range(SLOT_Quantity):
                            array.append('')
                        Dict_SN[key] = array
                        for sub_value in value:
                            if isinstance(sub_value, tuple):
                                Dict_SN[key][sub_value[1]] = sub_value[0] # sub_value[1] is index to place in tuple, sub_value[0] is data
                            else:
                                if type(sub_value) == int:
                                    Dict_SN[key][sub_value] = value[0]   
                #******************************************************************************************************#      
                # Add \n between failure mode ans SN
                new_dict = {}
                for i in range(len(Dict_Status)):
                    new_dict[str(list(Dict_Status.keys())[i])] = [Dict_Status[str(list(Dict_Status.keys())[i])][j] + '\n' + Dict_SN[str(list(Dict_SN.keys())[i])][j] + '\n' + Dict_Mode[str(list(Dict_SN.keys())[i])][j] for j in range(len(Dict_Status[str(list(Dict_Status.keys())[i])]))]
                
                # Set column and row header        
                cols_header = list(Dict_Status.keys())
                for key in Grouped_Data_Status.keys():
                    cols_header.append(key)      

                Table_Array[index].setColumnCount(len(Dict_Status))
                Table_Array[index].setRowCount(len(rows_header))
                Table_Array[index].setHorizontalHeaderLabels(cols_header)
                Table_Array[index].setVerticalHeaderLabels(rows_header)         
                
                Dict_Status = new_dict
                print(Dict_Status)
                # Set color following failure
                for i, row_header in enumerate(rows_header):
                    for j, cols_head in enumerate(Dict_Status.keys()):                  
                        val_status = Dict_Status[cols_head][i]
                        val_mode = Dict_Mode[cols_head][i]
                        val_status_splted = val_status.split("\n")
                        if val_status_splted[0] == '':
                            Table_Array[index].setItem(i, j, QtWidgets.QTableWidgetItem('')) # Insert data to table
                        else:
                            Table_Array[index].setItem(i, j, QtWidgets.QTableWidgetItem(val_status)) # Insert data to table
                        Table_Array[index].item(i, j).setToolTip(val_status) # Add tooltip
                        bold_font = QtGui.QFont()
                        bold_font.setBold(True)                   
                        if val_status_splted[0] == "PASS":
                            if val_mode == "KGB":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(46, 255, 0))       
                            elif val_mode == "SPC":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(46, 255, 0))                              
                            elif val_mode == "RMA":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 58, 255))
                            elif val_mode == "EXPERIMENT":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(164, 0, 255))
                            else:
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 0, 0))
                            Table_Array[index].item(i, j).setBackground(QtGui.QColor(13, 158, 25))

                        elif val_status_splted[0] == "":
                            Table_Array[index].item(i, j).setBackground(QtGui.QColor(255, 255, 255))  
                        else:
                            if val_mode == "KGB":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(46, 255, 0))  
                            elif val_mode == "SPC":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(46, 255, 0))                 
                            elif val_mode == "RMA":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 58, 255))
                            elif val_mode == "EXPERIMENT":
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(164, 0, 255))
                            else:
                                Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 0, 0))
                            Table_Array[index].item(i, j).setBackground(QtGui.QColor(199, 2, 2))   

                        Table_Array[index].item(i, j).setFont(bold_font) 

                for i in range(Table_Array[index].columnCount()): # Resize column
                    Table_Array[index].setColumnWidth(i, 70)
                for i in range(Table_Array[index].rowCount()): # Resize row
                    Table_Array[index].setRowHeight(i, 10)
                
                font = QFont()
                font.setPointSize(7)
                Table_Array[index].setFont(font)
                Table_Array[index].horizontalHeader().setFont(font)
                Table_Array[index].verticalHeader().setFont(font)

                Table_Array[index].setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn) # Enable horizontal scroll bar
                if self.TAB_Name == "ZEPHYR" and self.process == "EXS":
                    if self.process == "EXP" or "EXS":
                        Table_Array[index].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn) # Enable horizontal scroll bar
                    else:
                        Table_Array[index].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Disable horizontal scroll bar                     

                Table_Array[index].horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #00FFFD}")
                Table_Array[index].verticalHeader().setStyleSheet("QHeaderView::section{background-color: #FFC200}")        
                Table_Array[index].setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")

                Table_Array[index].setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
                Table_Array[index].setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

                index += 1 
                time.sleep(0.1) 

            self.progress_bar.setVisible(False)
            # with open('temp/trigger.txt', 'w') as f:
            #     f.write('0')
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def showMenu(self, pos, table_in):    
        try:
            self.menu_right_click = QMenu()
            self.row_right_click = table_in.currentRow()
            self.column_right_click = table_in.currentColumn()
            self.menu_right_click.addAction("ATS")
            self.menu_right_click.addAction("FITs")
            self.menu_right_click.addAction("LINECARD/CHASSIS History")
            # self.menu_right_click.addAction("Failure Analyze")
            self.menu_right_click.addSeparator()
            self.action = self.menu_right_click.exec_(table_in.mapToGlobal(pos))

            if self.action and self.action.text() == "ATS":
                item_ATS = table_in.item(self.row_right_click, self.column_right_click)
                if len(item_ATS.text()) > 0:
                    self.Data = item_ATS.text()
                    self.newWindow_ATS(self.Data)
            elif self.action and self.action.text() == "FITs":
                item_FITs = table_in.item(self.row_right_click, self.column_right_click)
                if len(item_FITs.text()) > 0:
                    self.Data = item_FITs.text()
                    self.newWindow_FITs(self.Data)
            elif self.action and self.action.text() == "LINECARD/CHASSIS History":
                item_LC = table_in.item(self.row_right_click, self.column_right_click)
                if len(item_LC.text()) > 0:
                    self.Data = item_LC.text()
                    self.newWindow_LC(self.Data)
            else:
                None

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
        
    def run_GIF(self):
        dialog = QDialog(self)

        label = QLabel(dialog)
        label.setGeometry(20, 70, 100, 30)
        label.setAlignment(Qt.AlignCenter)

        movie = QMovie("C:\\Users\\waruntronk\\Downloads\\arrow.gif")
        movie.setScaledSize(label.size())
        label.setMovie(movie)

        dialog.setFixedSize(300,200)

        movie.start()
        dialog.show()

    def newWindow_ATS(self, Data_in):
        try:
            self.data_to_ATS = Data_in

            dialog_ATS = QDialog(self)

            self.table_ATS = QTableWidget(dialog_ATS)
            self.table_ATS.setGeometry(10,50,1280,440)

            label_day = QLabel('Select day', dialog_ATS)
            label_day.move(10,16)
            self.day_box = QComboBox(dialog_ATS)
            self.day_box.addItem('1 day')
            self.day_box.addItem('5 days')
            self.day_box.addItem('1 week')
            self.day_box.addItem('2 weeks')
            self.day_box.addItem('1 month')
            self.day_box.addItem('3 months')
            self.day_box.addItem('All')
            self.day_box.setGeometry(68,10,75,30)
            self.day_box.setCurrentIndex(2)
            self.day_box.currentIndexChanged.connect(self.day_window_ATS_Change)

            dialog_ATS.setWindowTitle("UUT ATS History")
            dialog_ATS.setGeometry(300,150,1300,500)
            dialog_ATS.setFixedSize(1300,500)
            dialog_ATS.show()

            self.data_to_table_ATS()

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def data_to_table_ATS(self):
        try:
            if self.day_box.currentText() == '1 day':
                day_selected = '1'
            elif self.day_box.currentText() == '5 days':
                day_selected = '5'
            elif self.day_box.currentText() == '1 week':
                day_selected = '7'
            elif self.day_box.currentText() == '2 weeks':
                day_selected = '14'
            elif self.day_box.currentText() == '1 month':
                day_selected = '30'
            elif self.day_box.currentText() == '3 months':
                day_selected = '90'
            elif self.day_box.currentText() == 'All':
                day_selected = '999'

            UUT_SN_ATS = self.data_to_ATS.split("\n")
            Query_Result_Test_SN = QueryResultTestSN()        
            DATA_Query_by_SN = Query_Result_Test_SN.SN_In(UUT_SN_ATS[1], self.TAB_Name, True, day_selected)
        
            Query_Value_Test = QueryValueTest()
            SN_Value = Query_Value_Test.receive_SN(UUT_SN_ATS[1], DATA_Query_by_SN, self.TAB_Name)

            Array_Tupple = []
            for idx, i in enumerate(DATA_Query_by_SN):
                Tuple = SN_Value[idx]
                Inner_Tuple = (Tuple[0], Tuple[1], Tuple[2])
                Mapping_Data = i[:5] + Inner_Tuple + i[5:]        
                Array_Tupple.append(Mapping_Data)     
            
            headers_ATS = ['STATION_ID', 'SLOT', 'SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'DATA', 'LOW_LIMIT', 'HIGH_LIMIT', 'LINECARD', 'CHASSIS', 'MODE', 'PROCESS', 'TEST_COUNT', 'PRODUCT_CODE', 'PRODUCT_CODE_REV', 'HW_PART_NUMBER', 'HW_REV', 'TPS_NAME', 'TPS_PART_NUMBER', 'TPS_REV', 'SW_NAME', 'SW_PART_NUMBER', 'SW_REV', 'FW_NAME', 'FW_PART_NUMBER', 'FW_REV']     
            self.table_ATS.setColumnCount(len(headers_ATS))
            self.table_ATS.setRowCount(len(Array_Tupple))
            self.table_ATS.setHorizontalHeaderLabels(headers_ATS)

            for i, row in enumerate(Array_Tupple):
                for j, value in enumerate(row):
                    table_item = QtWidgets.QTableWidgetItem(str(value))
                    self.table_ATS.setItem(i, j, table_item)
                    if j == 4:
                        if value == "PASS":
                            table_item.setBackground(QtGui.QColor(0, 255, 0))
                        else:
                            table_item.setBackground(QtGui.QColor(255, 0, 0))

            self.table_ATS.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
            self.table_ATS.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
            self.table_ATS.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.table_ATS.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.table_ATS.verticalHeader().setVisible(False)

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def day_window_ATS_Change(self):
        self.data_to_table_ATS()

    def newWindow_LC(self, Data_in):
        try:
            UUT_SN_LC = Data_in.split("\n")
            Query_Result_Test_SN = QueryResultTestSN()        
            DATA_Query_by_SN = Query_Result_Test_SN.SN_In(UUT_SN_LC[1], self.TAB_Name, False, '')
            Query_Value_Test = QueryValueTest()
            SN_Value = Query_Value_Test.receive_SN(UUT_SN_LC[1], DATA_Query_by_SN, self.TAB_Name)

            j = 0
            Array_Tupple = []
            for i in DATA_Query_by_SN:
                Tuple = SN_Value[j]
                Inner_Tuple = (Tuple[0], Tuple[1], Tuple[2])
                Mapping_Data = i[:5] + Inner_Tuple + i[5:]        
                Array_Tupple.append(Mapping_Data)
                j += 1

            dialog_LC = QDialog(self)
            self.table_LC = QtWidgets.QTableWidget(dialog_LC)
            self.text_L_SN = QLineEdit(dialog_LC)    
            self.text_L_SN.setAlignment(Qt.AlignCenter)
            self.text_C_SN = QLineEdit(dialog_LC)    
            self.text_C_SN.setAlignment(Qt.AlignCenter)
            L_label = QLabel("SN_LINECARD", dialog_LC)
            C_label = QLabel("SN_CHASSIS", dialog_LC)

            L_label.move(10,10)       
            self.text_L_SN.move(85,7)
            self.text_L_SN.resize(100,20)
            C_label.move(17,36)
            self.text_C_SN.move(85,33)
            self.text_C_SN.resize(100,20)

            self.day_label_LC = QLabel("Select Day", dialog_LC)
            self.day_label_LC.move(200, 22)
            self.day_LC = QComboBox(dialog_LC)
            self.day_LC.addItem("1")
            self.day_LC.addItem("2")
            self.day_LC.addItem("3")
            self.day_LC.addItem("5")
            self.day_LC.addItem("7")
            self.day_LC.addItem("14")
            self.day_LC.addItem("30")
            self.day_LC.addItem("90")
            self.day_LC.move(260, 15)
            self.day_LC.setFixedSize(35, 30)
                
            headers_LC = ['STATION_ID', 'SLOT', 'SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'DATA', 'LOW_LIMIT', 'HIGH_LIMIT', 'LINECARD', 'CHASSIS', 'MODE', 'PROCESS', 'TEST_COUNT', 'PRODUCT_CODE', 'PRODUCT_CODE_REV', 'HW_PART_NUMBER', 'HW_REV', 'TPS_NAME', 'TPS_PART_NUMBER', 'TPS_REV', 'SW_NAME', 'SW_PART_NUMBER', 'SW_REV', 'FW_NAME', 'FW_PART_NUMBER', 'FW_REV']     
            self.table_LC.setColumnCount(len(headers_LC))
            self.table_LC.setRowCount(len(Array_Tupple))
            self.table_LC.setHorizontalHeaderLabels(headers_LC)

            for i, row in enumerate(Array_Tupple):
                for j, value in enumerate(row):
                    table_item = QtWidgets.QTableWidgetItem(str(value))
                    self.table_LC.setItem(i, j, table_item)
                    if j == 4:
                        if value == "PASS":
                            table_item.setBackground(QtGui.QColor(0, 255, 0))
                        else:
                            table_item.setBackground(QtGui.QColor(255, 0, 0))

            self.table_LC.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
            self.table_LC.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
            self.table_LC.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.table_LC.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.table_LC.verticalHeader().setVisible(False)
            self.Data_to_Table = Array_Tupple
            self.table_LC.cellClicked.connect(lambda pos: self.Show_Data_Table_ATS_Clicked(pos, self.table_LC, self.Data_to_Table))

            self.button = QPushButton("Query", dialog_LC)
            self.button.move(320, 13)
            self.button.setFixedSize(65, 35)
            self.button.clicked.connect(lambda: self.Query_SN_LINECARD_CHASSIS(self.TAB_Name, self.table_LC))

            self.table_LC.move(10,60)
            self.table_LC.setFixedSize(1285,485)
            dialog_LC.setWindowTitle("UUT ATS History")
            dialog_LC.setGeometry(300,150,1300,500)
            dialog_LC.setFixedSize(1300,550)
            dialog_LC.show()
        
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def Show_Data_Table_ATS_Clicked(self, pos, table_in, data_in):
        try:
            self.day_LC_Selected = self.day_LC.currentText()
            row_right_click = table_in.currentRow()
            column_right_click = table_in.currentColumn()
            self.SN_LINECARD_Out = ""
            self.SN_CHASSIS_Out = ""
            if column_right_click == 8:
                self.LINECARD_SN = data_in[row_right_click][column_right_click]
                self.text_L_SN.setText(self.LINECARD_SN)
                self.text_C_SN.setText("")
            elif column_right_click == 9:
                self.CHASSIS_SN = data_in[row_right_click][column_right_click]
                self.text_C_SN.setText(self.CHASSIS_SN)
                self.text_L_SN.setText("")
            else:
                self.text_L_SN.setText("")
                self.text_C_SN.setText("")
            self.SN_LINECARD_Out = self.text_L_SN.text()
            self.SN_CHASSIS_Out = self.text_C_SN.text()
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def Query_SN_LINECARD_CHASSIS(self, TAB_Name, table_in):   
        try:
            self.day_LC_Selected = self.day_LC.currentText()
            if self.SN_LINECARD_Out != "" and self.SN_CHASSIS_Out != "":
                None
            else :
                table_in.clearContents()   
                Query_LINECARD_CHASSIS = QueryLINECARDCHASSIS()
                History_LINE_CHAS = Query_LINECARD_CHASSIS.SN_In(self.SN_LINECARD_Out, self.SN_CHASSIS_Out, TAB_Name, self.day_LC_Selected)
                Query_Value_LINE_CHAS = QueryValueLINECHAS()
                Value_LINE_CHAS = Query_Value_LINE_CHAS.receive_SN(self.SN_LINECARD_Out, self.SN_CHASSIS_Out, History_LINE_CHAS, TAB_Name)

                j = 0
                LINE_CHASS_Tupple = []
                for i in History_LINE_CHAS:
                    Tuple = Value_LINE_CHAS[j]
                    Inner_Tuple = (Tuple[0], Tuple[1], Tuple[2])
                    Mapping_Data = i[:5] + Inner_Tuple + i[5:]        
                    LINE_CHASS_Tupple.append(Mapping_Data)
                    j += 1
                table_in.setRowCount(len(LINE_CHASS_Tupple))
                for i, row in enumerate(LINE_CHASS_Tupple):
                    for j, value in enumerate(row):
                        table_item = QtWidgets.QTableWidgetItem(str(value))
                        table_in.setItem(i, j, table_item)
                        if j == 4:
                            if value == "PASS":
                                table_item.setBackground(QtGui.QColor(0, 255, 0))
                            else:
                                table_item.setBackground(QtGui.QColor(255, 0, 0))
                self.Data_to_Table = LINE_CHASS_Tupple
                table_in.cellClicked.connect(lambda pos: self.Show_Data_Table_ATS_Clicked(pos, table_in, self.Data_to_Table))
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def newWindow_FITs(self, Data_in):
        try:
            UUT_SN_FITs = Data_in.split("\n")
            Query_FITs_History = QueryFITsHistory()
            FITs_Data = Query_FITs_History.SN_FITs_In(UUT_SN_FITs[1])

            dialog_FITs = QDialog(self)
            layout_history_FITs = QVBoxLayout()
            table_FITs = QtWidgets.QTableWidget()

            headers_FITs = ['SERIAL_NUMBER', 'OPERATION_No', 'OPERATION_NAME', 'MODEL_TYPE','RESULT', 'EN_No', 'DATE_TIME_CHECK_IN', 'DATE_TIME_CHECK_OUT', 'SHIFT', 'BUILDTYPE', 'RUNTYPE', 'WORKORDER', 'MODEL']    
            table_FITs.setColumnCount(len(headers_FITs))
            table_FITs.setRowCount(len(FITs_Data))
            table_FITs.setHorizontalHeaderLabels(headers_FITs)

            for i, row in enumerate(FITs_Data):
                for j, value in enumerate(row):
                    table_item = QtWidgets.QTableWidgetItem(str(value))
                    table_FITs.setItem(i, j, table_item)
                    # if j == 4:
                    #     print(value)
                    #     if value == "PASS":
                    #         table_item.setBackground(QtGui.QColor(0, 255, 0))
                    #     else:
                    #         table_item.setBackground(QtGui.QColor(255, 0, 0))
            table_FITs.resizeColumnsToContents()
            table_FITs.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
            table_FITs.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
            table_FITs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            table_FITs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            table_FITs.verticalHeader().setVisible(False)
            table_FITs.setEditTriggers(QTableWidget.NoEditTriggers)

            table_FITs.setContextMenuPolicy(Qt.CustomContextMenu)
            table_FITs.customContextMenuRequested.connect(lambda pos, table=table_FITs: self.showMenu_FITs(pos, table))

            layout_history_FITs.addWidget(table_FITs)
            dialog_FITs.setLayout(layout_history_FITs)
            dialog_FITs.setWindowTitle("UUT FITs History")
            dialog_FITs.setGeometry(300,150,1300,500)
            dialog_FITs.setFixedSize(1300,500)
            dialog_FITs.show() 

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
            
    def showMenu_FITs(self, pos, table_in):    
        try:
            self.menu_right_click = QMenu()
            self.row_right_click = table_in.currentRow()
            self.column_right_click = table_in.currentColumn()
            self.menu_right_click.addAction("Detail")
            self.menu_right_click.addSeparator()
            self.action = self.menu_right_click.exec_(table_in.mapToGlobal(pos))       

            if self.action and self.action.text() == "Detail":
                FITs_SN = table_in.item(self.row_right_click, 0)
                FITs_Opeation_ID = table_in.item(self.row_right_click, 1)
                FITs_DateTime = table_in.item(self.row_right_click, 6)

                Data_FITs_SN = FITs_SN.text()
                Data_FITs_Opeation_ID = FITs_Opeation_ID.text()
                Data_FITs_DateTime = FITs_DateTime.text()

                self.FITs_Detail(Data_FITs_SN, Data_FITs_Opeation_ID, Data_FITs_DateTime)

        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
        
    def FITs_Detail(self, SN, Opeation_ID, DateTime):
        try:
            Query_FITs_Operation = QueryFITsOperation()
            Detail_FITs_Out = Query_FITs_Operation.Detail_FITs_In(str(SN), str(Opeation_ID), str(DateTime))
            Description = []
            Value = []
            for i in Detail_FITs_Out:
                Description.append(i[4])
                Value.append(i[5])

            dialog_FITs_Detail = QDialog(self)
            layout_history_FITs_Detail = QVBoxLayout()
            table_FITs_Detail = QtWidgets.QTableWidget()

            table_FITs_Detail.setColumnCount(1)
            table_FITs_Detail.setRowCount(len(Description))
            table_FITs_Detail.setHorizontalHeaderLabels(['Detail'])
            table_FITs_Detail.setVerticalHeaderLabels(Description)

            for i, val in enumerate(Value):
                table_item = QtWidgets.QTableWidgetItem(str(val))
                table_FITs_Detail.setItem(i, 0, table_item)

            for i in range(table_FITs_Detail.columnCount()): # Resize column
                    table_FITs_Detail.setColumnWidth(i, 450)

            table_FITs_Detail.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #9CB2FF}")
            table_FITs_Detail.verticalHeader().setStyleSheet("QHeaderView::section{background-color: #FFCE00}")
            table_FITs_Detail.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
            table_FITs_Detail.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            table_FITs_Detail.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

            layout_history_FITs_Detail.addWidget(table_FITs_Detail)
            dialog_FITs_Detail.setLayout(layout_history_FITs_Detail)
            dialog_FITs_Detail.setWindowTitle("UUT FITs Operatio Detail")
            dialog_FITs_Detail.setGeometry(300,150,627,500)
            dialog_FITs_Detail.show()
            
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")
    
    def plot_SPC(self):
        dialog = QDialog(self)


        dialog.show()

    def loading_GIF(self):
        dialog = QDialog()
        layout = QVBoxLayout()

        gif_label = QLabel()
        layout.addWidget(gif_label)

        # Load the GIF file
        gif_path = "temp/loading.gif"
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)

        # Set the movie to play continuously
        # movie.setCacheMode(QMovie.CacheAll)
        # movie.setSpeed(100)
        movie.start()

        dialog.setLayout(layout)
        dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

        timer = QTimer()
        timer.timeout.connect(lambda: self.close_gui(dialog))
        timer.start(100)

        dialog.show()

    def close_gui(self, dia):
        with open('temp/trigger.txt', 'r') as f:
            file_read = f.read()
        if file_read == '0':
            dia.close() 

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()
