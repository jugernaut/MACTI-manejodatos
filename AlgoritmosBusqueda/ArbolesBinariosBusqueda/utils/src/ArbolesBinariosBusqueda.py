from utils.src.ArbolesBinarios import AB, Nodo

''' Clase arbol binario de busqueda, genera la estructura de un arbol binario
    de busqueda asi como sus funciones.'''
class ABB(AB):
  ''' Consructor de arboles'''
  def __init__(self, dato):
    # llamamos al constructor de la clase padre con la palabra super
    super(ABB, self).__init__(dato)
    # y se agrega la variable ultimo agregado que sirve para clases posteriores
    self.ultimo_agregado = self.raiz

  ''' Busca un dato en el arbol y devuelve el nodo'''
  def busqueda(self, nodo, dato):
    # si la raiz es None o el dato esta contenido en el nodo,
    # se devuelve el nodo.
    if nodo is None or nodo.dato == dato:
      return nodo
    # si el dato es mayo entonces se busca del lado derecho
    if nodo.dato < dato:
      return self.busqueda(nodo.der, dato)
    # si no, se busca en el lado izquierdo
    else:
      return self.busqueda(nodo.izq, dato)

  ''' Inserta un elemento en el arbol a partir de un nodo'''
  def insertar_nodo(self, nodo, dato):
    # si el nodo es vacio ahi se crea el nuevo nodo
    if nodo is None:
      nuevo_nodo = Nodo(dato)
      self.ultimo_agregado = nuevo_nodo
      return nuevo_nodo
    # si el dato es menor que su padre, se inserta en el lado izquierdo
    if dato < nodo.dato:
      nuevo_nodo = self.insertar_nodo(nodo.izq, dato)
      nodo.izq = nuevo_nodo
      nuevo_nodo.padre = nodo
    # de no ser asi se inserta del lado derecho
    else:
      nuevo_nodo = self.insertar_nodo(nodo.der, dato)
      nodo.der = nuevo_nodo
      nuevo_nodo.padre = nodo
    # nodo guarda toda la ruta de donde sera insertado el dato
    # hasta caer en el caso base, es por eso que se devuelve    
    return nodo
  
  ''' Inserta un nodo en el arbol, a partir de la raiz'''
  def insertar(self, dato):
    # si el dato a insertar no se encuentra en el ABB se inserta
    if self.busqueda(self.raiz, dato) is None:
      # Se inserta el dato desde la raiz
      self.insertar_nodo(self.raiz, dato)

  ''' Busca el minimo en el subarbol a partir de nodo, este metodo sirve
      para poder eliminar nodos del arbol y mantener el orden'''
  def minimo_en_subarbol(self, nodo):
    # caso base en el que no hay minimo
    if nodo is None:
      return nodo
    # caso base en el que el nodo es el minimo ya que no tiene hijo izq
    if nodo.izq is None:
      return nodo
    # llamada recursiva para movernos al siguiente minimo
    return self.minimo_en_subarbol(nodo.izq)

  ''' Borra un nodo en el arbol, busca al nodo que contiene a dato
      y en caso de existir lo borra, se pueden dar multiples casos'''
  def borra_nodo(self, nodo, dato):
    # Caso 0) revisamos si el arbol es vacio.
    if self.raiz is None:
      return None
    # buscamos el nodo a borrar
    nodo_a_borrar = self.busqueda(nodo, dato)
    aux = nodo_a_borrar

    # Caso 0.1) si el dato no se encontro en el arbol no se puede borrar
    if nodo_a_borrar is None:
      return None

    # Caso 1) si el nodo a borrar es la RAIZ
    if nodo_a_borrar is self.raiz:
      # caso1.1) no tiene hijos, solo se borra la raiz
      if nodo_a_borrar.izq is None and nodo_a_borrar.der is None:
        self.raiz = None
        self.ultimo_agregado = None
        return None

      # Caso1.2) solo se tiene hijo derecho, entonces se sube al hijo derecho
      if nodo_a_borrar.izq is None and nodo_a_borrar.der is not None:
        self.raiz = nodo_a_borrar.der
        self.raiz.padre = None
        return self.raiz

      # Caso1.3) solo se tiene hijo izquierdo, entonces se sube al hijo izquierdo
      if nodo_a_borrar.izq is not None and nodo_a_borrar.der is None:
        self.raiz = nodo_a_borrar.izq
        self.raiz.padre = None
        return self.raiz

      # Caso1.4) tiene ambos hijos
      if nodo_a_borrar.izq is not None and nodo_a_borrar.der is not None:
        # buscamos el minimo en el subarbol derecho (minimo de los mayores)
        minimo = self.minimo_en_subarbol(nodo_a_borrar.der)
        aux = minimo.padre
        self.raiz.dato = minimo.dato
        self.borra_nodo(minimo, minimo.dato)
        return aux

    else: #Caso 2)
      # a partir de aqui se tienen 3 casos:
      # si no tiene hijos simplemente se borra el nodo
      # si tiene un solo hijo (ya sea izquierdo o derecho) se sube al unico hijo
      # tiene ambos hijos

      # es necesario identificar si el nodo a borrar es hijo izquierdo o derecho
      es_izquierdo = False
      if nodo_a_borrar.padre.izq == nodo_a_borrar:
        es_izquierdo = True

      # Caso2.1) no tiene hijos, solo se borra el nodo
      if nodo_a_borrar.izq is None and nodo_a_borrar.der is None:
        aux = nodo_a_borrar.padre
        # revisamos si el nodo a borrar es un hijo izquiero o derecho
        if es_izquierdo: # Caso2.1.1)
          aux.izq = None
        else: # Caso2.1.2)
          aux.der = None
        nodo_a_borrar = None
        return aux
      
      # Caso2.2) solo se tiene hijo izquierdo, entonces se sube al hijo izquierdo
      if nodo_a_borrar.izq is not None and nodo_a_borrar.der is None:
        nodo_a_borrar.izq.padre = nodo_a_borrar.padre
        aux = nodo_a_borrar.padre
        # revisamos si el nodo a borrar es un hijo izquiero o derecho
        if es_izquierdo: # Caso2.2.1)
          nodo_a_borrar.padre.izq = nodo_a_borrar.izq
        else: # Caso2.2.2)
          nodo_a_borrar.padre.der = nodo_a_borrar.izq
        return aux

      # Caso2.3) solo se tiene hijo derecho, entonces se sube al hijo derecho
      if nodo_a_borrar.izq is None and nodo_a_borrar.der is not None:
        nodo_a_borrar.der.padre = nodo_a_borrar.padre
        aux = nodo_a_borrar.padre
        # revisamos si el nodo a borrar es un hijo izquiero o derecho
        if es_izquierdo: # Caso2.3.1)
          nodo_a_borrar.padre.izq = nodo_a_borrar.der
        else: # Caso2.3.2)
          nodo_a_borrar.padre.der = nodo_a_borrar.der
        return aux

      # Caso2.4) tiene ambos hijos
      if nodo_a_borrar.izq is not None and nodo_a_borrar.der is not None:
        # buscamos el minimo en el subarbol derecho
        minimo = self.minimo_en_subarbol(nodo_a_borrar.der)
        aux = minimo.padre
        nodo_a_borrar.dato = minimo.dato
        self.borra_nodo(minimo, minimo.dato)
        return aux
  
  ''' Borra un nodo que contiene a dato a partir de la raiz'''
  def borrar(self, dato):
    self.borra_nodo(self.raiz, dato)
