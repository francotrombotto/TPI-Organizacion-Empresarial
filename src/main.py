import csv

ESTADO_INICIO = "INICIO"
ESTADO_VALIDANDO_USUARIO = "VALIDANDO_USUARIO"
ESTADO_ESPERANDO_PROBLEMA = "ESPERANDO_PROBLEMA"
ESTADO_BUSCANDO_FAQ = "BUSCANDO_FAQ"
ESTADO_ESPERANDO_CONFIRMACION = "ESPERANDO_CONFIRMACION"
ESTADO_GENERANDO_TICKET = "GENERANDO_TICKET"
ESTADO_DERIVADO_N2 = "DERIVADO_N2"
ESTADO_CERRADO = "CERRADO"


def cargar_usuarios():
    usuarios = {}

    with open("datos/usuarios.csv", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            usuarios[fila["legajo"]] = fila

    return usuarios


def cargar_faq():
    faq = []

    with open("datos/faq.csv", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            faq.append(fila)

    return faq


def buscar_solucion(problema, faq):

    problema = problema.lower()

    for item in faq:

        palabras = item["palabras_clave"].lower().split(",")

        for palabra in palabras:

            if palabra.strip() in problema:
                return item["solucion"]

    return None


def calcular_prioridad(problema):

    problema = problema.lower()

    palabras_alta = [
        "servidor",
        "base de datos",
        "sistema caido",
        "sistema caído"
    ]

    palabras_media = [
        "internet",
        "vpn",
        "red"
    ]

    for palabra in palabras_alta:
        if palabra in problema:
            return "ALTA"

    for palabra in palabras_media:
        if palabra in problema:
            return "MEDIA"

    return "BAJA"


def generar_ticket(usuario, problema, prioridad):

    ruta = "datos/tickets.csv"

    ultimo_id = 0

    with open(ruta, encoding="utf-8") as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            try:
                ultimo_id = int(fila["id_ticket"])
            except:
                pass

    nuevo_id = ultimo_id + 1

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow(
            [
                nuevo_id,
                usuario,
                problema,
                prioridad,
                "ABIERTO"
            ]
        )

    return nuevo_id


def main():

    usuarios = cargar_usuarios()
    faq = cargar_faq()

    print("\n===================================")
    print(" MESA DE AYUDA IT ")
    print("===================================\n")

    legajo = input("Ingrese su legajo: ")

    if not legajo.isdigit():

        print("Error: debe ingresar un número.")
        return

    if legajo not in usuarios:

        print("Error: legajo inexistente.")
        return

    usuario = usuarios[legajo]["nombre"]

    print(f"\nBienvenido {usuario}")

    problema = input("\nDescriba su problema: ").strip()

    if problema == "":
        print("Debe describir un problema.")
        return

    solucion = buscar_solucion(problema, faq)

    if solucion:

        print("\nSe encontró una solución:")
        print(solucion)

        respuesta = input(
            "\n¿El problema fue resuelto? (SI/NO): "
        ).upper()

        while respuesta not in ["SI", "NO"]:

            respuesta = input(
                "Respuesta inválida. Ingrese SI o NO: "
            ).upper()

        if respuesta == "SI":

            print("\nIncidente resuelto.")
            print("Estado:", ESTADO_CERRADO)

        else:

            prioridad = calcular_prioridad(problema)

            ticket = generar_ticket(
                usuario,
                problema,
                prioridad
            )

            print(f"\nTicket generado N° {ticket}")
            print("Prioridad:", prioridad)

            if prioridad == "ALTA":

                print("Derivado a Soporte Nivel 2.")
                print("Estado:", ESTADO_DERIVADO_N2)

            else:

                print("Será atendido por Mesa de Ayuda.")
                print("Estado:", ESTADO_CERRADO)

    else:

        prioridad = calcular_prioridad(problema)

        ticket = generar_ticket(
            usuario,
            problema,
            prioridad
        )

        print(f"\nTicket generado N° {ticket}")
        print("Prioridad:", prioridad)

        if prioridad == "ALTA":

            print("Derivado a Soporte Nivel 2.")
            print("Estado:", ESTADO_DERIVADO_N2)

        else:

            print("Será atendido por Mesa de Ayuda.")
            print("Estado:", ESTADO_CERRADO)


if __name__ == "__main__":
    main()