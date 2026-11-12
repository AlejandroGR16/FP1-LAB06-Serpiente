import random

def comprueba_choque(serpiente: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], otra_serpiente: list[tuple[int, int]]) -> bool:
    '''
    Comprueba si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente. Tenga en cuenta
    que la serpiente avanza siempre por su cabeza, que está situada en la 
    primera posición de la lista.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de cada segmento de la serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    otra_serpiente: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.

    Devuelve:
    True si la serpiente se ha chocado consigo misma, con las paredes o con la otra serpiente, False en caso contrario.
    '''
    if (serpiente[0] in serpiente[1:]) or (serpiente[0] in otra_serpiente): return True
    for p in paredes:
        if (serpiente[0] in p): return True
    return False

def ha_comido_serpiente(serpiente: list[tuple[int, int]], posicion_comida: tuple[int, int]) -> bool:
    '''
    Comprueba si la cabeza de la serpiente está en la misma posición que la comida.

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    posicion_comida: Tupla representando la posición de la comida (columna, fila).

    Devuelve:
    True si la cabeza de la serpiente está en la misma posición que la comida, False en caso contrario.
    '''
    if serpiente[0]==posicion_comida: return True
    else: return False

def crece_serpiente(serpiente: list[tuple[int, int]]) -> None:
    '''
    Hace crecer la serpiente añadiendo duplicando la posición de la cola

    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    '''
    serpiente.append(serpiente[-1])

def genera_comida_aleatoria(serpiente_jugador: list[tuple[int, int]], serpiente_ia: list[tuple[int, int]], paredes: list[list[tuple[int, int]]], filas: int, columnas: int) -> tuple[int, int]:
    '''
    Genera una posición aleatoria para la comida que no esté en la misma posición que las serpientes o las paredes.

    Parámetros:
    serpiente_jugador: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    serpiente_ia: Lista de tuplas representando las posiciones (columna, fila) de la otra serpiente.
    paredes: Lista de listas de tuplas representando las posiciones (columna, fila) de los segmentos de las paredes.
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.

    Devuelve:
    Posición aleatoria para la comida (columna, fila).
    '''
    vacio=False
    while vacio==False:
        vacio=True
        (x, y) = (random.randint(0,columnas-1), random.randint(0,filas-1))
        if ((x,y) in serpiente_jugador) or ((x,y) in serpiente_ia): vacio=False
        for p in paredes:
            if (x,y) in p: vacio=False
    return (x,y)

def mueve_serpiente(serpiente: list[tuple[int, int]], direccion: str, filas: int, columnas: int, toroidal: bool = True) -> None:
    '''
    Mueve la serpiente en el tablero según la dirección dada. El tablero es circular, lo que significa
    que si la serpiente se sale por la derecha, debe aparecer por la izquierda, y viceversa (y lo
    mismo si se sale por arriba o por abajo).
    
    Parámetros:
    serpiente: Lista de tuplas representando las posiciones (columna, fila) de la serpiente.
    direccion: Dirección en la que se debe mover la serpiente ('Left', 'Right', 'Down', 'Up').
    filas: Número de filas en el tablero de juego.
    columnas: Número de columnas en el tablero de juego.
    '''
    col, fila = serpiente[0]

    if direccion == 'Up':
        fila -= 1
    elif direccion == 'Down':
        fila += 1
    elif direccion == 'Left':
        col -= 1
    elif direccion == 'Right':
        col += 1

    if toroidal==True:
        col %= columnas
        fila %= filas

    serpiente.insert(0, (col, fila))
    serpiente.pop()

def decide_movimiento_ia(serpiente_rival: list[tuple[int, int]], serpiente_jugador: list[tuple[int, int]],
    paredes: list[list[tuple[int, int]]], posicion_comida: tuple[int, int],
    filas: int, columnas: int) -> str:
    '''
    Decide la dirección de movimiento de la serpiente rival, intentando elegir la que más 
    le acerque a la comida sin chocar.

    Parámetros:
    serpiente_rival: lista de posiciones (columna, fila) de la serpiente rival.
    serpiente_jugador: lista de posiciones de la serpiente del jugador.
    paredes: lista de listas de posiciones de las paredes.
    posicion_comida: posición actual de la comida.
    filas, columnas: tamaño del tablero.

    Devuelve:
    Dirección elegida: 'Left', 'Right', 'Up' o 'Down'.    
    '''
    # Construiremos una lista de (distancia_a_la_comida, direccion)
    opciones = []
    for d in ("Up", "Down", "Left", "Right"):
        serpiente_rival_copia=serpiente_rival.copy()
        mueve_serpiente(serpiente_rival_copia,d,filas,columnas)
        if (comprueba_choque(serpiente_rival_copia,paredes,serpiente_jugador)==False):    
            distancia=abs(serpiente_rival_copia[0][0]-posicion_comida[0])+abs(serpiente_rival_copia[0][1]-posicion_comida[1])
            opciones.append((distancia,d))
        
    if opciones==[]: return 'Up'

    mejor_opcion=None
    for opcion in opciones:
        if mejor_opcion==None or mejor_opcion[0]>opcion[0]:
            mejor_opcion=opcion
    return mejor_opcion[1]