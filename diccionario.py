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
