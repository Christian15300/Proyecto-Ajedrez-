import pygame
import sys
import os

pygame.init()

ancho, alto = 700, 700
tamaño_celda = ancho // 8
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('A jedrez en Pygame')

fuente = pygame.font.SysFont(None, 48)

blanco = (240, 217, 181)
marron = (181, 136, 99)
amarillo = (255, 255, 0)
rojo = (220, 50, 50)


def cargar_imagen_pieza(nombre):
  
    try:
    
        ruta = os.path.join("images", nombre)
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (tamaño_celda, tamaño_celda))
    except FileNotFoundError:
        superficie = pygame.Surface((tamaño_celda, tamaño_celda))
        superficie.fill((255, 0, 0))
        return superficie

piezas = {
    'rey_blanco': cargar_imagen_pieza('rey_blanco.png'),
    'rey_negro': cargar_imagen_pieza('rey_negro.png'),
    'reina_blanca': cargar_imagen_pieza('reina_blanca.png'),
    'reina_negra': cargar_imagen_pieza('reina_negra.png'),
    'torre_blanca': cargar_imagen_pieza('torre_blanca.png'),

    'torre_negra': cargar_imagen_pieza('torre_negra.png'),

    'alfil_blanco': cargar_imagen_pieza('alfil_blanco.png'),

    'alfil_negro': cargar_imagen_pieza('alfil_negro.png'),

    'caballo_blanco': cargar_imagen_pieza('caballo_blanco.png'),
    
    'caballo_negro': cargar_imagen_pieza('caballo_negro.png'),
    'peon_blanco': cargar_imagen_pieza('peon_blanco.png'),
    'peon_negro': cargar_imagen_pieza('peon_negro.png'),
}

posiciones_piezas = {
    'rey_blanco': (4, 0), 'rey_negro': (4, 7),
    'reina_blanca': (3, 0), 'reina_negra': (3, 7),
    'torre_blanca': (0, 0), 'torre_blanca2': (7, 0),
    'torre_negra': (0, 7), 'torre_negra2': (7, 7),
    'alfil_blanco': (2, 0), 'alfil_blanco2': (5, 0),
    'alfil_negro': (2, 7), 'alfil_negro2': (5, 7),
    'caballo_blanco': (1, 0), 'caballo_blanco2': (6, 0),
    'caballo_negro': (1, 7), 'caballo_negro2': (6, 7),
    **{f'peon_blanco{i}': (i, 1) for i in range(8)},
    **{f'peon_negro{i}': (i, 6) for i in range(8)},
}

for i in range(8):
    piezas[f'peon_blanco{i}'] = piezas['peon_blanco']
    piezas[f'peon_negro{i}'] = piezas['peon_negro']
piezas['torre_blanca2'] = piezas['torre_blanca']
piezas['torre_negra2'] = piezas['torre_negra']
piezas['alfil_blanco2'] = piezas['alfil_blanco']
piezas['alfil_negro2'] = piezas['alfil_negro']
piezas['caballo_blanco2'] = piezas['caballo_blanco']
piezas['caballo_negro2'] = piezas['caballo_negro']


piezas_movidas = {
    'rey_blanco': False,
    'rey_negro': False,
    'torre_blanca': False,
    'torre_blanca2': False,
    'torre_negra': False,
    'torre_negra2': False,
}

contador_promocion = 0

def color_de(nombre_pieza):
    if ('blanco' in nombre_pieza) or ('blanca' in nombre_pieza):
        return 'blanco'
    if ('negro' in nombre_pieza) or ('negra' in nombre_pieza):
        return 'negro'
    return None

def mismo_color(p1, p2):
    return color_de(p1) == color_de(p2)

def obtener_pieza_en_posicion_board(board, columna, fila):
    for pieza, (c, f) in board.items():
        if (c, f) == (columna, fila):
            return pieza
    return None

