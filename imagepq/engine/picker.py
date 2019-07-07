#%%
from pyqtgraph.Qt import QtCore, QtGui
import collections

Event = collections.namedtuple('MEvent', 'index type x y')


def idle(start) :

    def empty() :
        while True:
            me = (yield)
            start += 1
            yield [(start, me)]

    return empty()


def line(start) :
    def gen():
        evs = []
        current = start
        while True:
            me = (yield)
            start += 1
            if len(evs) == 0 or len(evs) == 1 :
                evs.append((start, me))
            elif len(evs) == 2:
                evs.clear()
            else:
                raise RuntimeError("impossiable")

            yield evs
            
    return gen()



class Picker(object):

    """
    鼠标信息拾取器

    接收鼠标信息，转化为点击序列信息

    默认状态下
    """

    def __init__(self) :
        self.index = -1
        self.gen = idle(self.index)

    def onev(self, mouse_event) :
        self.index += 1
        self.gen.send(mouse_event)
        return next(self.gen)

    def clear(self):
        del self.gen 
        self.gen = idle(self.index)

    def setLine(self) :
        del self.gen
        self.gen = line(self.index)