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

