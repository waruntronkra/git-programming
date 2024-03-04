from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt

class CreateSlotEXS:
    def input_data(self, page, x_begin, y_begin): # x_begin = begin 32 || y_begin = begin 105
        frame = QFrame(page)
        frame.setGeometry(x_begin, y_begin, 135, 50)
        frame.setStyleSheet("background-color: #FFF899;")
        frame.setFrameShape(QFrame.Box)
        
        UUT_SN_Box = QLineEdit(page)
        UUT_SN_Box.setAlignment(Qt.AlignCenter)
        UUT_SN_Box.setMaxLength(9)
        validator = QIntValidator()
        UUT_SN_Box.setValidator(validator)
        UUT_SN_Box.setStyleSheet("background-color: #FFFFFF;")
        UUT_SN_Box.setGeometry(x_begin + 58, y_begin + 25, 70, 20)     

        label = QLabel("UUT", page)
        label.setGeometry(x_begin + 36, y_begin + 28, 20, 10)

        LoopBack_SN_Label = QLabel("LoopBack", page)
        LoopBack_SN_Label.move(x_begin + 7, y_begin - 1)
        
        LoopBack_SN = QLineEdit('', page)
        LoopBack_SN.setAlignment(Qt.AlignCenter)
        LoopBack_SN.setStyleSheet('font-size: 8px')
        LoopBack_SN.setMaxLength(14) # SN loopback max length
        LoopBack_SN.setGeometry(x_begin + 58, y_begin + 8, 70, 15)
        # LoopBack_SN.setReadOnly(True)
        
        return UUT_SN_Box, LoopBack_SN
