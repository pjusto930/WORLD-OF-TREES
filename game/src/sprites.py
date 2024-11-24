import pygame
import sys
import random
import json
import time
from button import Button
import sys
from play_menu import *

import json
# Inicializar Pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WORLD OF TREES")

# Cargar las imágenes de fondo
menu_background_image = pygame.image.load("menuuuuu.jpg")
menu_background_image = pygame.transform.scale(menu_background_image, (WIDTH, HEIGHT))



# Cargar la imagen del fondo seco
dry_background_image = pygame.image.load("Fondo seco f0.jpg")
dry_background_image = pygame.transform.scale(dry_background_image, (WIDTH, HEIGHT))

# Cargar las imágenes de fondo de los niveles
level_1_background_image = pygame.image.load("fondo seco f0.jpg")
level_1_background_image = pygame.transform.scale(level_1_background_image, (WIDTH, HEIGHT))

level_2_background_image = pygame.image.load("nivel2.jpg")
level_2_background_image = pygame.transform.scale(level_2_background_image, (WIDTH, HEIGHT))

level_3_background_image = pygame.image.load("fondo3.jpg")
level_3_background_image = pygame.transform.scale(level_3_background_image, (WIDTH, HEIGHT))


# Cargar imágenes para el título y los botones
title_image = pygame.image.load("tutilo.png").convert_alpha()
play_button_image = pygame.image.load("jugarr.png").convert_alpha()
options_button_image = pygame.image.load("opciones.png").convert_alpha()
exit_button_image = pygame.image.load("salir.png").convert_alpha()

# Coordenadas personalizables para el menú
title_position = (WIDTH // 1 - 100, HEIGHT // 100)  # Coordenadas del título
play_button_position = (WIDTH // 2 - 100, HEIGHT // 2)  # Coordenadas del botón de jugar
options_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 50)  # Coordenadas del botón de opciones
exit_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 100)  # Coordenadas del botón de salir



# Cargar el sonido de clic
click_sound = pygame.mixer.Sound('click.mp3')


