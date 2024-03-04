import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QFileDialog

class CameraStream(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera, change if needed
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton('Capture', self)
        self.capture_button.clicked.connect(self.capture_image)

        self.toggle_camera_button = QPushButton('Open Camera', self)
        self.toggle_camera_button.clicked.connect(self.toggle_camera)

        self.save_path_input = QLineEdit(self)
        self.save_path_input.setPlaceholderText('Enter path to save images...')

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_save_path)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.video_label)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.toggle_camera_button)
        layout.addWidget(self.save_path_input)
        layout.addWidget(self.browse_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every 30 milliseconds

        self.is_camera_open = True

    def update_frame(self):
        ret, frame = self.video_capture.read()

        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

    def toggle_camera(self):
        if self.is_camera_open:
            self.video_capture.release()
            self.toggle_camera_button.setText('Open Camera')
        else:
            self.video_capture.open(0)
            self.toggle_camera_button.setText('Close Camera')
        self.is_camera_open = not self.is_camera_open

    def capture_image(self):
        ret, frame = self.video_capture.read()

        if ret:
            save_path = self.save_path_input.text()
            if save_path:
                cv2.imwrite(save_path + "/captured_image.png", frame)
                print("Image saved successfully.")

    def browse_save_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.save_path_input.setText(path)

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = CameraStream()
    window.setWindowTitle("Camera Stream with PyQt5")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
