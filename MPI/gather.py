from mpi4py import MPI
import numpy as np
import math

# Método para balanceo de cargas
def nivelacion_cargas(valores, procesadores):
    mod = len(valores) % procesadores  # Por si sobran valores
    ind = math.floor(len(valores) / procesadores)  # Para saber cuántos le toca a cada uno
    final = []  # Para guardar las particiones

    # Inicializar los límites inferiores y superiores
    li = 0
    ls = ind

    for i in range(procesadores):  # Para un tiempo O(procesadores)
        ls = li + ind
        if i < mod:  # Para repartir los valores que sobran
            ls += 1
        final.append(valores[li:ls])
        li = ls
    return final

data = np.arange(100000)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Scatter los datos a los diferentes procesos
def scatter(data):
    data = nivelacion_cargas(data, size)
    if rank == 0:
        for i in range(1, size):
            comm.send(data[i], dest=i)
        return data[0]
    else:
        return comm.recv(source=0)

# Gather los datos desde los diferentes procesos
def gather(own_data):
    if rank == 0:
        gathered_data = [own_data]
        for i in range(1, size):
            gathered_data.append(comm.recv(source=i))
        gathered_data = np.concatenate(gathered_data)
        return gathered_data
    else:
        comm.send(own_data, dest=0)

# 1) Scatter: Primero se envían y reciben los datos
own_data = scatter(data)

# 2) Procesar los datos
print(f"Rank {rank}: Media de los datos locales: {np.mean(own_data)}")

# 3) Gather: Reunir los datos en el proceso raíz
gathered_data = gather(own_data)

if rank == 0:
    print("Media de todos los datos recolectados:", np.mean(gathered_data))
