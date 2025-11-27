from graficos.config import ARCHIVO_RANKING

def cargar_ranking() -> list[dict[str, str | float]]:

    """
    Carga el ranking desde el archivo CSV definido en ARCHIVO_RANKING.
    El archivo debe contener líneas con el siguiente formato:
        tiempo,dibujo,jugador

    Retorna:
        list[dict[str, str | float]]:
            Una lista de diccionarios donde cada diccionario representa un registro
            del ranking con claves:
                - "tiempo"  (float)
                - "dibujo"  (str)
                - "jugador" (str)
    """
    
    ranking = []

    archivo = open(ARCHIVO_RANKING, "r")

    for linea in archivo:
        if linea == "":
            continue

        valores = linea.split(",")

        tiempo = float(valores[0])
        dibujo = valores[1]
        jugador = valores[2]
        largo_jugador = len(jugador)
        if largo_jugador > 0:
            ultimo = jugador[largo_jugador - 1]
            if ord(ultimo) == 10:
                jugador = jugador[0:largo_jugador - 1]
        registro = {"tiempo": tiempo, "dibujo": dibujo, "jugador": jugador}
        ranking.append(registro)
    archivo.close()
    return ranking


def guardar_ranking(ranking: list[dict[str, str | float]]) -> None:

    """
    Guarda la lista del ranking en el archivo correspondiente
    en formato CSV: tiempo,dibujo,jugador

    Parámetros:
        ranking (list[dict]): Lista con los registros a guardar.

    Retorna:
        None: Solo escribe el archivo.
    """
    
    archivo = open(ARCHIVO_RANKING, "w")

    for registro in ranking:
        linea = f"{registro['tiempo']},{registro['dibujo']},{registro['jugador']}"
        print(linea, file=archivo)

    archivo.close()


def ordenar_ranking_por_tiempo(ranking: list[dict[str, float | str]]) -> None:

    """
    Ordena el ranking de jugadores en forma ascendente según el tiempo.

    Parámetros:
        ranking (list[dict]): Lista de registros a ordenar.

    Retorna:
        None: El ranking se modifica en la misma lista (ordenamiento in-place).
    """
    
    cantidad = len(ranking)
    for i in range(cantidad - 1):
        for j in range(0, cantidad - 1 - i):
            if ranking[j + 1]["tiempo"] < ranking[j]["tiempo"]:
                auxiliar = ranking[j]
                ranking[j] = ranking[j + 1]
                ranking[j + 1] = auxiliar


def agregar_registro_ranking(tiempo: float, nombre_dibujo: str, nombre_jugador: str) -> None:

    """
    Agrega un nuevo registro al ranking, lo ordena y guarda los primeros 10.

    Parámetros:
        tiempo (float): Tiempo obtenido por el jugador.
        nombre_dibujo (str): Nombre del nonograma resuelto.
        nombre_jugador (str): Nombre del jugador.

    Retorna:
        None
    """
    
    ranking = cargar_ranking()

    nuevo = {"tiempo": tiempo, 
            "dibujo": nombre_dibujo,
            "jugador": nombre_jugador
            }

    ranking.append(nuevo)
    ordenar_ranking_por_tiempo(ranking)

    while len(ranking) > 10:
        ranking.pop()

    guardar_ranking(ranking)
