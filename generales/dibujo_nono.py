# dibujo_interfaz.py

import pygame
import time


from graficos.config import *
from generales.ranking_puntajes import cargar_ranking

# CARGAR IMAGEN DE FONDO UNA SOLA VEZ
fondo = pygame.image.load("archivos/escudo afa.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))


#FUNCION PARA DIBUJAR TEXTO EN PANTALLA
def dibujar_texto(pantalla: any, texto: str, x: int, y: int, tamano: int, color: tuple) -> None:
    """
    Dibuja un texto en la pantalla de Pygame.

    Parámetros:
        pantalla (any): Superficie donde se va a dibujar el texto.
        texto (str): Cadena de texto a mostrar.
        x (int): Posición horizontal donde se dibujará el texto.
        y (int): Posición vertical donde se dibujará el texto.
        tamano (int): Tamaño de la fuente.
        color (tuple): Color del texto en formato RGB (R, G, B).

    Retorna:
        None: La función no devuelve ningún valor, solo dibuja en pantalla.
    """
    fuente = pygame.font.SysFont("arial", tamano)
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, (x, y))


def pintar_celda(pantalla: any, x: int, y: int, rectangulo: pygame.Rect, 
                valor_celda: int, solucion: list, fila: int, columna: int) -> None: 
    """
    Dibuja una celda del nonograma según su estado y la solución correcta.

    Parámetros:
        pantalla (any): Superficie donde se dibuja la celda.
        x (int): Posición horizontal de la celda.
        y (int): Posición vertical de la celda.
        rectangulo (pygame.Rect): Rectángulo que representa la celda.
        valor_celda (int): Estado de la celda:
                        0 = vacía,
                        1 = marcada (clic izquierdo),
                        2 = cruz roja (clic derecho).
        solucion (list): Matriz con la solución del nonograma (0 o 1).
        fila (int): Índice de la fila de la celda.
        columna (int): Índice de la columna de la celda.

    Retorna:
        None: No devuelve valor, solo dibuja la celda en pantalla.
    """

    pygame.draw.rect(pantalla, NEGRO, rectangulo, 1)

    if valor_celda == 1:
        if solucion[fila][columna] == 1:
            # CORRECTO --> SE PINTA DE NEGRO
            pygame.draw.rect(pantalla, NEGRO, rectangulo)
        else:
            # INCORRECTO --> SE HACE UNA CRUZ ROJA
            margen = 4
            pygame.draw.line(pantalla, ROJO,
                            (x + margen, y + margen),
                            (x + TAM_CELDA - margen, y + TAM_CELDA - margen), 2)
            pygame.draw.line(pantalla, ROJO,
                            (x + TAM_CELDA - margen, y + margen),
                            (x + margen, y + TAM_CELDA - margen), 2)

    #HACER UNA CRUZ ROJA CON EL CLICK DERECHO
    elif valor_celda == 2:
        margen = 4
        pygame.draw.line(pantalla, ROJO,
                        (x + margen, y + margen),
                        (x + TAM_CELDA - margen, y + TAM_CELDA - margen), 2)
        pygame.draw.line(pantalla, ROJO,
                        (x + TAM_CELDA - margen, y + margen),
                        (x + margen, y + TAM_CELDA - margen), 2)

#MOSTRAR LAS PISTAS DE LAS COLUMNAS
def mostrar_pistas_columnas(pantalla: any, pistas_columnas: list,
                            x_inicio: int, y_inicio: int) -> None:
    """
    Muestra en pantalla las pistas correspondientes a cada columna del nonograma.

    Parámetros:
        pantalla (any): Superficie donde se dibujarán los textos.
        pistas_columnas (list): Lista de listas con las pistas numéricas de cada columna.
        x_inicio (int): Posición horizontal desde donde se empiezan a mostrar las pistas.
        y_inicio (int): Posición vertical desde donde se empiezan a mostrar las pistas.

    Retorna:
        None: Dibuja el texto en pantalla sin devolver ningún valor.
    """
    dibujar_texto(pantalla, "Pistas columnas:", x_inicio, y_inicio - 30, 22, NEGRO)

    y = y_inicio
    for indice in range(len(pistas_columnas)):
        texto = f"C{indice + 1}: "
        for n in pistas_columnas[indice]:
            texto = f"{texto}{n} "

        dibujar_texto(pantalla, texto, x_inicio, y + 5, 18, NEGRO)
        y = y + 25

