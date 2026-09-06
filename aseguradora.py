from abc import ABC, abstractmethod   #Abstract Base Class

# ---Manejo de excepciones---
#Parámetros de error especificos, nos ayuda para identificar que lo genera
class EdadInvalidaError(Exception):
    pass


class SexoInvalidoError(Exception):
    pass


class OpcionInvalidaError(Exception):
    pass


class SumaAseguradaInvalidaError(Exception):
    pass


class TasaCambioInvalidaError(Exception):
    pass


#---Factores de edad---
class FactorEdadStrategy(ABC):    #FactorF/M  heredan y siguen su estructura
    @abstractmethod   #Indica que es obligatorio para las clases que hereden
    def obtener_factor(self, edad):   #Estructuras de las subclases
        pass


class FactorFemenino(FactorEdadStrategy):
    def obtener_factor(self, edad):    #Recibe edad y devuelve el factor
        if 18 <= edad <= 25:
            return 1.5
        if edad <= 45:
            return 1.7
        if edad <= 65:
            return 2.0
        return 2.2


class FactorMasculino(FactorEdadStrategy):
    def obtener_factor(self, edad):    #Recibe edad y devuelve el factor
        if 18 <= edad <= 25:
            return 2.0
        if edad <= 45:
            return 2.3
        if edad <= 65:
            return 2.5
        return 3.0