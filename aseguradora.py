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

