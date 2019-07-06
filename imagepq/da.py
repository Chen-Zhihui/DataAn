# -*- coding: utf-8 -*-
"""
ImageAn
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from . import SessionMngr
from . import HistView
from . import ViewMngr

class ImageWin(QtGui.QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ImageAn')
        self.setWindowIcon(QtGui.QIcon("icons/image.png"))
        self.setMaximumWidth(800)
        #self.setMinimumWidth(800)
        self.setMaximumHeight(200)
        #self.setMinimumHeight(200)

        self.toolbar = QtGui.QToolBar()
        self.addToolBar(self.toolbar)

        openAct = self.toolbar.addAction("Open")
        openAct.setIcon(QtGui.QIcon("icons/open.png"))
        openAct.triggered.connect(self.openImageFile)

        showHist = self.toolbar.addAction("History")
        showHist.setIcon(QtGui.QIcon("icons/histogram.png"))
        showHist.triggered.connect(self.showHist)

    def openImageFile(self):
        SessionMngr.instance().openFile()

    def showHist(self):
        HistView.create()
        imageView = ViewMngr.instance().currentImageView()
        if imageView is not None:
            imageView.updateHist()


