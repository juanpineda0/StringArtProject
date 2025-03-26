import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)  # 100 puntos entre 0 y 10

fig, ax = plt.subplots()  # Crea la figura y los ejes
ax.plot(x, np.sin(x), 'b--', label="Seno")
ax.plot(x, np.cos(x), 'g:', label="Coseno")
ax.legend()  # Muestra la leyenda

plt.show()  # Muestra la gráfica
