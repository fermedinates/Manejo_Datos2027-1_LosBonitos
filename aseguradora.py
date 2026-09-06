from abc import ABC, abstractmethod

# ---Manejo de excepciones---
#Parámetros de error especificos, nos ayuda para identificar que lo genera
class ErrorDatoInvalido(Exception):
    """Excepción base para datos de entrada no válidos."""


class EdadInvalidaError(ErrorDatoInvalido):
    """Excepción para edades fuera del rango [18, 99]."""


class SexoInvalidoError(ErrorDatoInvalido):
    """Excepción para sexo distinto de 'M' o 'F'."""


class OpcionInvalidaError(ErrorDatoInvalido):
    """Excepción para campos de opción 'Si'/'No' inválidos."""


class SumaAseguradaInvalidaError(ErrorDatoInvalido):
    """Excepción para suma asegurada fuera de [$500,000, $3,000,000]."""


class TasaCambioInvalidaError(ErrorDatoInvalido):
    """Excepción para tasas de cambio menores o iguales a cero."""


#---Clase de Asegurado: Datos del asegurado---


class Asegurado:


    def __init__(
        self,
        edad: int,
        sexo: str,
        es_fumador: str,
        tiene_extra_prima: str,
        suma_asegurada: float
    ) -> None:
        self.edad_original = edad   #Estandarizar texto
        self.sexo = sexo.upper()      
        self.es_fumador = es_fumador.capitalize()
        self.tiene_extra_prima = tiene_extra_prima.capitalize()
        self.suma_asegurada = suma_asegurada
        self.edad_ajustada = self._calcular_edad_ajustada()  
        #self._calcular_edad_ajustada()-Guarda la edad después de los ajustes

    def _calcular_edad_ajustada(self) -> int:   #Realiza los ajustes de edad
      
        edad = self.edad_original

        if self.es_fumador == "No":
            edad -= 5
        if self.sexo == "F":
            edad -= 10
        if self.tiene_extra_prima == "Si":
            edad += 10

        return max(18, min(99, edad)) #Mantiene el valor dentro de [18,99]


