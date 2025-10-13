import time


# --- CLASES BASE ---
# Se mantiene la clase ContenedorPesquero original.
class ContenedorPesquero:
    """
    Representa un contenedor de productos pesqueros del Puerto de Chimbote.
    Prioridades: 1=CRÍTICO, 2=URGENTE, 3=NORMAL
    """

    def __init__(self, codigo, peso_toneladas, tipo_producto, origen_planta, destino, prioridad=3):
        self.codigo = codigo
        self.peso_toneladas = peso_toneladas
        self.tipo_producto = tipo_producto
        self.origen_planta = origen_planta
        self.destino = destino
        self.prioridad = prioridad
        self.temperatura = self._calcular_temperatura()

    def _calcular_temperatura(self):
        temperaturas = {
            "frescos": "0-5°C", "congelados": "-18°C", "harina": "Ambiente",
            "conservas": "Ambiente", "aceite": "Ambiente"
        }
        return temperaturas.get(self.tipo_producto, "Ambiente")

    def __str__(self):
        return f"[{self.codigo} | P{self.prioridad} | {self.tipo_producto.upper()}]"


class Nodo:
    """
    Nodo para una lista doblemente enlazada.
    Ahora incluye un puntero 'anterior'.
    """

    def __init__(self, contenedor):
        self.contenedor = contenedor
        self.siguiente = None
        self.anterior = None


