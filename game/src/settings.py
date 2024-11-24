import pygame
import cv2
import sys
import moviepy.editor as mp

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reproducción de Video")

# Cargar el video usando OpenCV
video_path = "el mejor video.mp4"  # Reemplaza con la ruta a tu archivo de video
cap = cv2.VideoCapture(video_path)

# Comprobar si el video se cargó correctamente
if not cap.isOpened():
    print("Error: No se pudo cargar el video.")
    sys.exit()

# Usar moviepy para manejar el audio
clip = mp.VideoFileClip(video_path)
clip.audio.preview()  # Reproducir el audio junto con el video

# Configurar el reloj de Pygame
clock = pygame.time.Clock()

# Reproducir el video en un bucle
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()  # Liberar el video
            pygame.quit()
            sys.exit()

    # Leer el siguiente fotograma del video
    ret, frame = cap.read()

    # Si no se puede leer un fotograma (fin del video), reiniciar
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Volver al inicio del video
        continue

    # Convertir el fotograma de BGR (OpenCV usa BGR) a RGB (Pygame usa RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Si el video está en formato vertical, rotarlo
    # Esto depende de la orientación del video original
    frame_rgb = cv2.rotate(frame_rgb, cv2.ROTATE_90_CLOCKWISE)  # Rotar para que quede en horizontal

    # Convertir el fotograma a una superficie de Pygame
    frame_surface = pygame.surfarray.make_surface(frame_rgb)

    # Mostrar el fotograma en la ventana de Pygame
    screen.blit(frame_surface, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de reproducción (opcional)
    clock.tick(30)  # Limitar a 30 fotogramas por segundo
