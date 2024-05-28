import numpy as np
import random
import math
import multiprocessing
from multiprocessing import Pool
import time

import torch

# variables
cant_valores = 1000     # pasos
num_procesadores = 4

def nivelacion_cargas(valores, procesadores):
     mod = len(valores) % procesadores  # por si sobran valores
     ind = math.floor(len(valores)/procesadores )   # para saber cuantos le toca a cada uno
     final = []    # para guardar las particiones

     # inicializar los limites inferiores y superiores
     li = 0
     ls = ind

     for i in range(procesadores):      # para un tiempo O(procesadores)
          ls = li+ind
          if i < mod:    # para repartir los valores que sobran
               ls += 1
          final.append(valores[li:ls])
          li = ls
     return final

def construccionSerie(cant_valores):
     serie = []
     i = 3  # para que empieze en el 3
     while(len(serie) < cant_valores):          
          serie.append(1/i)
          i += 2

     return serie
     

serie = construccionSerie(cant_valores)
# print("Serie de Madhaua - Leibniz -> ", serie)
# print(len(serie))


cargas = nivelacion_cargas(serie, num_procesadores)
# print("Nivelacion de cargas -> ", cargas)

def suma2(carga,lock,results):
     lock.acquire()
     print(sum(carga))
     results.append(sum(carga))
     # sum(carga)
     lock.release()
     
results = multiprocessing.Manager().list()
lock=multiprocessing.Lock()
res = []

for i in range(num_procesadores):
     res.append(multiprocessing.Process(target = suma2, args=[cargas[i],lock, results]))

start_time = time.perf_counter()

for thread in res:
    thread.start()

for thread in res:
    thread.join()

finish_time = time.perf_counter()

print(f"Program finished in {finish_time-start_time} seconds")
print("Suma total -> ", sum(results) +1 )
print(res)

def run():
    torch.multiprocessing.freeze_support()
    print('loop')

if __name__ == '__main__':
    run()