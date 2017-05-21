

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
        self.container.setImageData(self.image_data)
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





