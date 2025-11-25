import random

def cargar_csv_a_matriz(ruta: any):
    matriz = []

    archivo = open(ruta, "r")

    for linea in archivo:
        if linea == "":
            continue
        valores = linea.split(",")
        fila = []
        for valor in valores:
            largo = len(valor)
            if largo > 0:
                ultimo = valor[largo - 1]
                if ord(ultimo) == 10:
                    valor = valor[0:largo - 1]

            if valor.isdigit():
                fila.append(int(valor))
            else:
                fila.append(valor)

        matriz.append(fila)

    archivo.close()
    return matriz


def elegir_nonograma_aleatorio(lista_rutas: any):
    cantidad = len(lista_rutas)
    indice = random.randint(0, cantidad - 1)
    ruta_elegida = lista_rutas[indice]
    return ruta_elegida
