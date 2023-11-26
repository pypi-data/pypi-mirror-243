import numpy as np
import matplotlib.pylab as plt
from PIL import Image as im
from scipy.signal import fftconvolve
from .propagacion import propLuz

class formIm(propLuz):
    '''
    This is a description of MyClass.
   
   Args:
       tipo (str): The name of the instance.
       age (int): The age of the instance.
    '''
    def __init__(self,Lado:int,Nmuestras:int,radiox:float,campo:list,\
                 lamb:float,distancia:float,tipo:str,ruta:str,radioy:float=False):
        propLuz.__init__(self,Lado,Nmuestras,radiox,campo,\
                 lamb,distancia,tipo,radioy) 
        self.path = ruta

    def Im(self):
        I = np.array(im.open(self.path))
        I = np.array(I[:,:,0])
        return I

    def conv(self):
        psf = self.prop()[0]
        ipsf = abs(psf)**2
        conv = fftconvolve(self.Im(),ipsf)
        return conv
    
    def plotConv(self):
        fig,axs = plt.subplots( nrows=1,ncols=2)
        fig.suptitle('Imaging Simulation')
        axs[0].set(title='Original Image',xlabel='x(m)',ylabel='y (m)')
        axs[0].imshow(self.Im(),cmap='gray')
        axs[1].set(title=f'Simulated Imaging at z = {self.z}m',xlabel='x(m)',ylabel='y (m)')
        axs[1].imshow(self.conv(),cmap='gray')
        plt.show()
