from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import os
import sys

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(150, 150)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.display_gif('temp/loading.gif')

    def display_gif(self, gif_path):
        movie = QtGui.QMovie(gif_path)
        self.label.setMovie(movie)
        movie.start()

def flag_changed(path):
    with open(path, "r") as f:
        flag = f.read().strip()
        if flag == "0":
            app.quit()

if __name__ == "__main__":
    if os.path.exists("temp/trigger.txt"):
        with open("temp/trigger.txt", "r") as f:
            flag = f.read().strip()
            if flag == "0":
                sys.exit()

    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()

    # Watch for changes to the flag.txt file
    watcher = QtCore.QFileSystemWatcher()
    watcher.addPath("temp/trigger.txt")
    watcher.fileChanged.connect(lambda path: flag_changed(path))

    sys.exit(app.exec_())
