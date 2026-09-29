from abc import ABC, abstractmethod
import time
import unicodedata


class TextoVacioError(Exception):
    pass


class TextoSinPalabrasError(Exception):
    pass


def extraer_palabras(texto):
    if not isinstance(texto, str):
        raise TypeError("El texto debe ser una cadena.")

    if not texto.strip():
        raise TextoVacioError("El texto está vacío.")

    # NFC unifica representaciones equivalentes de caracteres.
    # casefold permite comparar sin distinguir mayúsculas y minúsculas.
    texto = unicodedata.normalize("NFC", texto).casefold()

    caracteres_limpios = []

    for caracter in texto:
        # Conservamos la ñ porque en español es una letra distinta.
        if caracter == "ñ":
            caracteres_limpios.append(caracter)
        else:
            # NFD separa una letra acentuada de su marca diacrítica
            descompuesto = unicodedata.normalize("NFD", caracter)

            for parte in descompuesto:
                # Mn identifica marcas diacríticas, como la tilde de á
                if unicodedata.category(parte) != "Mn":
                    caracteres_limpios.append(parte)

    palabras = []
    palabra_actual = []

    for caracter in caracteres_limpios:
        if caracter.isalpha():
            palabra_actual.append(caracter)
        elif palabra_actual:
            palabras.append("".join(palabra_actual))
            palabra_actual = []

    # Agregamos la última palabra si el texto terminó con una letra
    if palabra_actual:
        palabras.append("".join(palabra_actual))

    if not palabras:
        raise TextoSinPalabrasError("El texto no contiene palabras.")

    return palabras

class TablaHashFrecuencia:
    def __init__(self, capacidad):
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser positiva.")

        self.capacidad = capacidad

        # Cada cubeta tiene su propia lista para resolver colisiones
        self.cubetas = [[] for _ in range(capacidad)]

    def _calcular_indice(self, palabra):
        # Función hash propia: transforma la palabra en un índice
        codigo = 0

        for caracter in palabra:
            codigo = (codigo * 31 + ord(caracter)) % self.capacidad

        return codigo

    def agregar(self, palabra):
        indice = self._calcular_indice(palabra)
        cubeta = self.cubetas[indice]

        # Buscamos solo dentro de la cubeta correspondiente
        for entrada in cubeta:
            if entrada[0] == palabra:
                # Si la palabra ya existe, incrementamos su frecuencia
                entrada[1] += 1
                return

        # Si no existe, agregamos [palabra, frecuencia inicial].
        cubeta.append([palabra, 1])

    def palabras_unicas(self):
        # Devuelve las palabras distintas: aún no están ordenadas.
        resultado = []

        for cubeta in self.cubetas:
            for entrada in cubeta:
                resultado.append(entrada[0])

        return resultado

    def frecuencia(self, palabra):
        # Permite consultar cuántas veces apareció una palabra.
        indice = self._calcular_indice(palabra)
        cubeta = self.cubetas[indice]

        for entrada in cubeta:
            if entrada[0] == palabra:
                return entrada[1]

        return 0


class Ordenador(ABC):
    # Contrato común: todo ordenador implementa ordenar().
    # Esta clase define la operación, pero no el algoritmo.
    @abstractmethod
    def ordenar(self, palabras):
        pass