#MOSTRAR PISTAS DE LAS FILAS
def mostrar_pistas_filas(pantalla: any, pistas_filas: list,
                        x_inicio: int, y_inicio: int) -> None:
    
    """
    Muestra en pantalla las pistas correspondientes a cada fila del nonograma.

    Parámetros:
        pantalla (any): Superficie donde se dibujan los textos.
        pistas_filas (list): Lista de listas que contiene las pistas numéricas de cada fila.
        x_inicio (int): Posición horizontal donde comienzan a mostrarse las pistas.
        y_inicio (int): Posición vertical donde comienzan a mostrarse las pistas.

    Retorna:
        None: La función no devuelve valores; solo dibuja texto en pantalla.
    """

    dibujar_texto(pantalla, "Pistas filas:", x_inicio, y_inicio - 30, 22, NEGRO)

    y = y_inicio
    for indice in range(len(pistas_filas)):
        texto = f"F{indice + 1}: "
        for n in pistas_filas[indice]:
            texto = f"{texto}{n} "

        dibujar_texto(pantalla, texto, x_inicio, y + 5, 18, NEGRO)
        y = y + 25

#DIBUJAR EL TABLERO
def dibujar_tablero(pantalla: any, tablero: list[list[int]], solucion: list[list[int]], pistas_filas:list[list[int]],
                    pistas_columnas: list[list[int]], vidas: int, nombre_jugador: str,
                    nombre_dibujo: str, tiempo_inicio: float, mensaje_penalizacion: str) -> None:
    """
    Dibuja en pantalla el tablero completo del nonograma, incluyendo:
    - título del juego, jugador y nombre del dibujo,
    - cantidad de vidas,
    - tiempo transcurrido,
    - grilla con las celdas pintadas según el estado actual,
    - pistas de filas y columnas,
    - mensaje de penalización si corresponde.

    Parámetros:
        pantalla (any): Superficie principal donde se dibuja todo el juego.
        tablero (list[list[int]]): Matriz con el estado actual del tablero.
                                0 = celda vacía,
                                1 = celda marcada,
                                2 = celda con cruz roja.
        solucion (list[list[int]]): Matriz con la solución del nonograma (0 o 1).
        pistas_filas (list[list[int]]): Pistas numéricas correspondientes a cada fila.
        pistas_columnas (list[list[int]]): Pistas numéricas correspondientes a cada columna.
        vidas (int): Cantidad de vidas restantes del jugador.
        nombre_jugador (str): Nombre del jugador actual.
        nombre_dibujo (str): Nombre identificador del dibujo del nonograma.
        tiempo_inicio (float): Momento en segundos (time.time()) en el que comenzó la partida.
        mensaje_penalizacion (str): Mensaje a mostrar cuando hubo una penalización,
                                    vacío ("") si no se muestra nada.

    Retorna:
        None: La función no devuelve ningún valor, solo dibuja en la pantalla.
    """
    pantalla.blit(fondo, (0, 0))

    dibujar_texto(pantalla, "Nonogramas Seleccion Argentina", 20, 20, 32, AZUL)
    dibujar_texto(pantalla, f"Jugador: {nombre_jugador}", 20, 60, 20, NEGRO)
    dibujar_texto(pantalla, f"Dibujo: {nombre_dibujo}", 20, 85, 20, NEGRO)

    dibujar_texto(pantalla, f"Vidas: {vidas}", 650, 20, 24, ROJO)

    tiempo_actual = time.time()
    segundos = int(tiempo_actual - tiempo_inicio)
    dibujar_texto(pantalla, f"Tiempo: {segundos} s", 650, 50, 20, NEGRO)

    #DIBUJOS DE LAS CELDAS
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            x = MARGEN_IZQUIERDO + columna * TAM_CELDA
            y = MARGEN_SUPERIOR + fila * TAM_CELDA
            rectangulo = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)

            valor_celda = tablero[fila][columna]

            pintar_celda(
                pantalla,
                x, y,
                rectangulo,
                valor_celda,
                solucion,
                fila, columna
            )

    #BORDE DE LAS CELDAS
    ancho_tablero = COLUMNAS * TAM_CELDA
    alto_tablero = FILAS * TAM_CELDA
    rect_borde = pygame.Rect(MARGEN_IZQUIERDO, MARGEN_SUPERIOR, ancho_tablero, alto_tablero)
    pygame.draw.rect(pantalla, NEGRO, rect_borde, 3)

    #MOSTRAR LAS PISTAS DE LAS COLUMNAS (UBICACION)
    mostrar_pistas_columnas(pantalla, pistas_columnas, MARGEN_IZQUIERDO - 180, MARGEN_SUPERIOR)
    #MOSTRAR LAS PISTAS DE LAS COLUMNAS (UBICACION)
    mostrar_pistas_filas(pantalla, pistas_filas, MARGEN_IZQUIERDO + ancho_tablero + 40, MARGEN_SUPERIOR)

    if mensaje_penalizacion != "":
        dibujar_texto(pantalla, mensaje_penalizacion, 150, ALTO_VENTANA - 40, 20, ROJO)

