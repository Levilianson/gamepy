import pygame

pygame.init()

ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("JUEGO DE NAVES")

def main():
    jugando= True
    while jugando:
        #OBTIENE LOS EVENTOS Y LOS RECORRE
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                jugando= False
    pygame.quit()
# SI EJECUTAN DIRECTO EL ARCHIVO
if __name__=="__main__":
    main()