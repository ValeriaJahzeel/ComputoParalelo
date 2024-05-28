from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	data = {'a':7, 'b':3.14}
	print('Proceso 0, envio data', data, 'a proceso 1')
	#comm.send(data, dest=1)
	

elif rank == 1:
	#time.sleep(5)
	data=comm.recv(source=0)
	print('Proceso 1, recibe data', data, 'de proceso 0')