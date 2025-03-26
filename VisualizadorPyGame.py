import pygame
import pygame_gui
import math
import tkinter.colorchooser

# Configuración inicial
WIDTH, HEIGHT = 1600, 1000
BACKGROUND_COLOR = (255, 255, 255)
NAIL_COLOR = (200, 200, 200)
n_clavos = 213
mostrar_etiquetas = False
RADIUS = 300
CENTER = (WIDTH // 2, HEIGHT // 2)
# Variables para el escalado de la imagen
escala = 1.0  # Escala inicial
factor_escalado = 0.1  # Factor de cambio de escala por cada paso de la rueda

# Cargar imagen de referencia
imagen = pygame.image.load("Recursos/ConejoSancocho.png")
escala = 1.0  # Escala inicial
factor_escalado = 0.1  # Factor de cambio de escala por cada paso de la rueda
nueva_ancho = int(imagen.get_width() * escala)
nueva_altura = int(imagen.get_height() * escala)
imagen_escalada = pygame.transform.scale(imagen, (nueva_ancho, nueva_altura))
imagen_rect = imagen_escalada.get_rect(center=CENTER)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("String Art Viewer")
clock = pygame.time.Clock()

# Inicializar pygame_gui
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
checkbox_etiquetas = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((20, 20), (150, 30)),
    text='Mostrar etiquetas',
    manager=manager)
entry_clavos = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((20, 60), (50, 30)),
    manager=manager
)
entry_clavos.set_text(str(n_clavos))

btn_mas = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((75, 60), (30, 30)),
    text='+',
    manager=manager
)

btn_menos = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((110, 60), (30, 30)),
    text='-',
    manager=manager
)

btn_color = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((20, 100), (120, 30)),
    text='Color clavos',
    manager=manager
)

# Variable para el selector de color
color_picker = None

# Calcular posiciones de los clavos
def calcular_clavos(n):
    return [
        (CENTER[0] + RADIUS * math.cos(2 * math.pi * i / n),
         CENTER[1] + RADIUS * math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]


clavos = calcular_clavos(n_clavos)

clavos = calcular_clavos(n_clavos)

# Variables para mover la imagen
moviendo_imagen = False
offset_x, offset_y = 0, 0

# Bucle principal
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    screen.fill(BACKGROUND_COLOR)
    
    # Mostrar imagen base (escalada)
    screen.blit(imagen_escalada, imagen_rect.topleft)
    
    # Dibujar los clavos
    for i, nail in enumerate(clavos):
        pygame.draw.circle(screen, NAIL_COLOR, (int(nail[0]), int(nail[1])), 3)
        if mostrar_etiquetas:
            font = pygame.font.Font(None, 20)
            text = font.render(str(i + 1), True, (0, 0, 0))
            screen.blit(text, (int(nail[0]) + 5, int(nail[1]) + 5))
    
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if imagen_rect.collidepoint(event.pos):
                moviendo_imagen = True
                offset_x = event.pos[0] - imagen_rect.x
                offset_y = event.pos[1] - imagen_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            moviendo_imagen = False
        elif event.type == pygame.MOUSEMOTION:
            if moviendo_imagen:
                imagen_rect.x = event.pos[0] - offset_x
                imagen_rect.y = event.pos[1] - offset_y
        elif event.type == pygame.MOUSEWHEEL:
            escala += event.y * factor_escalado
            escala = max(0.1, escala)
            nueva_ancho = int(imagen.get_width() * escala)
            nueva_altura = int(imagen.get_height() * escala)
            imagen_escalada = pygame.transform.scale(imagen, (nueva_ancho, nueva_altura))
            nuevo_centro = imagen_rect.center  # Guarda el centro anterior
            imagen_rect = imagen_escalada.get_rect(center=nuevo_centro) # Crea un nuevo rectangulo con el centro anterior
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == checkbox_etiquetas:
                    mostrar_etiquetas = not mostrar_etiquetas
                elif event.ui_element == btn_mas:
                    n_clavos = min(n_clavos + 1, 500)
                    entry_clavos.set_text(str(n_clavos))
                    clavos = calcular_clavos(n_clavos)
                elif event.ui_element == btn_menos:
                    n_clavos = max(n_clavos - 1, 3)
                    entry_clavos.set_text(str(n_clavos))
                    clavos = calcular_clavos(n_clavos)
                elif event.ui_element == btn_color:
                    btn_color_clicado = True
                    color = tkinter.colorchooser.askcolor(title="Selecciona un color")
                    if color:
                        NAIL_COLOR = color[0]  # Obtener los valores RGB
                        btn_color_clicado = False
                    else:
                        btn_color_clicado = False 
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == entry_clavos:
                    try:
                        nuevo_n_clavos = int(entry_clavos.get_text())
                        if nuevo_n_clavos > 0:
                            n_clavos = nuevo_n_clavos
                            clavos = calcular_clavos(n_clavos)
                    except ValueError:
                        pass  # Ignorar valores no válidos
        
        manager.process_events(event)
    
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()