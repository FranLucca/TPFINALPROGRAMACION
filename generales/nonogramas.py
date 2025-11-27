#FUNCION PARA INICIALIZAR LA MATRIZ
def inicializar_matriz(filas: int, columnas: int, valor_inicial: int) -> list[list[int]]:
    """
    Crea y devuelve una matriz inicializada con un valor específico.

    Parámetros:
        filas (int): Cantidad de filas que tendrá la matriz.
        columnas (int): Cantidad de columnas que tendrá la matriz.
        valor_inicial (int): Valor con el que se llenarán todas las celdas.

    Retorna:
        list[list[int]]: Matriz de tamaño filas x columnas con todas las
        posiciones inicializadas en valor_inicial.
    """
    matriz = []
    for indice_fila in range(filas):
        fila_nueva = []
        for indice_columna in range(columnas):
            fila_nueva.append(valor_inicial)
        matriz.append(fila_nueva)
    return matriz
#FUNCION PARA CALCULAR LAS PISTAS DE LAS FILAS
def calcular_pistas_filas(matriz: list[list[int]]) -> list[list[int]]:
    """
    Calcula las pistas numéricas correspondientes a cada fila del nonograma.
    Cada pista indica la cantidad de celdas consecutivas con valor 1.

    Ejemplo:
        Fila: [1, 1, 0, 1] → Pista: [2, 1]
        Fila: [0, 0, 0] → Pista: [0]

    Parámetros:
        matriz (list[list[int]]): Matriz del nonograma con valores 0 (vacío) y 1 (pintado).

    Retorna:
        list[list[int]]: Lista de pistas para cada fila. Cada pista es una lista de números.
    """
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
def calcular_pistas_columnas(matriz: list[list[int]]) -> list[list[int]]:
    """
    Calcula las pistas numéricas para cada columna del nonograma.
    Cada pista indica la cantidad de celdas consecutivas con valor 1.

    Parámetros:
        matriz (list[list[int]]): Matriz de enteros (0 o 1) que representa el nonograma completo.

    Retorna:
        list[list[int]]: Lista donde cada elemento corresponde a una columna,
        conteniendo los bloques consecutivos de 1 encontrados.
        Ejemplo: si una columna es [1,1,0,1], la pista será [2,1].
    """
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

