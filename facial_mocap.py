"""
MSc Project - Georgie Challis (s5400010), 2021 
Facial animation from webcam data to Unreal Engine.

Dependencies:
* OpenCV
* PyQt5 and PyQt3D 
* dlib
* eos 3D Morphable Face Model fitting library

See individual modules for code references and resources
See written report for academic references and theory
"""

from viewer import MainWindow
from PyQt5.QtWidgets import *

import sys

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())
