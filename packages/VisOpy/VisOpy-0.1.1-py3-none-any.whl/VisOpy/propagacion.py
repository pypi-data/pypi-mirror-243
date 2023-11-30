import numpy as np
import matplotlib.pylab as plt
from .transmitancia import transm

class propLuz(transm):
    '''
    Clase que permite propaga un campo fuente a través de una abertura hasta una distancia, dados:
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
    '''
    
    def __init__(self,Lado:int,Nmuestras:int,radiox:float,campo:list,\
                 lamb:float,distancia:float,tipo:str,radioy:float=False):
        transm.__init__(self,Lado,Nmuestras,radiox,campo,lamb,radioy) 
        self.z = distancia
        self.tp = tipo

    def prop(self):     # propagación
        dx=self.L/self.N
        u1 = self.u11()
        k=2*np.pi/self.lamb
        if self.tp == 'Fresnel':    # propagador de Fresnel
            zc = self.L*dx / (self.lamb)
            if self.z <= zc:    
                fx=np.arange(-1/(dx*2),1/(dx*2),1/self.L)
                FX, FY = np.meshgrid(fx, fx)
                H=np.exp(-1j*np.pi*self.lamb*self.z*(FX**2+FY**2))
                H= np.fft.fftshift(H)
                U1= np.fft.fft2(np.fft.fftshift(u1))
                U2= H*U1
                u2=np.fft.ifftshift(np.fft.ifft2(U2))
                uout, LL = u2,self.L
            else:
                k=2*np.pi/self.lamb
                h=1/(1j*self.lamb*self.z)*np.exp(1j*k/(2*self.z)*(self.xx()[0]**2+self.xx()[1]**2))
                H= np.fft.fft2(np.fft.fftshift(h))*dx**2
                U1= np.fft.fft2(np.fft.fftshift(u1))
                U2= H*U1
                u2=np.fft.ifftshift(np.fft.ifft2(U2))
                uout, LL = u2,self.L
        elif self.tp == 'Fraunhofer':   # propagador de Fraunhofer
            L2=self.lamb*self.z/dx
            dx2=self.lamb*self.z/self.L
            x2=np.arange(-L2/2,L2/2,dx2)
            X2, Y2 = np.meshgrid(x2, x2);
            c=1/(1j*self.lamb*self.z)*np.exp(1j*k/(2*self.z)*(X2**2+Y2**2))
            u2=c*np.fft.ifftshift(np.fft.fft2(np.fft.fftshift(u1)))*dx**2
            uout, LL = u2,L2
        else:
            print('Ingrese el tipo de propagador')
        return uout,LL

    def plotProp(self): # gráfica de la propagación
        u = self.prop()[0]
        I = np.abs(u)**2
        L = self.prop()[1]
        dx = L/self.N
        x = np.arange(-L/2,L/2,dx)
        if type(self.fase) != str:
            fase=''
        else:
            fase = self.fase
        fig,axs = plt.subplots( nrows=1,ncols=2,figsize=(12,6) ) 
        axs[0].set(title='Pattern of '+self.a+' '+fase+f' at z={self.z} m',xlabel='x (m)',ylabel='y (m)')
        axs[1].set(title='x axis profile of '+self.a+' '+fase+f' at z={self.z} m',xlabel='x (m)',ylabel='y (m)')
        axs[0].imshow(I**(1/3),cmap= 'gray',extent=[-L/2,L/2,L/2,-L/2])
        axs[1].plot(x,I[round(self.N/2),:],c='tab:pink')
        plt.show()