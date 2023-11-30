import numpy as np

class Aberturas:
    '''
    Contiene las aberturas principales usadas en óptica, circular y rectangular, construidas 
    a partir de los siguientes parámetros:
    Lado: Longitud de lado del espacio, float
    Nmuestras: Número de muestras, int
    radiox: semiancho en x de la abertura, float
    radioy: semiancho en y de la abertura, float
    '''

    def __init__(self,Lado:int,Nmuestras:int,radiox:float,radioy:float=False): #atributos
        self.L = Lado
        self.N = Nmuestras
        self.wx = radiox
        self.wy = radioy

    def x(self):    # se define el eje
        return np.arange(-self.L/2,self.L/2,self.L/self.N)
    
    def xx(self):   # se define el sistema coordenado cuadrado
        return np.meshgrid(self.x(),self.x())
    
    def rho(self):  # se define el sistema coordenado polar
        X,Y = self.xx()
        return np.sqrt(X**2+Y**2)/self.wx
    
    def phi(self):  # se define el sistema coordenado polar
        X,Y = self.xx()
        return np.arctan2(Y,X)
    
    def circ(self):     # abertura circular
        X,Y = self.xx()
        return (np.abs(np.sqrt(X**2+Y**2)/self.wx)<=1)*1

    def rect(self):     # abertura rectangular
        X,Y = self.xx()
        def rect2D(x): 
            out = np.zeros((len(x),len(x)))
            for cont in range(0,len(x)):
                for cont2 in range(0,len(x)):
                    out[cont,cont2]=int(np.abs(x[cont,cont2])<=1/2)
            return out
        if not(self.wy):
            return rect2D(X/(2*self.wx))*rect2D(Y/(2*self.wx))
        else:
            return rect2D(X/(2*self.wx))*rect2D(Y/(2*self.wy))