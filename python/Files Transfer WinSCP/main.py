from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QComboBox, QLineEdit, QPlainTextEdit, QLabel, QListWidget
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt, QSize
from utilities.List_Files_WinSCP import ListFilesWinSCP
from utilities.Read_Files_WinSCP import ReadFilesWinSCP
import configparser

class GUI(QtWidgets.QMainWindow):
    def __init__ (self):
        super().__init__()
        
        self.setWindowTitle('Files Transfer V1.0')
        self.setWindowIcon(QIcon('icons/cheese.ico'))
        self.setFixedSize(500, 480)

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
        line.setGeometry(10, 190, 400, 2)

        # ================================== Input SERIAL NUMBER & PROCESS ==================================
        label_serial_number = QLabel('SERIAL NUMBER :', self)
        label_serial_number.setStyleSheet('font-weight: bold;')
        label_serial_number.setGeometry(10, 211, 95, 20)
        self.input_serial_number = QLineEdit('', self)
        self.input_serial_number.setValidator(QIntValidator(1, 999999999, self))
        self.input_serial_number.setAlignment(Qt.AlignCenter)
        self.input_serial_number.setGeometry(110, 210, 100, 25)

        label_serial_number = QLabel('PROCESS :', self)
        label_serial_number.setStyleSheet('font-weight: bold;')
        label_serial_number.setGeometry(50, 246, 80, 20)
        process = ['PCAL', 'CAL', 'FVT', 'FPT', 'ESS', 'EXP', 'EXS', 'EXS5']
        self.input_process = QComboBox(self)
        self.input_process.addItems(process)
        self.input_process.setGeometry(110, 245, 50, 25)

        # ================================== Start run ==================================
        self.payload = QPlainTextEdit('', self)
        self.payload.setStyleSheet('font-size: 10px;')
        self.payload.setReadOnly(True)
        self.payload.setGeometry(10, 320, 200, 150)
        cursor = self.payload.textCursor()
        cursor.movePosition(cursor.End)
        self.payload.setTextCursor(cursor)

        button = QPushButton('Search', self)
        button.clicked.connect(self.startTransfering)
        button.setGeometry(10, 280, 201, 30)

        self.files_view = QListWidget(self)
        self.files_view.itemClicked.connect(self.getListSelected)
        self.files_view.setGeometry(220, 210, 100, 260)

        self.remot_path = '/data/FTP/'

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
    
    def getListSelected(self, clickedItem):
        if "." in clickedItem.text():
            self.payload.appendPlainText(f'''\nRead file from path [{self.remot_path + clickedItem.text()}] \n > {ReadFilesWinSCP().run(
                self.input_host.text(), 
                self.input_username.text(), 
                self.input_password.text(), 
                self.input_port.text(),
                self.remot_path,
                'state.txt'
            ).split("'")[1]}''')
        else:
            self.payload.appendPlainText(f'\n[{clickedItem.text()}] is not a file')

    def startTransfering(self):
        self.payload.appendPlainText('Connecting to WinSCP...')
        self.payload.appendPlainText(f'USER : {self.input_username.text()}')
        data = ListFilesWinSCP().run(
            self.input_host.text(), 
            self.input_username.text(), 
            self.input_password.text(), 
            self.input_port.text(),
            self.remot_path
        )
        self.payload.appendPlainText('Finished!')
        
        self.files_view.clear()
        for i in data:
            self.files_view.addItem(i)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = GUI()
    gui.show()
    app.exec_()