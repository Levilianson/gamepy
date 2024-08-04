import pygame            #importamos la libreria 
import sys  
import random

#variables 
ancho_pantalla=800 
alto_pantalla=608 

size=(ancho_pantalla,alto_pantalla)
COLOR_FONDO=(34,121,153)
COLOR_ELEMENTOS=(153,88,18)
clock=pygame.time.Clock()  # esto es para optimizar las animaciones  



#iniciamos pygame  
pygame.init()

#crear ventana  
screen=pygame.display.set_mode(size) 
screen.fill(COLOR_FONDO)

#Titulo 
pygame.display.set_caption("Animando")

#Clases
class Bola(): 
    
    def __init__(self, COLOR_ELEMENTOS, pos_X, pos_Y,
                 tam_X, tam_Y, vel_X, vel_Y): 
        
        self.color_elementos=COLOR_ELEMENTOS 
        self.pos_X=pos_X 
        self.pos_Y=pos_Y
        self.tam_X=tam_X 
        self.tam_Y=tam_Y 
        self.vel_X=vel_X
        self.vel_Y=vel_Y
    
    def dibuja(self): 
        pygame.draw.circle(screen,self.color_elementos,[self.pos_X,self.pos_Y],
                           self.tam_X,self.tam_Y)
    def mover(self): 
        
        if self.pos_Y>608-40: 
            self.vel_Y*=-1
        
        if self.pos_X>800-40: 
            self.vel_X*=-1
        
        if self.pos_Y<0+40: 
            self.vel_Y*=-1
            
        if self.pos_X<0+40: 
            self.vel_X*=-1
        
        
        
        self.pos_X+=self.vel_X
        self.pos_Y+=self.vel_Y
     
tamanio_bola= random.randint(10,40)
tamanio_bola2= random.randint(10,40)
tamanio_bola3= random.randint(10,40)
tamanio_bola4= random.randint(10,40)
tamanio_bola5= random.randint(10,40)

bola=Bola((random.randint(0,225),random.randint(0,225),random.randint(0,225)),
          random.randint(0,800),random.randint(0,608),tamanio_bola,tamanio_bola,3,3)
bola2=Bola((random.randint(0,225),random.randint(0,225),random.randint(0,225)),
           random.randint(0,800),random.randint(0,608),tamanio_bola2,tamanio_bola2,3,3)
bola3=Bola((random.randint(0,225),random.randint(0,225),random.randint(0,225)),
           random.randint(0,800),random.randint(0,608),tamanio_bola3,tamanio_bola3,3,3)
bola4=Bola((random.randint(0,225),random.randint(0,225),random.randint(0,225)),
           random.randint(0,800),random.randint(0,608),tamanio_bola4,tamanio_bola4,3,3)
bola5=Bola((random.randint(0,225),random.randint(0,225),random.randint(0,225)),
           random.randint(0,800),random.randint(0,608),tamanio_bola5,tamanio_bola5,3,3)

bolas=[bola, bola2, bola3, bola4, bola5]



#Bucle principal  

while True: 
    for event in pygame.event.get(): # decirle a pygame que coja todos los eventos y los recorra 
        if(event.type==pygame.QUIT): 
            sys.exit()
        
    screen.fill(COLOR_FONDO)
    
    for bol in bolas:
        bol.dibuja()
        bol.mover()
 
       
    #disparamos la ventana 
    pygame.display.flip()
    clock.tick(30)