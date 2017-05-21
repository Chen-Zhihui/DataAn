

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from .Views import *
from .Sessions import *


class VolSession(SessionBase):
    def __init__(self):
        super().__init__()
        self.data = None

        self.imax = 0
        self.imin = 0
        self.jmax = 0
        self.jmin = 0
        self.kmax = 0
        self.kmin = 0

        self.i = 0
        self.j = 0
        self.k = 0

        self.iAct = QtGui.QAction("I", self)
        self.jAct = QtGui.QAction("J", self)
        self.kAct = QtGui.QAction("K", self)

        self.acts = [self.iAct, self.jAct, self.kAct]

        for act in self.acts:
            act.setCheckable(True)
            act.setChecked(False)

        self.iview = None
        self.jview = None
        self.kview = None

        self.iAct.toggled.connect(self.showIView)
        self.jAct.toggled.connect(self.showJView)
        self.kAct.toggled.connect(self.showKView)

    def openFile(self, file):
        import nrrd
        readdata, options = nrrd.read(file)
        sizes = list(readdata.shape)
        print(readdata.shape)
        print(options)
        print(len(sizes))

        if len(sizes) == 2:
            return False

        if len(sizes) == 4:
            self.data = readdata[0, :, :, :]
            self.imax = sizes[3]
            self.jmax = sizes[2]
            self.kmax = sizes[1]

        if len(sizes) == 3:
            self.data = readdata[:, :, :]
            self.imax = sizes[2]
            self.jmax = sizes[1]
            self.kmax = sizes[0]

        self.imax = self.imax-1
        self.jmax = self.jmax-1
        self.kmax = self.kmax-1

        self.imin = 0
        self.jmin = 0
        self.kmin = 0

        self.i = int(self.imax/2)
        self.j = int(self.jmax/2)
        self.k = int(self.kmax/2)

        #self.imax = 128
        #self.jmax = 256
        #self.kmax = 196

        #x1 = np.linspace(-30, 10, self.imax)[:, np.newaxis, np.newaxis]
        #x2 = np.linspace(-20, 20, self.imax)[:, np.newaxis, np.newaxis]
        #y = np.linspace(-30, 10, self.jmax)[np.newaxis, :, np.newaxis]
        #z = np.linspace(-20, 20, self.kmax)[np.newaxis, np.newaxis, :]
        #d1 = np.sqrt(x1 ** 2 + y ** 2 + z ** 2)
        #d2 = 2 * np.sqrt(x1[::-1] ** 2 + y ** 2 + z ** 2)
        #d3 = 4 * np.sqrt(x2 ** 2 + y[:, ::-1] ** 2 + z ** 2)
        #self.data = (np.sin(d1) / d1 ** 2) + (np.sin(d2) / d2 ** 2) + (np.sin(d3) / d3 ** 2)

        self.showIView(True)
        self.showJView(True)
        self.showKView(True)

        desk = QtGui.QGuiApplication.primaryScreen()
        rect = desk.size()
        w = rect.width()/2 - 40
        h = rect.height()/2 - 40

        self.kview.move(w, 60)
        self.iview.move(0, h+20)
        self.jview.move(w, h+20)

        for v in self.views:
            v.setWindowTitle(file)
            v.resize(w,h)
            v.show()

        self.name = file
        self.hightLight(True)

        return True

    def roiChanged(self):
        # if has his win, show

        #y, x = self.container.hist()
        pass

    def hightLight(self, hig = True):
        for v in self.views:
            if hig :
                v.setWindowTitle("[" + self.name + "]")
            else :
                v.setWindowTitle(self.name)

    def updateIJK(self, i, j, k):
        self.i =i
        self.j =j
        self.k =k
        if self.iview is not None :
            self.iview.updateCW(j,k)
        if self.jview is not None :
            self.jview.updateCW(k,i)
        if self.kview is not None :
            self.kview.updateCW(i,j)

    def showIView(self, show):
        if self.iview is None and show:
            self.iview = ImageView()
            self.iview.session = self
            self.views.append(self.iview)
            self.iview.setImageData(self.data[:, :, self.i])

            self.iview.act = self.iAct
            for act in self.acts:
                self.iview.toolbar.addAction(act)
            self.iAct.setChecked(True)

            self.iview.slider = QtGui.QSlider(self.iview.toolbar)
            self.iview.slider.setOrientation(QtCore.Qt.Horizontal)
            self.iview.slider.setRange(self.imin, self.imax)
            self.iview.slider.setValue(self.i)
            self.iview.toolbar.addWidget(self.iview.slider)
            def sliderMoved(v) :
                self.iview.setImageData(self.data[v, :, :])
            self.iview.slider.sliderMoved.connect(sliderMoved)

            def mouseMoved(evt) :
                if self.iview.plot.sceneBoundingRect().contains(evt) :
                    pos = self.iview.vb.mapSceneToView(evt)
                    self.updateIJK(self.i, pos.x(), pos.y())
            self.iview.plot.scene().sigMouseMoved.connect(mouseMoved)

            return

        if self.iview is not None and show:
            self.iview.show()
            return

        if not show :
            if self.iview is None :
                pass
            else :
                self.iview.close()


    def showJView(self, show):
        if self.jview is None and show:
            self.jview = ImageView()
            self.jview.session = self
            self.views.append(self.jview)
            self.jview.setImageData(self.data[:, self.j, :])

            self.jview.act = self.jAct
            for act in self.acts:
                self.jview.toolbar.addAction(act)
            self.jAct.setChecked(True)

            self.jview.slider = QtGui.QSlider(self.jview.toolbar)
            self.jview.slider.setOrientation(QtCore.Qt.Horizontal)
            self.jview.slider.setRange(self.jmin, self.jmax)
            self.jview.slider.setValue(self.j)
            self.jview.toolbar.addWidget(self.jview.slider)
            def sliderMoved(v) :
                self.jview.setImageData(self.data[:, v, :])
            self.jview.slider.sliderMoved.connect(sliderMoved)

            def mouseMoved(evt) :
                if self.jview.plot.sceneBoundingRect().contains(evt) :
                    pos = self.jview.vb.mapSceneToView(evt)
                    self.updateIJK(pos.y(), self.j, pos.x())
            self.jview.plot.scene().sigMouseMoved.connect(mouseMoved)

            return

        if self.jview is not None and show:
            self.jview.show()
            return

        if not show:
            if self.jview is None:
                pass
            else:
                self.jview.close()

    def showKView(self, show):
        if self.kview is None and show:
            self.kview = ImageView()
            self.kview.session = self
            self.views.append(self.kview)
            self.kview.setImageData(self.data[self.k, :, :])

            self.kview.act = self.kAct
            for act in self.acts:
                self.kview.toolbar.addAction(act)
            self.kAct.setChecked(True)

            self.kview.slider = QtGui.QSlider(self.kview.toolbar)
            self.kview.slider.setOrientation(QtCore.Qt.Horizontal)
            self.kview.slider.setRange(self.kmin, self.kmax)
            self.kview.slider.setValue(self.k)
            self.kview.toolbar.addWidget(self.kview.slider)
            def sliderMoved(v) :
                self.kview.setImageData(self.data[v, :, :])
            self.kview.slider.sliderMoved.connect(sliderMoved)

            def mouseMoved(evt) :
                if self.kview.plot.sceneBoundingRect().contains(evt) :
                    pos = self.kview.vb.mapSceneToView(evt)
                    self.updateIJK(pos.x(), pos.y(),self.k)
            self.kview.plot.scene().sigMouseMoved.connect(mouseMoved)

            return

        if self.kview is not None and show:
            self.kview.show()
            return

        if not show:
            if self.kview is None:
                pass
            else:
                self.kview.close()

    def closeView(self, view):
        view.act.setChecked(False)
        if view.act is self.iAct:
            self.iView = None
        if view.act is self.jAct:
            self.jView = None
        if view.act is self.kAct:
            self.kView = None

        super().closeView( view)
