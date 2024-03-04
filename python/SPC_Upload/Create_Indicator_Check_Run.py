from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton

class CreateIndicatorCheckRun:
    def __init__(self):
        self.button = None

    def input_detail(self, name, parent, x, y, w, h):
        self.button = QPushButton(name, parent)
        self.button.setStyleSheet('''
                                        border-radius : 5px;
                                        background-color : white;
                                        font-weight : bold;
                                        font-size : 12px;
                                        font-family : Century Gothic;
                                    ''')
        self.button.setGeometry(x,y,w,h)

        effect = QGraphicsDropShadowEffect(parent)
        effect.setOffset(5, 5)
        effect.setBlurRadius(5)
        self.button.setGraphicsEffect(effect)

    def set_color(self, color):
        self.button.setStyleSheet(f'''
                                    border-radius : 5px;
                                    background-color : {color};
                                    font-weight : bold;
                                    font-size : 12px;
                                    font-family : Century Gothic;
                                ''')
