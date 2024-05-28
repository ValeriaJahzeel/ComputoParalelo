import math

def nivelacion_cargas(valores, procesadores):
     mod = len(valores) % procesadores  # por si sobran valores
     ind = math.floor(len(valores)/procesadores )   # para saber cuantos le toca a cada uno
     final = []    # para guardar las particiones

     # inicializar los limites inferiores y superiores
     li = 0
     ls = ind

     print(mod, ind)

     for i in range(procesadores):      # para un tiempo O(procesadores)
          ls = li+ind
          if i < mod:    # para repartir los valores que sobran
               ls += 1
          final.append(valores[li:ls])
          li = ls
     return final