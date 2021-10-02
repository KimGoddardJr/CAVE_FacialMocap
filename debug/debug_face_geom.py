from PyQt5.QtWidgets import *
from PyQt5.Qt3DExtras import Qt3DWindow, QFirstPersonCameraController
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DExtras import *
from PyQt5.Qt3DRender import *

class OrbitTransformController(QObject):
    def __init__(self, parent):
        super(OrbitTransformController, self).__init__(parent)
        self.m_target = QTransform()
        self.m_matrix = QMatrix4x4()
        self.m_radius = 1.0
        self.m_angle = 0

    def getTarget(self):
        return self.m_target

    def setTarget(self, target):
        if self.m_target != target:
            self.m_target = target
            self.targetChanged.emit()

    def getRadius(self):
        return self.m_radius

    def setRadius(self, radius):
        if not QtCore.qFuzzyCompare(self.m_radius, radius):
            self.m_radius = radius
            self.updateMatrix()
            self.radiusChanged.emit()

    def getAngle(self):
        return self.m_angle

    def setAngle(self, angle):
        if not QtCore.qFuzzyCompare(angle, self.m_angle):
            self.m_angle = angle
            self.updateMatrix()
            self.angleChanged.emit()

    def updateMatrix(self):
        self.m_matrix.setToIdentity()
        self.m_matrix.rotate(self.m_angle, QVector3D(0, 1, 0))
        self.m_matrix.translate(self.m_radius, 0, 0)
        self.m_target.setMatrix(self.m_matrix)

    # QSignal
    targetChanged = pyqtSignal()
    radiusChanged = pyqtSignal()
    angleChanged = pyqtSignal()

    # Qt properties
    target = pyqtProperty(QTransform, fget=getTarget, fset=setTarget)
    radius = pyqtProperty(float, fget=getRadius, fset=setRadius)
    angle = pyqtProperty(float, fget=getAngle, fset=setAngle)

class demo_Scene():
    def __init__(self):
        self.rootEntity = QEntity()
        self.material = QPhongMaterial(self.rootEntity)
        self.childEntity = QEntity(self.rootEntity)

        #sphere
        self.mesh = QMesh()
        url = QUrl()
        url.setScheme("file")
        url.setPath("../data/mp_facegeometry.obj")
        self.mesh.setSource(url)

    def createScene(self):
        objectTransform = QTransform()
        controller = OrbitTransformController(objectTransform)
        controller.setTarget(objectTransform)

        self.childEntity.addComponent(self.mesh)
        self.childEntity.addComponent(objectTransform)
        self.childEntity.addComponent(self.material)

        return self.rootEntity

class contained3dWindow(QWidget):
    def __init__(self):
        super(contained3dWindow, self).__init__()
        self.setGeometry(0,0,820,820)
        lay = QVBoxLayout(self)

        self.view = Qt3DWindow()

        container = QWidget.createWindowContainer(self.view)
        container.setMaximumSize(800,800)
        lay.addWidget(container)

        demoScene = demo_Scene()
        demoEntity = demoScene.createScene()
        self.rootEntity = demoEntity

        camera = self.view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
        camera.setPosition(QVector3D(0, 0, 40.0))
        camera.setViewCenter(QVector3D(0, 0, 0))
        camController = QFirstPersonCameraController(self.rootEntity)
        camController.setCamera(camera)
        
        self.view.setRootEntity(self.rootEntity)

if __name__ == "__main__":
    import sys

    App = QApplication(sys.argv)
    Root = contained3dWindow()
    Root.show()
    sys.exit(App.exec_())