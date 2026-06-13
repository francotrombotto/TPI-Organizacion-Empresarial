import csv
import os

ESTADO_INICIO = "INICIO"
ESTADO_VALIDANDO_USUARIO = "VALIDANDO_USUARIO"
ESTADO_ESPERANDO_PROBLEMA = "ESPERANDO_PROBLEMA"
ESTADO_BUSCANDO_FAQ = "BUSCANDO_FAQ"
ESTADO_ESPERANDO_CONFIRMACION = "ESPERANDO_CONFIRMACION"
ESTADO_GENERANDO_TICKET = "GENERANDO_TICKET"
ESTADO_EVALUANDO_PRIORIDAD = "EVALUANDO_PRIORIDAD"
ESTADO_DERIVADO_N2 = "DERIVADO_N2"
ESTADO_CERRADO = "CERRADO"


def cargar_usuarios():
    usuarios = {}

    with open("../datos/usuarios.csv", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            usuarios[fila["legajo"]] = fila

    return usuarios


def cargar_faq():
    faq = []

    with open("../datos/faq.csv", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            faq.append(fila)

    return faq


def buscar_solucion(problema, faq):

    problema = problema.lower()

    for item in faq:

        palabra_clave = item["problema"].lower()

        if palabra_clave in problema:
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
        "red",
        "vpn"
    ]

    for palabra in palabras_alta:
        if palabra in problema:
            return "ALTA"

    for palabra in palabras_media:
        if palabra in problema:
            return "MEDIA"

    return "BAJA"


def generar_ticket(usuario, problema, prioridad):

    ruta = "../datos/tickets.csv"

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

    estado = ESTADO_INICIO

    usuarios = cargar_usuarios()
    faq = cargar_faq()

    print("\n===================================")
    print(" MESA DE AYUDA IT ")
    print("===================================\n")

    estado = ESTADO_VALIDANDO_USUARIO

    legajo = input("Ingrese su legajo: ")

    if not legajo.isdigit():

        print("Error: debe ingresar un número.")
        return

    if legajo not in usuarios:

        print("Error: legajo inexistente.")
        return

    usuario = usuarios[legajo]["nombre"]

    print(f"\nBienvenido {usuario}")

    estado = ESTADO_ESPERANDO_PROBLEMA

    problema = input("\nDescriba su problema: ").strip()

    if problema == "":
        print("Debe describir un problema.")
        return

    estado = ESTADO_BUSCANDO_FAQ

    solucion = buscar_solucion(problema, faq)

    if solucion:

        print("\nSe encontró una solución:")
        print(solucion)

        estado = ESTADO_ESPERANDO_CONFIRMACION

        respuesta = input(
            "\n¿El problema fue resuelto? (SI/NO): "
        ).upper()

        while respuesta not in ["SI", "NO"]:

            respuesta = input(
                "Respuesta inválida. Ingrese SI o NO: "
            ).upper()

        if respuesta == "SI":

            estado = ESTADO_CERRADO

            print("\nIncidente resuelto.")
            print("Estado:", estado)

        else:

            estado = ESTADO_GENERANDO_TICKET

            prioridad = calcular_prioridad(problema)

            ticket = generar_ticket(
                usuario,
                problema,
                prioridad
            )

            print(f"\nTicket generado N° {ticket}")
            print("Prioridad:", prioridad)

            if prioridad == "ALTA":

                estado = ESTADO_DERIVADO_N2

                print("Derivado a Soporte Nivel 2.")
                print("Estado:", estado)

            else:

                estado = ESTADO_CERRADO

                print("Será atendido por Mesa de Ayuda.")
                print("Estado:", estado)

    else:

        estado = ESTADO_GENERANDO_TICKET

        prioridad = calcular_prioridad(problema)

        ticket = generar_ticket(
            usuario,
            problema,
            prioridad
        )

        print(f"\nTicket generado N° {ticket}")
        print("Prioridad:", prioridad)

        if prioridad == "ALTA":

            estado = ESTADO_DERIVADO_N2

            print("Derivado a Soporte Nivel 2.")
            print("Estado:", estado)

        else:

            estado = ESTADO_CERRADO

            print("Será atendido por Mesa de Ayuda.")
            print("Estado:", estado)


if __name__ == "__main__":
    main()
