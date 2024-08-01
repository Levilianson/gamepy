import pygame
import os

pygame.init()
#CARGAR IMAGENES
def cargarImagen(imagen):
    #CONTRUYE LA RUTA Y LUEGO CARGA LA IMAGEN
    ruta = os.path.join("cursogame\image",imagen)
    return pygame.image.load(ruta)
ANCHO = 800
ALTO = 600

def crearFondo():
    #CREA UNA IMAGEN  TIPO MOSAICO
    img = pygame.surface.Surface((ANCHO, ALTO))
    pieza = cargarImagen("stars.png")
    y=0 #RECORRE LA PANTALLA Y VA COLOCANDO LAS IMAGENES
    while (y < ALTO):
        x=0
        while (x <ANCHO):
            img.blit(pieza, (x,y))
            x += pieza.get_width()
        y += pieza.get_height()
    return img
#INICIALIZA LA VENTANA PRINCIPAL
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("NAVES DISPARANDO")
ICONO = cargarImagen("icon.png")
pygame.display.set_icon(ICONO)

FONDO = crearFondo()
#DIBUJA LA PANTALLA EN CADA ITERACION
def dibuja():
    PANTALLA.blit(FONDO, (0, 0))
    pygame.display.update() #actualiza

def main():
    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
        dibuja() 
    pygame.quit()

if __name__=="__main__":
    main()