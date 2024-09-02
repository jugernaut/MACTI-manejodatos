import random

# Clase Nodo necesaria para generar arboles binarios
class Nodo(object):
  '''
  Constructor de nodos
  dato: es el contenido del nodo
  '''
  def __init__(self, dato):
    self.izq = None
    self.dato = dato
    self.der = None
    self.padre = None

  # Nos dice si el nodo tiene al menos un hijo    
  def tieneHijos(self):
    return self.izq is not None and self.der is not None
  
  # Nos dide si el nodo es un hijo izquierdo
  def esIzq(self):
    return self.padre.izq == self
  
  # Nos dice si el nodo es un hijo derecho
  def esDer(self):
    return self.padre.der == self
  
  # Imprime el contenido del nodo
  def __str__(self):
    if self.dato is None:
      pass
    else:
      return '{}'.format(self.dato)

''' Clase AB (ArbolBinario), genera la estructura de un arbol binario, asi como sus funciones.'''
class AB(object):

  ''' Consructor de arboles binarios'''
  def __init__(self, dato):
    self.raiz = Nodo(dato)
      
  ''' Elimina todo el arbol'''
  def elimina(self):
    self.raiz = None
      
  ''' Devuelve el nivel del nodo que se le pasa como parametro.
      La raiz se ubica en el nivel cero'''
  def nivel(self, nodo):
    if nodo is None:
      return -1
    else:
      return 1 + self.nivel(nodo.padre)

  ''' Devuelve la altura a partir del nodo que se le pasa como parametro,
      si el arbol es vacio la altura es cero, si no se le suma 1 al maximo
      de las alturas de sus hijos'''
  def altura(self, nodo):
    if nodo is None:
      return 0
    else:
      return 1 + max(self.altura(nodo.izq), self.altura(nodo.der))
      
  ''' Inserta recursivamente un dato en el arbol de manera recursiva
      nodo: es el nodo a partir del cual se quiere insertar
      dato: es el dato que se quiere insertar
  '''
  def insertar_nodo(self, nodo, dato):
    # si el nodo es vacio ahi se crea el nuevo nodo
    if nodo is None:
      nuevo_nodo = Nodo(dato)
      return nuevo_nodo
    # dado que en los AB no hay un orden el nuevo nodo se inserta donde sea
    if bool(random.getrandbits(1)):
      nuevo_nodo = self.insertar_nodo(nodo.izq, dato)
      nodo.izq = nuevo_nodo
      nuevo_nodo.padre = nodo
    else:
      nuevo_nodo = self.insertar_nodo(nodo.der, dato)
      nodo.der = nuevo_nodo
      nuevo_nodo.padre = nodo
    #nodo guarda toda la ruta de donde sera insertado el dato
    #hasta caer en el caso base, es por eso que se devuelve    
    return nodo
  
  ''' Inserta un nodo en el arbol, a partir de la raiz'''
  def insertar(self, dato):
    #Se inserta el dato desde la raiz
    self.insertar_nodo(self.raiz, dato)
      
  ''' Recorre el arbol enorden e imprime cada uno de sus nodos'''
  def recorrido_enorden(self, nodo):
    if nodo is not None:
      self.recorrido_enorden(nodo.izq)
      print(nodo.dato)
      self.recorrido_enorden(nodo.der)

  ''' Recorre el arbol preorden e imprime cada uno de sus nodos'''
  def recorrido_preorden(self, nodo):
    if nodo is not None:
      print(nodo.dato)
      self.recorrido_preorden(nodo.izq)
      self.recorrido_preorden(nodo.der)

  ''' Recorre el arbol postorden e imprime cada uno de sus nodos'''
  def recorrido_postorden(self, nodo):
    if nodo is not None:
      self.recorrido_postorden(nodo.izq)
      self.recorrido_postorden(nodo.der)
      print(nodo.dato)