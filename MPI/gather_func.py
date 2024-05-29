from mpi4py import MPI
import numpy as np

# Se define el método para balanceo de cargas
def nivelacion_cargas(D, n_p):
    s = len(D) % n_p
    t = int((len(D) - s) / n_p)
    l_i = 0
    l_s = 0
    out = []
    for i in range(n_p):
        if i < s:
            l_i = i * t + i
            l_s = l_i + t + 1
        else:
            l_i = i * t + s
            l_s = l_i + t
        out.append(D[l_i:l_s])
    return out

# data = np.arange(100000)
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

own_data = np.empty_like(np.ones(shape=(len(nivelacion_cargas(data, size)[rank]),)), dtype='i')

def scatter(data):
    data = nivelacion_cargas(data, size)
    for i in range(1, size):
        comm.send(data[i], dest=i)
    return data[0]

# 1) Primero se envían y reciben los datos
if rank == 0:
    own_data = scatter(data)
else:
    own_data = comm.recv(source=0)

# 2) Luego se realiza el procesamiento
local_mean = np.mean(own_data)

# 3) Recolectar las medias de cada proceso
means = comm.gather(local_mean, root=0)

# 4) Calcular la media global en el proceso maestro
if rank == 0:
    global_mean = np.mean(means)
    print("Media global:", global_mean)