from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem

class MyUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        BT_Refresh = QPushButton('Refreh', self)
     
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MyUI()
    gui.show()
    app.exec_()