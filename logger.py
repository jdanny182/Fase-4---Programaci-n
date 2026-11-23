## Este archivo se encarga del registro de eventos y errores en un archivo de texto (el log).

## Importo datetime para poder ponerle fecha y hora a cada línea que guardo.
import datetime

## Aquí defino el nombre del archivo donde se va a guardar todo.
ARCHIVO_LOG = "logs.txt"


## Esta función deja el archivo limpio al arrancar el programa, así cada ejecución empieza desde cero.
def iniciar_log():
    ## Uso try por si el archivo no se puede crear (falta de permisos, por ejemplo).
    try:
        ## Abro el archivo en modo "w", que borra lo que había antes.
        with open(ARCHIVO_LOG, "w", encoding="utf-8") as archivo:
            ## Escribo un título para saber dónde empieza el registro.
            archivo.write("=== Inicio del registro de Software FJ ===\n")
    ## Si algo sale mal con el archivo, lo atrapo para que el programa no se caiga.
    except OSError as error:
        ## Muestro el problema en pantalla porque no puedo guardarlo en el log.
        print("No se pudo crear el archivo de log:", error)


## Esta función guarda una línea en el log. Recibe el nivel (INFO o ERROR) y el mensaje.
def registrar(nivel, mensaje):
    ## Saco la fecha y hora actual y le doy un formato fácil de leer.
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ## Armo la línea completa con la hora, el nivel y el mensaje.
    linea = f"[{ahora}] [{nivel}] {mensaje}\n"
    ## Intento escribir en el archivo.
    try:
        ## Uso el modo "a" para agregar al final sin borrar lo anterior.
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            ## Guardo la línea en el archivo.
            archivo.write(linea)
    ## Si falla la escritura, lo atrapo para que el sistema siga vivo.
    except OSError as error:
        ## Aviso por pantalla porque el log no funcionó.
        print("No se pudo escribir en el log:", error)