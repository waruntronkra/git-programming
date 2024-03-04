from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt

class CreateSlot:
    def input_data(self, page, tag_name, x_begin, y_begin): # x_begin = begin 32 || y_begin = begin 105
        frame = QFrame(page)
        frame.setGeometry(x_begin, y_begin, 155, 110)
        frame.setStyleSheet("background-color: #FFF899;")
        frame.setFrameShape(QFrame.Box)

        font = QFont("Arial", 12, QFont.Bold)
        UUT_SN_Box_Label = QLabel(tag_name, page)
        UUT_SN_Box_Label.setFont(font)
        UUT_SN_Box_Label.move(x_begin + 58, y_begin)

        UUT_SN_Box = QLineEdit(page)
        UUT_SN_Box.setAlignment(Qt.AlignCenter)
        UUT_SN_Box.setMaxLength(9)
        validator = QIntValidator()
        UUT_SN_Box.setValidator(validator)
        UUT_SN_Box.setStyleSheet("background-color: #FFFFFF;")
        UUT_SN_Box.setGeometry(x_begin + 28, y_begin + 45, 70, 20)
        
        TX_Label = QLabel("TX", page)
        TX_Label.move(x_begin + 12, y_begin + 19)
        RX_Label = QLabel("RX", page)
        RX_Label.move(x_begin + 12, y_begin + 59)  

        label = QLabel("UUT", page)
        label.setGeometry(x_begin + 6, y_begin + 48, 20, 10)
        
        TX_SN = QLineEdit('', page)
        TX_SN.setAlignment(Qt.AlignCenter)
        TX_SN.setGeometry(x_begin + 28, y_begin + 28, 120, 15)
        TX_SN.setReadOnly(True)
        
        RX_SN = QLineEdit('', page)
        RX_SN.setAlignment(Qt.AlignCenter)
        RX_SN.setGeometry(x_begin + 28, y_begin + 67, 120, 15)
        RX_SN.setReadOnly(True)

        Shim_SN_label = QLabel("Shim", page)
        Shim_SN_label.setGeometry(x_begin + 54, y_begin + 88, 30, 10)
        Shim_SN = QLineEdit('', page)
        Shim_SN.setAlignment(Qt.AlignCenter)
        Shim_SN.setMaxLength(5)
        Shim_SN.setGeometry(x_begin + 78, y_begin + 85, 70, 20)

        test_count = QLineEdit('', page)
        test_count.setGeometry(x_begin + 4, y_begin + 4, 20, 20)
        test_count.setStyleSheet("background-color: #00FFFD;")
        test_count.setAlignment(Qt.AlignCenter)
        test_count.setReadOnly(True)

        return UUT_SN_Box, TX_SN, RX_SN, test_count, Shim_SN
