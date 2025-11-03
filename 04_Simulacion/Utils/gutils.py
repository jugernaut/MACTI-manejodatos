#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 17:35:09 2020
@author: luiggi
"""
import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
#plt.style.use('seaborn')


class planoCartesiano():
    
    def __init__(self, rows = 1, cols = 1, par = None, par_fig={'figsize':(10,5)}, title=''):
        """
        Crea e inicializa una figura de matplotlib.
        Parameters
        ----------
        rows : int, opcional
            Número de renglones del arreglo de subplots. The default is 1.
        cols : int, opcional
            Número de columnas del arreglo de subplots. The default is 1.
        par : list of dicts, opcional
            Lista de diccionarios; cada diccionario define los parámetros que 
            se usarán decorar los `Axes` de cada subplot. The default is None.
        par_fig : dict, opcional
            Diccionario con los parámetros para decorar la figura. 
            The default is {}.
        """
        self.__fig = plt.figure(**par_fig)
        self.__fig.suptitle(title, fontweight='light', fontsize='12', color='blue')
        self.__nfigs =  rows *  cols

        import matplotlib
        self.__mpl_ver = matplotlib.__version__.split(sep='.')
        
        if par != None:
            Nfill = self.__nfigs - len(par)
        else:
            Nfill = self.__nfigs
            par = [ ]
            
        [par.append({}) for n in range(Nfill)]
            
        self.__ax = [plt.subplot(rows, cols, n, **par[n-1]) for n in range(1,self.__nfigs + 1)]
        plt.tight_layout()


    def plot(self, n = 1, x = None, y = None, par=None):        
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)        

        if par != None:
            out = self.__ax[n-1].plot(x, y, **par)
        else:
            out = self.__ax[n-1].plot(x, y)
                    
        return out        
 
    def scatter(self, n = 1, x = None, y = None, par=None):   
        
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)        

        if par != None:
            out = self.__ax[n-1].scatter(x, y, **par)
        else:
            out = self.__ax[n-1].scatter(x, y)         
        return out      

    def bar(self, n = 1, x = None, y = None, par=None):        
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)        

        if par != None:
            out = self.__ax[n-1].bar(x, y, **par)
        else:
            out = self.__ax[n-1].bar(x, y)
                    
        return out     

    def format_func(value, tick_number):
        # find number of multiples of pi/2
        N = int(np.round(2 * value / np.pi))
        if N == 0:
            return "0"
        elif N == 1:
            return r"$\pi/2$"
        elif N == 2:
            return r"$\pi$"
        elif N % 2 > 0:
            return r"${0}\pi/2$".format(N)
        else:
            return r"${0}\pi$".format(N // 2)

    def ticks(self, n = 1, xticks = [], yticks = [], trig = False):           
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)        

        if trig:
            self.__ax[n-1].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
            self.__ax[n-1].xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
            self.__ax[n-1].xaxis.set_major_formatter(plt.FuncFormatter(planoCartesiano.format_func))
        else:        
            if len(xticks) != 0:
                self.__ax[n-1].set_xticks(xticks)
            if len(yticks) != 0:
                self.__ax[n-1].set_yticks(yticks)

    def label_ticks(self, n = 1, xlabel = [], ylabel = []):
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)   
        
        if len(xlabel):
            self.__ax[n-1].set_xticklabels(xlabel)
        if len(ylabel):
            self.__ax[n-1].set_yticklabels(ylabel)
            
    def limits(self, n = 1, x = (), y = ()):
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        if len(x):
            offset = np.fabs(x[1] - x[0]) * 0.2
            self.__ax[n-1].set_xlim((x[0]-offset,x[1]+offset))
        if len(y):
            offset = np.fabs(y[1] - y[0]) * 0.2
            self.__ax[n-1].set_ylim((y[0]-offset,y[1]+offset))

    def colorbar(self, n=1, m=None, par=None):
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        if par != None:
            self.__fig.colorbar(m, ax = self.__ax[n-1], **par)
        else:
            self.__fig.colorbar(m, ax = self.__ax[n-1])

    def legend(self, par=None):
        """
        Muestra las leyendas de todos los subplots, si están definidos.
        Parameters
        ----------
        par : dict, opcional
            Diccionario con los parámetros para decorar las leyendas. 
            The default is None.
        Returns
        -------
        None.
        
        See Also
        --------
        matplotlib.axes.Axes.legend().
        """
        if par != None:   
            [self.__ax[n].legend(**par) for n in range(0,self.__nfigs)]        
        else:
            [self.__ax[n].legend() for n in range(0,self.__nfigs)]    
            

    def show(self):
        """
        Muestra las gráficas de cada subplot.
        
        See Also
        --------
        matplotlib.pyplot.show().
        
        """
        plt.show()
        
    def annotate(self, n = 1, par=None):   
        """
        Parameters
        ----------
        n : TYPE, optional
            DESCRIPTION. The default is 1.
        par : TYPE, optional
            DESCRIPTION. The default is None.
        Returns
        -------
        TYPE
            DESCRIPTION.
        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)    
 
        # Debido a incompatibilidades de Matplotlib 3.2
        if int(self.__mpl_ver[1]) < 3:
            par['s'] = par['text']
            del par['text']
            
        return self.__ax[n-1].annotate(**par)

