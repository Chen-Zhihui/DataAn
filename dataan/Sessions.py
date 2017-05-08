

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

from .Views import *

class SessionBase(object) :
    def __init__(self):
        self.mngr = None
        self.views = []
        self.name = str()

    def closeView(self, view):
        #find, erase, if empty remove me
        if view in self.views:
            self.views.remove(view)
            #print("view removed")

        if len(self.views) > 0:
            #print("self.views.ln")
            #print(len(self.views))
            return

        if self.mngr is not None :
            self.mngr.remSession(self)

    def hitIt(self):
        self.mngr.setCurrent(self)
        print(self.name)

    def hightLight(self, hig = True):
        pass


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
        return

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
        text = QtCore.QFile(file)
        text.open(QtCore.QFile.ReadOnly)
        text = text.readAll()
        self.view.setText(str(text))
        self.container.setWindowTitle(file)
        self.container.show()
        self.name = file
        self.hightLight(True)

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


class SessionMngr(object) :

    def __init__(self):
        self.sessions = set()
        self.current = None

    def addSession(self, session):
        if session in self.sessions :
            return
        self.sessions.add(session)
        self.setCurrent(session)

    def remSession(self, session):
        if session in self.sessions :
            self.sessions.remove(session)
            print("Session removed")
            if session is self.current :
                self.setCurrent(None)

    def setCurrent(self, ses):
        if ses is self.current:
            return

        old = self.current

        if ses is None:
            if len(self.sessions) > 0 :
                sl = list(self.sessions)
                self.current = sl[0]
            else:
                self.current = None
            return
        else:
            self.current = ses
            if ses not in self.sessions:
                self.sessions.add(ses)

        if self.current is not None :
            self.current.hightLight(True)

        if old is not None:
            old.hightLight(False)


    def getCurrent(self):
        return self.current

    def openFile(self):
        """
        todo: open file accr to file extension
        :return: 
        """
        from itertools import chain
        sess_dict = dict()
        imageExt = ["png", "jpg", "xpm"]
        txtExt = ["txt", "py"]
        sess_dict = {ext : se for ext, se in chain(zip(imageExt, map(lambda x : ImageSession, imageExt)),
                                                   zip(txtExt, map( lambda x : EditSession, txtExt)))}

        def compose(title, extensions):
            return title + " (" + " ".join(map(lambda e : "*."+e, extensions))+")"

        filter = (";;").join([compose("Images", imageExt), compose("Text", txtExt)])
        file, filter = QtGui.QFileDialog.getOpenFileName(None,"Open file", None, filter)
        if file is None :
            return
        if file == "" :
            return

#        file, filter = QtGui.QFileDialog.getOpenFileName(None,"Open file", None,
#                                                         "Images (*.png *.xpm *.jpg);;"
#                                                         "Text files (*.txt);;"
#                                                         "XML files (*.xml)")
        reg = r".*\((\*\.[0-9A-Za-z]*)( \*\.[0-9A-Za-z]*)*\)"
        fnreg = r".*\.([0-9A-Za-z]*)"
        import re
        ext = re.match(fnreg, file).group(1)
        s = sess_dict[ext]()
        s.mngr = self
        self.addSession(s)
        s.openFile(file)

    @classmethod
    def instance(cls):
        global session_mngr
        return session_mngr


session_mngr = SessionMngr()