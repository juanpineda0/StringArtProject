import pygame
import pygame_gui
import math
import tkinter.colorchooser
from typing import Tuple

def procesar_imagen(ruta_imagen: str) -> Tuple[str, str]:
    """
    Procesa una imagen para el String Art usando una interfaz gráfica.
    
    Args:
        ruta_imagen (str): Ruta a la imagen a procesar
        
    Returns:
        Tuple[str, str]: Rutas a la imagen procesada y la imagen de bordes
    """
    # Configuración inicial
    WIDTH, HEIGHT = 1600, 1000
    BACKGROUND_COLOR = (255, 255, 255)
    NAIL_COLOR = (200, 200, 200)
    n_clavos = 213
    mostrar_etiquetas = False
    RADIUS = 480
    CENTER = (WIDTH // 2, HEIGHT // 2)
    # Variables para el escalado de la imagen
    escala = 1.0  # Escala inicial
    factor_escalado = 0.1  # Factor de cambio de escala por cada paso de la rueda
    Ruta = ruta_imagen

    # Cargar imagen de referencia
    imagen = pygame.image.load(Ruta)
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
    btn_mascara = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 140), (120, 30)),
        text='Modo máscara',
        manager=manager
    )
    btn_restablecer = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 180), (120, 30)),
        text='Restablecer',
        manager=manager
    )
    btn_Guardar_imagen = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((20, 220), (120, 30)),
        text='Guardar imagen',
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

    def punto_dentro_circulo(punto):
        distancia = math.sqrt((punto[0] - CENTER[0])**2 + (punto[1] - CENTER[1])**2)
        return distancia <= RADIUS

    clavos = calcular_clavos(n_clavos)

    # Variables de la máscara
    mascara = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    mascara.fill((255, 255, 255, 255))
    pygame.draw.circle(mascara, (0, 0, 0, 0), CENTER, RADIUS)
    mascara_rect = mascara.get_rect(topleft=(0, 0))
    modo_mascara = False
    dibujando_mascara = False
    radio_pincel = 10
    texto_titulo_mascara = "Modo Máscara: Cick izquierdo para borrar, Click derecho para incluir."
    titulo_mascara = pygame.font.Font(None, 36).render(texto_titulo_mascara, True, (0, 0, 0))
    boton_izquierdo_presionado = False
    boton_derecho_presionado = False

    # Variables para mover la imagen
    moviendo_imagen = False
    offset_x, offset_y = 0, 0

    # Bucle principal
    running = True
    while running:
        time_delta = clock.tick(30) / 1000.0
        screen.fill(BACKGROUND_COLOR)
        
        # Crear una copia de la imagen escalada con canal alfa
        imagen_con_mascara = imagen_escalada.copy().convert_alpha()
        
        # Asegurar que la máscara tiene transparencia
        mascara.set_alpha(230)  # Ajusta la opacidad de la máscara (0 = transparente, 255 = opaco)
        
        # Dibujar la imagen en la pantalla
        screen.blit(imagen_escalada, imagen_rect.topleft)
        
        # Dibujar la máscara con transparencia sobre la imagen
        screen.blit(mascara, mascara_rect.topleft)

        # Mostrar la mascara si esta activo el modo mascara.
        if modo_mascara:
            pygame.draw.circle(screen, (255, 0, 0), pygame.mouse.get_pos(), radio_pincel, 1) # Circulo rojo
            # Calcular coordenadas para centrar el título
            x = (WIDTH - titulo_mascara.get_width()) // 2
            y = 10

            # Dibujar el borde blanco
            titulo_borde = pygame.font.Font(None, 36).render(texto_titulo_mascara, True, (255, 255, 255))
            screen.blit(titulo_borde, (x - 1, y - 1))
            screen.blit(titulo_borde, (x + 1, y - 1))
            screen.blit(titulo_borde, (x - 1, y + 1))
            screen.blit(titulo_borde, (x + 1, y + 1))

            # Dibujar el texto negro encima del borde
            screen.blit(titulo_mascara, (x, y))
        
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
                if modo_mascara:
                    dibujando_mascara = True
                    if event.button == 1:
                        boton_izquierdo_presionado = True
                    elif event.button == 3:
                        boton_derecho_presionado = True
                elif imagen_rect.collidepoint(event.pos):
                    moviendo_imagen = True
                    offset_x = event.pos[0] - imagen_rect.x
                    offset_y = event.pos[1] - imagen_rect.y

            elif event.type == pygame.MOUSEBUTTONUP:
                dibujando_mascara = False
                moviendo_imagen = False
                if event.button == 1:
                    boton_izquierdo_presionado = False
                elif event.button == 3:
                    boton_derecho_presionado = False

            elif event.type == pygame.MOUSEMOTION:
                if moviendo_imagen:
                    imagen_rect.x = event.pos[0] - offset_x
                    imagen_rect.y = event.pos[1] - offset_y
                elif dibujando_mascara:
                    mouse_x, mouse_y = event.pos
                    if boton_izquierdo_presionado:
                        pygame.draw.circle(mascara, (255, 255, 255, 255), (mouse_x, mouse_y), radio_pincel)
                    elif boton_derecho_presionado:
                        pygame.draw.circle(mascara, (0, 0, 0, 0), (mouse_x, mouse_y), radio_pincel)

            elif event.type == pygame.MOUSEWHEEL:
                if modo_mascara:
                    radio_pincel = max(1, radio_pincel + event.y)
                else:
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
                    elif event.ui_element == btn_restablecer:
                        escala = 1.0
                        imagen_escalada = pygame.transform.scale(imagen, imagen.get_size())
                        imagen_rect = imagen_escalada.get_rect(center=CENTER)
                        mascara.fill((255, 255, 255, 255))
                        pygame.draw.circle(mascara, (0, 0, 0, 0), CENTER, RADIUS)
                        radio_pincel = 10
                    elif event.ui_element == btn_mas:
                        n_clavos = min(n_clavos + 1, 500)
                        entry_clavos.set_text(str(n_clavos))
                        clavos = calcular_clavos(n_clavos)
                    elif event.ui_element == btn_mascara:
                        modo_mascara = not modo_mascara
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
                    elif event.ui_element == btn_Guardar_imagen:
                        # Obtener los parámetros de escala y ubicación
                        escala_imagen = escala
                        centro_imagen = imagen_rect.center
                        centro_pantalla = (WIDTH // 2, HEIGHT // 2)
                        ubicacion_imagen = (centro_imagen[0] - centro_pantalla[0], centro_imagen[1] - centro_pantalla[1])
                        ruta_mascara = "data/mascaras/mascara.png"

                        # Crear una cadena de texto con los parámetros
                        parametros = f"Ruta: {Ruta}\nEscala: {escala_imagen}\nUbicacion: {ubicacion_imagen}\nRuta_mascara: {ruta_mascara}"

                        # Guardar la cadena de texto en un archivo .txt
                        with open("data/mascaras/parametros_imagen.txt", "w") as archivo:
                            archivo.write(parametros)

                        # Crear una nueva superficie del tamaño adecuado para la máscara final
                        mascara_final = pygame.Surface((2 * RADIUS, 2 * RADIUS), pygame.SRCALPHA)

                        # Calcular la posición relativa del círculo dentro de la máscara original
                        x_offset = CENTER[0] - RADIUS
                        y_offset = CENTER[1] - RADIUS

                        # Copiar la parte relevante de la máscara original a la nueva superficie
                        mascara_final.blit(mascara, (0, 0), pygame.Rect(x_offset, y_offset, 2 * RADIUS, 2 * RADIUS))

                        # Guardar la nueva máscara con el tamaño correcto
                        pygame.image.save(mascara_final, ruta_mascara)
                        
                        # Establecer una bandera para salir en el siguiente ciclo de eventos
                        running = False  

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
    
    # Retornar las rutas de los archivos generados
    return "data/mascaras/parametros_imagen.txt", "data/mascaras/mascara.png"