def RMS(ua, u):
    """
    Calcula el error cuadrático medio entre u y ua.
    
    Parameters
    ----------
    ua: np.array
    Arreglo de valores aproximados.
    
    u: np.array
    Arreglo de valores exactos.
    
    Returns
    -------
    float
    El error cuadrático medio entre u y ua.
    """
    return np.sqrt(np.sum((ua - u)**2) / len(ua))

def RMS1(ua, u):
    """
    Calcula el error cuadrático medio entre u y ua.
    
    Parameters
    ----------
    ua: np.array
    Arreglo de valores aproximados.
    
    u: np.array
    Arreglo de valores exactos.
    
    Returns
    -------
    float
    El error cuadrático medio entre u y ua.
    """
    return np.sqrt(np.sum((ua - u)**2) / len(ua))

def biseccion(f,Tol,N,a,b):
    """
    implementa el metodo de la biseccion
    para encontrar la raiz de una funcion.
    
    Parameters
    ----------
    f: function
    funcion para calcular raiz.
    
    Tol: float
    Tolerancia.
    
    N: integer
    Numero de iteraciones maximo.
    
    a: float
    limite izquierdo.
    
    b: float
    limite derecho.
    
    Returns
    -------
    float
    La raiz de la funcion f.
    list
    Valores en la sucesion del algoritmo.
    """
    sucesion=[]
    fa=f(a)
    fb=f(b)
    #no hay un cambio de signo (teorema del valor medio)
    #no existe raiz en el intervalo [a,b]
    if fa*fb>0:
        print ("no hay raiz en [a,b]")
        return
    #contador de iteraciones    
    n=1
    x0=0.0
    #mientras no se exceda el numero de iteraciones
    while n<=N:
        #se busca la raiz en el punto medio
        x1=(a+b)/2.0
        fx=f(x1)
        sucesion.append(x1)
        #en caso de que la iteracion siguiente y la diferencia
        #entre la iteracion anterior no excedan Tol, entonces
        #la iteracion actual se aproxima a la solucion buscada
        if abs(f(x1)) <= Tol and abs(x1-x0) <= Tol:
            return x1, sucesion
        #en caso de no cumplir el criterio de tolerancia
        #se actualiza el rango de busqueda
        if (fa*fx <0.0):
            b=x1  
        if (fx*fa >0.0):      
            a=x1
        x0=x1
        #se incrementa el contador de iteraciones
        n=n+1
        