def obtener_pieza_en_posicion(columna, fila):
    return obtener_pieza_en_posicion_board(posiciones_piezas, columna, fila)

def camino_libre_board(board, col, fila, nueva_col, nueva_fila):
    dc = 0 if nueva_col == col else (1 if nueva_col > col else -1)
    df = 0 if nueva_fila == fila else (1 if nueva_fila > fila else -1)
    c, f = col + dc, fila + df
    while (c, f) != (nueva_col, nueva_fila):
        if obtener_pieza_en_posicion_board(board, c, f) is not None:
            return False
        c += dc
        f += df
    return True

def camino_libre(col, fila, nueva_col, nueva_fila):
    return camino_libre_board(posiciones_piezas, col, fila, nueva_col, nueva_fila)

def copia_tablero(board):
    return dict(board)



def pieza_ataca_a_en(board, pieza, desde_col, desde_fila, obj_col, obj_fila):
    dx = abs(obj_col - desde_col)
    dy = abs(obj_fila - desde_fila)

    if 'peon' in pieza:
        dir_p = 1 if color_de(pieza) == 'blanco' else -1
        return dx == 1 and (obj_fila - desde_fila) == dir_p

    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

    if 'rey' in pieza:
        return dx <= 1 and dy <= 1

    if 'alfil' in pieza:
        return dx == dy and camino_libre_board(board, desde_col, desde_fila, obj_col, obj_fila)

    if 'torre' in pieza:
        return (desde_col == obj_col or desde_fila == obj_fila) and camino_libre_board(board, desde_col, desde_fila, obj_col, obj_fila)

    if 'reina' in pieza:
        recto = (desde_col == obj_col or desde_fila == obj_fila)
        diagonal = (dx == dy)
        if recto or diagonal:
            return camino_libre_board(board, desde_col, desde_fila, obj_col, obj_fila)
        return False

    return False

def posicion_rey_en(board, color):
    clave = 'rey_blanco' if color == 'blanco' else 'rey_negro'
    return board.get(clave)

def esta_en_jaque_en(board, color):
    pos_rey = posicion_rey_en(board, color)
    if not pos_rey:
        return False
    rey_col, rey_fila = pos_rey
    enemigo = 'negro' if color == 'blanco' else 'blanco'
    for p, (c, f) in board.items():
        if color_de(p) == enemigo:
            if pieza_ataca_a_en(board, p, c, f, rey_col, rey_fila):
                return True
    return False

def esta_en_jaque(color):
    return esta_en_jaque_en(posiciones_piezas, color)

def casilla_atacada_en(board, color_revisado, col, fila):
    enemigo = 'negro' if color_revisado == 'blanco' else 'blanco'
    for p, (c, f) in board.items():
        if color_de(p) == enemigo:
            if pieza_ataca_a_en(board, p, c, f, col, fila):
                return True
    return False


def puede_enrocar_en(board, color, lado):
  
    fila = 0 if color == 'blanco' else 7
    rey_key = 'rey_blanco' if color == 'blanco' else 'rey_negro'

    if piezas_movidas.get(rey_key, True):
        return False

   
    if color == 'blanco':
        torre_lado = 'torre_blanca2' if lado == 'corto' else 'torre_blanca'
        col_torre = 7 if lado == 'corto' else 0
    else:
        torre_lado = 'torre_negra2' if lado == 'corto' else 'torre_negra'
        col_torre = 7 if lado == 'corto' else 0

   
    pieza_torre = board.get(torre_lado)
    if pieza_torre is None:
   
        pieza_en_casilla = obtener_pieza_en_posicion_board(board, col_torre, fila)
        if pieza_en_casilla is None or torre_lado not in board or color_de(pieza_en_casilla) != color:
            return False
    else:
  
        if piezas_movidas.get(torre_lado, True):
            return False

   
    if lado == 'corto':
        columnas_entre = [5, 6]
        columnas_king_path = [4, 5, 6]
    else:
        columnas_entre = [1, 2, 3]
        columnas_king_path = [4, 3, 2]

    for c in columnas_entre:
        if obtener_pieza_en_posicion_board(board, c, fila) is not None:
            return False

   
    if esta_en_jaque_en(board, color):
        return False

   
    for c in columnas_king_path:
        if casilla_atacada_en(board, color, c, fila):
            return False

    return True


