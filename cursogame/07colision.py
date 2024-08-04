import pygame
import os
import random

pygame.init()
#CARGAR IMAGENES
def cargarImagen(imagen):
    #CONTRUYE LA RUTA Y LUEGO CARGA LA IMAGEN
    ruta = os.path.join("cursogame\image",imagen)
    return pygame.image.load(ruta)
ANCHO = 800
ALTO = 600
#AGREGO LOS DATOS DE LA NAVE
NAVE_ANCHO= 80
NAVE_ALTO= 54
VEL_JUGADOR= 10
VEL_BALAS = 20
#DATOS DE LAS NAVES RIVALES
VEL_ENEMIGOS = 5
MAX_ENEMIGOS= 6
PROX_ENEMIGO= 40 #PROBABILIDAD QUE APAREZCA UN NUEVO ENEMIGO
ESPERA_ENEMIGOS= 20

#MODELOS DE NAVEAS ENEMIGAS
IMAGENES_ENEMIGAS = [
    cargarImagen("enemy1.png"),
    cargarImagen("enemy2.png"),
    cargarImagen("enemy3.png"),
]

def crearFondo():
    #CREA UNA IMAGEN  TIPO MOSAICO
    img = pygame.surface.Surface((ANCHO, ALTO))
    pieza = cargarImagen("stars.png")
    y=0 #RECORRE LA PANTALLA Y VA COLOCANDO LAS IMAGENES
    while (y < ALTO):
        x = 0
        while (x < ANCHO):
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
#CREO LOS GRUPOS DE NAVES
enemigos = pygame.sprite.Group()
todo = pygame.sprite.Group()
balasJugador= pygame.sprite.Group()

#CREO AL JUGADOR CON EL METODO SPRITE
class Jugador(pygame.sprite.Sprite):#deriva de Sprite
    #CONSTRUCTOR
    def __init__(self):
        super().__init__()
        nave = cargarImagen("playerShip.png")
        #REDUCE EL TAMAÑO
        self.image = pygame.transform.scale(nave,(NAVE_ANCHO, NAVE_ALTO))
        #CREA UN RECTANGULO CON EL TAMAÑO
        self.rect = self.image.get_bounding_rect()
        #AJUSTA LA POSICION
        self.rect.midbottom= (ANCHO//2, ALTO -20)
        #AÑADE EL SPRITE AL GRUPO GENERAL
        self.add(todo)

    # MOVIMIENTOS
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP]):
            self.rect.y -= VEL_JUGADOR
        if (keys[pygame.K_DOWN]):
            self.rect.y += VEL_JUGADOR
        if (keys[pygame.K_LEFT]):
            self.rect.x -= VEL_JUGADOR
        if (keys[pygame.K_RIGHT]):
            self.rect.x += VEL_JUGADOR  
        #CUANDO SOBREPASA EL TABLERO  
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

    '''#DIBUJA EL ELEMENTO SPRITE
    def draw(self):
        PANTALLA.blit(self.image, self.rect)
nave = jugador() # CREA AL JUGADOR'''
#SPRITE ENEMIGOS
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #SELECCIONA EL TIPO DE NAVE
        nave = random.choice(IMAGENES_ENEMIGAS)
        #CALCULA EL TAMAÑO COMO EL JUGADOR Y LO AJUSTA
        self.rect = nave.get_bounding_rect().fit((0,0, NAVE_ANCHO, NAVE_ALTO))
        self.image = pygame.transform.scale(nave, self.rect.size)
        #POSICION Y VELOCIDAD ALEATORIAS
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = -self.rect.height
        self.velx = random.choice([-VEL_ENEMIGOS, 0, VEL_ENEMIGOS])
        self.add(enemigos, todo)
    
    #MOVIMIENTO DEL ENEMIGO
    def update(self):
        self.rect.x += self.velx
        self.rect.y += VEL_ENEMIGOS
        #AJUSTES
        if self.rect.left < 0:
            self.rect.left = 0
            self.velx = -self.velx
        
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
            self.velx = -self.velx
        # SOBREPASA EL BORDE INFERIOR DESAPARECE
        if self.rect.y > ALTO:
            self.kill()

class BalaJugador(pygame.sprite.Sprite):
    def __init__(self, nave):
        super().__init__()
        #carga imagen y forma
        self.image = cargarImagen("laserGreen.png")
        self.rect = self.image.get_bounding_rect()
        #posicion centrada en el jugador
        self.rect.midbottom = nave.rect.midtop
        self.add(balasJugador, todo)

    def update(self):
        self.rect.y -= VEL_BALAS
        if self.rect.bottom < 0: #sobrepasa sup y arriba
            self.kill

class Explosion(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        #carga imagen y superficie
        self.image = cargarImagen("explosion.png")
        self.rect = self.image.get_bounding_rect()
        self.rect.center = sprite.rect.center
        self.paso = 10
        self.add(todo)

    def update(self):
        self.paso -= 1
        if self.paso == 0:
            self.kill()

nave = Jugador()


#DIBUJA LA PANTALLA EN CADA ITERACION
def dibuja():
    PANTALLA.blit(FONDO, (0, 0))
    #nave.draw() # dibuja la nave
    todo.draw(PANTALLA)
    pygame.display.update() #actualiza

#funcion detecta colisiones
def detectarColiciones():
    enemigos_tocados = pygame.sprite.groupcollide(enemigos, 
                                    balasJugador, True, True)
    
    for enemigo, balas in enemigos_tocados.items():
        Explosion(enemigo)
    
    muerte = False
    enemigos_chocan = pygame.sprite.spritecollide(nave, enemigos, True)
    for enemigo in enemigos_chocan:
        Explosion(enemigo)
        Explosion(nave)
        nave.kill()
        muerte = True
    return muerte

def reinicio():
    global nave
    pygame.time.delay(2000)
    todo.empty()
    enemigos.empty()
    balasJugador.empty()
    nave = Jugador()    

def main():
    esperaEnemigo = 0
    reloj = pygame.time.Clock() # para los frams
    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BalaJugador(nave)
                if event.key == pygame.K_ESCAPE:
                    jugando = False

        #genera los enemigos
        if esperaEnemigo ==0 and len(enemigos) < MAX_ENEMIGOS:
            #probabilidad
            if (random.uniform(0, 100) < PROX_ENEMIGO):
                Enemigo()
                esperaEnemigo = ESPERA_ENEMIGOS
        elif esperaEnemigo > 0:
            esperaEnemigo -=1 #DESCUENTA TIEMPO
        
        #nave.update() #actualiza la nave
        todo.update()
        muerte = detectarColiciones()
        dibuja() 

        if muerte:
            reinicio()
            
        reloj.tick(60) #frecuencia del reloj

    pygame.quit()

if __name__=="__main__":
    main()