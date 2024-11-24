from settings import *                      # Importa todas las configuraciones desde el archivo settings
                # Importa la clase Level para manejar los niveles del juego
from pytmx.util_pygame import load_pygame   # Carga los mapas .tmx con soporte para Pygame
from pathlib import Path                    # Manejo de rutas de archivos de manera flexible
import pygame, sys                          # Importa Pygame para el motor del juego y sys para la gestión del sistema
from button import Button                   # Importa la clase Button para todos los botones del menú                 # Importa la función main_menu para el menú principal


pygame.init()

music_playing = False                                                   # Variable global para controlar si la música del menú ya está sonando

SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)       # Cambiado a pantalla completa
pygame.display.set_caption("Game Menu")

BG = pygame.image.load("fondo nuevo.jpg")            # Carga la imagen de fondo del menú
                        # Escala la imagen al tamaño de la pantalla


def get_font(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font.ttf", size)
def get_font2(size):                                                 # Función para obtener la fuente con un tamaño específico
    return pygame.font.Font("assets/fonts/font2.ttf", size)


def play():
    # Pantalla de selección de niveles
    while True:
        
        # Obtener tamaño de la pantalla
        screen_width, screen_height = pygame.display.get_surface().get_size()
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú de selección de niveles
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        # Texto para la selección de nivel
        LEVEL_TEXT = get_font(135).render("Select Level", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        # Crea botones para los niveles y el botón de retroceso
        LEVEL_1_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 2), 
                                text_input="EASY", font=get_font(75), base_color="#361612", hovering_color="#97ff00") 
        LEVEL_2_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 150), 
                                text_input="MEDIUM", font=get_font(75), base_color="#361612", hovering_color="#ffef00")
        LEVEL_3_BUTTON = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 300), 
                                text_input="HARD", font=get_font(75), base_color="#361612", hovering_color="#ff0031")
        BACK_BUTTON = Button(image=None, pos=(screen_width // 7, screen_height // 7 + 650), 
                            text_input="BACK", font=get_font(55), base_color="White", hovering_color="Green",)
        

        # Cambiar color del botón si el mouse pasa sobre él
        for button in [LEVEL_1_BUTTON, LEVEL_2_BUTTON, LEVEL_3_BUTTON, BACK_BUTTON]:
            button.changeColor(LEVEL_MOUSE_POS)
            button.update(SCREEN)
        # Detectar eventos del mouse para cada botón
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    
                    pygame.mixer.music.stop() # Detener la música del menú principal
                    #pygame.mixer.music.load("assets/sounds/music/Hypertext.mp3") # Reproduce la música del nivel 1 al darle al boton level 1
                    #pygame.mixer.music.play(-1, fade_ms=3000)
    
                    #game = Game(0)  # Cargar el nivel 1
                    #game.run()
                elif LEVEL_2_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    print("Level 2 not yet implemented")  # Niveles aún no implementados
                elif LEVEL_3_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    print("Level 3 not yet implemented")
                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    from main_menu import main_menu
                    main_menu()  # Volver al menú principal

        pygame.display.update()

import json
def load_config():    # Cargar la configuración
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5}  # Valores predeterminados

def save_config(music_volume):  # Elimina effects_volume
    with open('config.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)


