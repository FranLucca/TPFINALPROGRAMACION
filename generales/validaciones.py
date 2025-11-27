from graficos.config import *

#CORRECTO E INCORRECTO

def validar_correcto(tablero: list[list[int]], solucion:list[list[int]]) -> bool:

    """
    Verifica si el tablero actual coincide completamente con la solución del nonograma.

    La validación compara celda por celda:
        - Si en la solución hay un 1 (celda pintada), en el tablero también debe haber un 1.
        - Si en la solución hay un 0 (celda vacía), en el tablero NO debe haber un 1.

    Parámetros:
        tablero (list[list[int]]): Matriz que representa el estado actual del jugador.
        solucion (list[list[int]]): Matriz con la solución correcta del nonograma.

    Retorna:
        bool: True si el tablero es correcto, False si existe al menos una diferencia.
    """
    
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if solucion[fila][columna] == 1 and tablero[fila][columna] != 1:
                return False
            if solucion[fila][columna] == 0 and tablero[fila][columna] == 1:
                return False
    return True

def validar_incorrecto(tablero:list[list[int]], solucion:list[list[int]], fila: int, columna: int) -> bool:

    """
    Determina si una celda marcada es incorrecta comparando contra la solución.

    Retorna:
        bool: True si el movimiento es incorrecto, False en caso contrario.
    """
    
    if tablero[fila][columna] == 1 and solucion[fila][columna] == 0:
        return True
    if tablero[fila][columna] == 2 and solucion[fila][columna] == 1:
        return True
    return False