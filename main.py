
#IMPORTACIONES

import pygame
import time
from graficos.config import *
from generales.validaciones import validar_correcto, validar_incorrecto
from generales.nonogramas import inicializar_matriz, calcular_pistas_filas, calcular_pistas_columnas
from generales.manejo_archivos import cargar_csv_a_matriz, elegir_nonograma_aleatorio
from generales.ranking_puntajes import agregar_registro_ranking
from generales.dibujo_nono import dibujar_tablero, dibujar_menu, dibujar_pantalla_registro, dibujar_pantalla_ranking, dibujar_pantalla_mensaje

#PYGAME FUNCIONES FUNDAMENTALES
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("archivos/LA T Y LA M - Pa' la Selección (Video Oficial).mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

archivo_ranking = open(ARCHIVO_RANKING, "a")
archivo_ranking.close()

pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Juego de Nonograma 8x8")
reloj = pygame.time.Clock()

imagen_ganador = pygame.image.load("archivos\Sin título.png")
imagen_ganador = pygame.transform.scale(imagen_ganador, (200, 200))
ancho_imagen_ganador = imagen_ganador.get_width()
alto_imagen_ganador = imagen_ganador.get_height()

#BANDERA PARA INICIALIZAR
ejecutando = True
estado = "menu"

nombre_jugador = ""
texto_registro = ""

#FUNCIONES DEL JUEGO
lista_nonogramas = [
    "archivos/nonogramas/numero10.csv",
    "archivos/nonogramas/carita.csv"
]

solucion_actual = []
tablero_actual = inicializar_matriz(FILAS, COLUMNAS, 0)
pistas_filas_actual = []
pistas_columnas_actual = []
nombre_dibujo_actual = ""

vidas = VIDAS_INICIALES
tiempo_inicio = 0.0
tiempo_final = 0.0
guardo_ranking = False

errores_pendientes = []
mensaje_game_over = ""
mensaje_penalizacion = ""
tiempo_mensaje_penalizacion = 0.0

#BUCLE PRINCIPAL DEL JUEGO
while ejecutando:
    reloj.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        #EVENTO MENU Y LOS BOTONES
        if estado == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                botones = dibujar_menu(pantalla, nombre_jugador)
                x, y = evento.pos
                #BOTON JUGAR
                if botones["jugar"].collidepoint(x, y):
                    if nombre_jugador == "":
                        estado = "game_over"
                        mensaje_game_over = "Debes registrar tu nombre antes de jugar."
                    else:
                        ruta_elegida = elegir_nonograma_aleatorio(lista_nonogramas)
                        solucion_actual = cargar_csv_a_matriz(ruta_elegida)

                        partes_ruta = ruta_elegida.split("/")
                        nombre_archivo = partes_ruta[len(partes_ruta) - 1]
                        nombre_dibujo_actual = nombre_archivo

                        tablero_actual = inicializar_matriz(FILAS, COLUMNAS, 0)
                        pistas_filas_actual = calcular_pistas_filas(solucion_actual)
                        pistas_columnas_actual = calcular_pistas_columnas(solucion_actual)

                        vidas = VIDAS_INICIALES
                        errores_pendientes = []
                        tiempo_inicio = time.time()
                        guardo_ranking = False
                        mensaje_penalizacion = ""
                        estado = "juego"
                #BOTON RANKING
                if botones["ranking"].collidepoint(x, y):
                    estado = "ranking"
                #BOTON REGISTRO
                if botones["registro"].collidepoint(x, y):
                    texto_registro = ""
                    estado = "registro"
                #BOTON SALIR
                if botones["salir"].collidepoint(x, y):
                    ejecutando = False
        #EVENTO REGISTRO
        elif estado == "registro":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    nombre_jugador = texto_registro.strip()
                    estado = "menu"
                elif evento.key == pygame.K_ESCAPE:
                    estado = "menu"
                elif evento.key == pygame.K_BACKSPACE:
                    texto_registro = texto_registro[:-1]
                else:
                    caracter = evento.unicode
                    if len(caracter) == 1 and len(texto_registro) < 20:
                        texto_registro = texto_registro + caracter
        #EVENTOS DEL JUEGO
        elif estado == "juego":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                columna = int((x - MARGEN_IZQUIERDO) / TAM_CELDA)
                fila = int((y - MARGEN_SUPERIOR) / TAM_CELDA)

                if columna >= 0 and columna < COLUMNAS and fila >= 0 and fila < FILAS:
                    if evento.button == 1:
                        if tablero_actual[fila][columna] == 1:
                            tablero_actual[fila][columna] = 0
                        else:
                            tablero_actual[fila][columna] = 1

                    if evento.button == 3:
                        if tablero_actual[fila][columna] == 2:
                            tablero_actual[fila][columna] = 0
                        else:
                            tablero_actual[fila][columna] = 2

                    if validar_incorrecto(tablero_actual, solucion_actual, fila, columna):
                        existe_error = False
                        for error in errores_pendientes:
                            if error["fila"] == fila and error["columna"] == columna:
                                existe_error = True
                        if existe_error == False:
                            errores_pendientes.append({"fila": fila, "columna": columna, "tiempo_error": time.time()})
                    if validar_correcto(tablero_actual, solucion_actual):
                        tiempo_final = time.time() - tiempo_inicio
                        if not guardo_ranking:
                            if nombre_jugador == "":
                                nombre_guardar = "Sin nombre"
                            else:
                                nombre_guardar = nombre_jugador
                            agregar_registro_ranking(
                                tiempo_final,
                                nombre_dibujo_actual,
                                nombre_guardar
                            )
                            guardo_ranking = True
                        estado = "ganador"
        #EVENTOS RANKING
        elif estado == "ranking":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"
        #EVENTOS GAME OVER Y GANADOR
        elif estado == "game_over":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                estado = "menu"
        elif estado == "ganador":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                estado = "menu"
    #FUNCIONES DEL JUEGO EN EJECUCION
    if estado == "juego":
        tiempo_actual = time.time()
        errores_a_eliminar = []
        #ERRORES
        for error in errores_pendientes:
            diferencia = tiempo_actual - error["tiempo_error"]
            if diferencia >= 3:
                fila_error = error["fila"]
                columna_error = error["columna"]
                if validar_incorrecto(tablero_actual, solucion_actual, fila_error, columna_error):
                    vidas = vidas - 1
                    mensaje_penalizacion = "Perdiste una vida por no corregir el error."
                    tiempo_mensaje_penalizacion = tiempo_actual
                errores_a_eliminar.append(error)
        #ELIMINAR ERRORES
        for error in errores_a_eliminar:
            if error in errores_pendientes:
                errores_pendientes.remove(error)
        #MENSAJE DE PENALIZACION
        if mensaje_penalizacion != "":
            if tiempo_actual - tiempo_mensaje_penalizacion >= 2:
                mensaje_penalizacion = ""
        #VIDAS
        if vidas <= 0:
            estado = "game_over"
            mensaje_game_over = "Te quedaste sin vidas. GAME OVER."
    #DIBUJAR EN PANTALLA EL MENU
    if estado == "menu":
        dibujar_menu(pantalla, nombre_jugador)
    #DIBUJAR LA PANTALLA DE REGISTRO
    elif estado == "registro":
        dibujar_pantalla_registro(pantalla, texto_registro)
    #DIBUJAR LA PANTAL DEL JUEGO
    elif estado == "juego":
        dibujar_tablero(pantalla, tablero_actual, solucion_actual, pistas_filas_actual,
                        pistas_columnas_actual, vidas, nombre_jugador, nombre_dibujo_actual,
                        tiempo_inicio, mensaje_penalizacion)
    #DIBUJAR LA PANTALLA DE RANKING
    elif estado == "ranking":
        dibujar_pantalla_ranking(pantalla)
    #DIBUJAR PANTALLA GAME OVER O GANADOR
    elif estado == "game_over":
        dibujar_pantalla_mensaje(pantalla, "GAME OVER", mensaje_game_over, ROJO)
    
    elif estado == "ganador":
        mensaje_ganador = f"Completaste el nonograma en {round(tiempo_final, 2)} segundos."
        dibujar_pantalla_mensaje(pantalla, "¡GANASTE!", mensaje_ganador, AZUL)
        #CONFIGURACION IMAGEN GANADOR
        x_imagen = ANCHO_VENTANA - ancho_imagen_ganador
        y_imagen = ALTO_VENTANA - alto_imagen_ganador
        pantalla.blit(imagen_ganador, (x_imagen, y_imagen))

    pygame.display.flip()
#FINALIZAR PYGAME
pygame.quit()
