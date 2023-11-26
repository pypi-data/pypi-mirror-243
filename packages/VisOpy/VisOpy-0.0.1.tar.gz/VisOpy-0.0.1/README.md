# Libreria de simulaciones en un sistema optico

## Clases

### Aberturas:
Construye la pupila del sistema. Puede ser circular circ() o rectangular rect().
### polZernike: 
Dados un grado del polinomio (en notacion OSA) y el valor de su respectivo coeficiente, se entrega el polinomio de Zernike evaluado en la pupila circular.
### transm: 
Construye el campo del sistema. Puede ser un tilt, focus, una transmitancia generalizada (que se ingresa en función de las coordenas esféricas) y/o coeficientes de Zernike para describir la aberración del sistema. El campo puede obtenerse del método u11()
### propLuz: 
Obtiene el campo en el plano imagen luego de propagarse con el propagador de Fresnel o Fraunhofer. El campo se puede obtener con prop() y el patron de irradiancia graficado con plotProp()
### formIm: 
Dada una imagen en el plano objeto, obtiene la imagen formada por el sistema. La imagen se obtiene con el método conv() y la grafica comparando ambos planos con plotConv()

## Variables de entrada
L: Longitud de lado del espacio, float
N: Número de muestras; int      
rx: Radiox de la abertura; float
ry: Radioy de la abertura; float
wl: Longitud de onda; float
campo: Características del sistema; list, compuesta por [abertura,fase,sets,aberrado,cAB]
    abertura: Tipo de abertura; str, 'circle' o 'rectangle'
    fase: Tipo de fase; str 'tilt' o 'focus' o función de theta y rho
    sets : Características de la fase; float si se usa 'focus', lista si se usa 'tilt', None para otro caso
    aberrado: Indica si se consideran o no aberraciones; True or False
    cAb: Características de las aberraciones; numpy array 2xn, la fila 1 son los grados de los coeficientes, la fila 2 sus correspondientes coeficientes. 
rut: Ruta a la imagen objeto; str
tip: Tipo de propagador;str, 'Fraunhofer' o 'Fresnel'
dist: Distancia de propagación; float

Se recomienda usar formIm pues esta contiene todos los métodos de los demás módulos.