#FUNCION PARA DIBUJAR EL MENU
def dibujar_menu(pantalla: any, nombre_jugador: str) -> dict[str, pygame.Rect]:
    """
    Dibuja el menú principal del juego Nonograma, incluyendo el título, el
    nombre del jugador actual y los botones interactivos.

    Parámetros:
        pantalla (any): Superficie donde se dibujará el menú.
        nombre_jugador (str): Nombre del jugador actualmente logueado.

    Retorna:
        dict[str, pygame.Rect]: Diccionario que contiene los rectángulos
        correspondientes a cada botón del menú:
            - "jugar"
            - "ranking"
            - "registro"
            - "salir"
    """
    pantalla.blit(fondo, (0, 0))
    dibujar_texto(pantalla, "MENU PRINCIPAL NONOGRAMA", 200, 80, 32, AZUL)
    dibujar_texto(pantalla, f"Jugador actual: {nombre_jugador}", 250, 130, 22, NEGRO)

    boton_jugar = pygame.Rect(280, 200, 240, 50)
    boton_ranking = pygame.Rect(280, 270, 240, 50)
    boton_registro = pygame.Rect(280, 340, 240, 50)
    boton_salir = pygame.Rect(280, 410, 240, 50)

    pygame.draw.rect(pantalla, GRIS, boton_jugar)
    pygame.draw.rect(pantalla, GRIS, boton_ranking)
    pygame.draw.rect(pantalla, GRIS, boton_registro)
    pygame.draw.rect(pantalla, GRIS, boton_salir)

    dibujar_texto(pantalla, "1 - Nuevo nonograma", 295, 215, 22, NEGRO)
    dibujar_texto(pantalla, "2 - Ver ranking", 305, 285, 22, NEGRO)
    dibujar_texto(pantalla, "3 - Registrar jugador", 290, 355, 22, NEGRO)
    dibujar_texto(pantalla, "4 - Salir", 335, 425, 22, NEGRO)

    botones = {
        "jugar": boton_jugar,
        "ranking": boton_ranking,
        "registro": boton_registro,
        "salir": boton_salir
    }
    return botones

#FUNCION PARA LA PANTALLA DE REGISTRO
def dibujar_pantalla_registro(pantalla: any, texto_actual: str) -> None:
    """
    Dibuja la pantalla de registro de jugador donde se ingresa el nombre.
    Muestra un campo de texto, instrucciones y un mensaje para volver al menú.

    Parámetros:
        pantalla (any): Superficie donde se dibujará la pantalla de registro.
        texto_actual (str): Texto que el usuario ha ingresado hasta el momento.

    Retorna:
        None: La función no devuelve valores, solo dibuja los elementos en pantalla.
    """
    pantalla.fill(CELESTE)
    dibujar_texto(pantalla, "REGISTRO DE JUGADOR", 230, 80, 32, AZUL)
    dibujar_texto(pantalla, "Escribi tu nombre y presiona ENTER:", 180, 160, 24, NEGRO)

    rect_input = pygame.Rect(150, 220, 500, 50)
    pygame.draw.rect(pantalla, GRIS, rect_input, 2)

    dibujar_texto(pantalla, texto_actual, 160, 230, 28, NEGRO)
    dibujar_texto(pantalla, "ESC para volver al menu sin guardar.", 200, 300, 20, ROJO)

