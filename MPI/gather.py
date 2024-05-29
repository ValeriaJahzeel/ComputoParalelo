from mpi4py import MPI
import numpy as np
import math


# se define el método para balanceo de cargas
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

data = np.arange(100000)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

own_data = np.empty_like(np.ones(shape=(len(nivelacion_cargas( data, size)[rank]),)), dtype='i')

def scatter(data):
     data = nivelacion_cargas(data, size)
     for i in range(1,size):
          comm.send(data[i], dest=i)
     return data[0]

# 1) Primero se envian y reciben los datos
if rank==0:
     own_data = scatter(data)
else:
     own_data = comm.recv(source=0)

# 2) Luego se realiza el procesamiento
if rank==0:
     print(np.mean(own_data))
else:
     print(np.mean(own_data))
     
def gatter(own_data):
     own_data = nivelacion_cargas(data, size)[0]
     received_data = [own_data]
     for i in range(1, size):
          received_data.append(comm.recv(source=i))

     # Reunir todos los datos en el proceso raíz
     gathered_data = np.concatenate(received_data)
     
     print("Media de los datos recolectados:", np.mean(gathered_data))

# 1) Cada proceso envía sus datos al proceso raíz
if rank != 0:
     comm.send(nivelacion_cargas(data, size)[rank], dest=0)
else:
     gatter(own_data)