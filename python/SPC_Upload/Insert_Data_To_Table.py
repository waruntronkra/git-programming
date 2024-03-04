from PyQt5 import QtWidgets, QtCore, QtGui, Qt

class InsertDataToTable:
    def input_detail(self, data_input, table_widget, loop, slot, station):
        if len(data_input) > 0:
            for i, val in enumerate(data_input[0]):
                table_item = QtWidgets.QTableWidgetItem(str(val))
                table_item_insert_station = QtWidgets.QTableWidgetItem(station.split('_')[2] + f" : {slot}")
                table_item_insert_active = QtWidgets.QTableWidgetItem('True')

                table_widget.setItem(loop, i, table_item)
                table_widget.setItem(loop, 18, table_item_insert_station)
                table_widget.setItem(loop, 19, table_item_insert_active)    
                table_widget.item(loop, 19).setForeground(QtGui.QColor(5, 255, 0))
                        
        else:
            table_item_insert_station = QtWidgets.QTableWidgetItem(station.split('_')[2] + f" : {slot}")
            table_item_insert_active = QtWidgets.QTableWidgetItem('False')

            table_widget.setItem(loop, 18, table_item_insert_station)
            table_widget.setItem(loop, 19, table_item_insert_active)
            table_widget.item(loop, 19).setForeground(QtGui.QColor(255, 0, 0))