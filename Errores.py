import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True

def benchmark(y, yg):
    
    def mse(y, yg):
        return np.mean((y-yg)**2)
    
    def rmse(y, yg):
        return np.sqrt(mse(y, yg))
        #return np.sqrt(np.mean((y - yg)**2))
    
    def mae(y, yg):
        return np.mean(np.abs(yg, y))
    
    def mape(y, yg):
        return 100*np.mean(np.abs((y - yg)/y)) #por numpy lo hago dato por dato, sino se tendría que usar un for
    
    def fit(y, yg):
        100*(1 - np.linalg.norm(y - yg)/np.linalg.norm(y - np.mean(y)))
        
    results = {
        'MSE': mse(y, yg),
        'RMSE':rmse(y, yg),
        'MAE': mae(y, yg),
        'MAPE': mape(y, yg),
        'FIT': fit(y, yg)
        }
    return results

t = np.linspace(0, 10, 100)

y = np.random.rand(1000)

yg = y + 0.01*np.ones(1000) 

resultados = benchmark(y, yg)
print(resultados)

plt.figure
plt.plot(t, y, label = r'$y(t)$')   
plt.plot(t, yg, label = r'$\hat{y}_{g}(t)$')  
plt.xlabel('Time') 
plt.legend(loc = 'best')
plt.show()
        
        
