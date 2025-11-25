from graficos.config import *

#CORRECTO E INCORRECTO

def validar_correcto(tablero: any, solucion:any):
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if solucion[fila][columna] == 1 and tablero[fila][columna] != 1:
                return False
            if solucion[fila][columna] == 0 and tablero[fila][columna] == 1:
                return False
    return True

def validar_incorrecto(tablero:any, solucion:any, fila:any, columna:any):
    if tablero[fila][columna] == 1 and solucion[fila][columna] == 0:
        return True
    if tablero[fila][columna] == 2 and solucion[fila][columna] == 1:
        return True
    return False