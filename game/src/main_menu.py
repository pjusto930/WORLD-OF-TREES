import pygame
import json
import sys
from button import *
from play_menu import *
from options_menu import *

pygame.init()

# Variables globales
is_music_playing = False
SCREEN = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Game Menu")

# Cargar fondo del menú
BACKGROUND_IMG = pygame.image.load("menuuuuu.jpg")

# Configuración predeterminada
DEFAULT_CONFIG = {"music_volume": 0.5}

# Funciones para cargar y guardar la configuración
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_CONFIG

def save_config(music_volume):
    with open('config.json', 'w') as f:
        json.dump({"music_volume": music_volume}, f)

# Función para obtener fuentes de diferentes tamaños
def load_font(path, size):
    return pygame.font.Font(path, size)

# Iniciar el menú principal
def main_menu():
    global is_music_playing
    config = load_config()

    # Configurar y reproducir música de fondo
    if not is_music_playing:
        pygame.mixer.music.load("Main Menu.mp3")
        pygame.mixer.music.set_volume(config.get("music_volume", 0.5))
        pygame.mixer.music.play(-1, fade_ms=3000)
        is_music_playing = True

    # Configurar tamaños de pantalla y texto
    screen_width, screen_height = pygame.display.get_surface().get_size()
    version_font = load_font("assets/fonts/font2.ttf", 30)
    version_text = version_font.render("Version 2.1.0", True, (255, 255, 255))
    version_rect = version_text.get_rect(topleft=(1320, screen_height - 40))

    while True:
        # Dibujar el fondo y obtener la posición del mouse
        SCREEN.blit(BACKGROUND_IMG, (0, 0))
        mouse_position = pygame.mouse.get_pos()

        # Configuración de título y botones del menú
        title_button = Button(image=pygame.image.load("assets/images/ui/menu_title_bt.png"), 
                              pos=(screen_width // 2, screen_height // 4), text_input="", 
                              font=load_font("assets/fonts/font.ttf", 105), base_color="#d7fcd4", hovering_color="Cyan")

        play_button = Button(image=None, pos=(screen_width // 2, screen_height // 1.6), 
                             text_input="PLAY", font=load_font("assets/fonts/font.ttf", 99), 
                             base_color="#0f3906", hovering_color="#31b714")

        options_button = Button(image=None, pos=(screen_width // 2 - 10, screen_height // 2 + 240), 
                                text_input="OPTIONS", font=load_font("assets/fonts/font.ttf", 60), 
                                base_color="#0f3906", hovering_color="#14b79a")

        quit_button = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 350), 
                             text_input="EXIT", font=load_font("assets/fonts/font.ttf", 60), 
                             base_color="#0f3906", hovering_color="#820018")

        # Dibujar la versión del juego en pantalla
        SCREEN.blit(version_text, version_rect)
        title_button.update(SCREEN)

        # Cambiar color de los botones cuando el cursor está encima
        for button in [play_button, options_button, quit_button]:
            button.changeColor(mouse_position)
            button.update(SCREEN)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_position):
                    play()
                elif options_button.checkForInput(mouse_position):
                    options()
                elif quit_button.checkForInput(mouse_position):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()