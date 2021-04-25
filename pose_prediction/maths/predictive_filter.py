from collections import deque
import numpy as np
import math


class PredictiveFilter:
    """
    Esta clase crea una lista donde calcula el promedio con pesos ponderados
    """

    def __init__(self, size):
        """
        Inicializa una fila de tamaño requerido y pesos de forma lineal

        :param size: Tamaño de la fila
        """

        self.queue = deque(maxlen=size)
        self.weights = [i*1/(size) for i in range(1, size+1)]

        # Llenar la fila
        for _ in range(size):
            self.queue.append(0)

    def update(self, data):
        """
        Calcula el promedio ponderado y luego inserta el dato

        :param data: Nuevo dato
        :returns: El promedio de la fila con los pesos
        """

        avg = np.average(self.queue, weights=self.weights)
        self.queue.append(data)

        return avg
