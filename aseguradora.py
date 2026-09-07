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
        #------------En VSC-------
class Asegurado:
    def __init__(self, nombre, edad, fumador, sexo, extra_prima,
                 suma_asegurada):    #Guarda los datos del asegurado
        self.nombre = nombre
        self.edad = edad
        self.fumador = fumador
        self.sexo = sexo
        self.extra_prima = extra_prima
        self.suma_asegurada = suma_asegurada

    def calcular_edad_ajustada(self, considerar_extra=True): #Ajuste de edad
        edad_ajustada = self.edad

        if self.fumador == "No":
            edad_ajustada -= 5

        if self.sexo == "F":
            edad_ajustada -= 10

        if self.extra_prima == "Si" and considerar_extra:
            edad_ajustada += 10

        if edad_ajustada < 18:    #Regula que la edad no salga del rango
            edad_ajustada = 18
        elif edad_ajustada > 99:
            edad_ajustada = 99

        return edad_ajustada

#---Calcular Prima---
class CalculadoraPrima:
    def __init__(self, estrategia_factor):    #Recibe factor de edad a utilizar
        self.estrategia_factor = estrategia_factor

    def calcular_prima(self, asegurado):    #Calcula prima sin EP
        edad_ajustada = asegurado.calcular_edad_ajustada()
        factor = self.estrategia_factor.obtener_factor(edad_ajustada)
        #Factor correspondiente
        prima = asegurado.suma_asegurada * factor / 1000
        return prima
          def calcular_extra_prima(self, asegurado):    #Prima con EP
        if asegurado.extra_prima == "No":
            return 0

        edad_con_extra = asegurado.calcular_edad_ajustada()   #+10 años
        edad_sin_extra = asegurado.calcular_edad_ajustada(False)    #No suma
        #obtiene los 2 factores
        factor_con_extra = self.estrategia_factor.obtener_factor(
            edad_con_extra
        )
        factor_sin_extra = self.estrategia_factor.obtener_factor(
            edad_sin_extra
        )
        #Calcula Primas
        prima_con_extra = (
            asegurado.suma_asegurada * factor_con_extra / 1000
        )
        prima_sin_extra = (
            asegurado.suma_asegurada * factor_sin_extra / 1000
        )

        return prima_con_extra - prima_sin_extra    #Cuanto aumento por EP

