import pygame
import sys

pygame.init()

# --- Configuración general ---
ancho, alto = 800, 800
tamaño_celda = ancho // 8
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Ajedrez en Pygame')

# Colores
blanco = (240, 217, 181)
marron = (181, 136, 99)
amarillo = (255, 255, 0)

# --- Cargar imágenes ---
def cargar_imagen_pieza(nombre):
    try:
        imagen = pygame.image.load(nombre)
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

# --- Funciones de dibujo ---
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

# --- Reglas de movimiento ---
def movimiento_valido(pieza, nueva_pos):
    col, fila = posiciones_piezas[pieza]
    nueva_col, nueva_fila = nueva_pos
    dx = abs(nueva_col - col)
    dy = abs(nueva_fila - fila)

    # --- REY ---
    if 'rey' in pieza:
        return dx <= 1 and dy <= 1

    # --- REINA ---
    if 'reina' in pieza:
        return (dx == dy) or (col == nueva_col) or (fila == nueva_fila)

    # --- TORRE ---
    if 'torre' in pieza:
        return (col == nueva_col) or (fila == nueva_fila)

    # --- ALFIL ---
    if 'alfil' in pieza:
        return dx == dy

    # --- CABALLO ---
    if 'caballo' in pieza:
        return (dx, dy) in [(1, 2), (2, 1)]

    # --- PEÓN ---
    if 'peon' in pieza:
        direccion = 1 if 'blanco' in pieza else -1
        # Movimiento hacia adelante
        if nueva_col == col and nueva_fila == fila + direccion:
            return True
        # Movimiento inicial de dos pasos
        if nueva_col == col and ((fila == 1 and 'blanco' in pieza) or (fila == 6 and 'negro' in pieza)):
            if nueva_fila == fila + 2 * direccion:
                return True
        # Captura diagonal
        if dx == 1 and nueva_fila == fila + direccion:
            pieza_en_destino = obtener_pieza_en_posicion(nueva_col, nueva_fila)
            if pieza_en_destino and ('blanco' in pieza) != ('blanco' in pieza_en_destino):
                return True
    return False

# --- Bucle principal ---
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
                # Intentar mover
                if movimiento_valido(pieza_seleccionada, (columna, fila)):
                    # Si hay pieza enemiga, la elimina
                    pieza_destino = obtener_pieza_en_posicion(columna, fila)
                    if pieza_destino and ('blanco' in pieza_destino) != ('blanco' in pieza_seleccionada):
                        posiciones_piezas.pop(pieza_destino)
                    # Actualizar posición
                    posiciones_piezas[pieza_seleccionada] = (columna, fila)
                    pieza_seleccionada = None
                    turno = 'negro' if turno == 'blanco' else 'blanco'
                else:
                    pieza_seleccionada = None
            else:
                # Seleccionar pieza del turno correcto
                if pieza_clic and turno in pieza_clic:
                    pieza_seleccionada = pieza_clic

    # Dibujar todo
    dibujar_tablero()
    dibujar_piezas()

    if pieza_seleccionada:
        col, fil = posiciones_piezas[pieza_seleccionada]
        pygame.draw.rect(pantalla, amarillo,
                         (col * tamaño_celda, fil * tamaño_celda,
                          tamaño_celda, tamaño_celda), 5)

    pygame.display.flip()
