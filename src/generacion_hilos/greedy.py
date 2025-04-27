import numpy as np
import os
from typing import List, Tuple

def generar_patron_greedy() -> str:
    """
    Genera un patrón de String Art usando un algoritmo greedy.
    Retorna la ruta al archivo con el patrón generado.
    """
    # TODO: Implementar algoritmo greedy
    # Por ahora solo creamos un archivo de ejemplo
    ruta_resultado = "data/resultados/patron_greedy.txt"
    os.makedirs(os.path.dirname(ruta_resultado), exist_ok=True)
    
    # Ejemplo de patrón: 1,2;2,3;3,4;...
    with open(ruta_resultado, "w") as f:
        f.write("1,2;2,3;3,4")
    
    return ruta_resultado
