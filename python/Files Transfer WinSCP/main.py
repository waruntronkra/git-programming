from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QIcon

class GUI(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        
        self.setWindowTitle('Files Transfer V1.0')
        self.setWindowIcon(QIcon('icons/cheese.ico'))
        self.setFixedSize(500, 500)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = GUI()
    gui.show()
    app.exec_()