class ListaDoblementeEnlazada:
    """
    Una lista doblemente enlazada con punteros a cabeza y cola para máxima eficiencia.
    """

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def siguiente_para_inspeccion(self):
        """
        Elimina y retorna el primer contenedor.
        CORREGIDO para manejar punteros 'anterior' y 'tamanio'.
        """
        if self.cabeza is None:
            # print("No hay contenedores en la lista") # Opcional: imprimir
            return None

        contenedor_a_retornar = self.cabeza.contenedor
        nodo_eliminado = self.cabeza

        self.cabeza = self.cabeza.siguiente
        self.tamanio -= 1  # CORRECCIÓN 1: Actualizar el tamaño.

        if self.cabeza is None:
            # La lista quedó vacía
            self.cola = None
        else:
            # CORRECCIÓN 2: Romper el enlace 'anterior' de la nueva cabeza.
            self.cabeza.anterior = None

        # Opcional: limpiar punteros del nodo eliminado para liberar memoria antes
        nodo_eliminado.siguiente = None
        return contenedor_a_retornar

    
    # VERSIÓN CORREGIDA Y ADAPTADA (es el mismo que ya te había proporcionado)
    def agregar_contenedor_prioritario(self, contenedor):
        """
        Agrega un contenedor manteniendo la lista ordenada por prioridad.
        CORREGIDO para manejar todos los punteros de una lista doble.
        """
        nuevo_nodo = Nodo(contenedor)

        # CASO 1: Lista vacía o el nuevo nodo va al inicio.
        if self.cabeza is None or nuevo_nodo.contenedor.prioridad < self.cabeza.contenedor.prioridad:
            nuevo_nodo.siguiente = self.cabeza
            if self.cabeza:
                # El antiguo 'cabeza' debe apuntar hacia atrás, al nuevo nodo.
                self.cabeza.anterior = nuevo_nodo
            else:
                # Si la lista estaba vacía, el nuevo nodo también es la cola.
                self.cola = nuevo_nodo
            self.cabeza = nuevo_nodo
        # CASO 2: Insertar en el medio o al final.
        else:
            actual = self.cabeza
            # Recorrer hasta encontrar el lugar correcto
            while actual.siguiente and actual.siguiente.contenedor.prioridad <= nuevo_nodo.contenedor.prioridad:
                actual = actual.siguiente

            # Realizar el doble enlace
            nuevo_nodo.siguiente = actual.siguiente
            if actual.siguiente:
                # El nodo que va DESPUÉS del nuevo, debe apuntar hacia atrás a él.
                actual.siguiente.anterior = nuevo_nodo
            else:
                # Si no hay nodo siguiente, el nuevo es la cola.
                self.cola = nuevo_nodo

            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual  # El nuevo nodo debe apuntar hacia atrás.

        self.tamanio += 1  # Siempre se actualiza el tamaño.

    def agregar_al_final(self, contenedor):
        """Agrega un contenedor al final. Útil para construir listas de prueba. O(1)"""
        nuevo_nodo = Nodo(contenedor)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo
        self.tamanio += 1

    def mostrar_adelante(self, mensaje=""):
        """Muestra la lista de cabeza a cola."""
        if mensaje:
            print(mensaje)
        if self.esta_vacia():
            print("LA LISTA ESTÁ VACÍA")
            return
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(str(actual.contenedor))
            actual = actual.siguiente
        print("CABEZA -> " + " <=> ".join(elementos) + " <- COLA")

    # --- MÉTODOS RESUELTOS DE LA GUÍA DE ESTUDIO ---
    def separar_por_tipo(self, tipo_producto):
        """
        Busca contenedores por tipo, los elimina de la lista principal
        y los retorna en una nueva lista. O(n)
        """
        lista_separada = ListaDoblementeEnlazada()
        actual = self.cabeza
        while actual:
            siguiente_nodo = actual.siguiente
            if actual.contenedor.tipo_producto == tipo_producto:
                # --- Desconectar el nodo de la lista principal ---
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:  # Es la cabeza
                    self.cabeza = actual.siguiente

                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:  # Es la cola
                    self.cola = actual.anterior

                self.tamanio -= 1

                # --- Agregar el nodo a la lista separada ---
                actual.anterior = None
                actual.siguiente = None
                if lista_separada.esta_vacia():
                    lista_separada.cabeza = actual
                    lista_separada.cola = actual
                else:
                    lista_separada.cola.siguiente = actual
                    actual.anterior = lista_separada.cola
                    lista_separada.cola = actual
                lista_separada.tamanio += 1
            actual = siguiente_nodo
        return lista_separada

    def mover_al_inicio_por_alerta(self, codigo):
        """
        Busca un contenedor por código y lo mueve al inicio de la lista. O(n)
        """
        actual = self.cabeza
        while actual:
            if actual.contenedor.codigo == codigo:
                if actual == self.cabeza:  # Ya es la cabeza
                    print(f"INFO: El contenedor {codigo} ya está al inicio.")
                    return True

                # --- Desconectar ---
                actual.anterior.siguiente = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:  # Era la cola
                    self.cola = actual.anterior

                # --- Conectar al inicio ---
                actual.anterior = None
                actual.siguiente = self.cabeza
                self.cabeza.anterior = actual
                self.cabeza = actual
                print(f"ÉXITO: Contenedor {codigo} movido al inicio por alerta.")
                return True
            actual = actual.siguiente
        print(f"ERROR: No se encontró el contenedor con código {codigo}.")
        return False

    def fusionar_listas(self, otra_lista):
        """
        Añade todos los elementos de otra_lista al final de esta. O(1)
        """
        if otra_lista.esta_vacia():
            return
        if self.esta_vacia():
            self.cabeza = otra_lista.cabeza
            self.cola = otra_lista.cola
        else:
            self.cola.siguiente = otra_lista.cabeza
            otra_lista.cabeza.anterior = self.cola
            self.cola = otra_lista.cola

        self.tamanio += otra_lista.tamanio
        # Vaciar la otra lista para evitar inconsistencias
        otra_lista.cabeza = None
        otra_lista.cola = None
        otra_lista.tamanio = 0

    # --- NUEVOS MÉTODOS PROPUESTOS ---

    def invertir_orden_de_carga(self):
        """
        Invierte la lista completa en O(n).
        Ideal para cambiar la prioridad de descarga (LIFO en vez de FIFO).
        """
        if self.esta_vacia() or self.cabeza == self.cola:
            return

        actual = self.cabeza
        while actual:
            # Intercambiar punteros anterior y siguiente
            temp = actual.anterior
            actual.anterior = actual.siguiente
            actual.siguiente = temp
            # Moverse al siguiente nodo (que ahora es el 'anterior' original)
            actual = actual.anterior

        # Intercambiar cabeza y cola de la lista
        temp = self.cabeza
        self.cabeza = self.cola
        self.cola = temp

    def eliminar_duplicados_por_codigo(self):
        """
        Elimina contenedores con código duplicado, conservando el primero
        que se encuentra (el más cercano a la cabeza). O(n)
        """
        if self.tamanio < 2:
            return

        codigos_vistos = set()
        actual = self.cabeza
        while actual:
            if actual.contenedor.codigo in codigos_vistos:
                # Eliminar este nodo duplicado
                siguiente = actual.siguiente
                if actual.anterior:
                    actual.anterior.siguiente = siguiente
                if siguiente:
                    siguiente.anterior = actual.anterior

                # Si el duplicado es cabeza o cola
                if actual == self.cabeza: self.cabeza = siguiente
                if actual == self.cola: self.cola = actual.anterior

                self.tamanio -= 1
                actual = siguiente
            else:
                codigos_vistos.add(actual.contenedor.codigo)
                actual = actual.siguiente

    def revision_desde_extremos(self):
        """
        Simula una inspección simultánea desde la cabeza y la cola.
        Retorna pares de contenedores hasta que los punteros se cruzan. O(n)
        """
        if self.esta_vacia():
            print("No hay contenedores para revisar.")
            return

        puntero_izq = self.cabeza
        puntero_der = self.cola
        paso = 1

        print("\n--- INICIANDO REVISIÓN SIMULTÁNEA ---")
        while puntero_izq and puntero_der and puntero_izq.anterior != puntero_der:
            print(
                f"Paso {paso}: Inspector A revisa {puntero_izq.contenedor} | Inspector B revisa {puntero_der.contenedor}")
            if puntero_izq == puntero_der:
                print("--- PUNTEROS SE ENCONTRARON EN EL CENTRO ---")
                break

            puntero_izq = puntero_izq.siguiente
            puntero_der = puntero_der.anterior
            paso += 1
        print("--- FIN DE LA REVISIÓN ---\n")


