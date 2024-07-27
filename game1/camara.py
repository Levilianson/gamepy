from pygame import sprite
from pygame.locals import*

import pygame
import sys

WIDTH = 800
HEIGHT = 600
TOTAL_WIDTH=1000
TOTAL_HEIGHT= 700

pygame.init()

ventana = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("tipo camara")

class Magikarp(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.spriteSheet = pygame.image.load("game1/sprites/sheet.png").convert_alpha()
        self.image = pygame.transform.scale(self.spriteSheet.subsurface((0,0,200,420)),(100,200))
        self.rect= self.image.get_rect()
        self.rect.center = (TOTAL_WIDTH/2, TOTAL_HEIGHT/2)

        self.speed = 10

        self.frames = 4
        self.current_frame = 0
        self.frame_width = 100
        self.frame_height = 200
    
    def update(self, dt, ventana):
        if self.current_frame >= self.frames -1:
            self.current_frame = 0
        else:
            self.current_frame += 3*dt
    
        self.image= pygame.transform.scale(
            self.spriteSheet.subsurface((int(self.current_frame)*self.frame_width*2,0,200,420)),
            (self.frame_width,self.frame_height))
    def mover(self, x=0, y=0):
        if self.rect.centerx+x >= TOTAL_WIDTH or self.rect.centerx+x < 0:
            return
        if self.rect.centery+y >= TOTAL_HEIGHT or self.rect.centery+y <0:
            return
        
        self.rect.center = (self.rect.centerx+x, self.rect.centery+y)

class Camera(object):
    def __init__(self, camera_func, width, heigth):
        self.camera_func = camera_func 
        self.state = Rect(0, 0, width, heigth)

    # sobre el objeto donde se va a seguir
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    
    #desplaza al mundo
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

#camaras simples 1 con limites y la otra con limites de otra manera
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _,_, w, h = camera
    return Rect(-l + WIDTH//2, -t+HEIGHT//2, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _=target_rect
    _, _, w, h = camera
    l, t, _, _= -l+WIDTH//2, -t + HEIGHT//2, w, h

    l= min(0, l)
    l= max(-(camera.width - WIDTH), l)
    t= max(-(camera.height - HEIGHT), t)
    t= min(0, t)
    return Rect(l,t,w,h)

camera = Camera(complex_camera, TOTAL_WIDTH, TOTAL_HEIGHT)
main_pj=Magikarp()
otro_pj= Magikarp()
otro_pj.rect.centerx = 900
otro_pj.rect.centery = 450
#donde van los elementos
ingame_elements = pygame.sprite.Group()
ingame_elements.add(otro_pj)
ingame_elements.add(main_pj)

clock = pygame.time.Clock()
#bucle principal
while True:
    dt = clock.tick(30) / 1000
    pixels_h = pixels_v =0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys= pygame.key.get_pressed()
        if keys[K_w]:
            pixels_v= -main_pj.speed
        if keys[K_a]:
            pixels_h= -main_pj.speed
        if keys[K_d]:
            pixels_h= main_pj.speed
        if keys[K_s]:
            pixels_v= main_pj.speed

    ventana.fill((255,255,0)) #limpia pantalla
    camera.update(main_pj)
    main_pj.mover(pixels_h, pixels_v)
    ingame_elements.update(dt, ventana)
    for e in ingame_elements:
        ventana.blit(e.image, camera.apply(e))

    pygame.display.update()