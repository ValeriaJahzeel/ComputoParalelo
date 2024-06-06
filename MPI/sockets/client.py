import socket
import pickle

HOST = 'localhost'
PORT = 65432

caracteristicas = [5.1, 3.5, 1.4, 0.2]  

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

datos = pickle.dumps(caracteristicas)

cliente.sendall(datos)

clase = cliente.recv(1024).decode('utf-8')
print(f"La clase predicha es: {clase}")

cliente.close()
