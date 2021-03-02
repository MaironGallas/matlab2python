import numpy as np
from loading_simulations import loading_variables
import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
from fourier import fft

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


def indice_crossing_zero(H1, newtime):

    registroP = []
    registroN = []
    ok = False

    ciclo = 1/60/newtime[1] - newtime[0]

    for i in range(2000002, 2050002, 1):
        if (H1[i] < 0) and (H1[i - 1] > 0):
            registroP.append(i)
            ok = True
        if (H1[i] > 0) and (H1[i - 1] < 0) and ok:
            registroN.append(i)

    return registroP, registroN

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

def signal_recomp(data):

    Va_modulo, Va_fase = fft(data['Va'], data['time'], 60, 128)
    Vb_modulo, Vb_fase = fft(data['Vb'], data['time'], 60, 128)
    Vc_modulo, Vc_fase = fft(data['Vc'], data['time'], 60, 128)

    Ia_modulo, Ia_fase = fft(data['Ia'], data['time'], 60, 128)
    Ib_modulo, Ib_fase = fft(data['Ib'], data['time'], 60, 128)
    Ic_modulo, Ic_fase = fft(data['Ic'], data['time'], 60, 128)

    print(len(Ia_modulo))
    print(len(Ia_fase))

    Va1H = np.zeros((len(Ia_modulo), 1))
    Vb1H = np.zeros((len(Ia_modulo), 1))
    Vc1H = np.zeros((len(Ia_modulo), 1))
    Ia1H = np.zeros((len(Ia_modulo), 1))
    Ib1H = np.zeros((len(Ia_modulo), 1))
    Ic1H = np.zeros((len(Ia_modulo), 1))


    for i in range(0, len(Ia_modulo), 1):
        Va1H[i] = Va_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Va_fase[i]*(np.pi/180))
        Vb1H[i] = Vb_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Vb_fase[i]*(np.pi/180))
        Vc1H[i] = Vc_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Vc_fase[i]*(np.pi/180))

        Ia1H[i] = Ia_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Ia_fase[i]*(np.pi/180))
        Ib1H[i] = Ib_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Ib_fase[i]*(np.pi/180))
        Ic1H[i] = Ic_modulo[i] * np.sin(2 * np.pi * 60 * data['time'][i] + Ic_fase[i]*(np.pi/180))

    data_1h = {'Va': Va1H, 'Vb': Vb1H, 'Vc': Vc1H,
               'Ia': Ia1H, 'Ib': Ib1H, 'Ic': Ic1H}

    return data_1h


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
    data = loading_variables(r'D:\Mairon\Algoritimo Localizador de Falta\Simulacoes_Python\SI_FAIResistencia_N5261_S0_FA_T1')
    """dIdt = calculo_derivadas(data, R, L)
    H1 = calculo_queda_tensão(data, dIdt, R, L)"""
    data_1h = signal_recomp(data)
    plt.plot(data_1h['Va'])
    plt.plot(data_1h['Vb'])
    plt.plot(data_1h['Vc'])
    plt.show()
    """Vsubfalta = classificador(data, 1)
    H1, Vsubfalta, new_time = interpolacao(data, Vsubfalta, H1)
    distancia = distancia_estimada(data, Vsubfalta, H1)
    indiceP, indiceN = indice_crossing_zero(H1, new_time)"""
