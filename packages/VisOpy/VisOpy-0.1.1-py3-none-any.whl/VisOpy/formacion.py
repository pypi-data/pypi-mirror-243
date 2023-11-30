import numpy as np
import matplotlib.pylab as plt
from PIL import Image as im
from scipy.signal import fftconvolve
from .propagacion import propLuz

class formIm(propLuz):
    '''
    Clase que simula la imagen formada por un sistema dado:
    Lado: Longitud de lado del espacio, float
    Nmuestras: Número de muestras, int
    radiox: semiancho en x de la abertura, float
    radioy: semiancho en y de la abertura (opcional), float
    Campo: lista que contiene: [abertura,fase,set,abe,abset]
        abertura: tipo de abertura 'circle' o 'rectangle', str
        fase: tipo de fase 'tilt','focus' o una función de (rho,theta) personalizada
        set: características de la fase. Para 'tilt' es un arreglo de dos elementos [theta,alpha]
            para 'focus' es un float que indica la longitud de enfoque.
        abe: booleano que indica si se consideran o no aberraciones
        abset: arreglo de dos filas, la primera contiene los grados de las aberraciones y la segunda
            los coeficientes de las aberraciones
    lamb: longitud de onda, float 
    distancia: distancia de propagación, float
    tipo: tipo de propagador, 'Fresnel' o 'Fraunhofer', str
    ruta: ruta a la imagen ubicada en el plano objeto, str.
    '''
    def __init__(self,Lado:int,Nmuestras:int,radiox:float,campo:list,\
                 lamb:float,distancia:float,tipo:str,ruta:str,radioy:float=False):
        propLuz.__init__(self,Lado,Nmuestras,radiox,campo,\
                 lamb,distancia,tipo,radioy) 
        self.path = ruta

    def Im(self):   # se lee la imagen original
        I = np.array(im.open(self.path))
        I = np.array(I[:,:,0])
        return I

    def conv(self):     # se convoluciona la imagen con la psf
        psf = self.prop()[0]
        ipsf = abs(psf)**2
        conv = fftconvolve(self.Im(),ipsf)
        return conv
    
    def plotConv(self):    # se grafica la imagen original y la imagen formada
        fig,axs = plt.subplots( nrows=1,ncols=2)
        fig.suptitle('Imaging Simulation')
        axs[0].set(title='Original Image',xlabel='x(m)',ylabel='y (m)')
        axs[0].imshow(self.Im(),cmap='gray')
        axs[1].set(title=f'Simulated Imaging at z = {self.z}m',xlabel='x(m)',ylabel='y (m)')
        axs[1].imshow(self.conv(),cmap='gray')
        plt.show()
