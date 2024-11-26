import pygame
import sys
import random

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
dry_background_image = pygame.image.load("niveell2.jpg")
dry_background_image = pygame.transform.scale(dry_background_image, (WIDTH, HEIGHT))

# Cargar las imágenes de fondo de los niveles
level_1_background_image = pygame.image.load("fondo seco f0.jpg")
level_1_background_image = pygame.transform.scale(level_1_background_image, (WIDTH, HEIGHT))

level_2_background_image = pygame.image.load("niveell2.jpg")
level_2_background_image = pygame.transform.scale(level_2_background_image, (WIDTH, HEIGHT))

level_3_background_image = pygame.image.load("fondo3.jpg")
level_3_background_image = pygame.transform.scale(level_3_background_image, (WIDTH, HEIGHT))


# Cargar imágenes para el título y los botones
title_image = pygame.image.load("tutilo.png").convert_alpha()
play_button_image = pygame.image.load("jugarr.png").convert_alpha()
options_button_image = pygame.image.load("opcioness.png").convert_alpha()
exit_button_image = pygame.image.load("salirr.png").convert_alpha()

# Coordenadas personalizables para el menú
title_position = (WIDTH // 1 - 100, HEIGHT // 100)  # Coordenadas del título
play_button_position = (WIDTH // 10 - 100, HEIGHT // 2)  # Coordenadas del botón de jugar
options_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 50)  # Coordenadas del botón de opciones
exit_button_position = (WIDTH // 2 - 100, HEIGHT // 2 + 100)  # Coordenadas del botón de salir



# Cargar el sonido de clic
click_sound = pygame.mixer.Sound('click.mp3')


# Función para mostrar la pantalla inicial
def show_main_menu():
    screen.blit(menu_background_image, (0, 0))
    # Ajustar posiciones del título y botones
    screen.blit(title_image, (WIDTH // 1.95 - title_image.get_width() // 2, HEIGHT // 12))  # Título más arriba
    screen.blit(play_button_image, (WIDTH // 2 - play_button_image.get_width() // 2, HEIGHT // 2.07 - 20))  # Ajuste del botón Jugar
    screen.blit(options_button_image, (WIDTH // 2 - options_button_image.get_width() // 2, HEIGHT // 2 + 60))  # Ajuste del botón Opciones
    screen.blit(exit_button_image, (WIDTH // 2.07 - exit_button_image.get_width() // 2, HEIGHT // 1.9 + 140))  # Ajuste del botón Salir
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
    def __init__(self):  # Corregido __init__
        super().__init__()  # Llamada correcta al constructor de la clase base
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
        if keys[pygame.K_a]:  # Cambiado de pygame.K_LEFT a pygame.K_a
            self.rect.x -= player_speed
            self.image = self.images["left"]
            self.moving = True
        elif keys[pygame.K_d]:  # Cambiado de pygame.K_RIGHT a pygame.K_d
            self.rect.x += player_speed
            self.image = self.images["right"]
            self.moving = True
        else:
            self.moving = False

        if not self.moving:
            self.image = self.images["front"]

        # Limitar el movimiento del jugador para que no se salga de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))



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

# Función para mostrar la pantalla de "Juego Terminado" con fondo y botones en imágenes
def show_game_over():
    # Cargar fondo de "Game Over"
    fondo_img = pygame.image.load("buenintento.jpg")
    fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))  # Ajustar al tamaño de la ventana
    screen.blit(fondo_img, (0, 0))  # Dibujar fondo

    # Cargar imágenes de botones
    btn_reiniciar_img = pygame.image.load("volver.png")
    btn_menu_img = pygame.image.load("casa.png")
    
    # Escalar imágenes al tamaño deseado
    btn_width, btn_height = 200, 60
    btn_reiniciar_img = pygame.transform.scale(btn_reiniciar_img, (btn_width, btn_height))
    btn_menu_img = pygame.transform.scale(btn_menu_img, (btn_width, btn_height))
    
    # Coordenadas de los botones
    btn_reiniciar_rect = btn_reiniciar_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    btn_menu_rect = btn_menu_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    
    # Dibujar botones
    screen.blit(btn_reiniciar_img, btn_reiniciar_rect)
    screen.blit(btn_menu_img, btn_menu_rect)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Retornar rectángulos para detectar clics
    return btn_reiniciar_rect, btn_menu_rect

# Manejo de la lógica de los botones
running = True
while running:
    # Mostrar pantalla de "Game Over"
    btn_reiniciar_rect, btn_menu_rect = show_game_over()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if btn_reiniciar_rect.collidepoint(event.pos):
                click_sound.play()
                print("Botón 'Reiniciar' presionado")
                # Lógica para reiniciar el juego


# Cargar la imagen de fondo para la selección de dificultad
difficulty_background_image = pygame.image.load("fondo nuevo.jpg")
difficulty_background_image = pygame.transform.scale(difficulty_background_image, (WIDTH, HEIGHT))



# Variables globales del juego
game_active = False
running = True
paused = False  # Variable para saber si el juego está en pausa
muted = False  # Estado de la música
level = 1  # Nivel actual (puede cambiarse según la lógica del juego)
time_limit = 60  # Tiempo límite para el nivel
start_ticks = 0  # Variable para el cronómetro del nivel


# Cargar música de fondo
pygame.mixer.music.load("menu.mp3")  # Reemplaza con tu archivo de música
pygame.mixer.music.set_volume(0.5)  # Ajustar volumen (0.0 a 1.0)
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle

# Crear reloj
clock = pygame.time.Clock()

# Función para mostrar el menú de opciones
def show_options_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    language_button = font.render("Idioma", True, WHITE)
    controls_button = font.render("Controles", True, WHITE)
    characters_button = font.render("Personajes", True, WHITE)
    back_button = font.render("Volver", True, WHITE)
    screen.blit(language_button, (WIDTH // 2 - language_button.get_width() // 2, HEIGHT // 4))
    screen.blit(controls_button, (WIDTH // 2 - controls_button.get_width() // 2, HEIGHT // 2))
    screen.blit(characters_button, (WIDTH // 2 - characters_button.get_width() // 2, HEIGHT // 1.5))
    screen.blit(back_button, (WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 1.8))
    pygame.display.flip()
    return pygame.Rect(WIDTH // 2 - language_button.get_width() // 2, HEIGHT // 4, language_button.get_width(), language_button.get_height()), \
           pygame.Rect(WIDTH // 2 - controls_button.get_width() // 2, HEIGHT // 2, controls_button.get_width(), controls_button.get_height()), \
           pygame.Rect(WIDTH // 2 - characters_button.get_width() // 2, HEIGHT // 1.5, characters_button.get_width(), characters_button.get_height()), \
           pygame.Rect(WIDTH // 2 - back_button.get_width() // 2, HEIGHT // 1.8, back_button.get_width(), back_button.get_height())

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
    back_button_image = pygame.image.load("salir.png").convert_alpha()
    screen.blit(back_button_image, (WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    return spanish_button.get_rect(topleft=(WIDTH // 2 - spanish_button.get_width() // 2, HEIGHT // 2)), \
           english_button.get_rect(topleft=(WIDTH // 2 - english_button.get_width() // 2, HEIGHT // 2 + 50)), \
           back_button_image.get_rect(topleft=(WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 100))

# Función para mostrar los controles
def show_controls():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    controls_text = font.render("Controles:", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 4))
    movement_text = font.render("Izquierda: ←   Derecha: →", True, WHITE)
    screen.blit(movement_text, (WIDTH // 2 - movement_text.get_width() // 2, HEIGHT // 2))
    back_button_image = pygame.image.load("salir.png").convert_alpha()
    screen.blit(back_button_image, (WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    return back_button_image.get_rect(topleft=(WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))

# Función para mostrar personajes (aún no implementado)
def show_characters():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    characters_text = font.render("Personajes:", True, WHITE)
    screen.blit(characters_text, (WIDTH // 2 - characters_text.get_width() // 2, HEIGHT // 4))
    # Aquí puedes agregar la lógica para mostrar los personajes disponibles
    back_button_image = pygame.image.load("salir.png").convert_alpha()
    screen.blit(back_button_image, (WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    return back_button_image.get_rect(topleft=(WIDTH // 2 - back_button_image.get_width() // 2, HEIGHT // 2 + 50))

# Cargar música de fondo
pygame.mixer.music.load("menu.mp3")  # Reemplaza con tu archivo de música del menú
pygame.mixer.music.set_volume(0.3)  # Ajustar volumen (0.0 a 1.0)
pygame.mixer.music.play(-1, 0.0)  # Reproducir música en bucle

# Cargar sonidos de colisión
collision_sound_tire = pygame.mixer.Sound("llantazo.mp3")  # Sonido para las llantas
collision_sound_plant = pygame.mixer.Sound("plantazo.mp3")  # Sonido para las plantas

# Cargar imágenes de las barras de vida (barra1.png a barra10.png)
barra_images = []
for i in range(1, 11):  # Ahora cargamos barra1.png hasta barra10.png
    barra_image = pygame.image.load(f"barra{i}.png")  # Cargar barra1.png, barra2.png, ..., barra10.png
    barra_images.append(barra_image)  # Agregar cada barra a la lista

# Función para dibujar la barra de vida
def draw_health_bar(screen, x, y, current_health, max_health):
    # Asegurarse de que current_health no exceda max_health
    if current_health > max_health:
        current_health = max_health
    if current_health < 0:
        current_health = 0  # No permitir que la salud sea menor que 0
    
    # Calcular qué barra de vida mostrar
    health_percentage = current_health / max_health
    health_index = int(health_percentage * 10)  # La barra tiene 10 estados (barra1, barra2, ..., barra10)
    if health_index == 0:
        health_index = 1  # Asegurar que no se dibuje una barra vacía (barra1 es la mínima)

    # Dibujar la barra de vida (usando la imagen correspondiente)
    screen.blit(barra_images[health_index - 1], (x, y))  # Mostrar la barra correspondiente


# Variables globales de dificultad
tire_speed_easy = 5
tire_speed_hard = 8
tire_damage_easy = 10
tire_damage_hard = 15

plant_speed_easy = 2
plant_speed_hard = 4
plant_heal_easy = 8
plant_heal_hard = 8

# Clase para las llantas (WaterDrop)
class WaterDrop(pygame.sprite.Sprite):
    def __init__(self, speed, damage):  # Recibe velocidad y daño como parámetros
        super().__init__()
        self.image = pygame.image.load("llanta.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)
        self.speed = speed  # Velocidad de la caída de la llanta
        self.damage = damage  # Daño que causa la llanta

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()

# Clase para las plantas (Tire)
class Tire(pygame.sprite.Sprite):
    def __init__(self, speed, heal):  # Recibe velocidad y curación como parámetros
        super().__init__()
        self.image = pygame.image.load("planta.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)
        self.speed = speed  # Velocidad de la planta
        self.heal = heal  # Curación que produce la planta

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -30)
            self.rect.x = random.randint(0, WIDTH - 30)

# Función para crear las llantas y plantas según la dificultad
def create_tires(difficulty):
    global tire_speed, tire_damage, plant_speed, plant_heal
    
    if difficulty == 'easy':
        tire_speed = tire_speed_easy
        tire_damage = tire_damage_easy
        plant_speed = plant_speed_easy
        plant_heal = plant_heal_easy
    elif difficulty == 'hard':
        tire_speed = tire_speed_hard
        tire_damage = tire_damage_hard
        plant_speed = plant_speed_hard
        plant_heal = plant_heal_hard

    for _ in range(5):  # Número de llantas
        water_drop = WaterDrop(tire_speed, tire_damage)
        water_drops.add(water_drop)

    for _ in range(3):  # Número de plantas
        tire = Tire(plant_speed, plant_heal)
        tires.add(tire)

# Funciones para mostrar menús y elementos del juego
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

def show_difficulty_selection():
    # Cargar los fondos específicos para cada dificultad
    beginner_background_image = pygame.image.load("fondo nuevo.jpg")
    beginner_background_image = pygame.transform.scale(beginner_background_image, (WIDTH, HEIGHT))
    
    advanced_background_image = pygame.image.load("Fondoprincipiante.jpg")
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
level_background_image = pygame.image.load("fondoavanzado.jpg")
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


# Lógica principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pausar o reanudar el juego al presionar "P"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Tecla "P" para pausar o reanudar el juego
                paused = not paused

            # Mutear o desmutear la música al presionar "M"
            if event.key == pygame.K_m:
                music_muted = not music_muted
                if music_muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    if not game_active:
        # Mostrar menú principal
        play_rect, options_rect, exit_rect = show_main_menu()
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(mouse_pos):
                click_sound.play()  # Reproducir sonido de clic
                easy_rect, hard_rect, back_rect_difficulty = show_difficulty_selection()
                difficulty_selected = False
                while not difficulty_selected:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            if easy_rect.collidepoint(mouse_pos):
                                difficulty = 'easy'
                                difficulty_selected = True
                            elif hard_rect.collidepoint(mouse_pos):
                                difficulty = 'hard'
                                difficulty_selected = True
                            elif back_rect_difficulty.collidepoint(mouse_pos):  # Volver
                                difficulty_selected = True

                # Selección de nivel
                if 'difficulty' in locals():
                    level_selected = False
                    level1_rect, level2_rect, level3_rect, back_rect_level = show_level_selection()
                    while not level_selected:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = event.pos
                                if level1_rect.collidepoint(mouse_pos):
                                    level = 1
                                    level_selected = True
                                elif level2_rect.collidepoint(mouse_pos):
                                    level = 2
                                    level_selected = True
                                elif level3_rect.collidepoint(mouse_pos):
                                    level = 3
                                    level_selected = True
                                elif back_rect_level.collidepoint(mouse_pos):  # Volver
                                    level_selected = True

                    # Activar el juego
                    if 'level' in locals():
                        game_active = True
                        player_health = 100
                        start_ticks = pygame.time.get_ticks()
                        tires.empty()
                        create_tires(difficulty)

                        # Detener la música del menú
                        pygame.mixer.music.stop()

                        if level == 1:
                            pygame.mixer.music.load("NIVEL 1.mp3")
                        elif level == 2:
                            pygame.mixer.music.load("NIVEL 2.mp3")
                        elif level == 3:
                            pygame.mixer.music.load("NIVEL 3.mp3")

                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1, 0.0)

            elif options_rect.collidepoint(mouse_pos):
                click_sound.play()  # Reproducir sonido de clic
                controls_rect, language_rect, back_rect_options = show_options_menu()
                options_selected = False
                while not options_selected:
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
                                    else:
                                        continue
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
                                            elif back_rect_language.collidepoint(mouse_pos):
                                                break
                                    else:
                                        continue
                                    break
                                break
                            elif back_rect_options.collidepoint(mouse_pos):
                                options_selected = True
            elif exit_rect.collidepoint(mouse_pos):
                click_sound.play()  # Reproducir sonido de clic
                running = False

    else:
        if paused:
            pause_text = pygame.font.Font(None, 72).render("PAUSADO", True, (255, 0, 0))
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
            pygame.display.flip()
            continue

        else:
            player.update()
            tires.update()

            if random.randint(1, 30) == 1:
                water_drop = WaterDrop(tire_speed, tire_damage)
                water_drops.add(water_drop)

            water_drops.update()

            water_hits = pygame.sprite.spritecollide(player, water_drops, False)
            if water_hits:
                player_health -= tire_damage
                collision_sound_tire.play()
                for water in water_hits:
                    water.kill()

            tire_hits = pygame.sprite.spritecollide(player, tires, False)
            if tire_hits:
                player_health += plant_heal
                collision_sound_plant.play()
                for tire in tire_hits:
                    tire.rect.y = random.randint(-100, -30)

            if player_health <= 0:
                restart_rect, menu_rect = show_game_over()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            if restart_rect.collidepoint(mouse_pos):
                                click_sound.play()  # Reproducir sonido de clic
                                restart_level()
                                break
                            elif menu_rect.collidepoint(mouse_pos):
                                click_sound.play()  # Reproducir sonido de clic
                                game_active = False
                                break

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > time_limit:
                show_game_finished()
                game_active = False

            if level == 1:
                screen.blit(level_1_background_image, (0, 0))
            elif level == 2:
                screen.blit(level_2_background_image, (0, 0))
            elif level == 3:
                screen.blit(level_3_background_image, (0, 0))

            tires.draw(screen)
            water_drops.draw(screen)
            screen.blit(player.image, player.rect)

            draw_health_bar(screen, 50, 50, player_health, 100)

            timer_text = pygame.font.Font(None, 36).render(f'Tiempo: {int(time_limit - seconds)}', True, WHITE)
            screen.blit(timer_text, (WIDTH - 150, 50))

            pygame.display.flip()
            clock.tick(120)

pygame.quit()
sys.exit()