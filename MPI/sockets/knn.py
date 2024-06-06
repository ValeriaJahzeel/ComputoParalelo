import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import math
from multiprocessing import Pool
from scipy import stats as st

n_samples = 500

# Se crea el conjunto de datos con la función círculos
X, y = datasets.make_circles(n_samples, noise=0.1, factor=0.2, random_state=42)

def nivelacion_cargas(D, n_p):
    s = len(D) % n_p
    t = len(D) // n_p
    out = []
    for i in range(n_p):
        if i < s:
            out.append(D[i * (t + 1):(i + 1) * (t + 1)])
        else:
            out.append(D[i * t + s:(i + 1) * t + s])
    return out

def distancias(D, p, k):
    dist = np.sqrt(np.sum((D - p) ** 2, axis=1))
    return np.argsort(dist)[:k]

n_p = 5
cargas = nivelacion_cargas(X, n_p)
k = 3

# Se da un punto arbitrario
p = X[0]

# Se hace la nivelación de cargas
n_c = nivelacion_cargas(X, n_p)
# Se juntan los parametros para enviarlos a los procesos
parametros = zip(n_c, [p for _ in range(n_p)], [k for _ in range(n_p)])

# Se hace la nivelación de cargas sobre y
n_cy = nivelacion_cargas(y, n_p)
if __name__ == '__main__':

     with Pool(n_p) as pool:
          # Se guardan los resultados en una variable
          resultados = pool.starmap(distancias, parametros)
          # Se crea un nuevo conjunto de datos
          new_x = []
          new_y = []
          for i in range(len(resultados)):
               new_x.extend(n_c[i][resultados[i]])
               new_y.extend(n_cy[i][resultados[i]])
          # Se sacan las clases de acuerdo al nuevo conjunto de datos
          new_x = np.array(new_x)
          new_y = np.array(new_y)
          print(new_y[distancias(new_x, p, k)])
          # Para sacar la clase mayoritaria se utiliza la moda de las clases que se extrajeron
          print(st.mode(new_y[distancias(new_x, p, k)]))
          # En la posición 0 se guarda la moda de los resultados
          print(st.mode(new_y[distancias(new_x, p, k)])[0])
