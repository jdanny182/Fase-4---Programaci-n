## Este es el archivo principal: aquí simulo las operaciones para demostrar que el sistema aguanta los errores.

## Traigo todas las clases y funciones que armé en los otros archivos.
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger import iniciar_log, registrar

## Estas son las listas internas donde guardo todo (como no hay base de datos, la memoria es mi "base").
clientes = []
servicios = []
reservas = []


## Esta función me ahorra repetir código: muestra el error en pantalla y lo guarda en el log.
def manejar_error(numero, error):
    ## Muestro el error en consola con el número de la operación.
    print(f"   [Error controlado] {error}")
    ## Si el error viene encadenado, también muestro la causa original.
    if error.__cause__ is not None:
        ## Imprimo la causa original del error.
        print(f"   [Causa original] {error.__cause__}")
    ## Guardo el error en el archivo de logs.
    registrar("ERROR", f"Operación {numero}: {error}")


## Esta es la función principal donde se ejecuta todo.
def main():
    ## Primero dejo el log limpio.
    iniciar_log()
    ## Aviso que arrancó el programa.
    print("=== Sistema de gestión de Software FJ ===\n")
    ## Lo anoto también en el log.
    registrar("INFO", "El programa arrancó.")

    ## ---------- OPERACIÓN 1: cliente válido ----------
    print("Operación 1: registrar un cliente válido")
    ## Uso try/except/else para esta operación.
    try:
        ## Intento crear el cliente.
        cliente1 = Cliente(1, "Ana Torres", "ana@correo.com", "3101234567")
    ## Si falla, atrapo cualquier error del sistema.
    except ErrorSoftwareFJ as error:
        ## Lo manejo con la función de arriba.
        manejar_error(1, error)
    ## Si no hubo error, entra aquí.
    else:
        ## Agrego el cliente a la lista.
        clientes.append(cliente1)
        ## Muestro que se pudo.
        print("   OK ->", cliente1.describir())
        ## Lo registro en el log.
        registrar("INFO", "Operación 1: cliente 1 registrado.")

    ## ---------- OPERACIÓN 2: cliente con correo inválido ----------
    print("Operación 2: registrar un cliente con correo inválido")
    ## Intento crear un cliente con un correo sin arroba.
    try:
        ## Este correo no tiene arroba, debería fallar.
        cliente2 = Cliente(2, "Luis Pérez", "luis.correo.com", "3209876543")
        ## Si por alguna razón no falla, lo agrego.
        clientes.append(cliente2)
    ## Atrapo el error esperado.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(2, error)

    ## ---------- OPERACIÓN 3: cliente con nombre vacío ----------
    print("Operación 3: registrar un cliente con nombre vacío")
    ## Intento crear un cliente sin nombre.
    try:
        ## El nombre va vacío a propósito.
        cliente3 = Cliente(3, "   ", "maria@correo.com", "3001112233")
        ## Si no falla, lo agrego.
        clientes.append(cliente3)
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(3, error)

    ## ---------- OPERACIÓN 4: sala válida ----------
    print("Operación 4: crear una sala válida")
    ## Intento crear la sala.
    try:
        ## Sala con capacidad de 10 personas.
        sala = ReservaSala(101, "Sala Ejecutiva", 50000, 10)
    ## Si falla, lo manejo.
    except ErrorSoftwareFJ as error:
        ## Manejo el error.
        manejar_error(4, error)
    ## Si todo salió bien.
    else:
        ## Agrego la sala a la lista de servicios.
        servicios.append(sala)
        ## Muestro la descripción.
        print("   OK ->", sala.describir())
        ## Lo registro en el log.
        registrar("INFO", "Operación 4: sala 101 creada.")

    ## ---------- OPERACIÓN 5: equipo inválido ----------
    print("Operación 5: crear un equipo con cantidad en cero")
    ## Intento crear un equipo con cantidad 0.
    try:
        ## La cantidad es 0 a propósito, debería fallar.
        equipo_malo = AlquilerEquipo(102, "Portátiles", 20000, "Computador", 0)
        ## Si no falla, lo agrego.
        servicios.append(equipo_malo)
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(5, error)

    ## ---------- OPERACIÓN 6: asesoría válida ----------
    print("Operación 6: crear una asesoría válida")
    ## Intento crear la asesoría.
    try:
        ## Asesoría de nivel avanzado.
        asesoria = AsesoriaEspecializada(103, "Asesoría en Python", 80000, "Carlos Ruiz", "avanzado")
    ## Si falla, lo manejo.
    except ErrorSoftwareFJ as error:
        ## Manejo el error.
        manejar_error(6, error)
    ## Si salió bien.
    else:
        ## La agrego a la lista.
        servicios.append(asesoria)
        ## Muestro la descripción.
        print("   OK ->", asesoria.describir())
        ## Lo registro en el log.
        registrar("INFO", "Operación 6: asesoría 103 creada.")

    ## ---------- OPERACIÓN 7: reserva exitosa ----------
    print("Operación 7: reserva exitosa de la sala por 3 horas")
    ## Intento crear y procesar la reserva.
    try:
        ## Creo la reserva con el primer cliente y la sala.
        reserva1 = Reserva(1, clientes[0], servicios[0], 3)
        ## La proceso y guardo el costo.
        costo = reserva1.procesar()
    ## Si algo falla, lo manejo.
    except ErrorSoftwareFJ as error:
        ## Manejo el error.
        manejar_error(7, error)
    ## Si todo salió bien.
    else:
        ## Guardo la reserva en la lista.
        reservas.append(reserva1)
        ## Muestro el resultado.
        print("   OK ->", reserva1.describir())
        ## Muestro el costo con IVA.
        print(f"   Costo total con IVA: ${costo:.2f}")

    ## ---------- OPERACIÓN 8: reserva con horas negativas ----------
    print("Operación 8: reserva con horas negativas")
    ## Intento crear una reserva con -2 horas.
    try:
        ## Las horas son negativas a propósito.
        reserva2 = Reserva(2, clientes[0], servicios[1], -2)
        ## Si no falla, la agrego.
        reservas.append(reserva2)
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(8, error)

    ## ---------- OPERACIÓN 9: reserva de un servicio no disponible ----------
    print("Operación 9: reservar un servicio que no está disponible")
    ## Intento todo el proceso dentro de un try.
    try:
        ## Creo un equipo válido pero lo dejo no disponible.
        proyector = AlquilerEquipo(104, "Proyector", 15000, "Video beam", 2, disponible=False)
        ## Lo agrego a la lista de servicios.
        servicios.append(proyector)
        ## Creo la reserva con ese servicio.
        reserva3 = Reserva(3, clientes[0], proyector, 4)
        ## La guardo en la lista (todavía está pendiente).
        reservas.append(reserva3)
        ## Intento procesarla, aquí debe fallar porque no está disponible.
        reserva3.procesar()
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo (también muestra la causa original por el encadenamiento).
        manejar_error(9, error)

    ## ---------- OPERACIÓN 10: cancelar dos veces ----------
    print("Operación 10: cancelar la misma reserva dos veces")
    ## Intento cancelar dos veces la reserva 1.
    try:
        ## Primera cancelación, debería funcionar.
        reservas[0].cancelar()
        ## Muestro el nuevo estado.
        print("   Primera cancelación OK ->", reservas[0].estado)
        ## Segunda cancelación, debería fallar.
        reservas[0].cancelar()
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(10, error)

    ## ---------- OPERACIÓN 11: descuento inválido ----------
    print("Operación 11: calcular un costo con descuento mayor al 100%")
    ## Intento calcular el costo con un descuento de 150%.
    try:
        ## El descuento 1.5 es inconsistente, debería fallar.
        total = servicios[0].calcular_costo_total(2, 0.19, 1.5)
        ## Si no falla, lo muestro.
        print("   Total:", total)
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(11, error)

    ## ---------- OPERACIÓN 12: reserva sin cliente ----------
    print("Operación 12: reserva sin cliente (parámetro faltante)")
    ## Intento crear la reserva pasando None como cliente.
    try:
        ## Falta el cliente a propósito.
        reserva4 = Reserva(4, None, servicios[0], 2)
        ## Si no falla, la agrego.
        reservas.append(reserva4)
    ## Atrapo el error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(12, error)

    ## ---------- OPERACIÓN 13: probar las variantes del costo (sobrecarga) ----------
    print("Operación 13: costo de la asesoría con diferentes parámetros")
    ## Uso try/except/finally para variar un poco.
    try:
        ## Solo con las horas.
        print("   Solo horas:", servicios[2].calcular_costo_total(2))
        ## Con horas e impuesto.
        print("   Horas + IVA:", servicios[2].calcular_costo_total(2, 0.19))
        ## Con horas, impuesto y descuento del 10%.
        print("   Horas + IVA + descuento:", servicios[2].calcular_costo_total(2, 0.19, 0.10))
    ## Atrapo cualquier error.
    except ErrorSoftwareFJ as error:
        ## Lo manejo.
        manejar_error(13, error)
    ## Esto se ejecuta siempre.
    finally:
        ## Lo anoto en el log.
        registrar("INFO", "Operación 13 terminada.")

    ## Al final muestro un resumen de lo que quedó guardado en las listas.
    print("\n=== Resumen final ===")
    ## Cuento los clientes.
    print("Clientes registrados:", len(clientes))
    ## Cuento los servicios.
    print("Servicios creados:", len(servicios))
    ## Cuento las reservas.
    print("Reservas guardadas:", len(reservas))
    ## Recorro las reservas para mostrar cada una (aquí también se ve el polimorfismo).
    for reserva in reservas:
        ## Muestro la descripción de la reserva.
        print("  -", reserva.describir())
    ## Recorro los servicios y muestro cada descripción, cada uno responde a su manera.
    for servicio in servicios:
        ## Muestro la descripción del servicio.
        print("  *", servicio.describir())
    ## Aviso que el programa terminó bien, sin caerse.
    print("\nEl programa terminó sin caerse. Revisa logs.txt para ver el registro.")
    ## Lo anoto en el log.
    registrar("INFO", "El programa terminó correctamente.")


## Esto hace que main() se ejecute solo cuando corro este archivo directamente.
if __name__ == "__main__":
    ## Llamo a la función principal.
    main()