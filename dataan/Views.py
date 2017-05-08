

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


class ViewMngr(object) :
    """
    view manager
    which one is the current view
    """

    class EventEator(QtCore.QObject):
        def eventFilter(self, obj, evnt):
            if isinstance(evnt, (QtGui.QFocusEvent, QtGui.QCloseEvent)):
                t = self.target(obj)
                if t is not None:
                    if isinstance(evnt, QtGui.QCloseEvent):
                        t = None
                    ViewMngr.instance().resetCurrentView(t)

            return super().eventFilter(obj,evnt)

        def target(self, obj):
            if not isinstance(obj, QtGui.QWidget):
                return None

            pw = obj
            while pw is not None:
                if isinstance(pw, ViewBase):
                    return pw
                pw = pw.parentWidget()
            return None

    def __init__(self):
        self.eator = ViewMngr.EventEator()
        QtGui.QGuiApplication.instance().installEventFilter(self.eator)

        self.current = None

    @classmethod
    def currentViewBase(cls):
        widget = QtGui.QGuiApplication.instance().activeWindow()
        if isinstance(widget, ViewBase) :
            return widget
        else:
            parent = widget.parentWidget()
            while parent is not None:
                if isinstance(parent, ViewBase):
                    return parent
                parent = parent.parentWidget()
            return None

    def resetCurrentView(self, new):
        #old.setWindowTitle("old")
        if new is None:
            self.current = None
        else :
            self.current = new
            new.hitIt()

        if isinstance(self.current, ImageView) :
            y, x = self.current.hist()
            HistView.updateHist(x,y)

        if self.current is None:
            HistView.updateHist(None, None)


    def currentImageView(self):
        if isinstance(self.current, ImageView):
            return self.current
        else:
            return None

    def currentView(self):
        return self.current

    @classmethod
    def instance(cls):
        global view_mngr
        if view_mngr is None:
            view_mngr = ViewMngr()
        return view_mngr

view_mngr = None #ViewMngr()


class ViewBase(QtGui.QMainWindow) :
    def __init__(self):
        super().__init__()
        super().setMouseTracking(False)
        self.toolbar = QtGui.QToolBar()
        super().addToolBar(self.toolbar)
        self.session = None

    def closeEvent(self, event):
        if self.session is not None :
            self.session.closeView(self)
        super().closeEvent(event)
        self.session = None

    def hitIt(self):
        self.session.hitIt()


class ImageView(ViewBase):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon("icons/image.png"))

        self.view = pg.GraphicsLayoutWidget()
        self.view.setParent(self)
        self.setCentralWidget(self.view)

        self.img = pg.ImageItem()
        self.data = None
        self.rois = set()
        self.currentRoi = None
        self.plot = self.view.addPlot()
        self.plot.addItem(self.img)

        rect = self.toolbar.addAction("Roi")
        rect.setIcon(QtGui.QIcon("icons/rect.png"))
        rect.triggered.connect(self.addRect)

        clear = self.toolbar.addAction("Clear")
        clear.setIcon(QtGui.QIcon("icons/clear.png"))
        clear.triggered.connect(self.clear)


    def setImageData(self, data):
        self.data = data
        self.img.setImage(self.data)

    def addRect(self):
        if self.currentRoi is not None:
            return

        geo = self.plot.getViewBox().viewRange()
        xlen = geo[0][1]-geo[0][0]
        ylen = geo[1][1]-geo[1][0]
        ratio = 0.5
        xmin = geo[0][0] + xlen * ratio * 0.5
        xmax = geo[0][1] - xlen * ratio #* 0.5

        ymin = geo[1][0] + ylen * ratio * 0.5
        ymax = geo[1][1] - ylen * ratio #* 0.5

        # Custom ROI for selecting an image region
        roi = pg.ROI([xmin, ymin], [xmax, ymax])
        roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        roi.setZValue(10)  # make sure ROI is drawn above image
        self.plot.addItem(roi)
        self.rois.add(roi)
        self.currentRoi = roi

        roi.sigRegionChanged.connect(self.updateHist)
        #roi.sigRegionChangeFinished.connect(self.updateHist)
        self.updateHist()


    def hist(self):
        if self.currentRoi is not None:
            selected = self.currentRoi.getArrayRegion(self.data, self.img)
        else :
            selected = self.data
        y, x = np.histogram(selected, bins=np.linspace(-10, 300, 200))
        return y,x

    def updateHist(self):
        if HistView.instance() is not None:
            y,x = self.hist()
            HistView.updateHist(x, y)

    def clear(self):
        self.plot.removeItem(self.currentRoi)
        del self.currentRoi
        self.currentRoi = None
        map(lambda x : self.plot.removeItem(x), self.rois)
        self.rois.clear()
        self.updateHist()


class HistView(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = pg.PlotWidget()
        self.setCentralWidget(self.widget)
        self.setWindowTitle("Histogram")
        self.setWindowIcon(QtGui.QIcon("icons/histogram.png"))

    def plot(self, x, y):
        if x is None:
            return
        if y is None:
            return
        self.widget.plotItem.clear()
        self.widget.getPlotItem().plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))

    def closeEvent(self, envt):
        global hist_view
        hist_view = None
        super().closeEvent(envt)

    @classmethod
    def updateHist(cls, x, y ):
        view = HistView.instance()
        if view is not None:
            view.plot(x,y)

    @classmethod
    def create(cls):
        global hist_view
        if hist_view is None:
            hist_view = HistView()
            hist_view.show()


    @classmethod
    def instance(cls):
        global hist_view
        return hist_view

hist_view = None