def movimiento_por_patron(pieza, nueva_pos, board=None):
    if board is None:
        board = posiciones_piezas

    col, fila = board[pieza]
    nueva_col, nueva_fila = nueva_pos
    dx = abs(nueva_col - col)
    dy = abs(nueva_fila - fila)

    if (nueva_col, nueva_fila) == (col, fila):
        return False

   
    pieza_destino = obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila)
    if pieza_destino and mismo_color(pieza, pieza_destino):
        return False

  
    if 'rey' in pieza:
  
        if dx <= 1 and dy <= 1:
            return True
   
        if dy == 0 and dx == 2:
            color = color_de(pieza)
            lado = 'corto' if nueva_col > col else 'largo'
            return puede_enrocar_en(board, color, lado)
        return False

  
    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

   
    if 'alfil' in pieza:
        return dx == dy and camino_libre_board(board, col, fila, nueva_col, nueva_fila)


    if 'torre' in pieza:
        return (col == nueva_col or fila == nueva_fila) and camino_libre_board(board, col, fila, nueva_col, nueva_fila)

   
    if 'reina' in pieza:
        recto = (col == nueva_col or fila == nueva_fila)
        diagonal = (dx == dy)
        return (recto or diagonal) and camino_libre_board(board, col, fila, nueva_col, nueva_fila)

    
    if 'peon' in pieza:
        color = color_de(pieza)
        direccion = 1 if color == 'blanco' else -1
        inicio = 1 if color == 'blanco' else 6

        if nueva_col == col and nueva_fila == fila + direccion:
            if obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila) is None:
                return True
            return False

        if fila == inicio and nueva_col == col and nueva_fila == fila + 2 * direccion:
            if (obtener_pieza_en_posicion_board(board, col, fila + direccion) is None and
                obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila) is None):
                return True
            return False

        if dx == 1 and nueva_fila == fila + direccion:
            if pieza_destino and not mismo_color(pieza, pieza_destino):
                return True
            return False

        return False

    return False


def movimiento_legal(pieza, nueva_pos):
   
    if not movimiento_por_patron(pieza, nueva_pos, posiciones_piezas):
        return False

  
    board = copia_tablero(posiciones_piezas)
    origen = board[pieza]
    destino_pieza = None
    for p, pos in list(board.items()):
        if pos == nueva_pos and p != pieza:
            destino_pieza = p
            break
    if destino_pieza:
        board.pop(destino_pieza)
    board[pieza] = nueva_pos

    if 'rey' in pieza:
        col_origen, fila_origen = origen
        col_dest, fila_dest = nueva_pos
        if abs(col_dest - col_origen) == 2 and fila_origen == fila_dest:
    
            if col_dest > col_origen:
   
                torre_origen_col, torre_dest_col = 7, 5
            else:
    
                torre_origen_col, torre_dest_col = 0, 3
   
            torre_a_mover = obtener_pieza_en_posicion_board(board, torre_origen_col, fila_origen)
            if torre_a_mover:
                board[torre_a_mover] = (torre_dest_col, fila_origen)


    if 'rey' in pieza:
        color = color_de(pieza)
        if esta_en_jaque_en(board, color):
            return False

  
    color = color_de(pieza)
    return not esta_en_jaque_en(board, color)

def dibujar_tablero():
    for fila in range(8):
        for columna in range(8):
            color = blanco if (fila + columna) % 2 == 0 else marron
            pygame.draw.rect(pantalla, color,
                             (columna * tamaño_celda, fila * tamaño_celda,
                              tamaño_celda, tamaño_celda))

