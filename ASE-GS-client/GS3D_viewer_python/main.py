from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtOpenGL import *
from PyQt5.QtCore import *
import time
import numpy as np
import math
import socket
import json
import threading


class QTGLWidget2(QGLWidget):
    
    xr = 50.0
    yr = 50.0
    zr = 50.0

    viewLon = 45.0
    viewLat = 45.0
    viewRds = 50.0

    yaw = 0.0
    pitch = 0.0
    roll = 0.0

    move = 1.0
    r = 0
    t = 0
    byouga = 0.0

    x_unit = np.array([1.0,0.0,0.0])
    y_unit = np.array([0.0,1.0,0.0])
    z_unit = np.array([0.0,0.0,-1.0])

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(300, 300)

        f = open('CubeSat-edu2-convert.STL', 'r', encoding='UTF-8')
        self.datalist = f.readlines()
        f.close()

        self.thread1 = threading.Thread(target=self.tuusinLoop)
        self.thread1.start()

        self.polygon = []
        self.polynum = int((len(self.datalist)-2)/7)
        for i in range(self.polynum):
            n = self.datalist[i * 7 + 1].split()[2:]
            a = self.datalist[i * 7 + 3].split()[1:]
            b = self.datalist[i * 7 + 4].split()[1:]
            c = self.datalist[i * 7 + 5].split()[1:]
            self.polygon.append([[float(n[0]),float(n[1]),float(n[2])],[float(a[0]),float(a[1]),float(a[2])],
            [float(b[0]),float(b[1]),float(b[2])],[float(c[0]),float(c[1]),float(c[2])]])
    
    def __del__(self):
        self.thread1.raise_exception()

    def paintGL(self):
        t2 = time.time()

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(self.xr, self.yr, self.zr, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

        glLight(GL_LIGHT0, GL_POSITION, [self.xr, self.yr, self.zr, 1.0])

        glDisable(GL_LIGHTING)

        glLineWidth(5)
        glBegin(GL_LINES)
        glColor(0.5,0.5,0.5,0.7)
        k = 100
        glVertex(k, 0, 0)
        glVertex(-k, 0, 0)
        glVertex(0, k, 0)
        glVertex(0, -k, 0)
        glVertex(0, 0, k)
        glVertex(0, 0, -k)
        glEnd()

        aL = 15
        self.drawArrow(0, 0, 0, aL*self.x_unit[0], aL*self.x_unit[1], aL*self.x_unit[2], 0.5, 0, 0)
        self.drawArrow(0, 0, 0, aL*self.y_unit[0], aL*self.y_unit[1], aL*self.y_unit[2], 0, 0.5, 0)
        self.drawArrow(0, 0, 0, aL*self.z_unit[0], aL*self.z_unit[1], aL*self.z_unit[2], 0, 0, 0.5)

        aL = 20
        glPushMatrix()
        glRotate(self.yaw, 0, 0, 1)
        glRotate(-self.pitch, 0, 1, 0)
        glRotate(-self.roll, 1, 0, 0)
        self.drawArrow(0, 0, 0, aL*self.x_unit[0], aL*self.x_unit[1], aL*self.x_unit[2], 1, 0, 0)
        self.drawArrow(0, 0, 0, aL*self.y_unit[0], aL*self.y_unit[1], aL*self.y_unit[2], 0, 1, 0)
        self.drawArrow(0, 0, 0, aL*self.z_unit[0], aL*self.z_unit[1], aL*self.z_unit[2], 0, 0, 1)

        glEnable(GL_LIGHTING)
        
        glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

        glLineWidth(1)
        glBegin(GL_TRIANGLES)
        for i in range(self.polynum):
            #glColor(1.0, 0.5, 0.5, 0.3)
            glNormal(self.polygon[i][0][0], self.polygon[i][0][1], self.polygon[i][0][2])
            glVertex(self.polygon[i][1][0], self.polygon[i][1][1], self.polygon[i][1][2])
            glVertex(self.polygon[i][2][0], self.polygon[i][2][1], self.polygon[i][2][2])
            glVertex(self.polygon[i][3][0], self.polygon[i][3][1], self.polygon[i][3][2])
        glEnd()

        glDisable(GL_LIGHTING)

        glPopMatrix()

        glFlush()

        self.byouga = time.time() - t2
    
    def drawArrow(self, x1, y1, z1, x2, y2, z2, r, g, b):
        arrowLength = 3
        arrowAngle = 0.4
        phi = -math.atan2(y2-y1, x2-x1)
        theta = 0.5*math.pi - math.atan2(z2-z1, x2-x1)

        glLineWidth(10)
        glBegin(GL_LINES)
        glColor(r,g,b,1.0)
        glVertex(x1,y1,z1)
        glVertex(x2,y2,z2)
        glEnd()

        glPushMatrix()
        glTranslate(x2, y2, z2)
        glRotate(math.degrees(theta), 0, 1, 0)
        glRotate(math.degrees(phi), 1, 0, 0)
        self.drawCone(arrowLength, arrowLength*math.sin(arrowAngle), r, g, b)
        glPopMatrix()
    
    def drawCone(self, L, radius, r, g, b):
        glTranslate(0, 0, L)
        glBegin(GL_POLYGON)
        glColor(r, g, b)
        glVertex(0, 0, -L)
        i = 0.0
        while (i<2*math.pi):
            x = radius * math.cos(i)
            y = radius * math.sin(i)
            glVertex(x, y, -L)
            i += 0.01
        glEnd()

        j = 0.0
        glBegin(GL_POLYGON)
        glColor(r, g, b)
        glVertex(0, 0, 0)
        while (j<2*math.pi):
            x = radius * math.cos(j)
            y = radius * math.sin(j)
            glVertex(x, y, -L)
            j += 0.01
        glEnd()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(30.0, w/h, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
    
    def initializeGL(self):
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_LIGHT0)
        glLight(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
        glLight(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 0.01, 3000.0)
    
    def calcViewPos(self):
        self.zr = self.viewRds * math.sin(math.radians(self.viewLat))
        viewRdsCos = self.viewRds * math.cos(math.radians(self.viewLat))
        self.xr = viewRdsCos * math.cos(math.radians(self.viewLon))
        self.yr = viewRdsCos * math.sin(math.radians(self.viewLon))
        
    def chcord_xp(self):
        self.viewLon += self.move
        self.calcViewPos()
        self.updateGL()

    def chcord_yp(self):
        self.viewLat += self.move
        self.calcViewPos()
        self.updateGL()

    def chcord_zp(self):
        self.viewRds += self.move
        self.calcViewPos()
        self.updateGL()
    
    def chcord_xm(self):
        self.viewLon += -self.move
        self.calcViewPos()
        self.updateGL()
    
    def chcord_ym(self):
        self.viewLat += -self.move
        self.calcViewPos()
        self.updateGL()
    
    def chcord_zm(self):
        self.viewRds += -self.move
        self.calcViewPos()
        self.updateGL()

    def chcord_rst(self):
        self.viewRds = 50.0
        self.viewLat = 45.0
        self.viewLon = 45.0
        self.calcViewPos()
        self.updateGL()

    def eventLoop(self):
        dt = time.time() - self.t
        self.t = time.time()
        if self.r == 0:
            self.r = 10
            print("fps: " + str(round(1 / dt, 2)))
            print("描画時間: " + str(round(self.byouga, 2)))
        else:
            self.r -= 1
        self.calcViewPos()
        self.updateGL()
    
    def tuusinLoop(self):
        host = socket.gethostbyname(socket.gethostname())
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((host,10002))
        while True:
            try:
                data = client.recv(1024).decode('UTF-8')
                tuusinData = json.loads(data)
                self.yaw = float(tuusinData["euler_angle"]["yaw"])
                self.pitch = float(tuusinData["euler_angle"]["pitch"])
                self.roll = float(tuusinData["euler_angle"]["roll"])
            except:
                time.sleep(0.5)


class QTWidget(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.gl = QTGLWidget2(self)
        cb = QtWidgets.QPushButton('Close', self)
        cb.clicked.connect(QtWidgets.qApp.quit)
        xp = QtWidgets.QPushButton('X+', self)
        xp.clicked.connect(self.gl.chcord_xp)
        yp = QtWidgets.QPushButton('Y+', self)
        yp.clicked.connect(self.gl.chcord_yp)
        zp = QtWidgets.QPushButton('Z+', self)
        zp.clicked.connect(self.gl.chcord_zp)
        xm = QtWidgets.QPushButton('X-', self)
        xm.clicked.connect(self.gl.chcord_xm)
        ym = QtWidgets.QPushButton('Y-', self)
        ym.clicked.connect(self.gl.chcord_ym)
        zm = QtWidgets.QPushButton('Z-', self)
        zm.clicked.connect(self.gl.chcord_zm)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(cb)
        hbox.addWidget(xp)
        hbox.addWidget(yp)
        hbox.addWidget(zp)
        hbox.addWidget(xm)
        hbox.addWidget(ym)
        hbox.addWidget(zm)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.gl)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(300, 350)

        self.timer = QTimer()
        self.timer.timeout.connect(self.gl.eventLoop)
        self.timer.start(100)

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_W):
            self.gl.chcord_yp()
        if (event.key() == Qt.Key_D):
            self.gl.chcord_xp()
        if (event.key() == Qt.Key_S):
            self.gl.chcord_ym()
        if (event.key() == Qt.Key_A):
            self.gl.chcord_xm()
        if (event.key() == Qt.Key_Q):
            self.gl.chcord_zp()
        if (event.key() == Qt.Key_Z):
            self.gl.chcord_zm()
        if (event.key() == Qt.Key_R):
            self.gl.chcord_rst()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = QTWidget()
    w.setWindowTitle('PyQt OpenGL 2')
    try:
        w.show()
    except:
        w.gl.__del__()
    sys.exit(app.exec_())
