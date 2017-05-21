

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from .Views import *
from .SessionBase import *


class ImageSession(SessionBase):
    def __init__(self):
        super().__init__()
        self.data = None
        self.container=ImageView()
        self.container.session = self
        self.views.append(self.container)

    def openFile(self, file):
        from scipy.misc import imread
        self.data = imread(file)
        self.image_data = self.data
        self.data = self.data[:, :, 0]
        self.container.setImageData(self.data)
        self.container.setWindowTitle(file)
        self.container.show()
        self.name = file
        self.hightLight(True)
        return True

    def roiChanged(self):
        # if has his win, show

        #y, x = self.container.hist()
        pass

    def hightLight(self, hig = True):
        if hig :
            self.container.setWindowTitle("["+self.name+"]")
        else :
            self.container.setWindowTitle(self.name)



class EditSession(SessionBase):
    def __init__(self):
        super().__init__()
        self.view = QtGui.QTextEdit()
        self.container = ViewBase()
        self.container.resize(800, 600)
        self.container.setWindowIcon(QtGui.QIcon("icons/text.png"))
        self.container.setCentralWidget(self.view)
        self.view.setParent(self.container)
        self.container.session = self
        self.views.append(self.container)

    def openFile(self, file):
        self.view.clear()
        text = QtCore.QF;ile(file)
        text.open(QtCore.QFile.ReadOnly)
        text = text.readAll()
        self.view.setText(str(text))
        self.container.setWindowTitle(file)
        self.container.show()
        self.name = file
        self.hightLight(True)
        return True

    def save(self):
        file, filter = QtGui.QFileDialog.getSaveFileName()
        if file is None :
            return

        text = self.view.text()
        f = QtCore.QFile(file)
        f.open(QtCore.QFile.WriteOnly)
        f.write(text)

    def hightLight(self, hig = True):
        if hig :
            self.container.setWindowTitle("["+self.name+"]")
        else :
            self.container.setWindowTitle(self.name)