# Función para mostrar la pantalla inicial
def show_main_menu():
    screen.blit(menu_background_image, (0, 0))
    # Ajustar posiciones del título y botones
    screen.blit(title_image, (WIDTH // 2 - title_image.get_width() // 2, HEIGHT // 12))  # Título más arriba
    screen.blit(play_button_image, (WIDTH // 2 - play_button_image.get_width() // 2, HEIGHT // 2 - 20))  # Ajuste del botón Jugar
    screen.blit(options_button_image, (WIDTH // 2 - options_button_image.get_width() // 2, HEIGHT // 2 + 60))  # Ajuste del botón Opciones
    screen.blit(exit_button_image, (WIDTH // 2 - exit_button_image.get_width() // 2, HEIGHT // 2 + 140))  # Ajuste del botón Salir
    pygame.display.flip()
    return (
        play_button_image.get_rect(topleft=(WIDTH // 2 - play_button_image.get_width() // 2, HEIGHT // 2 - 20)),
        options_button_image.get_rect(topleft=(WIDTH // 2 - options_button_image.get_width() // 2, HEIGHT // 2 + 60)),
        exit_button_image.get_rect(topleft=(WIDTH // 2 - exit_button_image.get_width() // 2, HEIGHT // 2 + 140))
    )



# Reloj para controlar FPS
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Velocidad del jugador
player_speed = 3

# Configuraciones de aparición de llantas y gotas
TIRES_PER_LEVEL = {
    1: 1,
    2: 10,
    3: 15
}
TIRE_SPAWN_RATE = {  # Configuración de llantas por nivel
    1: 1,
    2: 10,
    3: 15
}
WATER_DROP_CHANCE = 1  # Mayor número significa menos frecuencia




# Clase para el jugador

player_speed = 3  # Velocidad del jugador

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def _init(self):  # Corregido __init_
        super()._init_()  # Llamada correcta al constructor de la clase base
        self.images = {
            "front": pygame.image.load("personaje enfrente.png").convert_alpha(),
            "left": pygame.image.load("personaje izquierda.png").convert_alpha(),
            "right": pygame.image.load("personaje derecha.png").convert_alpha(),
        }
        self.image = self.images["front"]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2.5
        self.rect.y = HEIGHT - 200
        self.health = 100
        self.moving = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= player_speed
            self.image = self.images["left"]
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += player_speed
            self.image = self.images["right"]
            self.moving = True
        else:
            self.moving = False

        if not self.moving:
            self.image = self.images["front"]

        # Limitar el movimiento del jugador para que no se salga de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

# Clase para las plantas (tires)
class Tire(pygame.sprite.Sprite):
    def _init(self):  # Corregido __init_
        super()._init_()  # Llamada correcta al constructor de la clase base
        self.image = pygame.image.load("planta.png").convert_alpha()  # Cargar la imagen de la planta
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)  # Posición aleatoria en X
        self.rect.y = random.randint(-100, -30)  # Posición aleatoria en Y (fuera de la pantalla)

    def update(self):
        self.rect.y += 2  # La planta se mueve hacia abajo
        if self.rect.y > HEIGHT:  # Si la planta se sale de la pantalla
            self.rect.y = random.randint(-100, -30)  # Reinicia la posición en Y
            self.rect.x = random.randint(0, WIDTH - 30)  # Cambia la posición en X de forma aleatoria
 

# Clase para las llantas (WaterDrop)
class WaterDrop(pygame.sprite.Sprite):
    def _init(self):  # Corregido __init_
        super()._init_()  # Llamada correcta al constructor de la clase base
        self.image = pygame.image.load("llanta.png").convert_alpha()  # Cargar la imagen de la llanta
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)  # Posición aleatoria en el eje X
        self.rect.y = random.randint(-100, -30)  # Posición aleatoria en el eje Y, fuera de la pantalla

    def update(self):
        self.rect.y += 5  # La llanta cae 5 píxeles por actualización
        if self.rect.y > HEIGHT:  # Si la llanta se sale de la pantalla
            self.kill()  # Elimina el sprite de los grupos de sprites


# Función para mostrar la pantalla de controles
def show_controls():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    controls_text = font.render("Controles:", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 4))
    movement_text = font.render("Izquierda: ←   Derecha: →", True, WHITE)
    screen.blit(movement_text, (WIDTH // 2 - movement_text.get_width() // 2, HEIGHT // 2))
    back_button_image = pygame.image.load("salir .png").convert_alpha()
    screen.blit(back_button_image, (WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    return back_button_image.get_rect(topleft=(WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))


# Función para mostrar la selección de idioma
def show_language_selection():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    lang_text = font.render("Selecciona Idioma:", True, WHITE)
    screen.blit(lang_text, (WIDTH // 2 - lang_text.get_width() // 2, HEIGHT // 4))
    spanish_button = font.render("Español", True, WHITE)
    english_button = font.render("Inglés", True, WHITE)
    screen.blit(spanish_button, (WIDTH // 2 - spanish_button.get_width() // 2, HEIGHT // 2))
    screen.blit(english_button, (WIDTH // 2 - english_button.get_width() // 2, HEIGHT // 2 + 50))
    back_button_image = pygame.image.load("salir .png").convert_alpha()
    screen.blit(back_button_image, (WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return spanish_button.get_rect(topleft=(WIDTH // 2 - spanish_button.get_width() // 2, HEIGHT // 2)), \
        english_button.get_rect(topleft=(WIDTH // 2 - english_button.get_width() // 2, HEIGHT // 2 + 50)), \
        back_button_image.get_rect(topleft=(WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 100))



#ar la pantalla de Juego Terminado
def show_game_over():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("¡Game Over!", True, RED)
    screen.blit(game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    restart_button = font.render("Reiniciar", True, WHITE)
    menu_button = font.render("Menu", True, WHITE)
    screen.blit(restart_button, (WIDTH // 2 - restart_button.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(menu_button, (WIDTH // 2 - menu_button.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return restart_button.get_rect(topleft=(WIDTH // 2 - restart_button.get_width() // 2, HEIGHT // 2 + 50)), \
        menu_button.get_rect(topleft=(WIDTH // 2 - menu_button.get_width() // 2, HEIGHT // 2 + 100))


# Función para mostrar la pantalla de Juego Terminado
def show_game_finished():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    finished_text = font.render("¡Juego Terminado!", True, GREEN)
    screen.blit(finished_text,
                (WIDTH // 2 - finished_text.get_width() // 2, HEIGHT // 2 - finished_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)


# Bucle principal del juego
running = True
game_active = False
selected_language = "español"  # Idioma por defecto
# Bucle principal del juego
running = True
game_active = False
selected_language = "español"  # Idioma por defecto

# Bucle principal del juego
running = True
game_active = False
selected_language = "español"  # Idioma por defecto



# Crear grupos de sprites
player = Player()
tires = pygame.sprite.Group()
water_drops = pygame.sprite.Group()


# Función para añadir llantas
def create_tires(level):
    tire_count = 5 if level == 'easy' else 10
    for _ in range(tire_count):
        tire = Tire()
        tires.add(tire)


# Temporizador
start_ticks = pygame.time.get_ticks()
time_limit = 60  # 60 segundos


# Función para dibujar la barra de vida
def draw_health_bar(screen, x, y, current_health, max_health):
    health_percentage = current_health / max_health
    bar_width = 300
    bar_height = 20
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, bar_width * health_percentage, bar_height))


# Cargar la imagen de fondo para la selección de dificultad
difficulty_background_image = pygame.image.load("fondo nuevo.jpg")
difficulty_background_image = pygame.transform.scale(difficulty_background_image, (WIDTH, HEIGHT))

# Definir los fondos para los niveles
level_1_background = pygame.image.load("fondo seco f0.jpg")
level_1_background = pygame.transform.scale(level_1_background, (WIDTH, HEIGHT))

level_2_background = pygame.image.load("nivel2.jpg")
level_2_background = pygame.transform.scale(level_2_background, (WIDTH, HEIGHT))


def show_difficulty_selection():
    # Cargar los fondos específicos para cada dificultad
    beginner_background_image = pygame.image.load("fondo nuevo.jpg")
    beginner_background_image = pygame.transform.scale(beginner_background_image, (WIDTH, HEIGHT))
    
    advanced_background_image = pygame.image.load("Fondo seco f0.jpg")
    advanced_background_image = pygame.transform.scale(advanced_background_image, (WIDTH, HEIGHT))

    # Predeterminar el fondo como el de principiante (esto se cambiará si el jugador elige avanzado)
    screen.blit(beginner_background_image, (0, 0))  # Dibuja el fondo de dificultad principiante

    # Título
    font = pygame.font.Font(None, 74)
    title_image = pygame.image.load("seleccciona dificultad .png").convert_alpha()
    screen.blit(title_image, (WIDTH // 2 - title_image.get_width() // 2, HEIGHT // 4))

    # Botones para seleccionar dificultad
    easy_button_image = pygame.image.load("principiante.png").convert_alpha()
    hard_button_image = pygame.image.load("Avanzado .png").convert_alpha()

    # Posicionar los botones
    screen.blit(easy_button_image, (WIDTH // 2 - easy_button_image.get_width() // 2, HEIGHT // 2.1))
    screen.blit(hard_button_image, (WIDTH // 2 - hard_button_image.get_width() // 2, HEIGHT // 1.8 + 50))

    # Botón para volver
    back_button_image = pygame.image.load("regresar.png").convert_alpha()
    screen.blit(back_button_image, (-200, 0))  # Posición del botón de "Volver"
    pygame.display.flip()
    return easy_button_image.get_rect(topleft=(WIDTH // 2 - easy_button_image.get_width() // 2, HEIGHT // 2.1)), \
        hard_button_image.get_rect(topleft=(WIDTH // 2 - hard_button_image.get_width() // 2, HEIGHT // 1.8 + 50)), \
        back_button_image.get_rect(topleft=(-1, -1))  # Botón de volver


# Cargar la imagen de fondo para la selección de niveles
level_background_image = pygame.image.load("fondo nuevo.jpg")
level_background_image = pygame.transform.scale(level_background_image, (WIDTH, HEIGHT))




# Función para mostrar los niveles
def show_level_selection(back_button_position=(-200, 0)):
    screen.blit(level_background_image, (0, 0))  # Dibuja el fondo común de la selección de niveles
    font = pygame.font.Font(None, 74)
    title_image = pygame.image.load("selecciona nivel.png").convert_alpha()
    screen.blit(title_image, (WIDTH // 2 - title_image.get_width() // 2, HEIGHT // 4))
    
    level1_button_image = pygame.image.load("nivel1.png").convert_alpha()
    level2_button_image = pygame.image.load("nivel2.png").convert_alpha()
    level3_button_image = pygame.image.load("nivel3.png").convert_alpha()
    
    screen.blit(level1_button_image, (WIDTH // 2 - level1_button_image.get_width() // 2.2, HEIGHT // 2.5))
    screen.blit(level2_button_image, (WIDTH // 2 - level2_button_image.get_width() // 1.92, HEIGHT // 2.2 + 50))
    screen.blit(level3_button_image, (WIDTH // 2 - level3_button_image.get_width() // 2.21, HEIGHT // 2 + 100))
    
    # Botón de Volver
    back_button_image = pygame.image.load("regresar.png").convert_alpha()
    screen.blit(back_button_image, back_button_position)
    pygame.display.flip()

    # Retornamos las posiciones de los botones
    return level1_button_image.get_rect(topleft=(WIDTH // 2 - level1_button_image.get_width() // 2.2, HEIGHT // 2.2)), \
           level2_button_image.get_rect(topleft=(WIDTH // 2 - level2_button_image.get_width() // 1.92, HEIGHT // 2.2 + 50)), \
           level3_button_image.get_rect(topleft=(WIDTH // 2 - level3_button_image.get_width() // 2.21, HEIGHT // 2 + 100)), \
           back_button_image.get_rect(topleft=back_button_position)

# Variables globales del juego
game_active = False
running = True
paused = False  # Variable para saber si el juego está en pausa
muted = False  # Estado de la música
level = 1  # Nivel actual (puede cambiarse según la lógica del juego)
time_limit = 60  # Tiempo límite para el nivel
start_ticks = 0  # Variable para el cronómetro del nivel

# Cargar música de fondo
pygame.mixer.music.load("Main Menu.mp3")  # Reemplaza con tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Ajustar volumen (0.0 a 1.0)
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle

# Crear reloj
clock = pygame.time.Clock()

# Función para mostrar el cuadro de pausa
def show_pause_menu():
    pause_font = pygame.font.Font(None, 74)
    resume_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 50, "Reanudar", pause_font)
    restart_button = Button(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, "Repetir Nivel", pause_font)
    quit_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 100, 300, 50, "Salir", pause_font)
    mute_button = Button(WIDTH // 2 - 150, HEIGHT // 2 + 200, 300, 50, "Mutear Música" if not muted else "Activar Música", pause_font)

    # Dibujar fondo de pausa
    screen.fill((0, 0, 0, 180))  # Fondo oscuro con transparencia

    # Dibujar botones
    resume_button.draw(screen)
    restart_button.draw(screen)
    quit_button.draw(screen)
    mute_button.draw(screen)

    pygame.display.flip()

    return resume_button, restart_button, quit_button, mute_button

# Función para reiniciar el nivel
def restart_level():
    global paused, game_active, start_ticks
    # Reiniciar las variables del nivel, jugador, etc.
    paused = False
    game_active = True
    player.health = 100
    start_ticks = pygame.time.get_ticks()  # Reinicia el temporizador
    tires.empty()  # Vacía las llantas existentes
    create_tires(difficulty)  # Crea nuevas llantas según la dificultad

# Lógica principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Tecla "P" para pausar el juego
                paused = not paused  # Alternar entre pausado y no pausado

    if not game_active:
        play_rect, options_rect, exit_rect = show_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_rect.collidepoint(mouse_pos):
                    # Selección de dificultad
                    easy_rect, hard_rect, back_rect_difficulty = show_difficulty_selection()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if easy_rect.collidepoint(mouse_pos):
                                    difficulty = 'easy'
                                    break
                                elif hard_rect.collidepoint(mouse_pos):
                                    difficulty = 'hard'
                                    break
                                elif back_rect_difficulty.collidepoint(mouse_pos):  # Volver
                                    break
                        else:
                            continue
                        break

                    # Selección de nivel
                    if 'difficulty' in locals():
                        level1_rect, level2_rect, level3_rect, back_rect_level = show_level_selection()
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = event.pos
                                    if level1_rect.collidepoint(mouse_pos):
                                        level = 1
                                        break
                                    elif level2_rect.collidepoint(mouse_pos):
                                        level = 2
                                        break
                                    elif level3_rect.collidepoint(mouse_pos):
                                        level = 3
                                        break
                                    elif back_rect_level.collidepoint(mouse_pos):  # Volver
                                        break
                            else:
                                continue
                            break

                        # Activar el juego
                        if 'level' in locals():
                            game_active = True
                            player.health = 100
                            start_ticks = pygame.time.get_ticks()  # Reinicia el temporizador
                            tires.empty()  # Vacía las llantas existentes
                            create_tires(difficulty)  # Crea nuevas llantas según la dificultad

                elif options_rect.collidepoint(mouse_pos):
                    controls_rect, language_rect, back_rect_options = show_options()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if controls_rect.collidepoint(mouse_pos):
                                    back_rect_controls = show_controls()
                                    while True:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                running = False
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                mouse_pos = event.pos
                                                if back_rect_controls.collidepoint(mouse_pos):
                                                    break
                                    break
                                elif language_rect.collidepoint(mouse_pos):
                                    spanish_rect, english_rect, back_rect_language = show_language_selection()
                                    while True:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                running = False
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                mouse_pos = event.pos
                                                if spanish_rect.collidepoint(mouse_pos):
                                                    selected_language = "español"
                                                    break
                                                elif english_rect.collidepoint(mouse_pos):
                                                    selected_language = "inglés"
                                                    break
                                                elif back_rect_language.collidepoint(mouse_pos):  # Volver
                                                    break
                                        else:
                                            continue
                                        break
                                    break
                                elif back_rect_options.collidepoint(mouse_pos):  # Volver
                                    break
                elif exit_rect.collidepoint(mouse_pos):
                    running = False

    else:  # Si el juego está activo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Tecla "P" para pausar el juego
                    paused = not paused  # Alternar entre pausado y no pausado

        if paused:
            resume_button, restart_button, quit_button, mute_button = show_pause_menu()

            # Lógica de los botones de pausa
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if resume_button.collidepoint(mouse_pos):
                        paused = False
                    elif restart_button.collidepoint(mouse_pos):
                        # Reiniciar nivel
                        restart_level()
                    elif quit_button.collidepoint(mouse_pos):
                        # Volver al menú
                        game_active = False
                        paused = False
                    elif mute_button.collidepoint(mouse_pos):
                        # Mutear o desmutear música
                        if muted:
                            pygame.mixer.music.unpause()
                            muted = False
                        else:
                            pygame.mixer.music.pause()
                            muted = True

        else:
            # Actualizar sprites
            player.update()
            tires.update()

            # Generar gotas de agua
            if random.randint(1, 30) == 1:
                water_drop = WaterDrop()
                water_drops.add(water_drop)

            water_drops.update()

            # Detectar colisiones con llantas
            tire_hits = pygame.sprite.spritecollide(player, tires, False)
            if tire_hits:
                player.health += 5
                for tire in tire_hits:
                    tire.rect.y = random.randint(-100, -30)

            # Detectar si la salud llega a 0
            if player.health <= 0:
                restart_rect, menu_rect = show_game_over()  # Mostrar la pantalla de Game Over
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            if restart_rect.collidepoint(mouse_pos):
                                # Reiniciar el juego
                                restart_level()
                                break  # Salir del bucle y continuar el juego
                            elif menu_rect.collidepoint(mouse_pos):
                                # Volver al menú principal
                                game_active = False  # Desactiva el juego
                                break  # Salir del bucle y volver al menú
                    else:
                        continue
                    break  # Salir del bucle de "Game Over"

            # Controlar el tiempo
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > time_limit:
                show_game_finished()
                game_active = False

            # Dibujar todo
            if level == 1:
                screen.blit(dry_background_image, (0, 0))
            elif level == 2:
                screen.blit(level_2_background_image, (0, 0))  # Fondo del Nivel 2
            elif level == 3:
                screen.blit(level_3_background_image, (0, 0))  # Fondo del Nivel 3

            tires.draw(screen)
            water_drops.draw(screen)
            screen.blit(player.image, player.rect)

            # Dibujar la barra de vida
            draw_health_bar(screen, 50, 50, player.health, 100)

            # Mostrar el tiempo restante
            timer_text = pygame.font.Font(None, 36).render(f'Tiempo: {int(time_limit - seconds)}', True, WHITE)
            screen.blit(timer_text, (WIDTH - 150, 50))

            # Actualizar pantalla
            pygame.display.flip()
            clock.tick(120)

pygame.quit()
sys.exit()