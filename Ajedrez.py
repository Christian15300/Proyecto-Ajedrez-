import pygame
import sys
import os  #  Agrega esta línea justo encima o al inicio del archivo


pygame.init()

# --- Configuración general ---
ancho, alto = 800, 800
tamaño_celda = ancho // 8
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Ajedrez en Pygame')

# Fuentes
fuente = pygame.font.SysFont(None, 48)

# Colores
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
    'torre_blanca': cargar_imagen_pieza('torre_blanco.png'),
    'torre_blanca2': cargar_imagen_pieza('torre_blanco.png'),
    'torre_negra': cargar_imagen_pieza('torre_negra.png'),
    'torre_negra2': cargar_imagen_pieza('torre_negra.png'),
    'alfil_blanco': cargar_imagen_pieza('alfil_blanco.png'),
    'alfil_blanco2': cargar_imagen_pieza('alfil_blanco.png'),
    'alfil_negro': cargar_imagen_pieza('alfil_negro.png'),
    'alfil_negro2': cargar_imagen_pieza('alfil_negro.png'),
    'caballo_blanco': cargar_imagen_pieza('caballo_blanco.png'),
    'caballo_blanco2': cargar_imagen_pieza('caballo_blanco.png'),
    'caballo_negro': cargar_imagen_pieza('caballo_negro.png'),
    'caballo_negro2': cargar_imagen_pieza('caballo_negro.png'),
    **{f'peon_blanco{i}': cargar_imagen_pieza('peon_blanco.png') for i in range(8)},
    **{f'peon_negro{i}': cargar_imagen_pieza('peon_negro.png') for i in range(8)},
}

# --- Posiciones iniciales ---
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

# =========================
# Patrón de movimiento (sin chequear jaque)
# =========================
def movimiento_por_patron(pieza, nueva_pos, board=None):
    if board is None:
        board = posiciones_piezas

    col, fila = board[pieza]
    nueva_col, nueva_fila = nueva_pos
    dx = abs(nueva_col - col)
    dy = abs(nueva_fila - fila)

    if (nueva_col, nueva_fila) == (col, fila):
        return False

    # no caer sobre aliada
    pieza_destino = obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila)
    if pieza_destino and mismo_color(pieza, pieza_destino):
        return False

    # REY
    if 'rey' in pieza:
        return dx <= 1 and dy <= 1

    # CABALLO
    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

    # ALFIL
    if 'alfil' in pieza:
        return dx == dy and camino_libre_board(board, col, fila, nueva_col, nueva_fila)

    # TORRE
    if 'torre' in pieza:
        return (col == nueva_col or fila == nueva_fila) and camino_libre_board(board, col, fila, nueva_col, nueva_fila)

    # REINA
    if 'reina' in pieza:
        recto = (col == nueva_col or fila == nueva_fila)
        diagonal = (dx == dy)
        return (recto or diagonal) and camino_libre_board(board, col, fila, nueva_col, nueva_fila)

    # PEÓN
    if 'peon' in pieza:
        color = color_de(pieza)
        direccion = 1 if color == 'blanco' else -1
        inicio = 1 if color == 'blanco' else 6

        # avance 1 (casilla libre)
        if nueva_col == col and nueva_fila == fila + direccion:
            if obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila) is None:
                return True
            return False

        # avance 2 desde inicio (ambas libres)
        if fila == inicio and nueva_col == col and nueva_fila == fila + 2 * direccion:
            if (obtener_pieza_en_posicion_board(board, col, fila + direccion) is None and
                obtener_pieza_en_posicion_board(board, nueva_col, nueva_fila) is None):
                return True
            return False

        # captura diagonal
        if dx == 1 and nueva_fila == fila + direccion:
            if pieza_destino and not mismo_color(pieza, pieza_destino):
                return True
            return False

        return False

    return False

# =========================
# Ataques y jaque (en un tablero dado)
# =========================
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

# =========================
# Legalidad completa (patrón + simulación anti-jaque)
# =========================
def movimiento_legal(pieza, nueva_pos):
    # 1) cumple patrón (incluye bloqueo de piezas propias y camino libre)
    if not movimiento_por_patron(pieza, nueva_pos, posiciones_piezas):
        return False

    # 2) simula el movimiento y verifica que el propio rey no quede en jaque
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

    # Si es el rey, además impedimos mover a casillas atacadas (esto ya se cubre con el jaque tras simular, pero lo dejamos explícito)
    if 'rey' in pieza:
        color = color_de(pieza)
        if esta_en_jaque_en(board, color):
            return False

    # Para cualquier pieza: después del movimiento, tu rey no puede estar en jaque
    color = color_de(pieza)
    return not esta_en_jaque_en(board, color)

# =========================
# Dibujo
# =========================

def dibujar_tablero():
    for fila in range(8):
        for columna in range(8):
            color = blanco if (fila + columna) % 2 == 0 else marron
            pygame.draw.rect(pantalla, color,
                             (columna * tamaño_celda, fila * tamaño_celda,
                              tamaño_celda, tamaño_celda))

def dibujar_piezas():
    for pieza, (columna, fila) in posiciones_piezas.items():
        pantalla.blit(piezas[pieza],
                      (columna * tamaño_celda, fila * tamaño_celda))

