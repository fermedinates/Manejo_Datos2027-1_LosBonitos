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
    def __init__(self, nombre, edad, fumador, sexo, extra_prima,   #
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
    def calcular_extra_prima(self, asegurado):    #Calcula el costo adicional de la extraprima 
        if asegurado.extra_prima == "No": 
            return 0  #Si no tiene extraprima no tiene un costo adicional

        edad_con_extra = asegurado.calcular_edad_ajustada()   #obtiene la edad ajustada considerando los 10 años de la EP
        edad_sin_extra = asegurado.calcular_edad_ajustada(False)    #Obtiene la edad ajustada sin sumar los 10 años de la EP 
        #obtiene los 2 factores correspondientes a cada edad 
        factor_con_extra = self.estrategia_factor.obtener_factor(
            edad_con_extra #Factor correspondiete edad con extra  prima 
        )
        factor_sin_extra = self.estrategia_factor.obtener_factor(
            edad_sin_extra
        )
        #Calcula Primas para poder obtener unicamente el incremento de la EP
        prima_con_extra = (
            asegurado.suma_asegurada * factor_con_extra / 1000
        )  #Prima calculada considerando La EP
        prima_sin_extra = (
            asegurado.suma_asegurada * factor_sin_extra / 1000
        ) #Prima calculada sin agregar la extra prima

        return prima_con_extra - prima_sin_extra    #Cuanto aumento por EP    la diferencia represewnta el costo adicional de la extraprima 

#---Tipo de Cambio---
class ProveedorTipoCambio(ABC):
    @abstractmethod
    def obtener_tasa(self):   #Si se tiene un tipo de cambio, debe obtener_tas
        pass


class TipoCambioFijo(ProveedorTipoCambio):    #Tasa fija
    def __init__(self, tasa=21.13):
        if tasa <= 0:   #Exitar negativos o 0
            raise TasaCambioInvalidaError(
                "La tasa de cambio debe ser mayor que cero."
            )
        self.tasa = tasa

    def obtener_tasa(self):
        return self.tasa    #Regresa la tasa que se guardo


class ConversorMoneda:    #Convierte MXN aUSD
    def __init__(self, proveedor_tipo_cambio):    #Recibe la tasa de cambio
        self.proveedor_tipo_cambio = proveedor_tipo_cambio

    def convertir_a_usd(self, cantidad_mxn):
        tasa = self.proveedor_tipo_cambio.obtener_tasa()    #Se obtiene la tasa

        if tasa <= 0:
            raise TasaCambioInvalidaError(
                "No se puede convertir con una tasa inválida."
            )

        return cantidad_mxn / tasa    #Pesos a DÓlares

#---Datos del CLiente---
class EntradaDatos:
    @staticmethod
    def pedir_nombre():   #Nombre cliente
        while True:
            nombre = input("Nombre del asegurado: ").strip()
            if nombre:
                return nombre
            print("El nombre no puede estar vacío.")

    @staticmethod
    def pedir_edad():   #Edad
        while True:
            try:
                edad = int(input("Edad: "))
                if edad < 18 or edad > 99:    #Edad entre 18-99
                    raise EdadInvalidaError(
                        "La edad debe estar entre 18 y 99."
                    )
                return edad
            except ValueError:
                print("Error: escribe la edad como un número entero.")
            except EdadInvalidaError as error:
                print("Error:", error)

    @staticmethod
    def pedir_sexo():   #Sexo
        while True:
            try:
                sexo = input("Sexo (M/F): ").strip().upper()
                if sexo not in ("M", "F"):    #Solo se permiten M o F
                    raise SexoInvalidoError(
                        "Solo se permite M o F."
                    )
                return sexo
            except SexoInvalidoError as error:
                print("Error:", error)

    @staticmethod
    def pedir_opcion(mensaje):    #Función para pedir Si/No en EP y fumador
        while True:
            try:
                opcion = input(mensaje).strip().capitalize()
                if opcion not in ("Si", "No"):
                    raise OpcionInvalidaError(
                        "Solo se permite escribir Si o No."
                    )
                return opcion
            except OpcionInvalidaError as error:
                print("Error:", error)

    @staticmethod
    def pedir_suma_asegurada():   #Suma Asegurada
        while True:
            try:
                suma = float(input("Suma asegurada en MXN: "))
                if suma < 500000 or suma > 3000000:
                    raise SumaAseguradaInvalidaError(
                        "La suma debe estar entre $500,000 y $3,000,000."
                    )
                return suma
            except ValueError:
                print("Error: escribe una cantidad numérica.")
            except SumaAseguradaInvalidaError as error:
                print("Error:", error)

    @staticmethod
    def pedir_cantidad_asegurados():    #Num personas
        while True:
            try:
                cantidad = int(input("¿Cuántos asegurados vas a registrar? "))
                if cantidad <= 0:
                    raise ValueError
                return cantidad
            except ValueError:
                print("Ingresa un número entero mayor que cero.")

#--- Carnet---
class ExportadorCarnet:   #Archivo .txt
    @staticmethod
    def guardar(numero, asegurado, edad_ajustada, prima_mxn, prima_usd):
    #Datos para crear el archivo
        nombre_archivo = f"carnet_{numero}.txt"

        try:    #Intento para guardar el txt
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("CARNET\n")   #Datos dentro del archivo
                archivo.write(f"Nombre: {asegurado.nombre}\n")
                archivo.write(f"Edad: {asegurado.edad}\n")
                archivo.write(f"Edad ajustada: {edad_ajustada}\n")
                archivo.write(f"Sexo: {asegurado.sexo}\n")
                archivo.write(f"Fumador: {asegurado.fumador}\n")
                archivo.write(
                    f"Extra-prima: {asegurado.extra_prima}\n"
                )
                archivo.write(
                    f"Suma asegurada: ${asegurado.suma_asegurada:,.2f} MXN\n"
                )
                archivo.write(f"Prima anual: ${prima_mxn:,.2f} MXN\n")
                archivo.write(f"Prima anual: ${prima_usd:,.2f} USD\n")

            print(f"Carnet guardado en {nombre_archivo}")   #Avisa que se guardo
        except OSError as error:    #Por un problema marca error, y continua
            print("No se pudo guardar el carnet:", error)


def crear_estrategia(sexo):   #Si se usa el FactorFem/Mas
    if sexo == "F":
        return FactorFemenino()
    return FactorMasculino()


def mostrar_reporte(resultados):    #Toma los datos para hacer un resumen
    primas = []   #Lista para guardar la prima mxn de casa asegurado

    for resultado in resultados:
        primas.append(resultado["prima_mxn"])   #Guarda en la lista

    promedio = sum(primas) / len(primas)    #Análisis
    prima_maxima = max(primas)
    prima_minima = min(primas)

    print(f" \n REPORTE")
    print(f"Prima promedio: ${promedio:,.2f} MXN")
    print(f"Prima máxima: ${prima_maxima:,.2f} MXN")
    print(f"Prima mínima: ${prima_minima:,.2f} MXN")

    con_extra = []    #Guarda asegurados con EP
    for resultado in resultados:
        if resultado["asegurado"].extra_prima == "Si":
            con_extra.append(resultado)

    if con_extra:   #Si tiene EP dic quien tuvo la EP más alta
        mayor_extra = max(
            con_extra,
            key=lambda resultado: resultado["monto_extra_prima"]
        )
        asegurado = mayor_extra["asegurado"]
        monto = mayor_extra["monto_extra_prima"]
        print(
            "Asegurado con la extra-prima más alta: "
            f"{asegurado.nombre} (${monto:,.2f} MXN)"
        )
    else:
        print("Ningún asegurado tiene extra-prima.")

#---Principal---
def main():
    print("CALCULADORA DE SEGUROS")

    try:    #Tipo de cambio, MXN a USA
        proveedor = TipoCambioFijo()
        conversor = ConversorMoneda(proveedor)
    except TasaCambioInvalidaError as error:
        print("Error con la tasa de cambio:", error)
        return

    cantidad = EntradaDatos.pedir_cantidad_asegurados()  #Guarda num de cliente
    resultados = []   #Guarda los datos de los clientes

    for numero in range(1, cantidad + 1):   #Repite según los asegurados
        print(f"\nASEGURADO {numero}")

        nombre = EntradaDatos.pedir_nombre()
        edad = EntradaDatos.pedir_edad()
        sexo = EntradaDatos.pedir_sexo()
        fumador = EntradaDatos.pedir_opcion("¿Es fumador? (Si/No): ")
        extra_prima = EntradaDatos.pedir_opcion(
            "¿Tiene extra-prima? (Si/No): "
        )
        suma_asegurada = EntradaDatos.pedir_suma_asegurada()

        asegurado = Asegurado(
            nombre,
            edad,
            fumador,
            sexo,
            extra_prima,
            suma_asegurada
        )

        estrategia = crear_estrategia(sexo)   #Estrategia
        calculadora = CalculadoraPrima(estrategia)

        prima_mxn = calculadora.calcular_prima(asegurado)    #Prima en mxn
        prima_usd = conversor.convertir_a_usd(prima_mxn)    #Prima en usa
        monto_extra = calculadora.calcular_extra_prima(asegurado)
        edad_ajustada = asegurado.calcular_edad_ajustada()

        print(f"Edad ajustada: {edad_ajustada}")
        print(f"Prima anual: ${prima_mxn:,.2f} MXN")
        print(f"Prima anual: ${prima_usd:,.2f} USD")

        resultados.append({
            "asegurado": asegurado,
            "prima_mxn": prima_mxn,
            "prima_usd": prima_usd,
            "monto_extra_prima": monto_extra
        })    #Guarda la información en la lista resultados

        ExportadorCarnet.guardar(
            numero,
            asegurado,
            edad_ajustada,
            prima_mxn,
            prima_usd
        )

    mostrar_reporte(resultados)


if __name__ == "__main__":
    main()    #Que el programa funcione en orden

