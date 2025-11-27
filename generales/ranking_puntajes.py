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
        linea_limpia = linea.strip()

        if linea_limpia == "":
            continue

        valores = linea_limpia.split(",")

        if len(valores) < 3:
            continue

        texto_tiempo = valores[0].strip()
        if texto_tiempo == "":
            continue

        tiempo = float(texto_tiempo)
        dibujo = valores[1].strip()
        jugador = valores[2].strip()

        registro = {
            "tiempo": tiempo,
            "dibujo": dibujo,
            "jugador": jugador
        }

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

def obtener_tiempo_registro(registro):
    """
    Funcion pura: recibe un registro y devuelve solo el tiempo.
    Se usa como funcion 'key' en sorted (programacion funcional).
    """
    return registro["tiempo"]

def ordenar_ranking_por_tiempo(ranking):
    """
    Usa sorted con una funcion como parametro (obtener_tiempo_registro).
    sorted no modifica la lista original: devuelve una nueva lista ordenada.
    """
    ranking_ordenado = sorted(ranking, key=obtener_tiempo_registro)
    return ranking_ordenado

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

    nuevo = {
        "tiempo": tiempo,
        "dibujo": nombre_dibujo,
        "jugador": nombre_jugador
    }

    ranking.append(nuevo)

    ranking = ordenar_ranking_por_tiempo(ranking)

    while len(ranking) > 10:
        ranking.pop()

    guardar_ranking(ranking)