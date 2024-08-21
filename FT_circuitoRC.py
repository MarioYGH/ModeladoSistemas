import control as ctrl 
import matplotlib.pyplot as plt
import numpy as np

#parametros del sistema
Vin = 1
R = 1000
C = 1000e-6

num = 1/(R*C)
den = [1,1/(R*C)]
sis1 = ctrl.tf(num,den)
t, y = ctrl.step_response(sis1)

#plt.plot(t, y)
#plt.figure()

s = ctrl.tf('s')
sis2 = (1/(R*C))/(s+1/(R*C))
# ctrl.poles(sis1) #polos
# ctrl.zeros(sis1) #zeros
# ctrl.pzmap(sis1) #mapa de polos y zeros


yt = lambda Vin, t, R, C : Vin*(1 - np.exp(-t/(R*C)))

plt.plot(t, y)
plt.plot(t, yt(Vin, t, R, C), '--')
plt.figure()


