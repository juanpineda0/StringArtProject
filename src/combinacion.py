import cv2
import numpy as np
import matplotlib.pyplot as plt

def leer_parametros(ruta_parametros):
    """Lee el archivo de parámetros y devuelve los valores necesarios."""
    parametros = {}
    with open(ruta_parametros, 'r', encoding="utf-8") as f:
        for linea in f:
            clave, valor = linea.strip().split(': ', 1)
            parametros[clave] = valor
    
    parametros['Escala'] = float(parametros['Escala'])
    parametros['Ubicacion'] = tuple(map(int, parametros['Ubicacion'][1:-1].split(', ')))
    return parametros

def cargar_imagen(ruta, escala):
    """Carga, escala y recorta la imagen a 600x600 manteniendo el centro, con fondo transparente si es necesario."""
    imagen = cv2.imread(ruta, cv2.IMREAD_UNCHANGED)  # Cargar con canal alfa si está disponible
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGBA)
    if imagen is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {ruta}")

    # Si la imagen no tiene canal alfa, se lo añadimos
    if imagen.shape[-1] == 3:  # Si es RGB, convertir a RGBA con fondo transparente
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2BGRA)
        imagen[:, :, 3] = 255  # Asignar opacidad total

    # Escalar la imagen
    nueva_dim = (int(imagen.shape[1] * escala), int(imagen.shape[0] * escala))
    imagen_escalada = cv2.resize(imagen, nueva_dim, interpolation=cv2.INTER_LINEAR)

    # Obtener dimensiones de la imagen escalada
    alto, ancho = imagen_escalada.shape[:2]

    # Calcular las coordenadas del recorte (centrado)
    x_centro, y_centro = ancho // 2, alto // 2
    x_ini = max(x_centro - 480, 0)
    y_ini = max(y_centro - 480, 0)
    x_fin = min(x_centro + 480, ancho)
    y_fin = min(y_centro + 480, alto)

    # Crear un lienzo transparente de 960x960
    imagen_recortada = np.zeros((960, 960, 4), dtype=np.uint8)  # 4 canales (RGBA), todo transparente

    # Recortar la imagen original
    recorte = imagen_escalada[y_ini:y_fin, x_ini:x_fin]

    # Insertar el recorte en el lienzo transparente centrado
    y_offset = (960 - recorte.shape[0]) // 2
    x_offset = (960 - recorte.shape[1]) // 2
    imagen_recortada[y_offset:y_offset+recorte.shape[0], x_offset:x_offset+recorte.shape[1]] = recorte

    return imagen_recortada

def aplicar_traslacion(imagen, tx, ty, escala):
    """Aplica un desplazamiento (traslación) a la imagen con transparencia en el fondo."""

    # Crear una imagen con transparencia (fondo alfa en 0)
    h, w = imagen.shape[:2]
    imagen_transparente = np.zeros((h, w, 4), dtype=np.uint8)

    # Matriz de traslación
    M = np.float32([[1, 0, tx], [0, 1, ty]])

    # Aplicar la traslación a los tres primeros canales (BGR)
    imagen_desplazada = cv2.warpAffine(imagen[:, :, :3], M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

    # Aplicar la traslación al canal alfa (mantener transparencia)
    canal_alpha = cv2.warpAffine(imagen[:, :, 3], M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    # Unir los canales con el alfa modificado
    imagen_transparente[:, :, :3] = imagen_desplazada
    imagen_transparente[:, :, 3] = canal_alpha

    return imagen_transparente

def aplicar_mascara(imagen, ruta_mascara):
    """Recorta la máscara manteniendo el mismo centro y la aplica a la imagen sin alterar transparencias previas."""
    mascara = cv2.imread(ruta_mascara, cv2.IMREAD_GRAYSCALE)
    if mascara is None:
        raise FileNotFoundError(f"No se pudo cargar la máscara en la ruta: {ruta_mascara}")

    # Invertir la máscara para que las áreas negras se vuelvan transparentes
    mascara = cv2.bitwise_not(mascara)

    # Convertir la imagen a BGRA si no tiene canal alfa
    if len(imagen.shape) == 2:  # Imagen en escala de grises
        imagen = cv2.cvtColor(imagen, cv2.COLOR_GRAY2BGRA)
        print("Escala de grises")
    elif imagen.shape[2] == 3:  # Imagen en BGR
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2BGRA)

    # Obtener dimensiones de imagen y máscara
    h_img, w_img = imagen.shape[:2]
    h_masc, w_masc = mascara.shape

    # Crear una máscara del tamaño de la imagen con la transparencia original
    nueva_mascara = imagen[:, :, 3].copy()  # Mantener la transparencia original

    # Calcular coordenadas para centrar la máscara en la imagen
    x_offset = (w_img - w_masc) // 2
    y_offset = (h_img - h_masc) // 2

    # Determinar los límites de recorte
    x1_masc, x2_masc = max(0, -x_offset), min(w_masc, w_img - x_offset)
    y1_masc, y2_masc = max(0, -y_offset), min(h_masc, h_img - y_offset)

    x1_img, x2_img = max(0, x_offset), min(w_img, x_offset + w_masc)
    y1_img, y2_img = max(0, y_offset), min(h_img, y_offset + h_masc)

    # Aplicar la máscara SOLO en las áreas donde la nueva máscara cubre
    nueva_mascara[y1_img:y2_img, x1_img:x2_img] = mascara[y1_masc:y2_masc, x1_masc:x2_masc]

    imagen[:, :, 3] = cv2.min(imagen[:, :, 3], nueva_mascara)

    return imagen

def visualizar_resultados(imagen_antes, titulo_antes, imagen_despues, titulo_despues):
    """Muestra la imagen y los bordes detectados."""
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(imagen_antes, cmap='gray')
    axs[0].set_title(titulo_antes)
    axs[1].imshow(imagen_despues, cmap='gray')
    axs[1].set_title(titulo_despues)

    # Recalcular clavos
    angles = np.linspace(0, 2 * np.pi, 213, endpoint=False) - np.pi
    clavos = np.column_stack((np.cos(angles)*480+480, np.sin(angles)*480+480))
    # Dibujar clavos
    axs[0].scatter(clavos[:, 0], clavos[:, 1], c='r', s=2)
    axs[1].scatter(clavos[:, 0], clavos[:, 1], c='r', s=2)
    plt.show()

def combinar_imagen() -> str:
    """
    Combina la imagen procesada con la máscara y aplica las transformaciones necesarias.
    
    Returns:
        str: Ruta a la imagen procesada
    """
    # Leer parámetros
    parametros = leer_parametros("data/mascaras/parametros_imagen.txt")
    ruta_imagen = parametros["Ruta"]
    escala = parametros["Escala"]
    tx, ty = parametros["Ubicacion"]
    ruta_mascara = parametros["Ruta_mascara"]

    # Cargar imagen y aplicar transformaciones
    imagen_elegida = cargar_imagen(ruta_imagen, escala)
    imagen_trasladada = aplicar_traslacion(imagen_elegida, tx, ty, escala)
    imagen = aplicar_mascara(imagen_trasladada, ruta_mascara)

    # Guardar resultado
    ruta_resultado = "data/resultados/imagen_procesada.jpg"
    cv2.imwrite(ruta_resultado, imagen)

    # Visualizar resultados
    visualizar_resultados(imagen_elegida, "Imagen elegida", imagen, "Imagen recortada")
    
    return ruta_resultado