import pygame
import json
import time
from button import Button
import sys
from play_menu import *

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


def options():
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Cargar los volúmenes de configuración
    config = load_config()

    # Centrar los sliders horizontalmente y ubicarlos más arriba
    slider_x_position = screen_width // 2 - 150  # Centrar los sliders en la pantalla
    music_slider_y_position = screen_height // 3

    music_slider = Slider((slider_x_position, music_slider_y_position + 60), 300, initial_value=config["music_volume"])

    while True:
        SCREEN.blit(BG, (0, 0))  # Establecer fondo del menú de opciones
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Títulos para las opciones
        OPTIONS_TITLE = get_font(135).render("OPTIONS", True, "Yellow")
        OPTIONS_TITLE_RECT = OPTIONS_TITLE.get_rect(center=(screen_width // 2, screen_height // 5))
        SCREEN.blit(OPTIONS_TITLE, OPTIONS_TITLE_RECT)

        # Dibuja el slider de música
        music_slider.draw(SCREEN)
        pygame.mixer.music.set_volume(music_slider.get_value())  # Establecer el volumen de música

        # Texto para los sliders, centrado y más arriba
        music_label = get_font(40).render("Music volume", True, "White")
        music_label_rect = music_label.get_rect(center=(screen_width // 2, music_slider_y_position + 30))
        SCREEN.blit(music_label, music_label_rect)

        

        # Botón para regresar al menú principal
        OPTIONS_BACK = Button(image=None, pos=(screen_width // 2, screen_height // 2 + 370), 
                            text_input="BACK", font=get_font(55), base_color="White", hovering_color="Green")
        
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        #OPTIONS_BACK.set_click_volume(0.3)

        OPTIONS_BACK.update(SCREEN)

        # Detectar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Maneja los eventos del slider
            music_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    # Guardar los volúmenes en la configuración antes de regresar
                    save_config(music_slider.get_value())
                    from main_menu import main_menu
                    main_menu()

        pygame.display.update()


class Slider:
    def _init_(self, position, width, initial_value=0.5):
        self.position = position
        self.width = width
        self.value = initial_value
        self.slider_rect = pygame.Rect(position[0], position[1], width, 10)  # Rectángulo del slider
        self.circle_rect = pygame.Rect(position[0] + initial_value * width - 10, position[1] - 10, 20, 30)  # Círculo del slider
        self.dragging = False  # Para controlar el arrastre

    def draw(self, screen):
        # Dibuja el fondo del slider
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)  # Color del fondo
        # Dibuja el círculo que representa el valor
        pygame.draw.ellipse(screen, (100, 100, 200, 150), self.circle_rect)  # Color del círculo
        # Opcional: Dibuja el valor del slider sin decimales
        value_text = get_font2(20).render(f"{int(self.value * 100)}%", True, "White")  # Convertir a entero y mostrar en porcentaje
        screen.blit(value_text, (self.position[0] + self.width + 20, self.position[1] - 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.circle_rect.collidepoint(event.pos):
                self.dragging = True
                
        if event.type == pygame.MOUSEBUTTONUP: 
            self.dragging = False
            
        if event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            # Limita el movimiento del slider dentro del rango
            if mouse_x < self.position[0]:
                mouse_x = self.position[0]
            elif mouse_x > self.position[0] + self.width:
                mouse_x = self.position[0] + self.width
            # Actualiza la posición del círculo
            self.circle_rect.x = mouse_x - 10  # Centra el círculo
            # Calcula el nuevo valor
            self.value = (self.circle_rect.x - self.position[0] + 10) / self.width  # Normaliza el valor entre 0 y 1

    def get_value(self):
        return self.value  # Devuelve el valor actual del Slider

    def set_volume(self, volume):
        # Establece el volumen del sonido (entre 0 y 1)
        self.value = volume
        self.circle_rect.x = self.position[0] + volume * self.width - 10  # Actualiza la posición del círculo