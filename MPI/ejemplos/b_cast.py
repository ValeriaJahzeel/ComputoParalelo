from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
	data_to_broadcast=np.arange(10, dtype='i')
	# Difundir datos desde el rango 0 a todos los procesos
else:
	data_to_broadcast = np.empty(10, dtype='i')
	

comm.Bcast(data_to_broadcast, root=0)
print(f"Proceso {rank}: Recibido datos {data_to_broadcast}")