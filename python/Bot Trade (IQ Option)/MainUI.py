import typing
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QTableWidget, QCheckBox, QLabel, QFrame, QPushButton, QMessageBox, QShortcut, QComboBox
from PyQt5.QtGui import QFont, QKeySequence, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets, QtCore
from iqoptionapi.stable_api import IQ_Option
from talib.abstract import *
import numpy as np
import time
import threading
import os
import csv
from datetime import datetime

class WindowTrading(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('temp\\robot.ico'))
        frame_logo = QFrame(self)
        frame_logo.setStyleSheet("background-color: #FFE6C1")
        frame_logo.setGeometry(0,0,500,50)
        
        font_logo = QFont()
        font_logo.setBold(True)
        font_logo.setPointSize(11)
        pixmap = QPixmap('temp\\logo_iq.png')
        pixmap = pixmap.scaled(145,150)
        logo = QLabel(self)
        logo.setPixmap(pixmap)
        logo.setGeometry(2,2,300,50)
        text_logo = QLabel("AI BotTrade for IQ Option V1.0", self)
        text_logo.setStyleSheet("color: #0109FF")
        text_logo.setFont(font_logo)
        text_logo.setGeometry(140,3,260,50)

        frame_user = QFrame(self)
        frame_user.setStyleSheet("background-color: white; border: 1px solid black")
        frame_user.setGeometry(5,55,280,130)

        frame_information = QFrame(self)
        frame_information.setStyleSheet("background-color: #B0FFFF; border: 1px solid black")
        frame_information.setGeometry(5,190,390,145)
        
        username_label = QLabel("Username", self)
        username_label.move(15,54)
        self.username = QLineEdit(self)
        self.username.setGeometry(80,60,200,20)

        password_label = QLabel("Password", self)
        password_label.move(17,79)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setGeometry(80,85,200,20)

        font = QFont()
        font.setPointSize(8)
        show_password_label = QLabel("Show password", self)
        show_password_label.setFont(font)
        show_password_label.setGeometry(100,114,100,20)
        show_password = QCheckBox(self)
        show_password.stateChanged.connect(self.show_password_mode)
        show_password.move(80,110)

        market_label = QLabel("Select Market", self)
        market_label.move(300,50)
        self.market_name = QComboBox(self)
        self.market_name.addItem('N/A')
        self.market_name.currentIndexChanged.connect(self.get_info_market)
        self.market_name.setDisabled(True)
        self.market_name.setGeometry(300,75,90,20)

        font_BT = QFont()
        font_BT.setBold(True)
        self.initial_BT = QPushButton("Connect", self)
        self.initial_BT.setFont(font_BT)
        self.initial_BT.clicked.connect(self.initialize)
        self.initial_BT.setGeometry(80,150,100,30)

        ENTER_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        ENTER_shortcut.activated.connect(self.initialize)

        self.active_run_candle_BT = QPushButton("Start Running", self)
        self.active_run_candle_BT.setStyleSheet("background-color: #53F932")
        self.active_run_candle_BT.setFont(font_BT)
        self.active_run_candle_BT.setDisabled(True)
        self.active_run_candle_BT.clicked.connect(self.stop_background_task)
        self.active_run_candle_BT.setGeometry(80,300,100,25)

        close_prize_lable = QLabel('Close Prize', self)
        close_prize_lable.setGeometry(20,199,100,20)
        self.close_prize = QLineEdit('', self)
        self.close_prize.setReadOnly(True)
        self.close_prize.setAlignment(Qt.AlignCenter)
        self.close_prize.setGeometry(80,200,70,20)

        open_prize_lable = QLabel('Open Prize', self)
        open_prize_lable.setGeometry(20,224,100,20)
        self.open_prize = QLineEdit('', self)
        self.open_prize.setReadOnly(True)
        self.open_prize.setAlignment(Qt.AlignCenter)
        self.open_prize.setGeometry(80,225,70,20)

        max_prize_lable = QLabel('Max Prize', self)
        max_prize_lable.setGeometry(26,249,100,20)
        self.max_prize = QLineEdit('', self)
        self.max_prize.setReadOnly(True)
        self.max_prize.setAlignment(Qt.AlignCenter)
        self.max_prize.setGeometry(80,250,70,20)

        min_prize_lable = QLabel('Min Prize', self)
        min_prize_lable.setGeometry(29,274,100,20)
        self.min_prize = QLineEdit('', self)
        self.min_prize.setReadOnly(True)
        self.min_prize.setAlignment(Qt.AlignCenter)
        self.min_prize.setGeometry(80,275,70,20)

        balance_label = QLabel("Balance", self)
        balance_label.move(220,194)
        self.balance = QLineEdit("N/A", self)
        self.balance.setReadOnly(True)
        self.balance.setGeometry(270,200,80,20)

        profit_label = QLabel("Profit", self)
        profit_label.setGeometry(230,225,100,20)
        self.profit = QLineEdit("N/A", self)
        self.profit.setReadOnly(True)
        self.profit.setGeometry(270,225,50,20)

        self.text_box = QLineEdit("",self)
        self.text_box.setAlignment(Qt.AlignCenter)
        self.text_box.setReadOnly(True)
        self.text_box.setGeometry(190,303,190,20)

        file_path = 'temp\\log.csv'
        csv_read = []   
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                csv_read.append(row)

        self.table = QTableWidget(self)
        self.table.setGeometry(5,340,390,155)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["DateTime","Prize","Revenue", "Profit"])
        self.table.setRowCount(len(csv_read))  

        for i, row in enumerate(csv_read):
            for j, val in enumerate(row):
                table_items = QtWidgets.QTableWidgetItem(str(val))
                self.table.setItem(i, j, table_items)
        
        self.table.setColumnWidth(1,90)
        self.table.setColumnWidth(2,90)
        self.table.setColumnWidth(3,90)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #F8CCFF}")
        self.table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.verticalHeader().setVisible(False)  

        self.setWindowTitle("AI BotTrade for IQ Option V1.0")
        self.setFixedSize(400,500)

        self.username.setText("waruntron.kra@gmail.com")
        self.password.setText("9199218Fwk")
        self.worker_thread = None
        self.connection_result = False
        self.backgroud_run = False
    
    def show_password_mode(self, state):
        if state == 2:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)
    
    def initialize(self):
        self.API = IQ_Option(self.username.text(), self.password.text())
        connection_result = self.API.connect()
        if connection_result[0] == True:    
            self.list_market_name()  
            self.connection_result = True   
            QMessageBox.information(self, "information", "Connection sucessfully!")    
            self.market_name.setDisabled(False)
            self.active_run_candle_BT.setDisabled(False)
        else:
            self.connection_result = False
            QMessageBox.information(self, "Error", f"{connection_result[0]}\n{connection_result[1]}")
            self.market_name.setDisabled(True)
            self.active_run_candle_BT.setDisabled(True)
        
    def list_market_name(self):
        get_balance = self.API.get_balance()
        self.balance.setText(f"{get_balance} $")
        group_market_opened = self.API.get_all_open_time()
        self.market_name.clear()
        for type_name, data in group_market_opened.items():
            if type_name == 'binary':
                for market, value in data.items():
                    if value['open'] == True:
                        self.market_name.addItem(market)
        self.get_info_market()
    
    def get_info_market(self):
        self.active_run_candle_BT.setDisabled(True)
        self.initial_BT.setDisabled(True)
        if self.market_name.currentText() != 'N/A' and self.market_name.currentText() != '':
           get_profit = self.API.get_all_profit()
           get_profit = get_profit[self.market_name.currentText()]
           self.profit.setText(f"{str(float(get_profit['binary']) * 100)} %")
        self.active_run_candle_BT.setDisabled(False)
        self.initial_BT.setDisabled(False)
    
    def start_background_task(self):
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.backgroud_run = True
            self.worker_thread = WorkerThread(self.background_task_finished, self.API, self.market_name.currentText(), self.close_prize, self.open_prize, self.max_prize, self.min_prize, self.text_box, self.table)
            self.worker_thread.start()

    def stop_background_task(self):       
        if self.connection_result == True:
            if self.active_run_candle_BT.text() == "Stop Running":
                self.market_name.setDisabled(False)
                self.initial_BT.setDisabled(False)
                self.active_run_candle_BT.setStyleSheet("background-color: #53F932")
                self.active_run_candle_BT.setText("Start Running")          
                if self.worker_thread is not None:
                    self.worker_thread.running = False
                    self.worker_thread.join()
                    self.worker_thread = None
                    self.close_prize.setText('')
                    self.open_prize.setText('')
                    self.max_prize.setText('')
                    self.min_prize.setText('')
                    self.text_box.setText('')
                    self.text_box.setStyleSheet('background-color : white')
                    
            elif self.active_run_candle_BT.text() == "Start Running":
                self.market_name.setDisabled(True)
                self.initial_BT.setDisabled(True)
                self.active_run_candle_BT.setStyleSheet("background-color: #FD4343")
                self.active_run_candle_BT.setText("Stop Running")
                self.start_background_task()
        else:
            QMessageBox.information(self, "Information", "Please connect to your accound first")

    def background_task_finished(self):
        self.backgroud_run = False

    def closeEvent(self, event):
        if self.backgroud_run == True:
            QMessageBox.information(self, "Information", "Please stop run before !")
            event.ignore()
            
