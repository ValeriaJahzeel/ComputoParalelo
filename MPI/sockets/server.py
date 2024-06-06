import socket
import pickle
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def KNN():
    iris = load_iris()
    X = iris.data
    y = iris.target

    # entrnamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)
    
    return knn, iris

# se entrena el modelo
model, iris = KNN()

# ---------- SOCKKETS ----------
HOST = 'localhost'
PORT = 65432

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor.bind((HOST, PORT))
servidor.listen()

print("Esperando al cliente...")

while True:
    sockett, direccion = servidor.accept()
    print("Conectado al cliente")
    
    datos = sockett.recv(1024)

    # recibe los datos
    caracteristicas = pickle.loads(datos)
    print(f"Características recibidas: {caracteristicas}")

    # hace la predicción
    prediccion = model.predict(np.array(caracteristicas).reshape(1, -1))
    clase = iris.target_names[prediccion][0]
    print(f"Predicción: {clase}")

    sockett.sendall(clase.encode('utf-8'))

    sockett.close()