'''Esta funcion implementa el metodo de la falsa posicion
para encontrar la raiz de una funcion.
f:   funcion de la cual se busca la raiz
Tol: tolerancia del error numerico
N:   numero maximo de iteraciones
a:   limite inferior del rango inicial
b:   limite superior del rango inicial
'''
def falsaPosicion(f,Tol,N,a,b):
    fa=f(a)
    fb=f(b)
    #en caso de que no haya cambio de signo, no existe raiz
    if fa*fb>0:
        print("No existe raiz en [a,b]")
        return
    #contador de iteraciones
    n=1
    #se toma una raiz inicial arbitraria   
    x0=0.0
    sucesion = []
    #mientras no se exceda el numero de iteraciones
    while n<=N:
        #se actualiza el rango de busqueda
        fa,fb =f(a),f(b)
        #se calcula la nueva iteracion
        x1= (a*fb-b*fa)/(fb-fa)
        fx=f(x1)
        sucesion.append(x1)
        #en caso de que la diferencia entre la iteracion actual
        #y la iteracion anterior no excedan Tol, y que la raiz
        #evaluada no exceda la tolerancia, se devuelve la raiz
        if abs(f(x1)) <= Tol and abs(x1-x0) <= Tol:
            return x1, sucesion
        #en caso de no cumplir el criterio de tolerancia
        #se actualiza el rango de busqueda
        if (fa*fx <0.0):
            b=x1 
        if (fx*fa >0.0):      
            a=x1
        #se actualiza x0
        x0=x1
        #se incrementa el contador de iteraciones
        n=n+1
        
'''Esta funcion implementa el metodo de la falsa posicion
para encontrar la raiz de una funcion.
f:   funcion de la cual se busca la raiz
df:  derivada de f
Tol: tolerancia del error numerico
N:   numero maximo de iteraciones
x0:  aproximacion inicial
'''
def newton(f,Tol,N,x0):
    #contador de iteraciones
    n=1
    #mientras no se haya superado el limite de iteraciones
    while n<=N:
        #se evalua la funcion y su derivada
        fx=f(x0)
        dfx=derivada(f,x0, Tol)
        #se calcula la siguiente aproximacion
        xn = x0-(fx/float(dfx))
        #en caso de cumplir criterios se devuelve la raiz
        if abs(f(xn)) <= Tol and abs(xn-x0) <= Tol:
            return xn
        #actualizamos las aproximaciones
        x0 = xn
        #se incrementa el contador de iteraciones    
        n=n+1
    raise Exception("Se alcanzo el maximo numero de iteraciones y no se encontro raiz")

def derivada(f, x, tol):
    return (f(x+tol)-f(x))/(tol)

# algoritmo para sustitucion hacia delante
# n es el tamano de la dimension del problema
# matriz L, vector b ya estan dados como parametros
# guardar los resultados en el vector y
# Ly=b
def sustDelante(L, b):
    n=len(L)
    y=np.empty_like(b)
    for i in range(0,n):
        y[i] = b[i]
        for j in range(0,i):
            y[i] -= L[i][j]*y[j]
        y[i] /= L[i][i]
    return y

# algoritmo para sustitucion hacia atras
# n es el tamano de la dimension del problema
# matriz U, vector y ya estan dados como parametros
# guardar los resultados en el vector x
# Ux=y
def sustAtras(U, y):
    n=len(U)
    x=np.empty_like(y)
    x[n-1] = y[n-1]/U[n-1][n-1]
    for i in range(n-2,-1,-1):
        x[i] = y[i]
        for j in range(i+1,n):
            x[i] -= U[i][j]*x[j]
        x[i] /= U[i][i]
    return x

# algoritmo para la factorizacion de Cholesky
# L y L transpuesta se alamacenan en la misma matriz
def cholesky(mat):
    L = np.zeros_like(mat)
    #Creamos un for que vaya de 0 al numero de renglones de la matriz.
    for k in range(len(mat)):
        #Creamos un for para ir sumando.
        for i in range(k):
            suma = mat[k,i]
            for j in range(i):
                suma -= (L[i,j]* L[k,j])
            L[k,i] = (suma)/ L[i,i]
            L[i,k] = L[k,i]
        suma = mat[k,k]
        for j in range(k):
            suma -= (L[k,j]*L[k,j])
        L[k,k] = np.sqrt(suma)
    return L

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    #test prueba
    print("prueba")