def dibujar_piezas():
    for pieza, (columna, fila) in posiciones_piezas.items():
        img = piezas.get(pieza)
        if img:
            pantalla.blit(img, (columna * tamaño_celda, fila * tamaño_celda))

def movimiento_valido(pieza, nueva_pos):
    col, fila = posiciones_piezas[pieza]
    nueva_col, nueva_fila = nueva_pos
    dx = abs(nueva_col - col)
    dy = abs(nueva_fila - fila)

    if (nueva_col, nueva_fila) == (col, fila):
        return False

    pieza_destino = obtener_pieza_en_posicion(nueva_col, nueva_fila)
    if pieza_destino and mismo_color(pieza, pieza_destino):
        return False

  
    if 'rey' in pieza:
      
        if dx <= 1 and dy <= 1:
            return True
      
        if dy == 0 and dx == 2:
            color = color_de(pieza)
            lado = 'corto' if nueva_col > col else 'largo'
            return puede_enrocar_en(posiciones_piezas, color, lado)
        return False

   
    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

    
    if 'alfil' in pieza:
        if dx == dy:
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    
    if 'torre' in pieza:
        if (col == nueva_col) or (fila == nueva_fila):
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    
    if 'reina' in pieza:
        if (dx == dy) or (col == nueva_col) or (fila == nueva_fila):
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    
    if 'peon' in pieza:
        color = color_de(pieza)
        direccion = 1 if color == 'blanco' else -1
        inicio = 1 if color == 'blanco' else 6

        if nueva_col == col and nueva_fila == fila + direccion:
            if obtener_pieza_en_posicion(nueva_col, nueva_fila) is None:
                return True
            return False

        if fila == inicio and nueva_col == col and nueva_fila == fila + 2 * direccion:
            if (obtener_pieza_en_posicion(col, fila + direccion) is None and
                obtener_pieza_en_posicion(nueva_col, nueva_fila) is None):
                return True
            return False

        if dx == 1 and nueva_fila == fila + direccion:
            if pieza_destino and not mismo_color(pieza, pieza_destino):
                return True
            return False

        return False

    return False


