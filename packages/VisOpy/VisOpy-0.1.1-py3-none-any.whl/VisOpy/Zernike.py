import numpy as np
from scipy.special import factorial as fac
from .aberturas import Aberturas

class polZernike:
    '''
    Clase que permite generar una aberración dado el grado del polinomio de Zernike, j 
    (en notación OSA) 
    '''

    def __init__(self,Lado:float,Nmuestras:int,radiox:float,orden:int):
        Aberturas.__init__(self,Lado,Nmuestras,radiox) 
        self.j = orden
        
    def genZj(self):    # se genera el polinomio de Zernike y se evalúa en el sistema coordenado polar
        def zernike_Rnm(m, n, rho):
            if (n < 0 or m < 0 or abs(m) > n):
                raise ValueError
            if ((n-m) % 2):
                return rho*0.0
            pre_fac = lambda k: (-1.0)**k * fac(n-k) / ( fac(k) * fac( (n+m)/2.0 - k ) * fac( (n-m)/2.0 - k ) )
            return sum(pre_fac(k) * rho**(n-2.0*k) for k in range(int((n-m)/2+1)))*np.sqrt((n+1))

        def Zernike(m, n, rho, phi):
            if (m > 0): return zernike_Rnm(m, n, rho) *2**0.5* np.cos(m * phi)
            if (m < 0): return zernike_Rnm(-m, n, rho) *2**0.5* np.sin(-m * phi)
            return zernike_Rnm(0, n, rho)

        ab = Aberturas(self.L,self.N,self.wx)
        rho,phi = ab.rho(),ab.phi()
        j = self.j
        n = 0
        while (j > n):
            n += 1
            j -= n

        m = -n+2*j
        return Zernike(m, n, rho, phi)