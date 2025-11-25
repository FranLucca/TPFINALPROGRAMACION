#FUNCION PARA INICIALIZAR LA MATRIZ
def inicializar_matriz(filas, columnas, valor_inicial):
    matriz = []
    for indice_fila in range(filas):
        fila_nueva = []
        for indice_columna in range(columnas):
            fila_nueva.append(valor_inicial)
        matriz.append(fila_nueva)
    return matriz
#FUNCION PARA CALCULAR LAS PISTAS DE LAS FILAS
def calcular_pistas_filas(matriz):
    pistas = []
    for fila in matriz:
        conteos = []
        contador = 0
        for valor in fila:
            if valor == 1:
                contador = contador + 1
            else:
                if contador > 0:
                    conteos.append(contador)
                    contador = 0
        if contador > 0:
            conteos.append(contador)
        if len(conteos) == 0:
            conteos.append(0)
        pistas.append(conteos)
    return pistas
#FUNCION PARA CALCULAR LAS PISTAS DE LAS COLUMNAS
def calcular_pistas_columnas(matriz):
    pistas = []
    cantidad_columnas = len(matriz[0])
    cantidad_filas = len(matriz)
    for indice_columna in range(cantidad_columnas):
        conteos = []
        contador = 0
        for indice_fila in range(cantidad_filas):
            valor = matriz[indice_fila][indice_columna]
            if valor == 1:
                contador = contador + 1
            else:
                if contador > 0:
                    conteos.append(contador)
                    contador = 0
        if contador > 0:
            conteos.append(contador)
        if len(conteos) == 0:
            conteos.append(0)
        pistas.append(conteos)
    return pistas

