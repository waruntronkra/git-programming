from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QComboBox, QLineEdit, QPlainTextEdit, QLabel, QListWidget, QRadioButton, QButtonGroup, QProgressBar, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize, QThread
from utilities.Read_Files_WinSCP import ReadFilesWinSCP
from utilities.Write_Files_WinSCP import WriteFilesWinSCP
from utilities.Copy_Files_WinSCP import CopyFilesWinSCP
import configparser
import time
import os
from threading import *

class GUI(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        
        self.setWindowTitle('Files Transfer V1.0')
        self.setWindowIcon(QIcon('icons/cheese.ico'))
        self.setFixedSize(320, 430)

        # ================================== Read .ini file ==================================
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.host_winscp = config['User Configuration']['host']
        self.port_winscp = config['User Configuration']['port']
        self.username_winscp = config['User Configuration']['username']
        self.password_winscp = config['User Configuration']['password']

        config.set('User Configuration', 'host', self.host_winscp)
        config.set('User Configuration', 'port', self.port_winscp)
        config.set('User Configuration', 'username', self.username_winscp)
        config.set('User Configuration', 'password', self.password_winscp)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        # ================================== Show user information ==================================
        frame_user_info = QFrame(self)
        frame_user_info.setStyleSheet('border: 1px solid black;')
        frame_user_info.setGeometry(10, 10, 240, 170)

        label_host = QLabel('HOST :', self)
        label_host.setGeometry(60, 21, 35, 20)
        self.input_host = QLineEdit(self.host_winscp, self)
        self.input_host.setReadOnly(True)
        self.input_host.setAlignment(Qt.AlignCenter)
        self.input_host.setStyleSheet('background-color: #E0E0E0')
        self.input_host.setGeometry(100, 20, 120, 25)

        label_port = QLabel('PORT :', self)
        label_port.setGeometry(60, 51, 35, 20)
        self.input_port = QLineEdit(self.port_winscp, self)
        self.input_port.setReadOnly(True)
        self.input_port.setAlignment(Qt.AlignCenter)
        self.input_port.setStyleSheet('background-color: #E0E0E0')
        self.input_port.setGeometry(100, 50, 120, 25)

        label_username = QLabel('USERNAME :', self)
        label_username.setGeometry(33, 81, 60, 20)
        self.input_username = QLineEdit(self.username_winscp, self)
        self.input_username.setReadOnly(True)
        self.input_username.setAlignment(Qt.AlignCenter)
        self.input_username.setStyleSheet('background-color: #E0E0E0')
        self.input_username.setGeometry(100, 80, 120, 25)

        self.visible_password = QPushButton(QIcon('icons/hide_password.ico'), '', self)
        self.visible_password.setVisible(False)
        self.visible_password.setStyleSheet('border: none;')
        self.visible_password.setIconSize(QSize(22, 22))
        self.visible_password.pressed.connect(self.showPassword)
        self.visible_password.released.connect(self.hidePassword)
        self.visible_password.setGeometry(222, 112, 25, 25)
        self.label_password = QLabel('PASSWORD :', self)
        self.label_password.setGeometry(30, 111, 65, 20)
        self.input_password = QLineEdit(self.password_winscp, self)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setReadOnly(True)
        self.input_password.setAlignment(Qt.AlignCenter)
        self.input_password.setStyleSheet('background-color: #E0E0E0')
        self.input_password.setGeometry(100, 110, 120, 25)

        self.update_user_info = QPushButton(QIcon('icons/edit_user_info.ico'), '  Edit user information', self)
        self.update_user_info.clicked.connect(self.editUserInfo)
        self.update_user_info.setGeometry(28, 140, 193, 30)

        line = QPushButton('', self)
        line.setStyleSheet('background-color: black;')
        line.setGeometry(10, 190, 300, 2)

        # ================================== Input SERIAL NUMBER & PROCESS ==================================
        label_serial_number = QLabel('SERIAL NUMBER :', self)
        label_serial_number.setStyleSheet('font-weight: bold;')
        label_serial_number.setGeometry(10, 211, 95, 20)
        self.input_serial_number = QLineEdit('', self)
        self.input_serial_number.setValidator(QIntValidator(1, 999999999, self))
        self.input_serial_number.setAlignment(Qt.AlignCenter)
        self.input_serial_number.setGeometry(110, 210, 80, 25)

        label_serial_number = QLabel('PROCESS :', self)
        label_serial_number.setStyleSheet('font-weight: bold;')
        label_serial_number.setGeometry(200, 211, 80, 20)
        process = ['OIT', 'OST', 'PCAL', 'CAL', 'FPT', 'FVT', 'FST', 'EPT', 'ESS', 'EXP', 'EXS', 'EXS5']
        self.input_process = QComboBox(self)
        self.input_process.addItems(process)
        self.input_process.setGeometry(260, 210, 50, 25)

        # ================================== Start run ==================================
        self.button_run = QPushButton('Start Searching', self)
        self.button_run.setStyleSheet('font-size: 15px; font-weight: bold;')
        self.button_run.clicked.connect(self.start_thread)
        self.button_run.setGeometry(10, 380, 302, 40)

        frame_progress_bar = QFrame(self)
        frame_progress_bar.setStyleSheet('border: 1px solid grey;')
        frame_progress_bar.setGeometry(10, 348, 302, 24)
        self.progress_bar = QPushButton(self)
        self.progress_bar.setDisabled(True)
        self.progress_bar.setStyleSheet('background-color: red;')
        self.progress_bar.setGeometry(12, 350, 0, 20)
        # self.progress_bar.setGeometry(10, 350, 298, 20)

        frame_product = QFrame(self)
        frame_product.setStyleSheet('border: 1px solid black; padding: 15px;')
        frame_product.setGeometry(110, 250, 100, 85)

        label_product = QLabel('PRODUCT', self)
        label_product.setAlignment(Qt.AlignCenter)
        label_product.setStyleSheet('background-color: rgb(240, 240, 240);')
        label_product.setGeometry(120, 240, 60, 20)

        product_ax1200 = QRadioButton('AX1200', self)
        product_ax1200.setChecked(True)
        product_ax1200.setStyleSheet('font-size: 13px;')
        product_ax1200.setGeometry(120, 260, 100, 30)

        product_ac1200 = QRadioButton('AC1200', self)
        product_ac1200.setStyleSheet('font-size: 13px;')
        product_ac1200.setGeometry(120, 280, 100, 30)

        product_ac1200ng = QRadioButton('AC1200NG', self)
        product_ac1200ng.setStyleSheet('font-size: 13px;')
        product_ac1200ng.setGeometry(120, 300, 100, 30)

        self.button_group_product = QButtonGroup(self)
        self.button_group_product.addButton(product_ax1200)
        self.button_group_product.addButton(product_ac1200)
        self.button_group_product.addButton(product_ac1200ng)
        self.button_group_product.buttonClicked.connect(self.select_product)

        frame_file_type = QFrame(self)
        frame_file_type.setStyleSheet('border: 1px solid black; padding: 15px;')
        frame_file_type.setGeometry(225, 250, 75, 85)

        label_file_type = QLabel('FILE TYPE', self)
        label_file_type.setAlignment(Qt.AlignCenter)
        label_file_type.setStyleSheet('background-color: rgb(240, 240, 240);')
        label_file_type.setGeometry(231, 240, 60, 20)

        file_type_html = QRadioButton('.html', self)
        file_type_html.setChecked(True)
        file_type_html.setStyleSheet('font-size: 13px;')
        file_type_html.setGeometry(235, 260, 100, 30)

        file_type_txt = QRadioButton('.txt', self)
        file_type_txt.setStyleSheet('font-size: 13px;')
        file_type_txt.setGeometry(235, 280, 100, 30)

        file_type_sqlite = QRadioButton('.sqlite', self)
        file_type_sqlite.setStyleSheet('font-size: 13px;')
        file_type_sqlite.setGeometry(235, 300, 100, 30)

        self.button_group_file_type = QButtonGroup(self)
        self.button_group_file_type.addButton(file_type_html)
        self.button_group_file_type.addButton(file_type_txt)
        self.button_group_file_type.addButton(file_type_sqlite)
        self.button_group_file_type.buttonClicked.connect(self.select_file_type)
        
        self.remot_path = '/data/FTP/'
        self.selected_product = 'AX1200'
        self.selected_file_type = '.html'
        self.worker_thread = None

    def select_product(self, index):
        self.selected_product = index.text()
        
    def select_file_type(self, index):
        self.selected_file_type = index.text()

    def showPassword(self):
        self.visible_password.setIcon(QIcon('icons/show_password.ico'))
        self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)

    def hidePassword(self):
        self.visible_password.setIcon(QIcon('icons/hide_password.ico'))
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
    
    def editUserInfo(self):
        if self.update_user_info.text() == '  Edit user information':
            self.input_host.setReadOnly(False)
            self.input_host.setStyleSheet('background-color: white')

            self.input_port.setReadOnly(False)
            self.input_port.setStyleSheet('background-color: white')

            self.input_username.setReadOnly(False)
            self.input_username.setStyleSheet('background-color: white')

            self.input_password.setReadOnly(False)
            self.input_password.setStyleSheet('background-color: white')

            self.visible_password.setVisible(True)
            self.update_user_info.setIcon(QIcon('icons/save_user_info.ico'))
            self.update_user_info.setText('  UPDATE') 

        elif self.update_user_info.text() == '  UPDATE':
            config = configparser.ConfigParser()
            config.read('config.ini')

            config.set('User Configuration', 'host', self.input_host.text())
            config.set('User Configuration', 'port', self.input_port.text())
            config.set('User Configuration', 'username', self.input_username.text())
            config.set('User Configuration', 'password', self.input_password.text())
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
                
            self.input_host.setReadOnly(True)
            self.input_host.setStyleSheet('background-color: #E0E0E0')

            self.input_port.setReadOnly(True)
            self.input_port.setStyleSheet('background-color: #E0E0E0')

            self.input_username.setReadOnly(True)
            self.input_username.setStyleSheet('background-color: #E0E0E0')

            self.input_password.setReadOnly(True)
            self.input_password.setStyleSheet('background-color: #E0E0E0')

            self.visible_password.setVisible(False)
            self.update_user_info.setIcon(QIcon('icons/edit_user_info.ico'))
            self.update_user_info.setText('  Edit user information')

    def start_thread(self):
        if self.input_serial_number.text() != '':
            if len(self.input_serial_number.text()) == 9:
                t1 = Thread(target=self.startRun)
                t1.start()
            else:
                QMessageBox.information(self, 'Notify', 'Serial Number lenght is not equal 9')
        else:
            QMessageBox.information(self, 'Notify', 'Please input Serial Number!')
    
    def startRun(self):
        if os.path.exists('temp\\storage\\files.7z'):
            os.remove('temp\\storage\\files.7z')

        self.button_run.setDisabled(True)
        self.button_run.setText('Loading...')
        self.input_process.setDisabled(True)
        self.update_user_info.setDisabled(True)

        self.progress_bar.setGeometry(12, 350, 0, 20)
        self.progress_bar.setStyleSheet('background-color: red;')
        self.progress_bar.setGeometry(12, 350, 30, 20)
        WriteFilesWinSCP().run(
            self.input_host.text(), 
            self.input_username.text(),
            self.input_password.text(),
            self.input_port.text(),
            'start',
            '/data/FTP/',
            'trigger.txt'
        )
        self.progress_bar.setStyleSheet('background-color: red;')
        self.progress_bar.setGeometry(12, 350, 110, 20)

        WriteFilesWinSCP().run(
            self.input_host.text(), 
            self.input_username.text(),
            self.input_password.text(),
            self.input_port.text(),
            f'{self.input_serial_number.text()}\n{self.selected_product}\n{self.input_process.currentText()}\n{self.selected_file_type}',
            '/data/FTP/',
            'detail.txt'
        )
        self.progress_bar.setStyleSheet('background-color: orange;')
        self.progress_bar.setGeometry(12, 350, 180, 20)

        trigger = "b'start'"
        while trigger.split("'")[1] != 'done' and trigger.split("'")[1] != 'empty':
            trigger = ReadFilesWinSCP().run(
                self.input_host.text(), 
                self.input_username.text(),
                self.input_password.text(),
                self.input_port.text(),
                '/data/FTP/',
                'trigger.txt'
            )
            self.progress_bar.setStyleSheet('background-color: orange;')
            self.progress_bar.setGeometry(12, 350, 220, 20)
            time.sleep(0.2)

        self.progress_bar.setStyleSheet('background-color: yellow;')
        self.progress_bar.setGeometry(12, 350, 250, 20)

        if trigger.split("'")[1] != 'empty':
            CopyFilesWinSCP().run(
                self.input_host.text(), 
                self.input_username.text(),
                self.input_password.text(),
                self.input_port.text(),
                '/data/FTP/',
                'temp/storage',
                'files.7z',
                '.7z'
            )
            os.startfile(os.path.realpath('temp/storage'))

        self.progress_bar.setStyleSheet('background-color: rgb(0, 255, 0);')
        self.progress_bar.setGeometry(12, 350, 298, 20)

        self.button_run.setDisabled(False)
        self.button_run.setText('Start Searching')
        self.input_process.setDisabled(False)
        self.update_user_info.setDisabled(False)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = GUI()
    gui.show()
    app.exec_()