import os
import sys
from src.procesamiento import procesar_imagen
from src.combinacion import combinar_imagen
from src.visualizacion import visualizar_nomenclatura
from src.generacion_hilos.genetico import generar_patron_genetico
from src.generacion_hilos.greedy import generar_patron_greedy
from src.generacion_hilos.hough import generar_patron_hough

def seleccionar_imagen():
    """Permite al usuario seleccionar una imagen del directorio de imágenes."""
    imagenes_dir = "data/imagenes"
    if not os.path.exists(imagenes_dir):
        os.makedirs(imagenes_dir)
        print(f"Directorio {imagenes_dir} creado. Por favor, coloca tus imágenes allí.")
        return None

    imagenes = [f for f in os.listdir(imagenes_dir) if f.endswith('.png')]
    if not imagenes:
        print(f"No se encontraron imágenes PNG en {imagenes_dir}")
        return None

    print("\nImágenes disponibles:")
    for i, img in enumerate(imagenes, 1):
        print(f"{i}. {img}")

    while True:
        try:
            seleccion = int(input("\nSelecciona el número de la imagen: ")) - 1
            if 0 <= seleccion < len(imagenes):
                return os.path.join(imagenes_dir, imagenes[seleccion])
            print("Selección inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def seleccionar_algoritmo():
    """Permite al usuario seleccionar el algoritmo de generación de hilos."""
    print("\nAlgoritmos disponibles:")
    print("1. Genético")
    print("2. Greedy")
    print("3. Hough")

    while True:
        try:
            seleccion = int(input("\nSelecciona el número del algoritmo: "))
            if seleccion == 1:
                return generar_patron_genetico
            elif seleccion == 2:
                return generar_patron_greedy
            elif seleccion == 3:
                return generar_patron_hough
            print("Selección inválida. Intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def main():
    """Función principal que orquesta todo el proceso."""
    print("=== Proyecto String Art ===")
    
    # Paso 1: Selección de imagen
    ruta_imagen = seleccionar_imagen()
    if not ruta_imagen:
        return

    # Paso 2: Procesamiento inicial
    print("\nProcesando imagen...")
    if not procesar_imagen(ruta_imagen):
        print("Error en el procesamiento de la imagen.")
        return

    # Paso 3: Combinación
    print("\nCombinando imagen con máscara...")
    if not combinar_imagen():
        print("Error en la combinación de la imagen.")
        return

    # Paso 4: Selección y ejecución del algoritmo
    print("\nSeleccionando algoritmo de generación de hilos...")
    algoritmo = seleccionar_algoritmo()
    print("\nGenerando patrón de hilos...")
    ruta_patron = algoritmo()
    if not ruta_patron:
        print("Error en la generación del patrón.")
        return

    # Paso 5: Visualización
    print("\nVisualizando resultado...")
    visualizar_nomenclatura(ruta_patron, 213)  # 213 es el número de clavos por defecto

if __name__ == "__main__":
    main()
