import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

def analyze_system():
    # Parámetros del sistema
    A1 = 0.2
    A2 = 0.5
    K1 = 0.0032
    K2 = 0.0036
    g = 9.81
    qi = 0.01

    # Puntos de equilibrio
    h1_eq = (qi / K1)**2 / g  # Puntos de equilibrio h1
    h2_eq = (K1 / K2) * h1_eq  # Puntos de equilibrio h2 

    print(f"Puntos de equilibrio: h1 = {h1_eq}, h2 = {h2_eq}")

    # Matriz Jacobiana
    jacobian = np.array([
        [-K1/(2 * A1 * np.sqrt(g * h1_eq)), 0],  # Derivada parcial de dh1/dt respecto a h1 y h2
        [K1/(2 * A2 * np.sqrt(g * h1_eq)), -K2/(2 * A2 * np.sqrt(g * h2_eq))]  # Derivadas parciales de dh2/dt respecto a h1 y h2
    ])

    # Eigenvalores de la matriz Jacobiana:
    eigenvals = np.linalg.eigvals(jacobian)
    print(f"Eigenvalores: {eigenvals}")
    
    # Determinar la estabilidad
    stability = all(e.real < 0 for e in eigenvals)
    print(f"El sistema es {'estable' if stability else 'inestable'} en el punto de equilibrio.")

    # Definición de las funciones de transferencia del sistema de dos tanques
    # Relación entrada-salida (Forma 1)
    num1 = [K1/(A1*A2)]
    den1 = [1, (K1/A2 + K2/A2), K1*K2/(A1*A2)]
    
    sis1 = ctrl.tf(num1, den1)
    print(f"Función de transferencia - Forma 1: {sis1}")
    
    # Gráfica de respuesta al escalón para la primera forma
    t, y = ctrl.step_response(sis1)
    plt.plot(t, y)
    plt.title('Respuesta al escalón - Forma 1')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura del tanque 2 (h2)')
    plt.grid()
    plt.show()

    # Forma 2: Definir la función de transferencia usando la variable s
    s = ctrl.tf('s')
    sis2 = (K1/(A1*A2)) / (s**2 + (K1/A2 + K2/A2)*s + K1*K2/(A1*A2))
    print(f"Función de transferencia - Forma 2: {sis2}")
    
    # Gráfica de respuesta al escalón para la segunda forma
    t, y = ctrl.step_response(sis2)
    plt.plot(t, y)
    plt.title('Respuesta al escalón - Forma 2')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura del tanque 2 (h2)')
    plt.grid()
    plt.show()

    # Mapa de polos y ceros para sis1
    plt.figure()
    ctrl.pzmap(sis1)
    plt.title('Mapa de Polos y Ceros - Forma 1')
    plt.grid()
    plt.show()

    # Mapa de polos y ceros para sis2
    plt.figure()
    ctrl.pzmap(sis2)
    plt.title('Mapa de Polos y Ceros - Forma 2')
    plt.grid()
    plt.show()

    # Retrato fase con base en el sistema y los puntos de equilibrio
    h1_vals, h2_vals = np.meshgrid(np.linspace(0, 2, 20), np.linspace(0, 2, 20))
    dh1_dt = qi/A1 - K1/A1 * np.sqrt(g * h1_vals)  # Ecuación de la derivada de h1
    dh2_dt = K1/A2 * np.sqrt(g * h1_vals) - K2/A2 * np.sqrt(g * h2_vals)  # Ecuación de la derivada de h2
    
    plt.figure()
    plt.streamplot(h1_vals, h2_vals, dh1_dt, dh2_dt)
    plt.title('Retrato Fase')
    plt.xlabel('h1')
    plt.ylabel('h2')
    plt.grid()
    plt.show()

# Llamada a la función para realizar el análisis
analyze_system()
