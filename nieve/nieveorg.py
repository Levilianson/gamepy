import pygame            #importamos la libreria 
import sys 
from objetos.objetos import Suelo 
from objetos.objetos import Heroe
from objetos.objetos import Bola_hielo
from objetos.objetos import Enemy
import random 


#variables 
ancho_pantalla=800 
alto_pantalla=600
color_fondo=(34,121,153)
size=(ancho_pantalla,alto_pantalla)
clock=pygame.time.Clock()  # esto es para optimizar las animaciones 
BLACK=(0,0,0) 
WHITE=(225,225,255)

#iniciamos pygame  
pygame.init() 

#Sonidos
pygame.mixer.init()
game_over=pygame.mixer.Sound("nieve/Audio/gameover.wav")
explosion=pygame.mixer.Sound("nieve/Audio/explosion.wav")
disparo=pygame.mixer.Sound("nieve/Audio/disparo.wav")
colisionEnemigo=pygame.mixer.Sound("nieve/Audio/colisionEnemigo.wav")



#crear ventana  
screen=pygame.display.set_mode(size)  
screen.fill(color_fondo)

#Titulo 
pygame.display.set_caption("Spaguetti Head")

#Imágenes de fondo  

inicio=pygame.image.load("nieve/fondos/fondo2.png").convert()
fondo=pygame.image.load("nieve/fondos/fondo1.png").convert()

#Suelo  
lista_suelo=pygame.sprite.Group()
todos_lista=pygame.sprite.Group()

#codigo del suelo  
suelo=Suelo()
suelo.rect.x=0
suelo.rect.y=570
lista_suelo.add(suelo)
todos_lista.add(suelo)

#Código de enemigos 
enemies_list=pygame.sprite.Group()

for dragon in range(20):
    enemy=Enemy()
    enemy.rect.x=random.randrange(800)
    enemy.rect.y=random.randint((-1400),20)

    enemies_list.add(enemy) 

#VARIABLES 
puntuacion=0 
vidas=3 
en_juego=True
en_inicio=any
en_partida=any
heroe=Heroe((0,257))
vel_heroe_x=0 



#BOTONES 

exit_img=pygame.image.load("nieve/imagen/salir.png").convert()
start_img=pygame.image.load("nieve/imagen/entrar.png").convert()

class Button(): 
    def __init__(self,x,y,image,scale): 
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
     
    def draw(self): 
        action=False 
        #cogemos la posicion del raton
        pos=pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False: 
                self.clicked=True 
                action=True 
                print("clicked")
        if  pygame.mouse.get_pressed()[0]==0: 
                self.clicked=False
        
            #pintar un boton en ventana 
 
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

#Crear instancias  
start_button=Button(300,220,start_img,0.1)
exit_button=Button(300,300,exit_img,0.1)

#TEXTO###################################################

fuente=pygame.font.SysFont("consolas",40) #1.Creamos la fuente  

#################################################################


#CODIGO BolaHielo  
bola=Bola_hielo()

def update_bola(): 
    screen.blit(bola.image,bola.rect)
    
    if heroe.disparo:
       bola.rect.y-=15
       if bola.rect.y<20: 
           bola.rect.y=heroe.rect.y
           bola.rect.x=heroe.rect.x
           
           heroe.disparo=False
    else: 
        bola.rect.y=heroe.rect.y 
        bola.rect.x=heroe.rect.x


#Bucle principal  
while en_juego:
     
    if vidas>=0: 
        en_inicio=True
        en_partida=False
            
        
    while en_inicio: 
        vidas=3 
        puntuacion=0
          
        for event in pygame.event.get(): 
            if(event.type==pygame.QUIT):
                sys.exit()
        screen.blit(inicio,(0,0)) 
        
        if start_button.draw():
            en_inicio=False 
            en_partida=True
        
        if exit_button.draw():
            sys.exit()
       
       
     
        pygame.display.flip()
        clock.tick(30)

    while en_partida: 

        for event in pygame.event.get(): 
            if(event.type==pygame.QUIT):
                sys.exit()

        screen.blit(fondo,(0,0))
        enemies_list.draw(screen)
        screen.blit(heroe.image,heroe.rect)
        heroe.handle_event(event)

        #Texto de marcador  

        v=fuente.render("VIDAS :" + str(vidas) ,True,WHITE,BLACK )
        p=fuente.render("PUNTOS :" + str(puntuacion) ,True,WHITE,BLACK)

        screen.blit(v,(200,20))
        screen.blit(p,(400,20))
        
        #FISICAS DEL JUGADOR  
        colision_player=pygame.sprite.collide_rect(heroe,suelo)
        colision_enemies=pygame.sprite.spritecollide(heroe,enemies_list,True)
        colision_bola=pygame.sprite.spritecollide(bola,enemies_list,True)

        #Colision de bola con enemigos 
        if colision_bola:
            puntuacion+=1 
            explosion.play()

        #Colision protagonista con suelo
        if colision_player:
             heroe.rect.y+=0
        else: 
            heroe.rect.y+=5
        
        #Colision Enemigo con jugador
        if colision_enemies:
             vidas-=1
             colisionEnemigo.play()
             if vidas<=-1:
                 en_juego=True 
                 en_inicio=True
                 en_partida=False
                 game_over.play()
 
        #SALTO  
     
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if colision_player:
                    if heroe.derecha:
                        heroe.rect.y-=89
                        heroe.rect.x+=80
                    if heroe.izquierda: 
                        heroe.rect.y-=89
                        heroe.rect.x-=80

        
        if event.type==pygame.MOUSEBUTTONDOWN: 
           disparo.play()
                   
        
        todos_lista.draw(screen)
        #Fisicas para los enemigos 
        for enemy in enemies_list: 
            enemy.rect.y+=2 
            if enemy.rect.y>600: 
                enemy.rect.y=-100
            
        #llamo a la función lanza 
        update_bola()
      #disparamos la ventana 
        pygame.display.flip()
        clock.tick(30)