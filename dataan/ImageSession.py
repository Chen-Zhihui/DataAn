


from .Views import ImageView
from .SessionBase import SessionBase
from PIL import Image
import numpy as np
from pyqtgraph.Qt import QtGui

class ImageSession(SessionBase):
    def __init__(self):
        super().__init__()
        self.data = None
        self.container=ImageView()
        self.container.session = self
        self.views.append(self.container)
        
        hand = QtGui.QAction(QtGui.QIcon("icons/view-top.svg"),"K", self)
        hand.triggered.connect(self.handStrock)
        self.container.toolbar.addAction(hand)

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
    
    def handStrock(self, b):
        a = np.asarray(Image.open(self.name).convert('L')).astype('float')
        depth = 10. 					#(0-100)
        grad = np.gradient(a)				#取图像灰度的梯度值
        grad_x, grad_y = grad 				#分别取横纵图像梯度值
        grad_x = grad_x*depth/100.
        grad_y = grad_y*depth/100.
        A = np.sqrt(grad_x**2 + grad_y**2 + 1.)
        uni_x = grad_x/A
        uni_y = grad_y/A
        uni_z = 1./A
        
        vec_el = np.pi/2.2 			        #光源的俯视角度，弧度值
        vec_az = np.pi/4. 			        #光源的方位角度，弧度值
        dx = np.cos(vec_el)*np.cos(vec_az) 	        #光源对x 轴的影响
        dy = np.cos(vec_el)*np.sin(vec_az) 	        #光源对y 轴的影响
        dz = np.sin(vec_el) 			        #光源对z 轴的影响
        
        b = 255*(dx*uni_x + dy*uni_y + dz*uni_z) 	#光源归一化
        b = b.clip(0,255)
        
        hand = ImageView()
        hand.setImageData(b)
        self.views.append(hand)
        hand.show()
        

    def hightLight(self, hig = True):
        if hig :
            self.container.setWindowTitle("["+self.name+"]")
        else :
            self.container.setWindowTitle(self.name)





