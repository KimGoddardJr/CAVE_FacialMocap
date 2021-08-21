# modified from pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QApplication

class StartWindow(QMainWindow):
    def __init__(self, camera):
        super().__init__()
        self.camera == camera

        self.central_widget = QWidget()
        self.button = QPushButton('Frame', self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button)
        self.setCentralWidget(self.central_widget)

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        frame = self.camera.get_frame()
        print("Maximum in frame {}".format(np.max(frame)))


if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow()
    window.show()
    app.exit(app.exec_())