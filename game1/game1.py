from pygame import sprite

from pygame.locals import*

import pygame
import sys
import os

#inicializamos el pygame

pygame.init() 

#Datos de las ventanas
ventana= pygame.display.set_mode((700,400))
pygame.display.set_caption("Game juego 1")

#Bucle del juego
while True:
    for event in pygame.event.get():
        #Uso de los objetos Sprites

        #Al apretar teclas
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                ventana.fill(pygame.Color("blue"))
            if keys[K_a]:
                ventana.fill(pygame.Color("red"))
            if keys[K_d]:
                ventana.fill(pygame.Color("green"))
                     
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()