class WorkerThread(threading.Thread):
    def __init__(self, callback, API_in, market_name_in, widget_close_prize, widget_open_prize, widget_max_prize, widget_min_prize, widget_text_box, widget_table):
        super().__init__()
        self.callback = callback
        self.running = False
        self.API_in = API_in
        self.market_name_in = market_name_in  
        self.widget_close_prize = widget_close_prize
        self.widget_open_prize = widget_open_prize
        self.widget_max_prize = widget_max_prize
        self.widget_min_prize = widget_min_prize
        self.widget_text_box = widget_text_box
        self.widget_table = widget_table

    def run(self):
        try:
            self.running = True
            while self.running:
                self.API_in.start_candles_stream(self.market_name_in, 60, 30) # 60 = 1 min * 60 sec || 10 = 10 dicts
                dict_candle = self.API_in.get_realtime_candles(self.market_name_in, 60) # get_realtime_candles(market_name, size)
                dict_data = {'open': np.array([]), 'high': np.array([]), 'low': np.array([]), 'close': np.array([]), 'volume': np.array([]) }
        
                for x in dict_candle:
                    dict_data['open'] = np.append(dict_data['open'], dict_candle[x]['open'])
                    dict_data['high'] = np.append(dict_data['open'], dict_candle[x]['max'])
                    dict_data['low'] = np.append(dict_data['open'], dict_candle[x]['min'])
                    dict_data['close'] = np.append(dict_data['open'], dict_candle[x]['close'])
                    dict_data['volume'] = np.append(dict_data['open'], dict_candle[x]['volume'])
                
                self.SMA_20 = SMA(dict_data, timeperiod = 20)
                self.SMA_50 = EMA(dict_data, timeperiod = 50) 

                dict_candle = list(dict_candle.items())
                self.widget_close_prize.setText(str(dict_candle[-1][1]['close']))
                self.widget_open_prize.setText(str(dict_candle[-1][1]['open']))
                self.widget_max_prize.setText(str(dict_candle[-1][1]['max']))
                self.widget_min_prize.setText(str(dict_candle[-1][1]['min']))     

                self.current_close_prize = dict_candle[-1][1]['close']
                self.current_open_prize = dict_candle[-1][1]['open']
                self.current_max_prize = dict_candle[-1][1]['max']
                self.current_min_prize = dict_candle[-1][1]['min']

                self.buy_sell_active()

                time.sleep(3)
            self.callback()
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

    def buy_sell_active(self):
        try:
            prize = 1
            period = 10
            file_path = 'temp\\log.csv'

            now = datetime.now()
            current_date = now.strftime("%d/%m/%Y %H:%M")
        
            if self.SMA_50[-3] > self.SMA_20[-3] and self.SMA_50[-2] < self.SMA_20[-2] and self.SMA_50[-1] < self.SMA_20[-1]: # Check SMA and EMA cross together
                if self.current_open_prize > self.SMA_50[-1] and self.current_open_prize > self.SMA_20[-1]: # Check open/close prize is upper SMA and EMA
                    check, id = self.API_in.buy(prize, self.market_name_in, 'call', period)
                    revenue = self.API_in.check_win_v3(id)
                    # Write result tos CSV file
                    with open(file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        row = [current_date, str(prize), str(revenue), str(prize + revenue)] 
                        writer.writerow(row)

                    time.sleep(0.2)

                    # Read CSV file
                    csv_read = []   
                    with open(file_path, mode='r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            csv_read.append(row)
                    for i, row in enumerate(csv_read):
                        for j, val in enumerate(row):
                            table_items = QtWidgets.QTableWidgetItem(str(val))
                            self.widget_table.setItem(i, j, table_items)

            elif self.SMA_50[-3] < self.SMA_20[-3] and self.SMA_50[-2] > self.SMA_20[-2] and self.SMA_50[-1] > self.SMA_20[-1]:
                if self.current_open_prize < self.SMA_50[-1] and self.current_open_prize < self.SMA_20[-1]: # Check open/close prize is lower SMA and EMA
                    check, id = self.API_in.buy(prize, self.market_name_in, 'put', period)
                    revenue = self.API_in.check_win_v3(id)
                    # Write result tos CSV file
                    with open(file_path, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        row = [current_date, str(prize), str(revenue), str(prize + revenue)] 
                        writer.writerow(row)

                    time.sleep(0.2)

                    # Read CSV file
                    with open(file_path, mode='r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            csv_read.append(row)
                    for i, row in enumerate(csv_read):
                        for j, val in enumerate(row):
                            table_items = QtWidgets.QTableWidgetItem(str(val))
                            self.widget_table.setItem(i, j, table_items)

            else:
                self.widget_text_box.setText("Scanning signal...")
                self.widget_text_box.setStyleSheet("background-color : yellow")
                
        except Exception as e:
            QMessageBox.information(self,"Error",f"Error : {e}")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = WindowTrading()
    gui.show()
    app.exec_()