from mpi4py import MPI
import numpy as np

# se define el método para balanceo de cargas
def nivelacion_cargas(D, n_p):
    s=len(D)%n_p
    t=int((len(D)-s)/n_p)
    l_i=0
    l_s=0
    out=[]
    for i in range(n_p):
        if i<s:
            l_i=i*t+i
            l_s=l_i+t+1
        else:
            l_i=i*t+s
            l_s=l_i+t
        out.append(D[l_i:l_s])
    return out

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Primero se debe hacer el broadcast del arreglo
if rank == 0:
    data_to_broadcast=np.arange(10000, dtype='i')
    
else:
    data_to_broadcast = np.empty(10000, dtype='i')
    

# Difundir datos desde el rango 0 a todos los procesos
comm.Bcast(data_to_broadcast, root=0)



if rank==0:
    data = nivelacion_cargas(data_to_broadcast, size)[rank]
    resultado=np.mean(data)
    for i in range(1,size):
        resultado+=comm.recv(source=i)
    resultado = resultado/size
    print('el resultado de la media global es:', resultado)
else:
    # se usa la nivelación de cargas pero se pueden hacer los 
    # cálculos en cada nodo
    resultado_parcial = np.mean(nivelacion_cargas(data_to_broadcast, size)[rank])
    comm.send(resultado_parcial, dest=0)