import numpy as np
from aberturas import Aberturas
from Zernike import polZernike

class transm(Aberturas):
    '''
    clase
    '''
    
    def __init__(self,Lado:int,Nmuestras:int,radiox:float,campo:list,lamb:float,radioy:float=False):
        Aberturas.__init__(self,Lado,Nmuestras,radiox,radioy) 
        self.a = campo[0]
        self.fase = campo[1]
        self.set = campo[2]
        self.abe = campo[3]
        self.abset = campo[4]
        self.lamb = lamb

    def u1(self):
        if self.a == 'circle':
            return self.circ()
        if self.a == 'rectangle':
            return self.rect()
        
    def k(self):
        return 2*np.pi/self.lamb

    def tilt(self): # PROPAGADOR BASADO EN LA FUNCIÓN DE TRANSFERENCIA
        theta, alpha = np.deg2rad(self.set)
        k=self.k()
        X, Y = self.xx()
        uout =np.exp(1j*k*(X*np.cos(theta)+Y*np.sin(theta))*np.tan(alpha))
        return uout
    
    def focus(self): # PROPAGADOR BASADO EN LA FUNCIÓN DE TRANSFERENCIA
        zf = self.set
        k=self.k()
        X, Y = self.xx()
        uout = np.exp(-1j*k/(2*zf)*(X**2+Y**2))
        return uout
    
    def faseZernike(self):

        if self.abe:
            try:
                Z = polZernike(self.L,self.N,self.wx,self.abset[0])
                Z = Z.genZj()
                Z = Z*self.abset[1]
                return np.exp(1j*Z)
            except:
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
            
        #     try: 
                # z = np.zeros(self.set.shape[1])
                # npol = self.abset[0,:]
                # coef = self.abset[1,:]
                # for i in range(self.set.shape[1]):
                #     z[i] = polZernike(self.L,self.N,self.wx,npol[i])
                #     z[i] = z[i].genZj()
                #     z[i] = z[i]*coef[i]
                # suma = np.sum(z,axis=0)
                # return np.exp(1j*suma)
        #     except:
        #         z = polZernike(self.L,self.N,self.wx,self.abset[0])
        #         z = z.genZj()
        #         z = z*self.abset[1]
        #         return np.exp(1j*z)
        else:
             return 1
        
    def u11(self):
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
