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

        'rey_blanco': cargar_imagen_pieza('rey_blanco.png')

}