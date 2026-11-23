## Aquí están la clase abstracta Servicio y los tres servicios que heredan de ella.

## Traigo la clase base Entidad y la herramienta para métodos abstractos.
from entidad import Entidad
from abc import abstractmethod
## Traigo las excepciones que voy a necesitar en los servicios.
from excepciones import ServicioInvalidoError, CalculoInconsistenteError


## Servicio es abstracta: define lo que todos los servicios deben tener, pero no se puede crear sola.
class Servicio(Entidad):
    ## El constructor guarda los datos comunes a todos los servicios.
    def __init__(self, id_servicio, nombre, precio_base, disponible=True):
        ## Le paso el id a la clase padre.
        super().__init__(id_servicio)
        ## Reviso que el nombre sea texto y no esté vacío.
        if not isinstance(nombre, str) or nombre.strip() == "":
            ## Si no sirve, lanzo el error del servicio.
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío.")
        ## Reviso que el precio sea un número mayor que cero.
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            ## Si no sirve, lanzo el error.
            raise ServicioInvalidoError("El precio base debe ser un número mayor que cero.")
        ## Guardo el nombre como atributo privado.
        self._nombre = nombre.strip()
        ## Guardo el precio base por hora.
        self._precio_base = precio_base
        ## Guardo si el servicio está disponible o no.
        self._disponible = disponible

    ## Getter del nombre.
    @property
    def nombre(self):
        ## Devuelvo el nombre.
        return self._nombre

    ## Getter del precio base.
    @property
    def precio_base(self):
        ## Devuelvo el precio base.
        return self._precio_base

    ## Getter de la disponibilidad.
    @property
    def disponible(self):
        ## Devuelvo True o False según esté disponible.
        return self._disponible

    ## Setter de disponibilidad, para poder activar o desactivar el servicio.
    @disponible.setter
    def disponible(self, valor):
        ## Solo acepto True o False.
        if not isinstance(valor, bool):
            ## Si mandan otra cosa, lanzo el error.
            raise ServicioInvalidoError("La disponibilidad debe ser True o False.")
        ## Guardo el nuevo valor.
        self._disponible = valor

    ## Método abstracto: cada servicio calcula su costo base a su manera.
    @abstractmethod
    def calcular_costo(self, horas):
        ## No se escribe nada aquí.
        pass

    ## Método abstracto: cada servicio revisa sus propios parámetros.
    @abstractmethod
    def validar_parametros(self):
        ## No se escribe nada aquí.
        pass

    ## Este es el método "sobrecargado": Python no tiene sobrecarga real, así que uso parámetros opcionales.
    ## Se puede llamar solo con horas, con horas e impuesto, o con horas, impuesto y descuento.
    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):
        ## Reviso que el impuesto no sea negativo.
        if impuesto < 0:
            ## Un impuesto negativo no tiene sentido, lanzo el error.
            raise CalculoInconsistenteError("El impuesto no puede ser negativo.")
        ## Reviso que el descuento esté entre 0 y 1 (0 = nada, 1 = 100%).
        if descuento < 0 or descuento > 1:
            ## Un descuento fuera de ese rango es inconsistente.
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 1.")
        ## Calculo el costo base usando la versión de cada hijo (aquí se ve el polimorfismo).
        costo = self.calcular_costo(horas)
        ## Le resto el descuento.
        costo = costo * (1 - descuento)
        ## Le sumo el impuesto.
        costo = costo * (1 + impuesto)
        ## Devuelvo el total final.
        return costo