# --- BLOQUE PRINCIPAL DE PRUEBA ---
if __name__ == "__main__":
    # Creación de contenedores de ejemplo
    c1 = ContenedorPesquero("CHM-HP-001", 25, "harina", "Planta A", "China", 3)
    c2 = ContenedorPesquero("CHM-CONG-101", 20, "congelados", "Planta B", "España", 2)
    c3 = ContenedorPesquero("CHM-FRESH-201", 15, "frescos", "Planta C", "Lima", 1)
    c4 = ContenedorPesquero("CHM-HP-002", 25, "harina", "Planta A", "Vietnam", 3)
    c5 = ContenedorPesquero("CHM-FRESH-202", 18, "frescos", "Planta D", "Trujillo", 1)

    # 1. Prueba de agregar_contenedor_prioritario
    print("===== 1. PRUEBA DE COLA PRIORITARIA =====")
    muelle = ListaDoblementeEnlazada()
    muelle.agregar_contenedor_prioritario(c1)  # P3
    muelle.agregar_contenedor_prioritario(c2)  # P2
    muelle.agregar_contenedor_prioritario(c3)  # P1
    muelle.agregar_contenedor_prioritario(c4)  # P3
    muelle.agregar_contenedor_prioritario(c5)  # P1
    muelle.mostrar_adelante("Estado del muelle ordenado por prioridad:")

    # 2. Prueba de separar_por_tipo
    print("\n===== 2. PRUEBA DE SEPARAR POR TIPO DE PRODUCTO =====")
    print("Separando todos los contenedores de 'frescos'...")
    lista_frescos = muelle.separar_por_tipo("frescos")
    muelle.mostrar_adelante("Estado del muelle después de separar:")
    lista_frescos.mostrar_adelante("Nueva lista solo con productos frescos:")

    # 3. Prueba de mover_al_inicio_por_alerta
    print("\n===== 3. PRUEBA DE MOVER POR ALERTA =====")
    muelle.mostrar_adelante("Muelle antes de la alerta:")
    muelle.mover_al_inicio_por_alerta("CHM-HP-001")
    muelle.mostrar_adelante("Muelle después de mover 'CHM-HP-001' al inicio:")

    # 4. Prueba de fusionar_listas
    print("\n===== 4. PRUEBA DE FUSIONAR LISTAS =====")
    print("El barco con la carga de 'frescos' regresa al muelle principal.")
    muelle.fusionar_listas(lista_frescos)
    muelle.mostrar_adelante("Muelle después de fusionar la carga de frescos:")
    lista_frescos.mostrar_adelante("La lista de frescos ahora debería estar vacía:")

    # 5. Prueba del NUEVO método invertir_orden_de_carga
    print("\n===== 5. PRUEBA DE INVERTIR LA LISTA =====")
    muelle.mostrar_adelante("Orden de carga actual:")
    muelle.invertir_orden_de_carga()
    muelle.mostrar_adelante("Se invierte el orden para descargar los últimos que llegaron:")

    # 6. Prueba del NUEVO método eliminar_duplicados_por_codigo
    print("\n===== 6. PRUEBA DE ELIMINAR DUPLICADOS =====")
    duplicado = ContenedorPesquero("CHM-CONG-101", 22, "congelados", "Planta X", "Italia", 2)
    muelle.agregar_al_final(duplicado)
    muelle.mostrar_adelante("Lista con un contenedor duplicado ('CHM-CONG-101') añadido:")
    muelle.eliminar_duplicados_por_codigo()
    muelle.mostrar_adelante("Lista después de eliminar duplicados:")

    # 7. Prueba del NUEVO método revision_desde_extremos
    print("\n===== 7. PRUEBA DE REVISIÓN DESDE EXTREMOS =====")
    muelle.mostrar_adelante("Contenedores a revisar:")
    muelle.revision_desde_extremos()
