import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2, 2,1000)
h = x[1] - x[0]
g=10
l=1
kf=1
m=1

sin = lambda x: (-g/l)*np.sin(x)

x1 = np.zeros(len(x))
x1[0] = np.pi*1/4

x2 = np.zeros(len(x))
x2[0] = 0

for i in range(1, 1000):
    x1[i] = x1[i-1] + h*x2[i-1]
    x2[i] = x2[i-1] + h*((-g/l)*sin(x[i-1]) - (kf/m)*x2[i-1])

plt.figure()
plt.plot(x[:len(x1)], x1)
plt.show()

plt.plot(x[:len(x1)], x2)
plt.show()

#derivar x1 y comparar con x2
xd1 = np.zeros(len(x))
xd1[0] = 0

for i in range(1, 1000):
    xd1[i] = (x1[i] - x1[i-1])/h

plt.plot(x[:len(x1)], xd1)
plt.show()

# comprobar error con mse
mse1_dhd = np.mean(xd1 - x2)
print(mse1_dhd)
