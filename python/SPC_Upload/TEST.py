from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt

class CustomButton(QPushButton):
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw a black shadow around the button
        shadow_color = QColor(0, 0, 0, 150)  # Adjust opacity (0-255) to control shadow intensity
        shadow_pen = QPen(shadow_color)
        shadow_pen.setWidth(8)  # Adjust the width of the shadow
        painter.setPen(shadow_pen)
        painter.drawRoundedRect(self.rect().adjusted(4, 4, 4, 4), 5, 5)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button_242 = CustomButton('ATE_400ZR_242', self)
        self.button_242.setStyleSheet('''
                                        background-color: #0CD16F;
                                        border-radius: 5px;
                                        font-weight: bold;
                                        font-size: 12px;
                                    ''')
        self.button_242.setGeometry(10, 470, 130, 50)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MyWidget()
    window.setWindowTitle('Button with Black Shadow')
    window.setGeometry(100, 100, 300, 200)
    window.show()
    sys.exit(app.exec_())
