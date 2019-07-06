

from pyqtgraph.Qt import QtGui, QtCore

from .Views import ViewBase
from .SessionBase import SessionBase


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