## Primer servicio: reserva de salas.
class ReservaSala(Servicio):
    ## Además de los datos comunes, la sala tiene una capacidad de personas.
    def __init__(self, id_servicio, nombre, precio_base, capacidad, disponible=True):
        ## Llamo al constructor del padre para los datos comunes.
        super().__init__(id_servicio, nombre, precio_base, disponible)
        ## Guardo la capacidad de la sala.
        self._capacidad = capacidad
        ## Valido los datos propios de la sala apenas se crea.
        self.validar_parametros()

    ## Reviso que la capacidad tenga sentido.
    def validar_parametros(self):
        ## Debe ser un entero mayor que cero.
        if not isinstance(self._capacidad, int) or self._capacidad <= 0:
            ## Si no, lanzo el error.
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero mayor que cero.")

    ## El costo de la sala es simplemente el precio por las horas.
    def calcular_costo(self, horas):
        ## Devuelvo precio por horas.
        return self._precio_base * horas

    ## Texto que describe la sala.
    def describir(self):
        ## Devuelvo los datos de la sala.
        return f"Sala '{self.nombre}' | Capacidad: {self._capacidad} personas | ${self._precio_base} por hora"


## Segundo servicio: alquiler de equipos.
class AlquilerEquipo(Servicio):
    ## El equipo tiene un tipo y una cantidad de unidades.
    def __init__(self, id_servicio, nombre, precio_base, tipo_equipo, cantidad, disponible=True):
        ## Llamo al constructor del padre.
        super().__init__(id_servicio, nombre, precio_base, disponible)
        ## Guardo el tipo de equipo.
        self._tipo_equipo = tipo_equipo
        ## Guardo cuántas unidades se alquilan.
        self._cantidad = cantidad
        ## Valido los datos propios del equipo.
        self.validar_parametros()

    ## Reviso el tipo y la cantidad.
    def validar_parametros(self):
        ## El tipo de equipo no puede estar vacío.
        if not isinstance(self._tipo_equipo, str) or self._tipo_equipo.strip() == "":
            ## Si está vacío, lanzo el error.
            raise ServicioInvalidoError("El tipo de equipo no puede estar vacío.")
        ## La cantidad debe ser un entero de al menos 1.
        if not isinstance(self._cantidad, int) or self._cantidad < 1:
            ## Si no, lanzo el error.
            raise ServicioInvalidoError("La cantidad de equipos debe ser mínimo 1.")

    ## El costo depende del precio, las horas y las unidades alquiladas.
    def calcular_costo(self, horas):
        ## Multiplico las tres cosas.
        return self._precio_base * horas * self._cantidad

    ## Texto que describe el equipo.
    def describir(self):
        ## Devuelvo los datos del equipo.
        return f"Equipo '{self.nombre}' ({self._tipo_equipo}) | Unidades: {self._cantidad} | ${self._precio_base} por hora"


## Tercer servicio: asesorías especializadas.
class AsesoriaEspecializada(Servicio):
    ## La asesoría tiene un especialista y un nivel (básico o avanzado).
    def __init__(self, id_servicio, nombre, precio_base, especialista, nivel, disponible=True):
        ## Llamo al constructor del padre.
        super().__init__(id_servicio, nombre, precio_base, disponible)
        ## Guardo el nombre del especialista.
        self._especialista = especialista
        ## Guardo el nivel de la asesoría.
        self._nivel = nivel
        ## Valido los datos propios de la asesoría.
        self.validar_parametros()

    ## Reviso especialista y nivel.
    def validar_parametros(self):
        ## El especialista no puede estar vacío.
        if not isinstance(self._especialista, str) or self._especialista.strip() == "":
            ## Si está vacío, lanzo el error.
            raise ServicioInvalidoError("La asesoría necesita un especialista.")
        ## El nivel solo puede ser "basico" o "avanzado".
        if self._nivel not in ("basico", "avanzado"):
            ## Si es otra cosa, lanzo el error.
            raise ServicioInvalidoError("El nivel debe ser 'basico' o 'avanzado'.")

    ## El costo es por hora, pero el nivel avanzado cuesta 50% más.
    def calcular_costo(self, horas):
        ## Calculo el costo normal.
        costo = self._precio_base * horas
        ## Si es avanzado, le subo el 50%.
        if self._nivel == "avanzado":
            ## Multiplico por 1.5.
            costo = costo * 1.5
        ## Devuelvo el costo final.
        return costo

    ## Texto que describe la asesoría.
    def describir(self):
        ## Devuelvo los datos de la asesoría.
        return f"Asesoría '{self.nombre}' con {self._especialista} | Nivel: {self._nivel} | ${self._precio_base} por hora"