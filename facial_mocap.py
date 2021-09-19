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

bShowGeomPreview = True

if __name__ == "__main__":
    import sys

    App = QApplication(sys.argv)
    Root = MainWindow()
    #Main GUI:
    Root.show()
    #Preview geometry window
    if bShowGeomPreview:
        Root.Show()
    sys.exit(App.exec_())
