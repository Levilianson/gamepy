from pygame import sprite

from pygame.locals import*

import pygame
import sys

pygame.init()
ventana = pygame.display.set_mode((700,400))
# Reloj para actualizar la imagen
clock = pygame.time.Clock()
#Uso de Spirte objeto de pygame
class Personaje(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        #Uso completo del sprite alpha es trasparencias
        self.spriteSheet = pygame.image.load("game1/sprites/boy.png").convert_alpha()
        #escalamos la imagen
        self.image = pygame.transform.scale(self.spriteSheet.subsurface((0,0,42,80)),(400,200))
        #para mostrar la imagen
        self.rect = self.image.get_rect()
        self.rect.center= (ventana.get_width()/2, ventana.get_height()/2)
        self.frame = 6 #maximo de imagenes       
        self.current_frame = 0
        self.frame_width = 80
        self.frame_height = 100

    #Metodo heredado aqui actualizamos el personaje
    def update(self, dt, ventana):
        if self.current_frame >= self.frame -1:
            self.current_frame = 0
        else:
            self.current_frame += 3*dt
        #Recortamos las imagenes para hacer el movimiento
        self.image = pygame.transform.scale(self.spriteSheet.subsurface((int(self.current_frame)*
            self.frame_width*2,0,40,80)),(self.frame_width, self.frame_height))

magikarp = Personaje()
#Buenas practicas que los sprite sean individuales
grupo_sprites = pygame.sprite.GroupSingle()
grupo_sprites.add(magikarp)

#juego
while True:
    #30 por segundo en cada iteracion sino se reinicia
    dt = clock.tick(30)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    #Actualizacion de objetos
    ventana.fill((0,0,0))
    grupo_sprites.update(dt, ventana)
    #dibujo grupos
    grupo_sprites.draw(ventana)
    # actualiza la ventana
    pygame.display.flip()
