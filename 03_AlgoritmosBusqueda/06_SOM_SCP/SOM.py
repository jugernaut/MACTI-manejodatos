import numpy as np
from matplotlib import pyplot as plt

class SOM(object):
    """
    Clase que representa una red neuronal tipo SOM.
    """

    #Para revisar si la red ya ha sido entrenada
    _trained = False

    def __init__(self, m, n, dim, n_iterations=100, alpha=None, sigma=None):
        """
        Constructor que toma como parametros los valores descritos en el
        algoritmo SOM. Genera un mapa de m renglones por n columnas y se entrenara
        con n_iterations
        """

        #Se inicializan variables que seran usadas a lo largo del coidgo
        self._m = m
        self._n = n
        if alpha is None:
            alpha = 0.3
        else:
            alpha = float(alpha)
        if sigma is None:
            sigma = max(m, n) / 2.0
        else:
            sigma = float(sigma)
        self._n_iterations = abs(int(n_iterations))

        '''Lista de pesos de los vectores de la red neuronal'''
        self._weightage_vects = np.random.normal(size=(m*n, dim))

        '''Lista de m*n entradas, y cada entrada representa una
        coordenada en la cual se encuentra cada neurona'''
        self._location_vects = np.array(
            list(self._neuron_locations(m, n)))

        '''centroid_grid es un mapa de bits en el cual se guardan los
        valores de las neuronas. Es de tamano m, por que para cada renglon
        se tienen n neuronas y sus respectivos valores. '''
        centroid_grid = [[] for i in range(self._m)]
        self._weightages = list(self._weightage_vects)
        self._locations = list(self._location_vects)

        '''Con este for, se accede a cada neurona por posicion y se guarda
        en centroid_grid sus pesos. El resultado es un mapa de bits que puede
        ser facilmente graficado por matplotlib. Es el mapa incial (SIN ENTRENAR)'''
        for i, loc in enumerate(self._locations):
            centroid_grid[loc[0]].append(self._weightages[i])
        self._mapa_inicial = centroid_grid

        # Store initial alpha and sigma for reset in train method
        self._initial_alpha = alpha
        self._initial_sigma = sigma

    def _neuron_locations(self, m, n):
        '''Yield regresa un generador flojo, y hasta que es necesario
        se evalua. Esto se hace para que no haya informacion no necesaria
        en memoria. En el constructor el resultado de esta funcion se
        mete en una lista para que sea accesible de inmediato'''
        for i in range(m):
            for j in range(n):
                yield np.array([i, j])

    def train(self, input_vects, debbug=False):
        # Reset alpha and sigma for each training session
        alpha = self._initial_alpha
        sigma = self._initial_sigma

        if not debbug:
            '''Para cada iteracion (epoca) se realiza el entrenamiento'''
            for iter_no in range(self._n_iterations):
                actual = np.linalg.norm(self._weightage_vects)
                #Se entrena con cada vector uno por uno
                for input_vect in input_vects:
                    # Find the Best Matching Unit (BMU)
                    distances = np.linalg.norm(self._weightage_vects - input_vect, axis=1)
                    bmu_index = np.argmin(distances)
                    bmu_loc = self._location_vects[bmu_index]

                    # Calculate learning rate and neighborhood function
                    learning_rate_op = 1.0 - (iter_no / self._n_iterations)
                    _alpha_op = alpha * learning_rate_op
                    _sigma_op = sigma * learning_rate_op

                    # Calculate distances to BMU for all neurons
                    bmu_distance_squares = np.sum(np.square(self._location_vects - bmu_loc), axis=1)
                    neighbourhood_func = np.exp(- (bmu_distance_squares / (2 * (_sigma_op**2))))
                    
                    # Calculate learning rate multiplier for each neuron
                    learning_rate_multiplier = np.tile(neighbourhood_func.reshape(-1, 1) * _alpha_op, (1, self._weightage_vects.shape[1]))

                    # Update weights
                    weightage_delta = learning_rate_multiplier * (input_vect - self._weightage_vects)
                    self._weightage_vects += weightage_delta

                siguiente = np.linalg.norm(self._weightage_vects)
                '''Si la norma del mapa actual no varia mucho con respecto
                al siguiente, se rompe el ciclo de las epocas'''
                if abs(siguiente - actual) <= 0.000001:
                    break
            '''centroid_grid es un mapa de bits en el cual se guardan los
                valores de las neuronas. Es de tamano m, por que para cada renglon
                se tienen n neuronas y sus respectivos valores. '''
            centroid_grid = [[] for i in range(self._m)]
            self._weightages = list(self._weightage_vects)
            self._locations = list(self._location_vects)

            '''Con este for, se accede a cada neurona por posicion y se guarda
                en centroid_grid sus pesos. El resultado es un mapa de bits que puede
                ser facilmente graficado por matplotlib. En este punto la red ya esta entrenada.'''
            for i, loc in enumerate(self._locations):
                centroid_grid[loc[0]].append(self._weightages[i])
            self._centroid_grid = centroid_grid

            '''En este punto la red ya esta entrenada.'''
            self._trained = True
            '''Esta seccion muestra como se entrena el SOM y es basicamente el mismo
            codigo de la seccion del if y al final solo se agrega la grafica del mapa.'''
        else:
            centroid_grid = [[] for i in range(self._m)]

            for iter_no in range(self._n_iterations):
                actual = np.linalg.norm(self._weightage_vects)
                #Se entrena con cada vector uno por uno
                for input_vect in input_vects:
                    # Find the Best Matching Unit (BMU)
                    distances = np.linalg.norm(self._weightage_vects - input_vect, axis=1)
                    bmu_index = np.argmin(distances)
                    bmu_loc = self._location_vects[bmu_index]

                    # Calculate learning rate and neighborhood function
                    learning_rate_op = 1.0 - (iter_no / self._n_iterations)
                    _alpha_op = alpha * learning_rate_op
                    _sigma_op = sigma * learning_rate_op

                    # Calculate distances to BMU for all neurons
                    bmu_distance_squares = np.sum(np.square(self._location_vects - bmu_loc), axis=1)
                    neighbourhood_func = np.exp(- (bmu_distance_squares / (2 * (_sigma_op**2))))

                    # Calculate learning rate multiplier for each neuron
                    learning_rate_multiplier = np.tile(neighbourhood_func.reshape(-1, 1) * _alpha_op, (1, self._weightage_vects.shape[1]))

                    # Update weights
                    weightage_delta = learning_rate_multiplier * (input_vect - self._weightage_vects)
                    self._weightage_vects += weightage_delta

                siguiente = np.linalg.norm(self._weightage_vects)

                if abs(siguiente - actual) <= 0.000001:
                    break
                if iter_no % 10 == 0:
                    centroid_grid = [[] for i in range(self._m)]
                    self._weightages = list(self._weightage_vects)
                    self._locations = list(self._location_vects)

                    for i, loc in enumerate(self._locations):
                        centroid_grid[loc[0]].append(self._weightages[i])
                    self._centroid_grid = centroid_grid

                    red_entrenada = self.get_centroids()
                    # SECCION PARA GRAFICAR
                    # Use the _map_vect method for a single vector classification in debug
                    bmu_coord = self.map_vect(input_vect) # input_vect is the last one processed

                    plt.text(bmu_coord[1], bmu_coord[0], "bmu", ha='center', va='center',
                        bbox=dict(facecolor='white', alpha=0.5, lw=0))
                    plt.imshow(red_entrenada)
                    plt.show()
                    input("Continuar?")

            '''En este punto la red ya esta entrenada.'''
            self._trained = True

    def get_centroids(self):
        # Solo devuelve los centroides para que puendan ser graficados
        #if not self._trained:
            #raise ValueError("La red aun no ha sido entrenada")
        return self._centroid_grid

    def map_vects(self, input_vects):
        '''to_return es la lista que contiene las coordenadas (x,y) de la
        neurona que mas se parece a cada una de las entradas de input_vects
        en el mismo orden'''

        if not self._trained:
            raise ValueError("SOM not trained yet")

        to_return = []
        for vect in input_vects:
            min_index = min([i for i in range(len(self._weightages))],
                            key=lambda x: np.linalg.norm(vect-
                                                         self._weightages[x]))
            to_return.append(self._locations[min_index])

        return to_return

    def map_vect(self, vect):
        '''
        Mapea un solo vector y devuelve la clasificacion vista como
        un indice relacionado a la coordenada (x,y) de la neurona
        '''

        min_index = min([i for i in range(len(self._weightages))],
                        key=lambda x: np.linalg.norm(
                            vect - self._weightages[x]))
        pos2D = self._locations[min_index]
        # polinomio de direccionamiento de la neurona
        #return pos2D[0]*self._m + pos2D[1], pos2D
        return (pos2D[1], pos2D[0])