import pyodbc
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import time
import math
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

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(450, 5, 200, 10)       
        self.progress_bar.setValue(0)
 
        self.main_layout = QtWidgets.QVBoxLayout()
        self.Main_TAB = QTabWidget(self)
        
        self.process = ""
        self.day = ""
        
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
        self.TAB_PROCESS_AC1200.resize(1650, 940)

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

        # Create process tab (ODB) inside main tab
        self.TAB_PROCESS_ODB = QTabWidget(self.ODB_Page)
        self.TAB_CAL_ODB = QWidget()
        self.TAB_PROCESS_ODB.addTab(self.TAB_CAL_ODB, "CAL")
        for i in range(1):
            self.TAB_PROCESS_ODB.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_ODB.resize(1880, 940)  

        # Create process tab (NITLA) inside main tab
        self.TAB_PROCESS_NITLA = QTabWidget(self.NITLA_Page)
        self.TAB_CAL_NITLA = QWidget()
        self.TAB_PROCESS_NITLA.addTab(self.TAB_CAL_NITLA, "CAL")
        for i in range(1):
            self.TAB_PROCESS_NITLA.tabBar().setTabVisible(i, False)
        self.TAB_PROCESS_NITLA.resize(1880, 940)
        
        # Config Windowapp
        self.setWindowTitle("Result Test and Yield Monitor")

        # Ratio button slect fresh unit
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)

        self.all_unit_button = QRadioButton("All", self.Main_TAB)
        self.all_unit_button.setChecked(True)
        self.all_unit_button.move(187, 45)
        self.fresh_unit_button = QRadioButton("Fresh Unit", self.Main_TAB)
        self.fresh_unit_button.move(237, 45)

        self.button_group.addButton(self.all_unit_button)
        self.button_group.addButton(self.fresh_unit_button)

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

        # Create ration button (ODB)
        self.process_ratio_ODB = QLabel("Select Process", self.TAB_PROCESS_ODB)
        self.process_ratio_ODB.move(10, 48)  
        self.cal_button_ODB = QRadioButton("CAL", self.TAB_PROCESS_ODB)
        self.cal_button_ODB.setChecked(True)
        self.cal_button_ODB.move(85, 47)

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
        self.day_dropbbox.setFixedSize(35, 30)

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
    
        # Create Table Yield *********************************************************************************  
        Header_Yield = ["Process","Input","PASS","FAIL","YIELD"] 
        self.table_yield = QtWidgets.QTableWidget(self)
        self.table_yield.move(1384, 5)
        self.table_yield.setFixedSize(266, 140)
        self.table_yield.setColumnCount(len(Header_Yield))
        self.table_yield.setHorizontalHeaderLabels(Header_Yield)
        self.table_yield.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_yield.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for i in range(self.table_yield.columnCount()): # Resize column
                self.table_yield.setColumnWidth(i, 53)
    
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
        self.Main_TAB.currentChanged.connect(self.updateLabel)
        self.TAB_Name = "AC1200"    
        
        Table_Array_1 = [self.table_ATE_132, self.table_ATE_182, self.table_ATE_256, self.table_ATE_266, self.table_ATE_309]
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

    def updateLabel(self, index):
        self.TAB_Name = self.Main_TAB.tabText(index) 

    def Query_SQL(self):
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
            if self.cal_button_ODB.isChecked():
                self.process = "CAL"
                self.TAB_PROCESS_ODB.setCurrentIndex(0) 
                STATION_ID = ["ATE_ODB_239", "ATE_ODB_261", "ATE_ODB_349"]
                Table_Array = [self.table_ATE_239, self.table_ATE_261, self.table_ATE_349]
                SLOT_Quantity = 4
        elif self.TAB_Name == "NITLA":
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

        rows_header = []   
        for i in range(SLOT_Quantity):
            str_val = "SLOT" + str(i)
            rows_header.append(str_val)
    
        self.process = "('" + self.process + "','KGB','SPC')"
        index = 0
        Table_Array[index].clearContents()     

        Query_Result_Test = QueryResultTest()
        for x in Query_Result_Test.Receive_Data(STATION_ID, self.day, self.process, self.fresh, self.TAB_Name):
            T = self.progress_bar.value()
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
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 171, 7))       
                        elif val_mode == "SPC":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 171, 7))                              
                        elif val_mode == "RMA":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 58, 255))
                        elif val_mode == "EXPERIMENT":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(164, 0, 255))
                        else:
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 0, 0))
                        Table_Array[index].item(i, j).setBackground(QtGui.QColor(0, 255, 0))

                    elif val_status_splted[0] == "":
                        Table_Array[index].item(i, j).setBackground(QtGui.QColor(255, 255, 255))  
                    else:
                        if val_mode == "KGB":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 171, 7))  
                        elif val_mode == "SPC":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 171, 7))                 
                        elif val_mode == "RMA":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 58, 255))
                        elif val_mode == "EXPERIMENT":
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(164, 0, 255))
                        else:
                            Table_Array[index].item(i, j).setForeground(QtGui.QColor(0, 0, 0))
                        Table_Array[index].item(i, j).setBackground(QtGui.QColor(255, 0, 0))   

                    Table_Array[index].item(i, j).setFont(bold_font) 

            for i in range(Table_Array[index].columnCount()): # Resize column
                Table_Array[index].setColumnWidth(i, 95)
            for i in range(Table_Array[index].rowCount()): # Resize row
                Table_Array[index].setRowHeight(i, 10)

            Table_Array[index].setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn) # Enable horizontal scroll bar
            if self.TAB_Name == "ZEPHYR" and self.process == "EXS":
                if self.process == "EXP" or "EXS":
                    Table_Array[index].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn) # Enable horizontal scroll bar
                else:
                    Table_Array[index].setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # Disable horizontal scroll bar                     

            Table_Array[index].horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #00FFFD}")
            Table_Array[index].verticalHeader().setStyleSheet("QHeaderView::section{background-color: #FFC200}")        
            Table_Array[index].setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")

            index += 1 
            val_for_loading = (index * 100) / len(STATION_ID)
            self.progress_bar.setValue(int(val_for_loading))
            time.sleep(0.1)    

    def showMenu(self, pos, table_in):    
        self.menu_right_click = QMenu()
        self.row_right_click = table_in.currentRow()
        self.column_right_click = table_in.currentColumn()
        self.menu_right_click.addAction("ATS")
        self.menu_right_click.addAction("FITs")
        self.menu_right_click.addAction("LINECARD/CHASSIS History")
        self.menu_right_click.addSeparator()
        self.action = self.menu_right_click.exec_(table_in.mapToGlobal(pos))

        if self.action and self.action.text() == "ATS":
            item_ATS = table_in.item(self.row_right_click, self.column_right_click)
            if item_ATS is not None:
                self.Data = item_ATS.text()
                self.newWindow_ATS(self.Data)
        elif self.action and self.action.text() == "FITs":
            item_FITs = table_in.item(self.row_right_click, self.column_right_click)
            if item_FITs is not None:
                self.Data = item_FITs.text()
                self.newWindow_FITs(self.Data)
        elif self.action and self.action.text() == "LINECARD/CHASSIS History":
            item_LC = table_in.item(self.row_right_click, self.column_right_click)
            if item_LC is not None:
                self.Data = item_LC.text()
                self.newWindow_LC(self.Data)
        else:
            None

    def newWindow_ATS(self, Data_in):
        UUT_SN_ATS = Data_in.split("\n")
        Query_Result_Test_SN = QueryResultTestSN()        
        DATA_Query_by_SN = Query_Result_Test_SN.SN_In(UUT_SN_ATS[1], self.TAB_Name)
        Query_Value_Test = QueryValueTest()
        SN_Value = Query_Value_Test.receive_SN(UUT_SN_ATS[1], DATA_Query_by_SN, self.TAB_Name)

        j = 0
        Array_Tupple = []
        for i in DATA_Query_by_SN:
            Tuple = SN_Value[j]
            Inner_Tuple = (Tuple[0], Tuple[1], Tuple[2])
            Mapping_Data = i[:5] + Inner_Tuple + i[5:]        
            Array_Tupple.append(Mapping_Data)
            j += 1

        dialog_ATS = QDialog(self)
        layout_history_ATS = QVBoxLayout()
        table_ATS = QtWidgets.QTableWidget()

        headers_ATS = ['STATION_ID', 'SLOT', 'SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'DATA', 'LOW_LIMIT', 'HIGH_LIMIT', 'LINECARD', 'CHASSIS', 'MODE', 'PROCESS', 'TEST_COUNT', 'PRODUCT_CODE', 'PRODUCT_CODE_REV', 'HW_PART_NUMBER', 'HW_REV', 'TPS_NAME', 'TPS_PART_NUMBER', 'TPS_REV', 'SW_NAME', 'SW_PART_NUMBER', 'SW_REV', 'FW_NAME', 'FW_PART_NUMBER', 'FW_REV']     
        table_ATS.setColumnCount(len(headers_ATS))
        table_ATS.setRowCount(len(Array_Tupple))
        table_ATS.setHorizontalHeaderLabels(headers_ATS)

        for i, row in enumerate(Array_Tupple):
            for j, value in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(value))
                table_ATS.setItem(i, j, table_item)
                if j == 4:
                    if value == "PASS":
                        table_item.setBackground(QtGui.QColor(0, 255, 0))
                    else:
                        table_item.setBackground(QtGui.QColor(255, 0, 0))

        table_ATS.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
        table_ATS.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        table_ATS.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_ATS.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_ATS.verticalHeader().setVisible(False)

        layout_history_ATS.addWidget(table_ATS)
        dialog_ATS.setLayout(layout_history_ATS)
        dialog_ATS.setWindowTitle("UUT ATS History")
        dialog_ATS.setGeometry(300,150,1300,500)
        dialog_ATS.setFixedSize(1300,500)
        dialog_ATS.show()      
        
    def newWindow_LC(self, Data_in):
        UUT_SN_LC = Data_in.split("\n")
        Query_Result_Test_SN = QueryResultTestSN()        
        DATA_Query_by_SN = Query_Result_Test_SN.SN_In(UUT_SN_LC[1], self.TAB_Name)
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
        table_LC = QtWidgets.QTableWidget(dialog_LC)
        text_L_SN = QLineEdit(dialog_LC)    
        text_L_SN.setAlignment(Qt.AlignCenter)
        text_C_SN = QLineEdit(dialog_LC)    
        text_C_SN.setAlignment(Qt.AlignCenter)
        L_label = QLabel("SN_LINECARD", dialog_LC)
        C_label = QLabel("SN_CHASSIS", dialog_LC)

        L_label.move(10,10)       
        text_L_SN.move(85,7)
        text_L_SN.resize(100,20)
        C_label.move(17,36)
        text_C_SN.move(85,33)
        text_C_SN.resize(100,20)
        
        headers_LC = ['STATION_ID', 'SLOT', 'SERIAL_NUMBER', 'START_DATE_TIME', 'RESULT', 'DATA', 'LOW_LIMIT', 'HIGH_LIMIT', 'LINECARD', 'CHASSIS', 'MODE', 'PROCESS', 'TEST_COUNT', 'PRODUCT_CODE', 'PRODUCT_CODE_REV', 'HW_PART_NUMBER', 'HW_REV', 'TPS_NAME', 'TPS_PART_NUMBER', 'TPS_REV', 'SW_NAME', 'SW_PART_NUMBER', 'SW_REV', 'FW_NAME', 'FW_PART_NUMBER', 'FW_REV']     
        table_LC.setColumnCount(len(headers_LC))
        table_LC.setRowCount(len(Array_Tupple))
        table_LC.setHorizontalHeaderLabels(headers_LC)

        for i, row in enumerate(Array_Tupple):
            for j, value in enumerate(row):
                table_item = QtWidgets.QTableWidgetItem(str(value))
                table_LC.setItem(i, j, table_item)
                if j == 4:
                    if value == "PASS":
                        table_item.setBackground(QtGui.QColor(0, 255, 0))
                    else:
                        table_item.setBackground(QtGui.QColor(255, 0, 0))

        table_LC.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
        table_LC.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        table_LC.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_LC.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_LC.verticalHeader().setVisible(False)

        table_LC.move(10,60)
        table_LC.setFixedSize(1285,485)
        dialog_LC.setWindowTitle("UUT ATS History")
        dialog_LC.setGeometry(300,150,1300,500)
        dialog_LC.setFixedSize(1300,550)
        dialog_LC.show()

    def Show_Data_Table_ATS_Clicked(self, pos, table_in, data_in):
        row_right_click = table_in.currentRow()
        column_right_click = table_in.currentColumn()
        if column_right_click == 8:
            self.LINECARD_SN = data_in[row_right_click][column_right_click]
            self.LINECARD_SN_Box.setText(self.LINECARD_SN)
            self.CHASSIS_SN_Box.setText("")
        elif column_right_click == 9:
            self.CHASSIS_SN = data_in[row_right_click][column_right_click]
            self.CHASSIS_SN_Box.setText(self.CHASSIS_SN)
            self.LINECARD_SN_Box.setText("")
        else:
            self.LINECARD_SN_Box.setText("")
            self.CHASSIS_SN_Box.setText("")

    def Query_SN_LINECARD_CHASSIS(self, SN_LINECARD, SN_CHASSIS, TAB_Name):      
        Query_LINECARD_CHASSIS = QueryLINECARDCHASSIS()
        History_LINE_CHAS = Query_LINECARD_CHASSIS.SN_In(SN_LINECARD, SN_CHASSIS, TAB_Name, '1')
        Query_Value_LINE_CHAS = QueryValueLINECHAS()
        Value_LINE_CHAS = Query_Value_LINE_CHAS.receive_SN(SN_LINECARD, SN_CHASSIS, History_LINE_CHAS, TAB_Name)

        j = 0
        LINE_CHASS_Tupple = []
        for i in History_LINE_CHAS:
            Tuple = Value_LINE_CHAS[j]
            Inner_Tuple = (Tuple[0], Tuple[1], Tuple[2])
            Mapping_Data = i[:5] + Inner_Tuple + i[5:]        
            LINE_CHASS_Tupple.append(Mapping_Data)
            j += 1
        print(LINE_CHASS_Tupple)

    def newWindow_FITs(self, Data_in):
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
                if j == 4:
                    if value == "PASS":
                        table_item.setBackground(QtGui.QColor(0, 255, 0))
                    else:
                        table_item.setBackground(QtGui.QColor(255, 0, 0))

        table_FITs.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFFB00}")
        table_FITs.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        table_FITs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_FITs.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        table_FITs.verticalHeader().setVisible(False)

        table_FITs.setContextMenuPolicy(Qt.CustomContextMenu)
        table_FITs.customContextMenuRequested.connect(lambda pos, table=table_FITs: self.showMenu_FITs(pos, table))

        layout_history_FITs.addWidget(table_FITs)
        dialog_FITs.setLayout(layout_history_FITs)
        dialog_FITs.setWindowTitle("UUT FITs History")
        dialog_FITs.setGeometry(300,150,1300,500)
        dialog_FITs.setFixedSize(1300,500)
        dialog_FITs.show() 
    
    def showMenu_FITs(self, pos, table_in):    
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
        
    def FITs_Detail(self, SN, Opeation_ID, DateTime):
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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()