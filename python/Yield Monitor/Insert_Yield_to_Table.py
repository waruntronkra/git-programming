from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *

class InsertYieldtoTable():
    def Yield_Detail(self, Array_Process_in, Array_Yield_in, Table):
        for i, row in enumerate(Array_Yield_in):
            Table.insertRow(i)
            for j, val in enumerate(row):
                table_yield_item = QtWidgets.QTableWidgetItem(str(val))
                Table.setItem(i, j, table_yield_item)
                Table.item(i, 0).setBackground(QtGui.QColor(214, 159, 255))
                if j == 4:
                    Yield_Num = val.split(" ")
                    if float(Yield_Num[0]) > 90:
                        Table.item(i, j).setBackground(QtGui.QColor(0, 255, 20))
                    elif float(Yield_Num[0]) > 75:
                        Table.item(i, j).setBackground(QtGui.QColor(255, 205, 0))
                    else:
                        Table.item(i, j).setBackground(QtGui.QColor(255, 57, 57))

        Table.setRowCount(len(Array_Process_in))
        for i in range(Table.rowCount()): # Resize row
            Table.setRowHeight(i, 11)

        Table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color: #FFF59F}")
        Table.setStyleSheet(f"QTableView {{gridline-color: {'black'};}}")
        Table.verticalHeader().setVisible(False)
