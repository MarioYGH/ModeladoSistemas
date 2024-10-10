# Mario Yahir García Hernández
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
import sympy as sp

def analyze_system():
    # Parámetros del sistema
    A1 = 0.2
    A2 = 0.5
    K1 = 0.0032
    K2 = 0.0036
    g = 9.81
    qi = 0.01

    # Definición simbólica de las variables h1 y h2 para calcular puntos de equilibrio
    h1, h2 = sp.symbols('h1 h2')
    
    # Definir las ecuaciones del sistema (derivadas de h1 y h2)
    eq1 = qi/A1 - K1/A1 * sp.sqrt(g * h1)
    eq2 = K1/A2 * sp.sqrt(g * h1) - K2/A2 * sp.sqrt(g * h2)
    
    # Resolver los puntos de equilibrio
    equilibria = sp.solve([eq1, eq2], (h1, h2))
    print(f"Puntos de equilibrio: {equilibria}")

    # Definir la matriz Jacobiana (linealización del sistema)
    variables = [h1, h2]
    equations = [eq1, eq2]
    jacobian = sp.Matrix(equations).jacobian(variables)
    
    # Evaluar la jacobiana en los puntos de equilibrio
    jacobian_at_eq = jacobian.subs({h1: equilibria[0][0], h2: equilibria[0][1]})
    jacobian_num = np.array(jacobian_at_eq).astype(np.float64)
    
    # Calcular los eigenvalores de la matriz Jacobiana
    eigenvals = np.linalg.eigvals(jacobian_num)
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

    # Retrato fase
    h1_vals, h2_vals = np.meshgrid(np.linspace(0, 2, 20), np.linspace(0, 2, 20))
    dh1_dt = qi/A1 - K1/A1 * np.sqrt(g * h1_vals)
    dh2_dt = K1/A2 * np.sqrt(g * h1_vals) - K2/A2 * np.sqrt(g * h2_vals)
    
    plt.figure()
    plt.streamplot(h1_vals, h2_vals, dh1_dt, dh2_dt)
    plt.title('Retrato Fase')
    plt.xlabel('h1')
    plt.ylabel('h2')
    plt.grid()
    plt.show()

# Llamada a la función para realizar el análisis
analyze_system()
