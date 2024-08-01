import pygame
from pygame.locals import*

class Director:
    #es la que mantiene el sistema
    def __init__(self):
        self.screen= pygame.display.set_mode([800,600])
        pygame.display.set_caption("escenas")
        self.scene= None
        self.quit_flag = False
        self.clock = pygame.time.Clock()
    
    def loop(self):
        while not self.quit_flag:
            time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    break
                #si no se cancela paso las escenas
                self.scene.on_event(time, event)
            
            self.scene.on_update(time)

            self.scene.on_draw(self.screen)
            pygame.display.flip()

    def change_scene(self, scene):
        #modifica la escena
        self.scene=scene
    
    def quit(self):
        self.quit_flag=True
    
    #definimos la clase escena abstracta
class Scene:
    def __init__(self, director):
        self.director= director
        
    def on_update(self, time):
            #por un evento especifico
        raise NotImplemented("falta el metodo on_update")
    
    def on_event(self, time, event):
        raise NotImplemented("falta evento on_event")
        
    def on_draw(self, screen):
            #para dibujar la pantalla
        raise NotImplemented("falta el metodo on.draw")
    
class Pantalla1(Scene):  #Pantalla azul hasta el enter que cambia
    def __init__(self, director):
        Scene.__init__(self, director)
    def on_update(self, time):
        pass

    def on_event(self, time, event):
        #los eventos que se captan
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_RETURN]:
                self.director.change_scene(Pantalla2(self.director))
    def on_draw(self, screen):
        #pantalla azul
        screen.fill((0,0,255))

class Pantalla2(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
    def on_update(self, time):
        pass

    def on_event(self, time, event):
        #los eventos que se captan
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_BACKSPACE]:
                self.director.change_scene(Pantalla1(self.director))
    def on_draw(self, screen):
        #pantalla roja
        screen.fill((255,0,0))

#creamos todos los obejetos y funciones
director= Director()
scene = Pantalla1(director)
director.change_scene(scene)
director.loop()