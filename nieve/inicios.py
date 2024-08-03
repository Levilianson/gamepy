import pygame
import sys
from math import pi

#Pantalla
ANCHO_PANTALLA  = 800
ALTO_PANTALLA   = 700
COLOR_FONDO     = (34, 121, 153)
COLOR_ELEMENTOS = (153, 88, 18)

size= (ANCHO_PANTALLA, ALTO_PANTALLA)
clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode(size)
screen.fill(COLOR_FONDO)

pygame.display.set_caption("Titulo")
# NO SE UTILIZA EL MAIN YA QUE ES SOLO UN MUESTREO DE LA PANTALLA
while True:
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            sys.exit()
        
        #dibujo objetos
        pygame.draw.rect(screen, COLOR_ELEMENTOS, (200, 200, 50, 50),
            width=0, border_radius= 9, border_bottom_left_radius= 9,
            border_bottom_right_radius= 0, border_top_right_radius= 0,
            border_top_left_radius= 0,)
        
        pygame.draw.polygon(screen, COLOR_ELEMENTOS,
                [[100, 100], [0, 200], [200, 200]], 8)
        
        pygame.draw.line(screen, COLOR_ELEMENTOS,
                [400, 0], [400, 200], 4)
        
        pygame.draw.arc(screen, COLOR_ELEMENTOS, [210, 75, 150, 125],
                0, pi/2, 10)
        
        pygame.draw.circle(screen, COLOR_ELEMENTOS, [500, 500], 90, 20,
                draw_bottom_left= True, draw_bottom_right= True,
                draw_top_left= True, draw_top_right= True)
        
        pygame.draw.ellipse(screen, COLOR_ELEMENTOS, [100, 500, 70, 50], 8)

        pygame.draw.aaline(screen, COLOR_ELEMENTOS, [700, 0],
                [700, 700], False,)

        pygame.display.flip() #inicia ventana
        clock.tick(30)