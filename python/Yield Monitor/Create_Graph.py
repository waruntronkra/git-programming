from PyQt5.QtChart import QChart, QChartView
from PyQt5.QtGui import QPainter

class CreateGraph:
    def input_detail(self, ax, ay, w, h, page, hide):
        Graph = QChart()
        Graph_View = QChartView(Graph, page)
        Graph_View.setGeometry(ax, ay, w, h)
        Graph_View.setRenderHint(QPainter.Antialiasing)

        if hide == True:
            Graph_View.hide()
        elif hide == False:
            Graph_View.show()

        return Graph, Graph_View