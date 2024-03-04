from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QScrollArea, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtChart import QLineSeries, QChartView, QChart
import csv
from Get_File_WinSCP import ConnectWinSCP_GET
from Read_File_WinSCP import ConnectWinSCP_READ
import time

class MyGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        main_widget = QWidget(scroll_area)
        scroll_area.setWidget(main_widget)
        main_widget.setMinimumSize(160, 5000)
        self.setCentralWidget(scroll_area)

        # ==================Creat chart for ATE_AC1200_154 ==================
        self.chart_ATE_154 = QChart()
        self.chart_ATE_154_view = QChartView(self.chart_ATE_154, main_widget)
        self.chart_ATE_154_view.setRenderHint(QPainter.Antialiasing)
        self.chart_ATE_154_view.setGeometry(10,10,700,400)

        self.delta_label_ATE_154 = QLabel('Delta :', main_widget)
        self.delta_label_ATE_154.setGeometry(30,25,100,20)

        self.delta_ATE_154 = QLineEdit('', main_widget)
        self.delta_ATE_154.setReadOnly(True)
        self.delta_ATE_154.setAlignment(Qt.AlignCenter)
        self.delta_ATE_154.setGeometry(70,27,50,20)     

        # ==================Creat chart for ATE_AC1200_211 ==================
        self.chart_ATE_211 = QChart()
        self.chart_ATE_211_view = QChartView(self.chart_ATE_211, main_widget)
        self.chart_ATE_211_view.setRenderHint(QPainter.Antialiasing)
        self.chart_ATE_211_view.setGeometry(750,10,700,400)

        self.delta_label_ATE_211 = QLabel('Delta :', main_widget)
        self.delta_label_ATE_211.setGeometry(770,25,100,20)

        self.delta_ATE_211 = QLineEdit('', main_widget)
        self.delta_ATE_211.setReadOnly(True)
        self.delta_ATE_211.setAlignment(Qt.AlignCenter)
        self.delta_ATE_211.setGeometry(810,27,50,20)   

        # ==================Creat chart for ATE_AC1200_195 ==================
        self.chart_ATE_195 = QChart()
        self.chart_ATE_195_view = QChartView(self.chart_ATE_195, main_widget)
        self.chart_ATE_195_view.setRenderHint(QPainter.Antialiasing)
        self.chart_ATE_195_view.setGeometry(10,420,700,400)       

        self.delta_label_ATE_195 = QLabel('Delta :', main_widget)
        self.delta_label_ATE_195.setGeometry(30,435,100,20)

        self.delta_ATE_195 = QLineEdit('', main_widget)
        self.delta_ATE_195.setReadOnly(True)
        self.delta_ATE_195.setAlignment(Qt.AlignCenter)
        self.delta_ATE_195.setGeometry(70,433,50,20)

        # ==================Creat chart for ATE_AC1200_213 ==================
        self.chart_ATE_213 = QChart()
        self.chart_ATE_213_view = QChartView(self.chart_ATE_213, main_widget)
        self.chart_ATE_213_view.setRenderHint(QPainter.Antialiasing)
        self.chart_ATE_213_view.setGeometry(750,420,700,400)

        self.delta_label_ATE_213 = QLabel('Delta :', main_widget)
        self.delta_label_ATE_213.setGeometry(770,435,100,20)

        self.delta_ATE_213 = QLineEdit('', main_widget)
        self.delta_ATE_213.setReadOnly(True)
        self.delta_ATE_213.setAlignment(Qt.AlignCenter)
        self.delta_ATE_213.setGeometry(810,433,50,20)

        self.array_chart = [self.chart_ATE_154, self.chart_ATE_195, self.chart_ATE_211, self.chart_ATE_213]
        self.array_delta = [self.delta_ATE_154, self.delta_ATE_195, self.delta_ATE_211, self.delta_ATE_213]
        
        self.start_timmer()   
    
        self.setGeometry(50,50,1500,950)
    
    def start_timmer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.set_trigger)
        self.timer.start(10000)

    def set_trigger(self):
        Read_File_WinSCP = ConnectWinSCP_READ()
        trigger = Read_File_WinSCP.start_read_file()
        print(trigger)
        if trigger == b'1':
            self.run_chart()
        else:
            None
            self.start_timmer() 

    def run_chart(self):
        WinSCP = ConnectWinSCP_GET()
        result = WinSCP.start_get_file()

        EXS_STATION = ['ATE_AC1200_154', 'ATE_AC1200_195', 'ATE_AC1200_211', 'ATE_AC1200_213', 'ATE_AC1200_252', 'ATE_AC1200_254']
        for j in range(len(self.array_chart)):
            self.array_chart[j].removeAllSeries()
        if len(result) > 0:   
            for i in result[1]:      
                position = EXS_STATION.index(i)    
                data = result[0][i] # First data (sort by Dict Name)
                # data_time = result[2][i]
                # print(data_time)

                Dict_Expect_Temp = {}
                with open('temp/TRS Spec/TRS AC1200 EXS.csv', 'r') as f:
                    csv_reader = csv.reader(f)
                    next(csv_reader)

                    column = [row[2] for row in csv_reader]
                    column = column[:len(data)]
                    Dict_Expect_Temp['Expect Temperature'] = column 

                data_expect_temp = list(Dict_Expect_Temp.values()) 

                series_1 = QLineSeries()
                series_1.setName(result[1][0])

                for x, value in enumerate(data):
                    series_1.append(int(x), float(value))
                    pen = QPen(Qt.red,2)
                    series_1.setPen(pen)

                series_2 = QLineSeries()
                series_2.setName("Expect Temperature")

                for y, value in enumerate(data_expect_temp[0]):
                    series_2.append(int(x), float(value))
                    pen = QPen(QColor("#15C800"), 2)
                    series_2.setPen(pen)

                self.array_chart[position].addSeries(series_1) 
                self.array_chart[position].addSeries(series_2) 

                self.array_chart[position].createDefaultAxes()

                dt = abs(float(data[-1]) - float(data_expect_temp[0][-1]))
                dt = "{:.2f}".format(dt)
                self.array_delta[position].setText(str(dt))

                time.sleep(0.1)

        self.start_timmer() 
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = MyGUI()
    gui.show()
    app.exec_()