def obtener_pieza_en_posicion(columna, fila):
    for pieza, (c, f) in posiciones_piezas.items():
        if (c, f) == (columna, fila):
            return pieza
    return None

def color_de(nombre_pieza):
    # Detecta blanco/blanca y negro/negra
    if ('blanco' in nombre_pieza) or ('blanca' in nombre_pieza):
        return 'blanco'
    if ('negro' in nombre_pieza) or ('negra' in nombre_pieza):
        return 'negro'
    return None

def mismo_color(p1, p2):
    return color_de(p1) == color_de(p2)

# --- Comprobación de camino libre (para torre/alfil/reina) ---
def camino_libre(col, fila, nueva_col, nueva_fila):
    dc = 0 if nueva_col == col else (1 if nueva_col > col else -1)
    df = 0 if nueva_fila == fila else (1 if nueva_fila > fila else -1)
    c, f = col + dc, fila + df
    while (c, f) != (nueva_col, nueva_fila):
        if obtener_pieza_en_posicion(c, f) is not None:
            return False
        c += dc
        f += df
    return True

# --- Reglas de movimiento ---
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

    # REY
    if 'rey' in pieza:
        return dx <= 1 and dy <= 1

    # CABALLO
    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

    # ALFIL
    if 'alfil' in pieza:
        if dx == dy:
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    # TORRE
    if 'torre' in pieza:
        if (col == nueva_col) or (fila == nueva_fila):
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    # REINA
    if 'reina' in pieza:
        if (dx == dy) or (col == nueva_col) or (fila == nueva_fila):
            return camino_libre(col, fila, nueva_col, nueva_fila)
        return False

    # PEÓN
    if 'peon' in pieza:
        color = color_de(pieza)
        direccion = 1 if color == 'blanco' else -1
        inicio = 1 if color == 'blanco' else 6

        # avance 1
        if nueva_col == col and nueva_fila == fila + direccion:
            if obtener_pieza_en_posicion(nueva_col, nueva_fila) is None:
                return True
            return False

        # avance 2 desde inicio
        if fila == inicio and nueva_col == col and nueva_fila == fila + 2 * direccion:
            if (obtener_pieza_en_posicion(col, fila + direccion) is None and
                obtener_pieza_en_posicion(nueva_col, nueva_fila) is None):
                return True
            return False

        # captura diagonal
        if dx == 1 and nueva_fila == fila + direccion:
            if pieza_destino and not mismo_color(pieza, pieza_destino):
                return True
            return False

        return False

    return False

# --- Bucle principal ---
# =========================
# Bucle principal
# =========================
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
                    # capturar si hay rival
                    pieza_destino = obtener_pieza_en_posicion(columna, fila)
                    if pieza_destino and not mismo_color(pieza_seleccionada, pieza_destino):
                        posiciones_piezas.pop(pieza_destino)
                # Solo permitimos movimientos legales (que quitan el jaque si lo hay)
                if movimiento_legal(pieza_seleccionada, (columna, fila)):
                    # capturar si hay rival
                    victima = obtener_pieza_en_posicion(columna, fila)
                    if victima and not mismo_color(pieza_seleccionada, victima):
                        posiciones_piezas.pop(victima)
                    # mover
                    posiciones_piezas[pieza_seleccionada] = (columna, fila)
                    pieza_seleccionada = None
                    turno = 'negro' if turno == 'blanco' else 'blanco'
                else:
                    # cambiar selección si clic en pieza del mismo turno
                    # re-selección si clic sobre propia pieza
                    if pieza_clic and color_de(pieza_clic) == turno:
                        pieza_seleccionada = pieza_clic
                    else:
                        pieza_seleccionada = None
            else:
                # Seleccionar pieza del turno correcto (funciona con blanca/blanco)

                if pieza_clic and color_de(pieza_clic) == turno:
                    pieza_seleccionada = pieza_clic

    # Dibujar
    dibujar_tablero()
    dibujar_piezas()

    # Resaltado de selección
    if pieza_seleccionada:
        col, fil = posiciones_piezas[pieza_seleccionada]
        pygame.draw.rect(pantalla, amarillo,
                         (col * tamaño_celda, fil * tamaño_celda,
                          tamaño_celda, tamaño_celda), 5)

    # --- Señalización de jaque ---
    en_jaque_blanco = esta_en_jaque('blanco')
    en_jaque_negro = esta_en_jaque('negro')

    if en_jaque_blanco:
        col, fil = posicion_rey_en(posiciones_piezas, 'blanco')
        pygame.draw.rect(pantalla, rojo,
                         (col * tamaño_celda, fil * tamaño_celda, tamaño_celda, tamaño_celda), 7)
        texto = fuente.render('¡Jaque a BLANCAS!', True, rojo)
        pantalla.blit(texto, (20, 10))

    if en_jaque_negro:
        col, fil = posicion_rey_en(posiciones_piezas, 'negro')
        pygame.draw.rect(pantalla, rojo,
                         (col * tamaño_celda, fil * tamaño_celda, tamaño_celda, tamaño_celda), 7)
        texto = fuente.render('¡Jaque a NEGRAS!', True, rojo)
        pantalla.blit(texto, (20, 60))

    pygame.display.flip()
