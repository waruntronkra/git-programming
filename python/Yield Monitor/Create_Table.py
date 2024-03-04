from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *

class CreateTable():
    def Table_Detail(self, Text_Label, Tab_Locate, x_label, y_label, x_table, y_table, w_table, h_table):
        table_label = QLabel(Text_Label, Tab_Locate)
        table_label.move(x_label, y_label)
        table = QtWidgets.QTableWidget(Tab_Locate)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed) # Disable resizeable row
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed) # Disable resizeable column
        table.setGeometry(x_table, y_table, w_table, h_table)
        return table
        