import pygame
import sys 

pygame.init()

ancho, alto = 800, 800
tamaño_celda = ancho // 8
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Ajedrez')
blanco = (255, 255, 255)
negro= (0, 0, 0)

def cargar_imagen_pieza(nombre):
  imagen = pygame.image.load(nombre)
  return pygame.transform.scale(imagen, (tamaño_celda, tamaño_celda))

pizas = {

        'rey_blanco': cargar_imagen_pieza('rey_blanco.png'),
        'rey_negro': cargar_imagen_pieza('rey_negro.png'),
        'reina_blanca': cargar_imagen_pieza('reina_blanca.png'),
        'reina_negra': cargar_imagen_pieza('reina_negra.png'),
        'torre_blanco': cargar_imagen_pieza('torre_blanco.png'),
        'torre_blanca2': cargar_imagen_pieza('torre_blanca.png'),
        'torre_negra': cargar_imagen_pieza ('torre_negra.png'),
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

posiciones_piezas= {
     'rey_blanco': (4,0), 'rey_negro':(4,7),
     'reina_blanca': (3,0), 'reina_negra':(3,7),
     'torre_blanca': (0,0), 'torre_blanca2':(7,0),
     'torre_negra': (0,7), 'torre_negra2':(7,7),
     'alfil_blanco': (2,0), 'alfil_blanco2':(5,0),
     'alfil_negro': (2,7), 'alfil_negro2':(5,7),
     'caballo_blanco': (1,0), 'caballo_blanco2':(6,0),
     'caballo_negro': (1,7), 'caballo_negro2':(6,7),
     **{f'peon_blanco{i}' : (i,1) for i in range (8)},
     **{f'peon_negro{i}' : (i,6) for i in range (8)},
}
def dibujar_tabalero():
  pantalla.fill(blanco)
  for fila in range (8):
    for columna in range(8):
        color = blanco if (fila + columna) % 2 == 0 else negro 
        pygame.draw.rect(pantalla, color, (columna * tamaño_celda, fila * tamaño_celda,  tamaño_celda, tamaño_celda))

def dibujar_pieza():
  for pieza, (columna, fila) in posiciones_piezas.items():
   pantalla.blit(pieza[pieza], (columna * tamaño_celda, fila * tamaño_celda))

def movimiento_valido(pieza, nueva_posicion):
    col, fila = posiciones_piezas[pieza]
    nueva_col, nueva_fila = nueva_posicion

    if 'rey' in pieza: 
        return abs(col - nueva_col) <= 1 and abs(fila - nueva_fila) <= 1
    elif 'reina' in pieza:
        return col == nueva_col or fila == nueva_fila or abs(col - nueva_col) == abs(fila-nueva_fila)
    elif 'torre' in pieza:
        return col == nueva_col or fila == nueva_fila
    elif 'alfil' in pieza:
        return abs(col - nueva_col) == abs(fila - nueva_fila)
    elif 'caballero' in pieza: 
        return (abs(col - nueva_col), abs(fila - nueva_fila)) in [(1, 2)(2,1)]
    elif 'peon' in pieza:
        direccion = 1 if 'blanco' in pieza else -1
        return nueva_fila == fila + direccion and (nueva_col == col or abs(nueva_col - col) == 1) 
    return False
pieza_seleccionada= None 

while True:
     for evento in pygame.event.get():
          if evento.type  == pygame.QUIT:
               pygame.quit()
               sys.exit()
          elif evento.type == pygame.MOUSEBUTTONDOWN:
               x, y = evento.pos 
               columna, fila = x // tamaño_celda, y // tamaño_celda
               if pieza_seleccionada:
                    if movimiento_valido(pieza_seleccionada, (columna, fila )):
                         pieza_seleccionada[pieza_seleccionada] = (columna, fila)
                    pieza_seleccionada = None 
               else: 
                    for pieza, (col, fil) in posiciones_piezas.items():
                         if (col, fil) == (columna, fila):
                              pieza_seleccionada = pieza
                              break
     dibujar_tabalero()
     dibujar_pieza()
     pygame.display.flip()