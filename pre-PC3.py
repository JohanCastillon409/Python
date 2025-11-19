# EJERCICIOS QUE PUEDEN VENIR EN EL EXAMEN DE ALGORITMOS Y ESTRUCTURAS DE DATOS


#Implementacion de arboles binarios
class Nodo:
    # cada no tiene un valor y dos hijos: izquierdo y derecho
    def __init__(self, valor):
        self.valor= valor
        self.izquierdo = None
        self.derecho = None 
        
#Fumcion para insertar nodos
def insertar (raiz,valor):
    if raiz is None:
        return Nodo(valor)
    #si el valor es menor, insertar en el sub arbol izquierdo
    if valor <raiz.valor:
        raiz.izquierdo = insertar(raiz.izquierdo, valor)
        #si el valor es mayor, insertar en el sub arbol derecho 
    if valor > raiz.valor:
        raiz.derecho= insertar (raiz.derecho, valor)
    return raiz

#Funcion para buscar un valor 
def buscar(raiz,valor):
    if raiz is None:
        return False
    #si encontramos valor 
    if raiz.valor== valor:
        return True
    #si el valor es menor, buscar por la izquierda
    if valor < raiz.valor:
        return buscar (raiz.izquierdo, valor)
    #si el valor es mayor, buscar por la derecha
    else:
        return buscar (raiz.derecho, valor)


# Recorridos del árbol 
def recorrido_inorden(raiz):
    # Recorrido IN-ORDEN: Izquierdo -> Raíz -> Derecho
    if raiz:
        recorrido_inorden(raiz.izquierdo)
        print(raiz.valor, end=' ')
        recorrido_inorden(raiz.derecho)


def recorrido_preorden(raiz):
    # PRE-ORDEN: Raíz -> Izquierdo -> Derecho
    if raiz:
        print(raiz.valor, end=' ')
        recorrido_preorden(raiz.izquierdo)
        recorrido_preorden(raiz.derecho)


def recorrido_postorden(raiz):
    # POST-ORDEN: Izquierdo -> Derecho -> Raíz
    if raiz:
        recorrido_postorden(raiz.izquierdo)
        recorrido_postorden(raiz.derecho)
        print(raiz.valor, end=' ')

def contar_hojas(raiz):
    if raiz is None:
        return 0
    if raiz.izquierdo is None and raiz.derecho is None:
        return 1
    return contar_hojas(raiz.izquierdo) + contar_hojas(raiz.derecho)

def altura_arbol(raiz):
    if raiz is None:
        return 0  # Altura de un árbol vacío es 0
    izquierda_altura = altura_arbol(raiz.izquierdo)
    derecha_altura = altura_arbol(raiz.derecho)
    return max(izquierda_altura, derecha_altura) + 1

def eliminar_nodo(raiz, valor):
    if not raiz: return None
    if valor < raiz.valor: raiz.izquierdo = eliminar_nodo(raiz.izquierdo, valor)
    elif valor > raiz.valor: raiz.derecho = eliminar_nodo(raiz.derecho, valor)
    else:
        if not raiz.izquierdo or not raiz.derecho:
            return raiz.izquierdo or raiz.derecho
        sucesor = raiz.derecho
        while sucesor.izquierdo: sucesor = sucesor.izquierdo
        raiz.valor = sucesor.valor
        raiz.derecho = eliminar_nodo(raiz.derecho, sucesor.valor)
    return raiz


def valor_izquierda(r, v):
    n = r
    while n and n.valor != v:
        n = n.izquierdo if v < n.valor else n.derecho
    if not n or not n.izquierdo: return None
    n = n.izquierdo
    while n.izquierdo: n = n.izquierdo
    return n.valor


def valor_derecha(r, v):
    n = r
    while n and n.valor != v:
        n = n.izquierdo if v < n.valor else n.derecho
    if not n or not n.derecho: return None
    n = n.derecho
    while n.derecho: n = n.derecho
    return n.valor


# Programa principal
arbol = None

valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]
print(f"Insertando valores: {valores}")

for valor in valores:
    arbol = insertar(arbol, valor)

print("\n==== RECORRIDOS DEL ÁRBOL ====")
print("In-Orden: ", end="")
recorrido_inorden(arbol)

print("\nPre-Orden: ", end="")
recorrido_preorden(arbol)

print("\nPost-Orden: ", end="")
recorrido_postorden(arbol)

print(f"En el arbol hay {contar_hojas(arbol)} hojas")

print(f"\n La altura del arbol es: {altura_arbol(arbol)}")

print("\n El numero 20 esta en el arbol?? ", buscar(arbol,20))

#print("\n Eliminar el nodo 20:" )
# eliminar_nodo(arbol,20)

print("In-Orden despues de eliminar 20: ", end="")
recorrido_inorden(arbol)

print("\n El valor mas a la derecha del nodo 30 es: ", valor_derecha(arbol,30))
print("\n El valor mas a la izquierda del nodo 70 es: ", valor_izquierda(arbol,70))