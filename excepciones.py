## En este archivo dejo todas las excepciones propias del proyecto, para no repetirlas en otros lados.

## Esta es la excepción "madre". Las demás heredan de ella, así puedo atrapar cualquier error del sistema con una sola línea.
class ErrorSoftwareFJ(Exception):
    ## No le agrego nada, solo sirve para agrupar todos los errores de Software FJ.
    pass


## Esta se lanza cuando los datos de un cliente no son correctos (nombre vacío, correo raro, etc.).
class ClienteInvalidoError(ErrorSoftwareFJ):
    ## Tampoco necesita nada extra, con el nombre ya se entiende de qué trata.
    pass


## Esta se usa cuando un servicio se intenta crear con datos que no sirven (precio negativo, cantidad en cero...).
class ServicioInvalidoError(ErrorSoftwareFJ):
    ## Solo hereda, no hay nada más que hacer aquí.
    pass


## Esta aparece cuando alguien quiere reservar un servicio que en ese momento no está disponible.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    ## Igual que las anteriores, solo hereda.
    pass


## Esta es para los problemas con las reservas (horas negativas, reserva ya cancelada, falta el cliente...).
class ReservaInvalidaError(ErrorSoftwareFJ):
    ## Solo hereda de la clase madre.
    pass


## Esta se lanza cuando un cálculo de costos no tiene sentido (por ejemplo un descuento mayor al 100%).
class CalculoInconsistenteError(ErrorSoftwareFJ):
    ## Solo hereda de la clase madre.
    pass