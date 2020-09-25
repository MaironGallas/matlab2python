import numpy as np
from loading_simulations import loading_variables
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt

# print(np.asarray(time).shape) Printa o shape só para salvar


##Constantes
    #Cabo P-150
R = np.array([[0.000289873666666667, 5.88696666666666e-05, 5.88696666666666e-05],
              [5.88696666666667e-05, 0.000289873666666667, 5.88696666666666e-05],
              [5.88696666666667e-05, 5.88696666666666e-05, 0.000289873666666667]])

L = np.array([[2.57085278481072e-06, 1.82770795644935e-06, 1.82770795644935e-06],
              [1.82770795644935e-06, 2.57085278481072e-06, 1.82770795644935e-06],
              [1.82770795644935e-06, 1.82770795644935e-06, 2.57085278481072e-06]])

    #Média dos Cabos
"""
R = np.array([[0.000699257333333333, 5.87893333333334e-05, 5.87893333333333e-05],
              [5.87893333333333e-05, 0.000699257333333334, 5.87893333333333e-05],
              [5.87893333333333e-05, 5.87893333333333e-05, 0.000699257333333333]])

L = np.array([[2.67788713662241e-06, 1.58358549440546e-06, 1.58358549440546e-06],
              [1.58358549440546e-06, 2.67788713662241e-06, 1.58358549440546e-06],
              [1.58358549440546e-06, 1.58358549440546e-06, 2.67788713662241e-06]])
"""

def calculo_derivadas(data, R, L):

    #Inicializa vetores
    dVdt = np.zeros((len(data['time']), 3))
    dV2dt = np.zeros((len(data['time']), 3))
    dIdt = np.zeros((len(data['time']), 3))

    # Passo de tempo
    dt = data['time'][1] - data['time'][0]

    #Calcula Derivadas
    for i in range(1, len(data['time']), 1):
        # Primeira Derivada da Tensão
        dVdt[i, 0] = (data['Va'][i] - data['Va'][i-1])/dt
        dVdt[i, 1] = (data['Vb'][i] - data['Vb'][i-1])/dt
        dVdt[i, 2] = (data['Vc'][i] - data['Vc'][i-1])/dt
        # Segunda Derivada da Tensão
        dV2dt[i, 0] = (dVdt[i, 0] - dVdt[i-1, 0])/dt
        dV2dt[i, 1] = (dVdt[i, 1] - dVdt[i-1, 1])/dt
        dV2dt[i, 2] = (dVdt[i, 2] - dVdt[i-1, 2])/dt
        # Primeira Derivada da Corrente
        dIdt[i, 0] = (data['Ia'][i] - data['Ia'][i-1])/dt
        dIdt[i, 1] = (data['Ib'][i] - data['Ib'][i-1])/dt
        dIdt[i, 2] = (data['Ic'][i] - data['Ic'][i-1])/dt

    return dIdt

def calculo_queda_tensão(data, dIdt, R, L):

    matriz_correntes = np.array([[data['Ia']], [data['Ib']], [data['Ic']]]).reshape(3, len(data['time']))
    H1 = ((R.dot(matriz_correntes)) + (L.dot(dIdt.T))).T

    return H1

def classificador(data, fase):

    if fase == 1:
        Ifalta = data['Ifalta_fonte']
        Vfalta = data['Va']
    elif fase == 2:
        Ifalta = data['Ifalta_fonte']
        Vfalta = data['Vb']
    else:
        Ifalta = data['Ifalta_fonte']
        Vfalta = data['Vc']

    return Vfalta

def interpolacao(data, Vfalta, H1):
    time = data['time'][:, 0]
    Vfalta = Vfalta[:, 0]
    H1 = H1[:, 0]

    new_x = np.arange(time[0], time[len(time)-1], 1E-6)

    H1_interpolado = interpolate.interp1d(time, H1, kind='cubic')(new_x)
    Vfalta_interpolado = interpolate.interp1d(time, Vfalta, kind='cubic')(new_x)

    return H1_interpolado, Vfalta_interpolado, new_x

def distancia_estimada(data, Vfalta, H1):

    distancia = np.zeros((len(Vfalta), 1))

    for i in range(0, len(Vfalta), 1):
        distancia[i] = Vfalta[i]/H1[i]
        if distancia[i] > 14000 or distancia[i] < 0:
            distancia[i] = 0


    return distancia


if __name__ == '__main__':
    data = loading_variables(r'C:\Users\Mairon\Desktop\Simulacoes_Python\SI_FAIResistencia_N5261_S0_FA_T1')
    dIdt = calculo_derivadas(data, R, L)
    H1 = calculo_queda_tensão(data, dIdt, R, L)
    Vfalta = classificador(data, 1)
    H1, Vfalta, new_time = interpolacao(data, Vfalta, H1)
    distancia = distancia_estimada(data, Vfalta, H1)
    plt.plot(new_time,distancia, data['time'], data['Ifalta_fonte']*200)
    plt.show()