
from pyqtgraph.Qt import QtCore, QtGui



MENU_FILE = "menu.file"
MENU_EDIT = "menu.edit"
MENU_PROCESS = "menu.process"
MENU_ANALYZE = "menu.analyze"
MENU_PLUGINS = "menu.plugins"
MENU_WINDOW = "menu.window"
MENU_HELP = "menu.help"


class IPAction(QtGui.QAction) :
    """
    Base Action show in Menu
    """
    pass


class MenuAction(IPAction) :
    """
    Menu
    """
    pass 


class MenuMngr(object):
    """
    菜单管理器
    （1）扫描指定模块（不是目录），加载
    """

    def reg(id, name, cls) :

        pass 







