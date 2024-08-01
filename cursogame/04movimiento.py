import pygame
import os

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

def crearFondo():
    #CREA UNA IMAGEN  TIPO MOSAICO
    img = pygame.surface.Surface((ANCHO, ALTO))
    pieza = cargarImagen("stars.png")
    y=0 #RECORRE LA PANTALLA Y VA COLOCANDO LAS IMAGENES
    while (y < ALTO):
        x=0
        while (x <ANCHO):
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
#CREO AL JUGADOR CON EL METODO SPRITE
class jugador(pygame.sprite.Sprite):#deriva de Sprite
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

    #DIBUJA EL ELEMENTO SPRITE
    def draw(self):
        PANTALLA.blit(self.image, self.rect)
nave = jugador() # CREA AL JUGADOR

#DIBUJA LA PANTALLA EN CADA ITERACION
def dibuja():
    PANTALLA.blit(FONDO, (0, 0))
    nave.draw() # dibuja la nave
    pygame.display.update() #actualiza

def main():
    reloj = pygame.time.Clock() # para los frams
    jugando = True
    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
        
        nave.update() #actualiza la nave
        dibuja() 
        reloj.tick(60) #frecuencia del reloj

    pygame.quit()

if __name__=="__main__":
    main()