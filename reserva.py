## Aquí está la clase Reserva, que junta al cliente, el servicio, las horas y el estado.

## Traigo la clase base y las clases que necesito relacionar.
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
## Traigo las excepciones que voy a usar.
from excepciones import (ErrorSoftwareFJ, ReservaInvalidaError, ServicioNoDisponibleError)
## Traigo la función para escribir en el log.
from logger import registrar


## Reserva también hereda de Entidad.
class Reserva(Entidad):
    ## El constructor recibe el cliente, el servicio y cuántas horas se reservan.
    def __init__(self, id_reserva, cliente, servicio, horas):
        ## Le paso el id a la clase padre.
        super().__init__(id_reserva)
        ## Reviso que realmente me hayan dado un cliente (si falta, es un parámetro faltante).
        if not isinstance(cliente, Cliente):
            ## Si no es un Cliente, lanzo el error.
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        ## Reviso que me hayan dado un servicio válido.
        if not isinstance(servicio, Servicio):
            ## Si no es un Servicio, lanzo el error.
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        ## Reviso que las horas sean un entero mayor que cero.
        if not isinstance(horas, int) or horas <= 0:
            ## Si no, lanzo el error.
            raise ReservaInvalidaError("La duración debe ser un número entero de horas mayor que cero.")
        ## Guardo el cliente.
        self._cliente = cliente
        ## Guardo el servicio.
        self._servicio = servicio
        ## Guardo las horas.
        self._horas = horas
        ## Toda reserva nueva empieza como pendiente.
        self._estado = "pendiente"

    ## Getter del estado para poder consultarlo desde afuera.
    @property
    def estado(self):
        ## Devuelvo el estado actual.
        return self._estado

    ## Getter del servicio (lo necesito en el main).
    @property
    def servicio(self):
        ## Devuelvo el servicio.
        return self._servicio

    ## Getter de las horas.
    @property
    def horas(self):
        ## Devuelvo las horas.
        return self._horas

    ## Confirma la reserva si se puede.
    def confirmar(self):
        ## Solo se puede confirmar si está pendiente.
        if self._estado != "pendiente":
            ## Si ya estaba confirmada o cancelada, no se permite.
            raise ReservaInvalidaError(f"No se puede confirmar una reserva que está {self._estado}.")
        ## Reviso que el servicio esté disponible.
        if not self._servicio.disponible:
            ## Si no lo está, lanzo el error de servicio no disponible.
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible.")
        ## Si todo está bien, cambio el estado.
        self._estado = "confirmada"
        ## Dejo constancia en el log.
        registrar("INFO", f"Reserva {self.id} confirmada.")

    ## Cancela la reserva si se puede.
    def cancelar(self):
        ## No tiene sentido cancelar algo que ya está cancelado.
        if self._estado == "cancelada":
            ## Lanzo el error.
            raise ReservaInvalidaError("La reserva ya estaba cancelada.")
        ## Cambio el estado a cancelada.
        self._estado = "cancelada"
        ## Dejo constancia en el log.
        registrar("INFO", f"Reserva {self.id} cancelada.")

    ## Procesa la reserva completa: la confirma y calcula cuánto cuesta (con IVA del 19%).
    def procesar(self):
        ## Empiezo el bloque donde pueden pasar errores.
        try:
            ## Primero intento confirmar.
            self.confirmar()
            ## Luego calculo el costo total con 19% de impuesto y sin descuento.
            costo = self._servicio.calcular_costo_total(self._horas, 0.19)
        ## Atrapo cualquier error propio del sistema.
        except ErrorSoftwareFJ as error:
            ## Dejo el error original en el log.
            registrar("ERROR", f"Falló el procesamiento de la reserva {self.id}: {error}")
            ## Lanzo un error nuevo pero encadenado con "from", para no perder la causa original.
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.id}.") from error
        ## El else se ejecuta solo si NO hubo errores en el try.
        else:
            ## Dejo constancia del éxito en el log.
            registrar("INFO", f"Reserva {self.id} procesada. Costo total: ${costo:.2f}")
            ## Devuelvo el costo calculado.
            return costo
        ## El finally se ejecuta siempre, haya error o no.
        finally:
            ## Aviso en el log que terminó el intento de procesamiento.
            registrar("INFO", f"Terminó el intento de procesar la reserva {self.id}.")

    ## Versión de describir() para la reserva.
    def describir(self):
        ## Devuelvo un resumen de la reserva.
        return (f"Reserva #{self.id} | Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | {self._horas} h | Estado: {self._estado}")