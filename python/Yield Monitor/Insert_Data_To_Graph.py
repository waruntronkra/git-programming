from PyQt5.QtChart import QLineSeries, QCategoryAxis, QValueAxis
from PyQt5.QtGui import QFont, QPen
from PyQt5.QtCore import Qt
import numpy as np

class InsertDataToGraph:
    def detail_in(self, data_in, array_date_in, graph_in, name, data_check, mode, product_type):
        if product_type == 'AC1200' or product_type == 'AX1200':
            if len(data_check) > 0:
                None
            else:
                data_in = [{'name': 'TX_LANE0', 'data': []}, {'name': 'RX_LANE0', 'data': []}, {'name': 'TX_LANE1', 'data': []}, {'name': 'RX_LANE1', 'data': []}]
            graph_in.removeAllSeries()
            serie_dict = {}
            group_data = []
            serie_index = 0
            for data_dict in data_in:
                series_name = data_dict['name'] # Serie name
                series = QLineSeries()
                series.setPointsVisible(True) # Show marker point
                if mode == "Base Line":
                    if serie_index == 4 or serie_index == 5:
                        pen = QPen(Qt.black, 2, Qt.DotLine)
                        series.setPen(pen)
                for point in data_dict['data']:
                    x_val = point[0]   
                    if point[1] != '':                     
                        y_val = float(point[1])
                        series.append(x_val, y_val)
                        group_data.append(y_val)  
                    else:
                        series.append(x_val, np.nan)
                series.setName(series_name)
                graph_in.addSeries(series)
                serie_dict[series_name] = series
                serie_index += 1

            graph_in.createDefaultAxes()
            graph_in.axisX().hide()
            graph_in.axisY().hide()
            graph_in.setTitle(name)

            # Create x-axis string (DateTime)
            x_axis = QCategoryAxis()
            x_axis.setLabelsAngle(-90)
            y_axis = QValueAxis()
                    
            x = 0      
            for point in data_in[0]['data']:
                if len(array_date_in) == 1:
                    x_val = point[0]
                else:
                    x_val = point[0]+1
                x_axis.setLabelsPosition(x_val) 
                x_axis.append(array_date_in[x], x_val)              
                x += 1   

            font = QFont()
            font.setPointSize(6)  # Set font size to 10 points

            x_axis.setLabelsFont(font)
            y_axis.setLabelsFont(QFont("Arial", 7))

            x_axis.setRange(-0.5, len(array_date_in) -0.5)
            if group_data:
                y_axis.setRange((min(group_data)) - 0.2, (max(group_data)) + 0.2)  

            graph_in.addAxis(x_axis, Qt.AlignBottom)
            graph_in.addAxis(y_axis, Qt.AlignLeft)
            for i in serie_dict.values():          
                i.attachAxis(x_axis)
            series.attachAxis(y_axis)
        
        elif product_type == '400ZR':
            if len(data_check) > 0:
                None
            else:
                data_in = [{'name': 'TX_LANE0', 'data': []}, {'name': 'RX_LANE0', 'data': []}]
            graph_in.removeAllSeries()
            serie_dict = {}
            group_data = []
            serie_index = 0
            for data_dict in data_in:
                series_name = data_dict['name'] # Serie name
                series = QLineSeries()
                series.setPointsVisible(True) # Show marker point
                if mode == "Base Line":
                    if serie_index == 2 or serie_index == 3:
                        pen = QPen(Qt.black, 2, Qt.DotLine)
                        series.setPen(pen)
                for point in data_dict['data']:
                    x_val = point[0]   
                    if point[1] != '':                     
                        y_val = float(point[1])
                        series.append(x_val, y_val)
                        group_data.append(y_val)  
                    else:
                        series.append(x_val, np.nan)
                series.setName(series_name)
                graph_in.addSeries(series)
                serie_dict[series_name] = series
                serie_index += 1

            graph_in.createDefaultAxes()
            graph_in.axisX().hide()
            graph_in.axisY().hide()
            graph_in.setTitle(name)

            # Create x-axis string (DateTime)
            x_axis = QCategoryAxis()
            x_axis.setLabelsAngle(-90)
            y_axis = QValueAxis()
                    
            x = 0      
            for point in data_in[0]['data']:
                if len(array_date_in) == 1:
                    x_val = point[0]
                else:
                    x_val = point[0]+1
                x_axis.setLabelsPosition(x_val) 
                x_axis.append(array_date_in[x], x_val)              
                x += 1   

            font = QFont()
            font.setPointSize(6)  # Set font size to 10 points

            x_axis.setLabelsFont(font)
            y_axis.setLabelsFont(QFont("Arial", 7))

            x_axis.setRange(-0.5, len(array_date_in) -0.5)
            if group_data:
                y_axis.setRange((min(group_data)) - 0.2, (max(group_data)) + 0.2)  

            graph_in.addAxis(x_axis, Qt.AlignBottom)
            graph_in.addAxis(y_axis, Qt.AlignLeft)
            for i in serie_dict.values():          
                i.attachAxis(x_axis)
            series.attachAxis(y_axis)