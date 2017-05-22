
from pyqtgraph.Qt import QtCore

class SessionBase(QtCore.QObject) :
    def __init__(self):
        super().__init__()
        self.mngr = None
        self.views = []
        self.name = str()

    def closeView(self, view):
        #find, erase, if empty remove me
        if view in self.views:
            self.views.remove(view)
            print("view removed")


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
