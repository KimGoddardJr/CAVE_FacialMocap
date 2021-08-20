from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

app = QApplication([])
win = QMainWindow()

label = QLabel('Test Window')
button = QPushButton('Test')
win.setCentralWidget(label)
win.setCentralWidget(button)

win.show()
app.exit(app.exec())