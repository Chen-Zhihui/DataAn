

from pyqtgraph.Qt import QtGui

from .ImageSession import ImageSession
from .VolSession import VolSession
from .EditSession import EditSession

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
        nrrdExt = ["nrrd"]
        sess_dict = {ext : se for ext, se
                     in chain(zip(imageExt, map(lambda x : ImageSession, imageExt)),
                              zip(txtExt, map( lambda x : EditSession, txtExt)),
                              zip(nrrdExt, map(lambda x: VolSession, nrrdExt)))}

        def compose(title, extensions):
            return title + " (" + " ".join(map(lambda e : "*."+e, extensions))+")"

        filter = (";;").join([compose("Images", imageExt),
                              compose("Text", txtExt),
                              compose("Nrrd", nrrdExt)])
        file, filter = QtGui.QFileDialog.getOpenFileName(None,"Open file", None, filter)
        if file is None :
            return
        if file == "" :
            return

#        file, filter = QtGui.QFileDialog.getOpenFileName(None,"Open file", None,
#                                                         "Images (*.png *.xpm *.jpg);;"
#                                                         "Text files (*.txt);;"
#                                                         "XML files (*.xml)")
        #reg = r".*\((\*\.[0-9A-Za-z]*)( \*\.[0-9A-Za-z]*)*\)"
        fnreg = r".*\.([0-9A-Za-z]*)"
        import re
        ext = re.match(fnreg, file).group(1)
        s = sess_dict[ext]()
        s.mngr = self
        self.addSession(s)
        ret = s.openFile(file)
        if not ret:
            QtGui.QMessageBox.information(None, "Error", "Error")

    @classmethod
    def instance(cls):
        global session_mngr
        return session_mngr


session_mngr = SessionMngr()