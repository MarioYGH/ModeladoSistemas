import numpy as np
import matplotlib.pyplot as plt

# Parámetros del problema
A = np.array([[0, 1], [-1, 0]])  # Matriz A
b = np.array([0, 0])  # Vector b

# Condiciones iniciales
X0 = np.array([1, 0])  # Estado inicial [x1(0), x2(0)]

# Parámetros de integración
h = 0.01  # Paso de integración
Tfin = 10  # Tiempo final de simulación
N = int(Tfin / h)  # Número de pasos

# Inicialización de las matrices para almacenar resultados
X = np.zeros((N, 2))  # Matriz para almacenar los valores de [x1(t), x2(t)]
t = np.zeros(N)  # Vector de tiempo

# Condición inicial
X[0, :] = X0

# Método de Euler matricial
for k in range(N - 1):
    t[k + 1] = t[k] + h
    X[k + 1, :] = X[k, :] + h * (A @ X[k, :] + b)

# Gráfica de resultados
plt.plot(t, X[:, 0], label='x1(t)')
plt.plot(t, X[:, 1], label='x2(t)')
plt.xlabel('Tiempo t')
plt.ylabel('Estado')
plt.legend()
plt.title('Método de Euler Matricial')
plt.grid()
plt.show()
