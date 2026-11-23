## Aquí está la clase abstracta que sirve de base para todo lo demás (clientes, servicios y reservas).

## Importo ABC y abstractmethod, que son lo que Python necesita para crear clases abstractas.
from abc import ABC, abstractmethod


## Esta clase no se puede instanciar directamente, solo sirve de molde para las otras.
class Entidad(ABC):
    ## El constructor recibe el identificador que va a tener cada entidad.
    def __init__(self, id_entidad):
        ## Guardo el id con guion bajo para indicar que es privado (encapsulación).
        self._id = id_entidad

    ## Con property dejo que el id se pueda leer desde afuera, pero no cambiar por accidente.
    @property
    def id(self):
        ## Devuelvo el id guardado.
        return self._id

    ## Este método es abstracto: todas las clases hijas están obligadas a escribir su propia versión.
    @abstractmethod
    def describir(self):
        ## Aquí no se escribe nada, cada hija lo implementa a su manera.
        pass