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

# data = np.arange(100000)

matriz1 = [[1, 1, 1],[1, 1, 1],[1, 1, 1]]
matriz1 = np.flatten(matriz1)

matriz2 = [[1, 1, 1],[1, 1, 1],[1, 1, 1]]
matriz2 = np.flatten(matriz2)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def scatter(data1, data2):
    matriz1 = nivelacion_cargas(data1, size)     # Balanceo de cargas
    matriz2 = nivelacion_cargas(data2, size)     # Balanceo de cargas
    
    if rank == 0:   
        for i in range(1, size):   # Envia los datos a los procesos
            comm.send(data1[i], dest=i) 
            comm.send(data2[i], dest=i) 
        return data1[0], data2[0]
    else:
        return comm.recv(source=0) # Recibe los datos

def gather(own_data):
    if rank == 0:   
        gathered_data = [own_data] # Obtiene datos 
        for i in range(1, size):   # Recibie datos
            gathered_data.append(comm.recv(source=i))  # Recolecta datos
        gathered_data = np.concatenate(gathered_data)  # Une datos
        return gathered_data 
    else:
        comm.send(own_data, dest=0)     # Enviar los datos

# 1) Se envían y reciben los datos
own_data = scatter(matriz1, matriz2)

# 2) Media con sactter
print(f"Scatter -> {np.r(own_data)}")

# 3) Se reunen los datos 
gathered_data = gather(own_data)

# 4) Media con gather
if rank == 0:
    print("Gather -> ", np.sum(gathered_data))
