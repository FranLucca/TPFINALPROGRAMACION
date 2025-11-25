from graficos.config import ARCHIVO_RANKING

def cargar_ranking():
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


def guardar_ranking(ranking):
    archivo = open(ARCHIVO_RANKING, "w")

    for registro in ranking:
        linea = f"{registro['tiempo']},{registro['dibujo']},{registro['jugador']}"
        print(linea, file=archivo)

    archivo.close()


def ordenar_ranking_por_tiempo(ranking):
    cantidad = len(ranking)
    for i in range(cantidad - 1):
        for j in range(0, cantidad - 1 - i):
            if ranking[j + 1]["tiempo"] < ranking[j]["tiempo"]:
                auxiliar = ranking[j]
                ranking[j] = ranking[j + 1]
                ranking[j + 1] = auxiliar


def agregar_registro_ranking(tiempo, nombre_dibujo, nombre_jugador):
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