pieza_seleccionada = None
turno = 'blanco'

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            columna, fila = x // tamaño_celda, y // tamaño_celda
            pieza_clic = obtener_pieza_en_posicion(columna, fila)

            if pieza_seleccionada:
                if movimiento_valido(pieza_seleccionada, (columna, fila)):
                    if movimiento_legal(pieza_seleccionada, (columna, fila)) and color_de(pieza_seleccionada) == turno:
                        victima = obtener_pieza_en_posicion(columna, fila)
                        if victima and not mismo_color(pieza_seleccionada, victima):
                            posiciones_piezas.pop(victima)
                            piezas.pop(victima, None)

                        origen = posiciones_piezas[pieza_seleccionada]
                        posiciones_piezas[pieza_seleccionada] = (columna, fila)

                        if 'rey' in pieza_seleccionada:
                            col_origen, fila_origen = origen
                            col_dest, fila_dest = (columna, fila)
                            if fila_origen == fila_dest and abs(col_dest - col_origen) == 2:
                                if col_dest > col_origen:
                                    torre_origen_col, torre_dest_col = 7, 5
                                else:
                                    torre_origen_col, torre_dest_col = 0, 3
                                torre_a_mover = obtener_pieza_en_posicion(torre_origen_col, fila_origen)
                                if torre_a_mover and 'torre' in torre_a_mover:
                                    posiciones_piezas[torre_a_mover] = (torre_dest_col, fila_origen)
                                    piezas_movidas[torre_a_mover] = True

                            piezas_movidas[pieza_seleccionada] = True

                        if 'torre' in pieza_seleccionada:
                            piezas_movidas[pieza_seleccionada] = True

                        if 'peon' in pieza_seleccionada:
                            colp, filap = posiciones_piezas[pieza_seleccionada]
                            es_blanco = (color_de(pieza_seleccionada) == 'blanco')
                            if (es_blanco and filap == 7) or (not es_blanco and filap == 0):
                                seleccion = None
                                mensaje = "Promoción: presiona Q=Reina, T=Torre, A=Alfil, C=Caballo"
                                print(mensaje)
                                esperando = True
                                while esperando:
                                    for e in pygame.event.get():
                                        if e.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if e.type == pygame.KEYDOWN:
                                            k = pygame.key.name(e.key).upper()
                                            if k in ['Q', 'T', 'A', 'C']:
                                                seleccion = k
                                                esperando = False
                                    pygame.time.wait(50)

                                nonlocal_counter = globals().get('contador_promocion', 0)
                                globals()['contador_promocion'] = nonlocal_counter + 1
                                suf_color = 'blanca' if es_blanco else 'negra'

                                if seleccion == 'Q':
                                    nombre = 'reina'
                                    key_base = f'reina_{suf_color}'
                                elif seleccion == 'T':
                                    nombre = 'torre'
                                    key_base = f'torre_{suf_color}'
                                elif seleccion == 'A':
                                    nombre = 'alfil'
                                    key_base = f'alfil_{suf_color}'
                                else:
                                    nombre = 'caballo'
                                    key_base = f'caballo_{suf_color}'

                                nueva_clave = f"{nombre}_{suf_color}_prom{globals()['contador_promocion']}"
                                if piezas.get(key_base):
                                    piezas[nueva_clave] = piezas[key_base]
                                else:
                                    piezas[nueva_clave] = piezas[f'{nombre}{suf_color}'] if piezas.get(f'{nombre}{suf_color}') else list(piezas.values())[0]

                                posiciones_piezas.pop(pieza_seleccionada, None)
                                piezas.pop(pieza_seleccionada, None)
                                posiciones_piezas[nueva_clave] = (colp, filap)

                        pieza_seleccionada = None
                        turno = 'negro' if turno == 'blanco' else 'blanco'
                    else:
                        if pieza_clic and color_de(pieza_clic) == turno:
                            pieza_seleccionada = pieza_clic
                        else:
                            pieza_seleccionada = None
                else:
                    if pieza_clic and color_de(pieza_clic) == turno:
                        pieza_seleccionada = pieza_clic
                    else:
                        pieza_seleccionada = None
            else:
                if pieza_clic and color_de(pieza_clic) == turno:
                    pieza_seleccionada = pieza_clic

    dibujar_tablero()
    dibujar_piezas()

    if pieza_seleccionada:
        col, fil = posiciones_piezas[pieza_seleccionada]
        pygame.draw.rect(pantalla, amarillo,
                         (col * tamaño_celda, fil * tamaño_celda,
                          tamaño_celda, tamaño_celda), 5)

    en_jaque_blanco = esta_en_jaque('blanco')
    en_jaque_negro = esta_en_jaque('negro')

    if en_jaque_blanco:
        pos = posicion_rey_en(posiciones_piezas, 'blanco')
        if pos:
            col, fil = pos
            pygame.draw.rect(pantalla, rojo,
                             (col * tamaño_celda, fil * tamaño_celda, tamaño_celda, tamaño_celda), 7)
            texto = fuente.render('¡Jaque a BLANCAS!', True, rojo)
            pantalla.blit(texto, (20, 10))

    if en_jaque_negro:
        pos = posicion_rey_en(posiciones_piezas, 'negro')
        if pos:
            col, fil = pos
            pygame.draw.rect(pantalla, rojo,
                             (col * tamaño_celda, fil * tamaño_celda, tamaño_celda, tamaño_celda), 7)
            texto = fuente.render('¡Jaque a NEGRAS!', True, rojo)
            pantalla.blit(texto, (20, 60))
    pygame.display.flip()