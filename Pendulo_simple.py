import numpy as np
import matplotlib.pyplot as plt

# if _name_ == "_main_" #nada mas para terminal
if __name__ == '__main__':
  m = 0.5 #masa
  l = 0.30 #longitud
  kf = 0.1 #coeficiente de friccion
  g = 9.81 #gravedad

  h = 1e-3 #Paso de integración
  Tfin = 20 #tiempo de simulación
  N = int((Tfin-h)/h)

  t = np.zeros(N)
  X1 = np.zeros(N)
  X2 = np.zeros(N)

  X1[0] = np.pi/4 #Posicion inicial
  X2[0] = 0 #velociodad inicial

  for k in range(N-1):
    t[k+1] = t[k] + h
    X1[k+1] = X1[k] + h*(X2[k])
    X2[k+1] = X2[k] + h*(-(g/l)*np.sin(X1[k+1])-(kf/m)*X2[k]) #Euler no jala sin el k+1

  plt.figure
  plt.plot(t, X1)
  plt.show()

