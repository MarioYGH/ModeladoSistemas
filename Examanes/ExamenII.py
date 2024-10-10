# Mario Yahir García Hernández

import numpy as np
import control as ctrl
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parámetros del sistema
J1 = 10/9
J2 = 10
c = 0.1
k = 1
kI = 1

# Definir matrices A, B, C, D
A = np.array([
    [0, 1, 0, 0],
    [-(k/J1), -(c/J1), k/J1, c/J1],
    [0, 0, 0, 1],
    [k/J2, c/J2, -(k/J2), -(c/J2)]
])
B = np.array([[0], [kI/J1], [0], [0]])
C = np.array([[1, 0, 0, 0]])
D = np.array([[0]])

# Sistema en espacio de estados en lazo abierto
sys_ss = ctrl.ss(A, B, C, D)

# Eigenvalores en lazo abierto
eig_open = np.linalg.eigvals(A)
print("\nEigenvalores en lazo abierto:", eig_open)

# Respuesta al escalón en lazo abierto
t_open, y_open = ctrl.step_response(sys_ss)
plt.plot(t_open, y_open)
plt.title('Respuesta al Escalón en Lazo Abierto')
plt.xlabel('Tiempo (s)')
plt.ylabel('Ángulo φ1')
plt.grid(True)
plt.show()

# Lazo cerrado
A = A - B@C
sys_ss = ctrl.ss(A, B, C, 0)
sys_tf = ctrl.ss2tf(sys_ss)

t, y = ctrl.step_response(sys_tf)
plt.plot(t, y)
plt.xlabel('Tiempo (s)')
plt.ylabel('Respuesta (y)')
plt.title('Respuesta al escalón en Lazo Cerrado')
plt.grid(True)
plt.show()

# Eigenvalores en lazo cerrado
eig_close = np.linalg.eigvals(A)
print("\nEigenvalores en lazo cerrado:", eig_close)

# Diseño del controlador para un sobretiro del 2%
OS = 2
zeta = -np.log(OS / 100) / np.sqrt(np.pi**2 + (np.log(OS / 100))**2)
omega_n = 5
sigma = zeta * omega_n
omega_d = omega_n * np.sqrt(1 - zeta**2)
eig_deseados = np.array([
    -sigma + 1j * omega_d,
    -sigma - 1j * omega_d,
    -sigma + 1j * omega_d,
    -sigma - 1j * omega_d
])
print("Eigenvalores deseados:", eig_deseados)

# Controlabilidad y diseño del controlador
ctrb_matrix = ctrl.ctrb(A, B)
if np.linalg.matrix_rank(ctrb_matrix) == A.shape[0]:
    K = ctrl.acker(A, B, eig_deseados)
    print("\nMatriz de ganancia K:", K)

    # Factor de escala k_r
    A_closed = A - B @ K
    try:
        inv_term = np.linalg.inv(A_closed)
        k_r = 1.0 / (C @ inv_term @ B)
    except np.linalg.LinAlgError:
        k_r = 1.0
    print(f"\nFactor de escala k_r: {k_r[0][0]:.4f}")

    # Sistema en Retroalimentación de Estados
    B_closed = B * k_r
    sys_closed = ctrl.ss(A_closed, B_closed, C, D)

    # Eigenvalores en Retroalimentación de Estados
    eig_retro = np.linalg.eigvals(A_closed)
    print("\nEigenvalores en Retroalimentación de Estados:", eig_retro)

    # Respuesta al escalón en Retroalimentación de Estados
    t = np.linspace(0, 10, 1000)
    t_closed, y_closed = ctrl.step_response(sys_closed, T=t)

    info = ctrl.step_info(sys_closed)
    print("\nSobretiro:", info['Overshoot'])
    print("\nTiempo de asentamiento:", info['SettlingTime'])
    print("\nTiempo de levantamiento:", info['RiseTime'])

    plt.plot(t_closed, y_closed)
    plt.title('Retroalimentación de Estados')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Ángulo φ1')
    plt.grid(True)
    plt.show()

    # Simular los estados en Retroalimentación de Estados
    def closed_loop_dynamics(x, t, A_cl, B_cl, K, k_r, r):
        dxdt = A_cl @ x + B_cl.flatten() * r
        return dxdt

    x0 = np.zeros(A.shape[0])
    r = 1.0
    x = odeint(closed_loop_dynamics, x0, t, args=(A_closed, B_closed, K, k_r, r))

    u_t = -x @ K.T + k_r * r

    # Graficar u(t)
    plt.plot(t, u_t)
    plt.title('Señal de Control u(t)')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('u(t)')
    plt.grid(True)
    plt.show()

# Función de transferencia en lazo abierto
sys_tf_open = ctrl.ss2tf(sys_ss)
print("\nFunción de transferencia en lazo abierto:", sys_tf_open)

# Función de transferencia en lazo cerrado
sys_tf_closed = ctrl.ss2tf(sys_closed)
print("\nFunción de transferencia en lazo cerrado:", sys_tf_closed)
