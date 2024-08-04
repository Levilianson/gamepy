import pygame
import sys
import random
#from objetos.objetos import *
from objetos.objetos import Suelo
from objetos.objetos import Heroe
from objetos.objetos import Bola_hielo
from objetos.objetos import Enemy

ANCHO_PANTALLA= 800
ALTO_PANTALLA = 600
COLOR_FONDO= (34, 121, 153)
size= (ANCHO_PANTALLA, ALTO_PANTALLA)
clock= pygame.time.Clock()
BLACK= (0, 0, 0)
WHITE= (255, 255, 255)

pygame.init()

#sonidos
pygame.mixer.init()
game_over= pygame.mixer.Sound('nieve/Audio/gameover.wav')
explosion= pygame.mixer.Sound('nieve/Audio/explosion.wav')
disparo= pygame.mixer.Sound('nieve/Audio/disparo.wav')
colisionEnemigo= pygame.mixer.Sound('nieve/Audio/colisionEnemigo.wav')

screen= pygame.display.set_mode(size)
screen.fill(COLOR_FONDO)
pygame.display.set_caption("juego")

inicio= pygame.image.load('nieve/fondos/fondo2.png').convert()
fondo= pygame.image.load('nieve/fondos/fondo1.png').convert()
lista_suelo= pygame.sprite.Group()
todos_lista= pygame.sprite.Group()

suelo= Suelo()
suelo.rect.x= 0
suelo.rect.y= 570
lista_suelo.add(suelo)
todos_lista.add(suelo)

enemy_list= pygame.sprite.Group()

for dragon in range(20):
    enemy= Enemy()
    enemy.rect.x= random.randrange(800)
    enemy.rect.y= random.randint((-1400),20)

    enemy_list.add(enemy)

puntuacion= 0
vidas= 3
en_juego= True
en_inicio= any
en_partida= any
heroe= Heroe((0, 257))
vel_heroe_x= 0

#botones
exit_img= pygame.image.load('nieve/imagen/salir.png').convert()
start_img= pygame.image.load('nieve/imagen/entrar.png').convert()

class Button():
    def __init__(self, x, y, image, scale):
        width= image.get_width()
        heigth= image.get_height()
        self.image= pygame.transform.scale(image,(int(width*scale),int(heigth*scale)))
        self.rect= self.image.get_rect()
        self.rect.topleft= (x, y)
        self.clicked= False

    def draw(self):
        action= False
        pos= pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked= True
                action= True
                print("clicked")
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked= False

            screen.blit(self.image, (self.rect.x, self.rect.y))
            return action

start_button= Button(300, 220, start_img, 0.1)
exit_button= Button(300, 300, exit_img, 0.1) 

#TEXTO
fuente= pygame.font.SysFont("consolas", 40)

bola= Bola_hielo()

def update_bola():
    screen.blit(bola.image, bola.rect)

    if heroe.disparo:
        bola.rect.y -=15
        if bola.rect.y < 20:
            bola.rect.y = heroe.rect.y
            bola.rect.x = heroe.rect.x

            heroe.disparo = False
    
    else:
        bola.rect.y = heroe.rect.y
        bola.rect.x = heroe.rect.x

#Principal
while en_juego:
    if vidas >=0:
        en_inicio = True
        en_partida= False
    
    while en_inicio:
        vidas = 3
        puntuacion= 0

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                sys.exit()
        screen.blit(inicio, (0, 0))

        if start_button.draw():
            en_inicio= False
            en_partida= True
        
        if exit_button.draw():
            sys.exit()

        pygame.display.flip()
        clock.tick(30)

    while en_partida:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                sys.exit()

        screen.blit(fondo,(0, 0))
        enemy_list.draw(screen)
        screen.blit(heroe.image, heroe.rect)
        heroe.handle_event(event)

        v= fuente.render("VIDAS : " + str(vidas), True, WHITE, BLACK)
        p= fuente.render("PUNTOS : "+ str(puntuacion), True, WHITE, BLACK)

        screen.blit(v,(200, 20))
        screen.blit(p,(400, 20))

        colision_jugador = pygame.sprite.collide_rect(heroe, suelo)
        colision_enemigo = pygame.sprite.spritecollide(heroe, enemy_list, True)
        colision_bola = pygame.sprite.spritecollide(bola, enemy_list, True)

        if colision_bola:
            puntuacion += 1
            explosion.play()
        
        if colision_jugador:
            heroe.rect.y += 0
        else:
            heroe.rect.y += 5

        if colision_enemigo:
            vidas -= 1
            colisionEnemigo.play()
            if vidas <= -1:
                en_juego= True
                en_inicio= True
                en_partida= False
                game_over.play()

        #salto
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if colision_jugador:
                    if heroe.derecha:
                        heroe.rect.y -= 89
                        heroe.rect.x += 80
                    if heroe.izquierda:
                        heroe.rect.y -= 89
                        heroe.rect.x -= 80
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            disparo.play()

        todos_lista.draw(screen)

        for enemy in enemy_list:
            enemy.rect.y += 2
            if enemy.rect.y >600:
                enemy.rect.y = -100

        update_bola()

        pygame.display.flip()
        clock.tick(30)