class MergeSort(Ordenador):
    def ordenar(self, palabras):
        # Caso base: una lista de cero o una palabra ya está ordenada.
        if len(palabras) <= 1:
            return palabras.copy()

        # Dividimos la lista en dos mitades.
        mitad = len(palabras) // 2
        izquierda = self.ordenar(palabras[:mitad])
        derecha = self.ordenar(palabras[mitad:])

        # Ordenamos cada mitad y después las mezclamos.
        return self._mezclar(izquierda, derecha)

    def _mezclar(self, izquierda, derecha):
        resultado = []
        indice_izquierda = 0
        indice_derecha = 0

        # Elegimos primero la palabra menor de las dos mitades.
        while (
            indice_izquierda < len(izquierda)
            and indice_derecha < len(derecha)
        ):
            if izquierda[indice_izquierda] <= derecha[indice_derecha]:
                resultado.append(izquierda[indice_izquierda])
                indice_izquierda += 1
            else:
                resultado.append(derecha[indice_derecha])
                indice_derecha += 1

        # Agregamos lo que haya quedado en alguna de las mitades.
        resultado.extend(izquierda[indice_izquierda:])
        resultado.extend(derecha[indice_derecha:])

        return resultado
   
    # Complejidad temporal: O(n log n) en mejor y peor caso.
    # Divide la lista en dos en cada nivel; mezclar cuesta O(n).
    # Hay aproximadamente log(n) niveles: n * log(n).
    # Memoria auxiliar: O(n).


class QuickSort(Ordenador):
    def ordenar(self, palabras):
        # Ordenamos una copia para conservar la lista original.
        resultado = palabras.copy()
        self._quick_sort(resultado, 0, len(resultado) - 1)
        return resultado

    def _quick_sort(self, palabras, inicio, fin):
        # Caso base: una parte de cero o un elemento ya está ordenada.
        if inicio >= fin:
            return

        indice_izquierda = inicio
        indice_derecha = fin

        # El pivote es el valor ubicado en la posición central.
        pivote = palabras[(inicio + fin) // 2]

        # Particionamos: menores a la izquierda y mayores a la derecha.
        while indice_izquierda <= indice_derecha:
            while palabras[indice_izquierda] < pivote:
                indice_izquierda += 1
                
                while palabras[indice_derecha] > pivote:
                indice_derecha -= 1

            if indice_izquierda <= indice_derecha:
                palabras[indice_izquierda], palabras[indice_derecha] = (
                    palabras[indice_derecha],
                    palabras[indice_izquierda],
                )
                indice_izquierda += 1
                indice_derecha -= 1

        # Repetimos el proceso recursivamente en ambos lados.
        if inicio < indice_derecha:
            self._quick_sort(palabras, inicio, indice_derecha)

        if indice_izquierda < fin:
            self._quick_sort(palabras, indice_izquierda, fin)

    # Complejidad temporal: O(n log n) si las particiones quedan equilibradas.
    # Peor caso: O(n²), si el pivote deja partes de tamaños n-1 y 0
    # Elegir la posición central ayuda, pero no garantiza elegir la mediana
    # Recursión: O(log n) espacio promedio y O(n) en el peor caso.


def palabra_desde_indice(indice):
    # Convierte un índice en una palabra única de tres letras
    # Hay 26 ** 3 combinaciones, suficientes para estas pruebas.
    if not 0 <= indice < 26 ** 3:
        raise ValueError("El índice está fuera del rango generado.")

    letras = []

    for _ in range(3):
        letra = chr(ord("a") + indice % 26)
        letras.append(letra)
        indice //= 26

    return "".join(reversed(letras))


def generar_texto_prueba(cantidad_palabras):
    # Generamos palabras distintas y repetimos la primera una vez.
    # Así el texto tiene exactamente la cantidad solicitada de palabras.
    if cantidad_palabras < 2:
        raise ValueError("Se necesitan al menos dos palabras.")

    tokens = [
        palabra_desde_indice(indice)
        for indice in range(cantidad_palabras - 1)
    ]
    tokens.append(tokens[0])

    return " ".join(tokens)
    
    def medir_tabla_hash(palabras, repeticiones):
    tiempos = []
    tabla_ultima = None

    for _ in range(repeticiones):
        inicio = time.perf_counter()

        capacidad = 2 * len(palabras) + 1
        tabla = TablaHashFrecuencia(capacidad)

        for palabra in palabras:
            tabla.agregar(palabra)

        fin = time.perf_counter()
        tiempos.append(fin - inicio)
        tabla_ultima = tabla

    promedio = sum(tiempos) / repeticiones
    return promedio, tabla_ultima