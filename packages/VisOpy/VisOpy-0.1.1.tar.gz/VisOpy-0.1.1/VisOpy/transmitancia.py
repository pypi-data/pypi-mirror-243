import numpy as np
from .aberturas import Aberturas
from .Zernike import polZernike

class transm(Aberturas):
    '''
    Clase que construye la transmitancia de un sistema dadas:
    Lado: Longitud de lado del espacio, float
    Nmuestras: Número de muestras, int
    radiox: semiancho en x de la abertura, float
    radioy: semiancho en y de la abertura (opcional), float
    Campo: lista que contiene: [abertura,fase,set,abe,abset]
        abertura: tipo de abertura 'circle' o 'rectangle'
        fase: tipo de fase 'tilt','focus' o una función de (rho,theta) personalizada
        set: características de la fase. Para 'tilt' es un arreglo de dos elementos [theta,alpha]
            para 'focus' es un float que indica la longitud de enfoque.
        abe: booleano que indica si se consideran o no aberraciones
        abset: arreglo de dos filas, la primera contiene los grados de las aberraciones y la segunda
            los coeficientes de las aberraciones
    lamb: longitud de onda, float    
    '''
    
    def __init__(self,Lado:int,Nmuestras:int,radiox:float,campo:list,lamb:float,radioy:float=False):
        Aberturas.__init__(self,Lado,Nmuestras,radiox,radioy) 
        self.a = campo[0]
        self.fase = campo[1]
        self.set = campo[2]
        self.abe = campo[3]
        self.abset = campo[4]
        self.lamb = lamb

    def u1(self):   # se escoge la abertura
        if self.a == 'circle':
            return self.circ()
        if self.a == 'rectangle':
            return self.rect()
        
    def k(self):    # número de onda
        return 2*np.pi/self.lamb

    def tilt(self): # fase de la inclinación
        theta, alpha = np.deg2rad(self.set)
        k=self.k()
        X, Y = self.xx()
        uout =np.exp(1j*k*(X*np.cos(theta)+Y*np.sin(theta))*np.tan(alpha))
        return uout
    
    def focus(self): # fase del enfoque
        zf = self.set
        k=self.k()
        X, Y = self.xx()
        uout = np.exp(-1j*k/(2*zf)*(X**2+Y**2))
        return uout
    
    def faseZernike(self):  # fase de las aberraciones

        if self.abe:
            try:    # si hay un sólo término de aberración
                Z = polZernike(self.L,self.N,self.wx,self.abset[0])
                Z = Z.genZj()
                Z = Z*self.abset[1]
                return np.exp(1j*Z)
            except: # si hay más múltiples polinomios
                z = []
                npol = self.abset[0,:]
                coef = self.abset[1,:]
                for i in range(self.abset.shape[1]):
                    Z = polZernike(self.L,self.N,self.wx,npol[i])
                    Z = Z.genZj()
                    Z = Z*coef[i]
                    z.append(Z)
                suma = np.sum(np.vstack(z), axis=0)
                return np.exp(1j*suma)
        else:
             return 1
        
    def u11(self):  # se escoge la fase y se incluyen las aberraciones
        if self.fase == 'tilt':
            u = self.tilt()*self.u1()*self.faseZernike()
        elif self.fase == 'focus':
            u = self.focus()*self.u1()*self.faseZernike()
        elif self.fase == None:
            u = self.u1()*self.faseZernike()
        else:
            X, Y = self.xx()
            rho=np.sqrt(X**2+Y**2)
            thet=np.arctan2(Y,X)+np.pi
            k=self.k()
            u = self.u1()*np.exp(1j*k*self.fase(rho,thet))*self.faseZernike()
        return u
