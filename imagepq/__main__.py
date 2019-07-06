
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from . import SessionMngr
from . import HistView
from . import ViewMngr
from . import da
if __name__ == '__main__':
    app = pg.mkQApp()
    ViewMngr.instance()

    pg.setConfigOptions(imageAxisOrder='row-major')
    mw = da.ImageWin()
    mw.move(0,0)
    mw.resize(600, 300)
    mw.show()
    QtGui.QApplication.instance().exec_()