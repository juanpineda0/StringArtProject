# Proyecto String Art

Este proyecto transforma imágenes en representaciones de arte con hilos (String Art) mediante un proceso de múltiples etapas.

## Estructura del Proyecto

```
StringArtProject/
├── data/
│   ├── imagenes/          # Imágenes de entrada
│   ├── mascaras/          # Máscaras y parámetros de procesamiento
│   └── resultados/        # Resultados finales
├── src/
│   ├── generacion_hilos/  # Algoritmos de generación de patrones
│   │   ├── genetico.py    # Algoritmo genético
│   │   ├── greedy.py      # Algoritmo greedy
│   │   └── hough.py       # Transformada de Hough
│   ├── procesamiento.py   # Procesamiento inicial de imágenes
│   ├── combinacion.py     # Combinación de imagen y máscara
│   └── visualizacion.py   # Visualización del resultado final
├── main.py               # Punto de entrada principal
└── requirements.txt      # Dependencias del proyecto
```

## Flujo del Proyecto

El flujo completo del proyecto se controla desde `main.py`, que orquesta las siguientes etapas:

1. **Procesamiento Inicial** (`procesamiento.py`)
   - Carga la imagen de entrada
   - Aplica una máscara para ignorar partes no deseadas
   - Ajusta la imagen dentro del círculo de clavos
   - Guarda los resultados en `data/mascaras/`

2. **Combinación** (`combinacion.py`)
   - Toma la imagen procesada y la máscara
   - Genera una versión combinada que será la base para el String Art
   - Visualiza el resultado para verificación

3. **Generación de Patrones** (`generacion_hilos/`)
   - Implementa diferentes algoritmos para generar patrones de hilos:
     - **Genético**: Optimización evolutiva
     - **Greedy**: Selección local óptima
     - **Hough**: Detección de líneas
   - Cada algoritmo genera un archivo de texto con el formato:
     ```
     clavo_inicial,clavo_siguiente;clavo_inicial,clavo_siguiente;...
     ```

4. **Visualización** (`visualizacion.py`)
   - Toma el archivo de texto generado
   - Visualiza cómo se vería el String Art final
   - Permite ajustar parámetros como número de clavos y grosor de hilos

## Cómo Empezar

1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Colocar la imagen de entrada en `data/imagenes/`

3. Ejecutar el programa principal:
   ```bash
   python main.py
   ```

   El programa principal te guiará a través de:
   - Selección de imagen
   - Procesamiento inicial
   - Selección del algoritmo de generación de hilos
   - Visualización del resultado

## Formato de Archivos

- **Parámetros de Imagen** (`data/mascaras/parametros_imagen.txt`):
  ```
  Ruta: ruta/a/imagen.png
  Escala: valor_escala
  Ubicacion: (x, y)
  Ruta_mascara: ruta/a/mascara.png
  ```

- **Patrones de Hilos** (`data/resultados/patron.txt`):
  ```
  clavo_inicial,clavo_siguiente;clavo_inicial,clavo_siguiente;...
  ```

## Notas Importantes

- Las imágenes de entrada deben estar en formato PNG
- La máscara debe ser una imagen en escala de grises
- El número de clavos por defecto es 213
- Los resultados se guardan automáticamente en las carpetas correspondientes
- Todo el proceso se controla desde `main.py` 