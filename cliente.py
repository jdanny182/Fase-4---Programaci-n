## En este archivo está la clase Cliente, con sus datos protegidos y sus validaciones.

## Traigo la clase base de la que hereda Cliente.
from entidad import Entidad
## Traigo la excepción personalizada que voy a lanzar cuando un dato venga mal.
from excepciones import ClienteInvalidoError


## Cliente hereda de Entidad, por eso también tiene id y el método describir.
class Cliente(Entidad):
    ## El constructor recibe todos los datos personales del cliente.
    def __init__(self, id_cliente, nombre, correo, telefono):
        ## Le paso el id a la clase padre para que lo guarde.
        super().__init__(id_cliente)
        ## Al asignar así se ejecutan los setters de abajo, o sea que las validaciones corren desde el inicio.
        self.nombre = nombre
        ## Igual aquí, esto valida el correo antes de guardarlo.
        self.correo = correo
        ## Y aquí se valida el teléfono.
        self.telefono = telefono

    ## Getter del nombre: permite leerlo sin tocar el atributo privado.
    @property
    def nombre(self):
        ## Devuelvo el nombre guardado.
        return self._nombre

    ## Setter del nombre: antes de guardarlo revisa que sea válido.
    @nombre.setter
    def nombre(self, valor):
        ## Si no es texto o está vacío (o solo tiene espacios), no sirve.
        if not isinstance(valor, str) or valor.strip() == "":
            ## Lanzo el error personalizado con un mensaje claro.
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        ## Si es muy corto tampoco lo acepto, pido mínimo 3 letras.
        if len(valor.strip()) < 3:
            ## Lanzo el error porque el nombre es demasiado corto.
            raise ClienteInvalidoError("El nombre del cliente es demasiado corto.")
        ## Si pasó todo, lo guardo sin espacios sobrantes.
        self._nombre = valor.strip()

    ## Getter del correo.
    @property
    def correo(self):
        ## Devuelvo el correo guardado.
        return self._correo

    ## Setter del correo con su validación.
    @correo.setter
    def correo(self, valor):
        ## Reviso que sea texto, que tenga arroba y que no tenga espacios.
        if not isinstance(valor, str) or "@" not in valor or " " in valor:
            ## Si no cumple, lanzo el error.
            raise ClienteInvalidoError("El correo no tiene un formato válido.")
        ## Separo lo que va después de la arroba para revisar que tenga un punto (como .com).
        dominio = valor.split("@")[-1]
        ## Si el dominio no tiene punto, el correo está mal.
        if "." not in dominio:
            ## Lanzo el error por dominio inválido.
            raise ClienteInvalidoError("El dominio del correo no es válido.")
        ## Si todo está bien, guardo el correo.
        self._correo = valor

    ## Getter del teléfono.
    @property
    def telefono(self):
        ## Devuelvo el teléfono guardado.
        return self._telefono

    ## Setter del teléfono con su validación.
    @telefono.setter
    def telefono(self, valor):
        ## Debe ser texto, tener solo números y entre 7 y 10 dígitos.
        if not isinstance(valor, str) or not valor.isdigit() or not (7 <= len(valor) <= 10):
            ## Si no cumple, lanzo el error.
            raise ClienteInvalidoError("El teléfono debe tener solo números (entre 7 y 10 dígitos).")
        ## Si pasó la validación, lo guardo.
        self._telefono = valor

    ## Esta es la versión de describir() para el cliente (sobrescribe la abstracta).
    def describir(self):
        ## Devuelvo un texto con los datos principales del cliente.
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | Tel: {self.telefono}"