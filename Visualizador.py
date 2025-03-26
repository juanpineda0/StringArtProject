import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons, TextBox, Slider
from matplotlib.collections import LineCollection

# Datos base
n_clavos = 213
grosor_hilo = 0.1
mostrar_etiquetas = False

# Leer nomenclatura desde archivo
with open("Recursos\ConejoSancocho.txt", "r", encoding="utf-8") as file:
    nomenclatura = file.read().strip()

def parse_string_to_lines(clavos_str, clavos):
    segmentos = clavos_str.split(';')
    return [[(clavos[int(i1)-1, 0], clavos[int(i1)-1, 1]), (clavos[int(i2)-1, 0], clavos[int(i2)-1, 1])]
            for segmento in segmentos for i1, i2 in zip(segmento.split(',')[:-1], segmento.split(',')[1:])]

# Crear figura y ejes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.3, bottom=0.1)
fig.set_size_inches(17, 9)

# Crear clavos en circunferencia
angles = np.linspace(0, 2 * np.pi, n_clavos, endpoint=False) - np.pi
clavos = np.column_stack((np.cos(angles), np.sin(angles)))

# Crear colección de líneas
lineas = parse_string_to_lines(nomenclatura, clavos)
line_collection = LineCollection([], colors='k', linewidths=grosor_hilo)
ax.add_collection(line_collection)

def actualizar_grafico(val):
    global n_clavos, grosor_hilo, mostrar_etiquetas, clavos, lineas
    
    try:
        nuevo_n_clavos = int(textbox_clavos.text) if textbox_clavos.text.isdigit() else n_clavos
        nuevo_grosor_hilo = float(textbox_grosor.text) if textbox_grosor.text.replace('.', '', 1).isdigit() else grosor_hilo

        n_clavos = nuevo_n_clavos
        grosor_hilo = nuevo_grosor_hilo
    except ValueError:
        return

    mostrar_etiquetas = check_etiquetas.get_status()[0]

    ax.clear()
    
    # Recalcular clavos
    angles = np.linspace(0, 2 * np.pi, n_clavos, endpoint=False) - np.pi
    clavos = np.column_stack((np.cos(angles), np.sin(angles)))

    # Recalcular líneas
    lineas = parse_string_to_lines(nomenclatura, clavos)

    # Dibujar clavos
    ax.scatter(clavos[:, 0], clavos[:, 1], c='r')

    if mostrar_etiquetas:
        for i, (x, y) in enumerate(clavos, start=1):
            ax.text(x, y, str(i), fontsize=8, ha='right', va='bottom', color='blue')

    # Redibujar líneas con el número actualizado de hilos
    actualizar_lineas(slider_hilos.val)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.draw()

def actualizar_lineas(val):
    global line_collection

    n_mostrar = int(slider_hilos.val)

    # Eliminar la colección de líneas anterior de manera segura
    for coll in ax.collections:
        if isinstance(coll, LineCollection):
            coll.remove()

    # Crear nueva colección con las líneas actualizadas
    line_collection = LineCollection(lineas[:n_mostrar], linewidths=grosor_hilo, color='black')

    # Agregar nueva colección sin acumulación
    ax.add_collection(line_collection)

    # Redibujar
    fig.canvas.draw_idle()

# Controles interactivos
ax_check = plt.axes([0.1, 0.2, 0.1, 0.1])
check_etiquetas = CheckButtons(ax_check, ['Etiquetas'], [mostrar_etiquetas])
check_etiquetas.on_clicked(actualizar_grafico)

# Cajas de texto
ax_text_clavos = plt.axes([0.1, 0.15, 0.15, 0.04])
textbox_clavos = TextBox(ax_text_clavos, 'Clavos', initial=str(n_clavos))
textbox_clavos.on_submit(lambda text: actualizar_grafico(None))

ax_text_grosor = plt.axes([0.1, 0.1, 0.15, 0.04])
textbox_grosor = TextBox(ax_text_grosor, 'Grosor', initial=str(grosor_hilo))
textbox_grosor.on_submit(lambda text: actualizar_grafico(None))

# Slider para controlar el número de líneas mostradas
ax_slider = plt.axes([0.1, 0.05, 0.7, 0.05])
slider_hilos = Slider(ax_slider, 'Hilos', 10, len(lineas), valinit=len(lineas), valstep=1)
slider_hilos.on_changed(actualizar_lineas)

actualizar_grafico(None)
plt.show()