#FUNCION PARA LA PANTALLA DEL RANKING
def dibujar_pantalla_ranking(pantalla: any) -> None:
    """
    Dibuja la pantalla del ranking de jugadores, mostrando el top 10 de partidas
    registradas, incluyendo posición, tiempo, dibujo resuelto y nombre del jugador.

    Parámetros:
        pantalla (any): Superficie donde se renderiza toda la pantalla
                                del ranking.

    Retorna:
        None: La función no devuelve ningún valor; solo dibuja elementos visuales.
    """
    pantalla.fill(CELESTE)

    texto_titulo = "RANKING DE JUGADORES"
    ancho_texto = len(texto_titulo) * 12
    x_centrado = (ANCHO_VENTANA - ancho_texto) // 2
    dibujar_texto(pantalla, texto_titulo, x_centrado, 50, 32, AZUL)

    ranking = cargar_ranking()

    if len(ranking) == 0:
        dibujar_texto(pantalla, "No hay registros todavia.", 260, 150, 24, NEGRO)
    else:
        ancho_columna = 140
        cantidad_columnas = 4
        ancho_tabla = ancho_columna * cantidad_columnas

        x_inicio_tabla = (ANCHO_VENTANA - ancho_tabla) // 2
        y_inicio_tabla = 150

        x_pos_posicion = x_inicio_tabla
        x_pos_tiempo = x_inicio_tabla + ancho_columna
        x_pos_dibujo = x_inicio_tabla + ancho_columna * 2
        x_pos_jugador = x_inicio_tabla + ancho_columna * 3

        dibujar_texto(pantalla, "Pos",       x_pos_posicion, y_inicio_tabla, 22, NEGRO)
        dibujar_texto(pantalla, "Tiempo(s)", x_pos_tiempo,   y_inicio_tabla, 22, NEGRO)
        dibujar_texto(pantalla, "Dibujo",    x_pos_dibujo,   y_inicio_tabla, 22, NEGRO)
        dibujar_texto(pantalla, "Jugador",   x_pos_jugador,  y_inicio_tabla, 22, NEGRO)

        y = y_inicio_tabla + 30
        posicion = 1

        for registro in ranking:
            tiempo = round(registro["tiempo"], 2)

            dibujar_texto(pantalla, f"{posicion}",       x_pos_posicion, y, 20, NEGRO)
            dibujar_texto(pantalla, f"{tiempo}",         x_pos_tiempo,   y, 20, NEGRO)
            dibujar_texto(pantalla, registro["dibujo"],  x_pos_dibujo,   y, 20, NEGRO)
            dibujar_texto(pantalla, registro["jugador"], x_pos_jugador,  y, 20, NEGRO)

            y = y + 25
            posicion = posicion + 1
            if posicion > 10:
                break

    dibujar_texto(pantalla, "Presiona ESC para volver al menu.", 220, 520, 22, ROJO)

#FUNCION PARA MENSAJES
def dibujar_pantalla_mensaje(pantalla: any, titulo: str, mensaje: str, color_titulo: tuple) -> None:
    """
    Dibuja una pantalla de mensaje genérico, utilizada para notificaciones,
    alertas o indicaciones al jugador.

    Parámetros:
        pantalla (any): Superficie donde se mostrará el mensaje.
        titulo (str): Texto principal que se muestra como título del mensaje.
        mensaje (str): Texto secundario con la información que se desea comunicar.
        color_titulo (tuple): Color RGB del título (por ejemplo, (255,0,0) para rojo).

    Retorna:
        None: Solo dibuja los textos en pantalla, sin devolver ningún valor.
    """
    pantalla.fill(CELESTE)
    dibujar_texto(pantalla, titulo, 250, 200, 36, color_titulo)
    dibujar_texto(pantalla, mensaje, 160, 260, 26, NEGRO)
    dibujar_texto(pantalla, "Presiona ENTER para volver al menu.", 190, 330, 22, AZUL)
