from time import sleep
import pygame
import pygame_menu #pip install pygame-menu
from pygame_menu import themes
import pygame_menu.events
import pygame_menu.widgets

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_dificulty(value, difficulty):
    print(value)
    print(difficulty)

def start_the_game():
    
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading,30)

def level_menu():
    mainmenu._open(level)

mainmenu = pygame_menu.Menu('HOLA',600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Nombre: ', default= 'username', maxchar=20)
mainmenu.add.button('Jugar', start_the_game)
mainmenu.add.button('Nivel',level_menu)
mainmenu.add.button('Salir', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Elegir Dificultad', 600, 400, theme = themes.THEME_GREEN)
level.add.selector('Dificultad : ', [('Dificil', 1),('Moderado', 2),('Facil',3)], onchange= set_dificulty)

#barra de progreso
loading= pygame_menu.Menu('Cargando el juego...', 600,400, theme=themes.THEME_DARK)
loading.add.progress_bar("Carga", progressbar_id= "1", default=0, width =200)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10,15))

update_loading = pygame.USEREVENT + 0

#reemplamos esto para poder utilizar el pygeme sin el pygame_menu
# mainmenu.mainloop(surface)
while True:
    events= pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() +1)
            if progress.get_value() == 100:
                progress.set_value(progress.get_value() -100)
                pygame.time.set_timer(update_loading, 0)

        if event.type == pygame.QUIT:
            exit()

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if (mainmenu.get_current().get_selected_widget()):
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())
    
    pygame.display.update()