import random

def cargar_csv_a_matriz(ruta: str) -> list[list[object]]:
    """
    Carga un archivo CSV y lo convierte en una matriz (lista de listas).
    Cada valor numérico se transforma a entero; el resto queda como string.

    Parámetros:
        ruta (str): Ruta del archivo CSV a leer.

    Retorna:
        list[list[object]]: Matriz resultante donde cada fila contiene
        valores convertidos según su tipo (int o str).
    """
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


def elegir_nonograma_aleatorio(lista_rutas: list[str]) -> str:
    """
    Selecciona aleatoriamente una ruta de archivo desde una lista de nonogramas.

    Parámetros:
        lista_rutas (list[str]): Lista de rutas correspondientes a los archivos
                                de distintos nonogramas disponibles.

    Retorna:
        str: La ruta elegida de manera aleatoria.
    """
    cantidad = len(lista_rutas)
    indice = random.randint(0, cantidad - 1)
    ruta_elegida = lista_rutas[indice]
    return ruta_elegida
