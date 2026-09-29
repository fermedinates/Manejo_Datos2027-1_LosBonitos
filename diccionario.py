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