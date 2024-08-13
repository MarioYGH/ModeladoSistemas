import numpy as np
import matplotlib.pyplot as plt

#En derivacion numerica siempre dependo de h, si es muy pequeña aproximo, si es muy grande me alejo
x = np.linspace(-2, 2, 1000) #x
h = x[1] - x[0] #delta_x

f = lambda x: 2*x #como tiene lambda se puede ocupar como funcion, variable que funge como funcion simbolica
fp = lambda x:2*np.ones(len(x)) #crea un vector de 1 que multiplica por mi funcion y meto como argumento el tamaño que desee

#derivacion numerica 
N = len(x)
xd = np.zeros(N-1)

fx = f(x) #resultado de evalar a f en x, en la practica es lo que vamos a tener 

for k in range(N-1): #N-1 para que no salga del vector 
    xd[k] = (f(x[k]+h) - f(x[k]))/h #si conozco el cuerpo de la funcion
    # Diferencia hacia delante DHD
    xd[k] = (f(x[k]) - f(x[k]-h))/h #si conozco el cuerpo de la funcion
    # Diferencia hacia atras DHA
    xd[k] = (f(x[k]+h) - f(x[k]-h))/(2*h) #si conozco el cuerpo de la funcion
    # Diferencia central DC
    #xd[k] = (fx[k+1] - f(x[k]))/h #si no conozco el cuerpo de la funcion
    

plt.figure 
plt.plot(x, fp(x))
plt.plot(x[:-1], xd,'-.')
plt.show()

# error
e = fp(x[:N-1]) - xd
plt.figure
plt.plot(x[:-1], e)
plt.show()


