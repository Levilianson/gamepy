from pygame import sprite

from pygame.locals import*

import pygame
import sys
import random
import os
#Si falla el sonido y se retrasa 
#pygame.mixer.pre_init(44100,-16,2,2048)
#pygame.mixer.init()
pygame.init()

ventana = pygame.display.set_mode((700,400))
# Reloj para actualizar la imagen
clock = pygame.time.Clock()
#Uso de Spirte objeto de pygame
class Personaje(sprite.Sprite):

    def __init__(self):
        sprite.Sprite.__init__(self)
        #Uso completo del sprite alpha es trasparencias
        self.spriteSheet = pygame.image.load("game1/sprites/sheet.png").convert_alpha()
        #escalamos la imagen
        self.image = pygame.transform.scale(self.spriteSheet.subsurface((780,1900,200,420)),(100,200))
        #para mostrar la imagen
        self.rect = self.image.get_rect()
        self.rect.center= (ventana.get_width()/2, ventana.get_height()/2)

        sprite.mask = pygame.mask.from_surface(self.image)

        self.speed = 10

        #Para el control de los objetos
        self.frame = 8 #maximo de imagenes
        self.current_frame = 0
        self.frame_width = 100
        self.frame_height = 200

    #Metodo heredado aqui actualizamos el personaje
    def update(self, dt, ventana):
        if self.current_frame >= self.frame -1:
            self.current_frame = 0
        else:
            self.current_frame += 3*dt

        #Recortamos las imagenes para hacer el movimiento
        self.image = pygame.transform.scale(self.spriteSheet.subsurface((int(self.current_frame)*
            self.frame_width*2,1800,200,420)),(self.frame_width, self.frame_height))
        # frame horizontal, vertical, posicionx e y pantalla, largo y ancho
    def mover(self, x=0, y=0):
        #Para no salir del mapa
        if self.rect.centerx+x >= ventana.get_width() or self.rect.centerx+x < 0:
            return
        if self.rect.centery+y >= ventana.get_height() or self.rect.centery+y <0:
            return
        self.rect.center = (self.rect.centerx+x, self.rect.centery+y)

magikarp = Personaje()
speed= magikarp.speed
#Buenas practicas que los sprite sean individuales
grupo_sprites = pygame.sprite.GroupSingle()
grupo_sprites.add(magikarp)

magikarp_obstaculo = Personaje()
magikarp_obstaculo.rect.center = (ventana.get_width()-100), ventana.get_height()/2
grupo_obstaculo = pygame.sprite.GroupSingle()
grupo_obstaculo.add(magikarp_obstaculo)

# Sonido atravez del mixer
pygame.mixer.init()
if pygame.mixer.get_init() is not None:
    pj_music = pygame.mixer.Sound("game1/sound"+os.sep+"sound06.wav")

#juego
while True:
    #30 por segundo en cada iteracion sino se reinicia
    dt = clock.tick(30) /1000
    pixels_h = pixels_v = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                pixels_v = -speed
                pixels_h = 0
            if keys[K_a]:
                pixels_v = 0
                pixels_h = -speed
            if keys[K_d]:
                pixels_v = 0
                pixels_h = speed
            if keys[K_s]:
                pixels_v = speed
                pixels_h = 0
    
    for i in grupo_sprites:
        if pixels_v !=0 or pixels_h !=0:
            pj_music.play()
            i.mover(pixels_h, pixels_v)
    
    #Si hay colicion
    if pygame.sprite.collide_mask(magikarp, magikarp_obstaculo):
        #Evitar que se corte las imagenes
        magikarp_obstaculo.rect.center= (ventana.get_width()/2 + int(random.uniform(-300,300)),
                                         ventana.get_height()/2 + int(random.uniform(-200,100)))
    
    #Actualizacion de objetos
    ventana.fill((0,0,0))
    grupo_sprites.update(dt, ventana)
    #dibujo grupos
    grupo_sprites.draw(ventana)
    grupo_obstaculo.draw(ventana)
    # actualiza la ventana
    pygame.display.flip()#pygame.display.update() es lo mismo
