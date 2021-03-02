import numpy as np
import math

def fft(data, time, frequencia, amostragem):

    dt = 1/amostragem*frequencia
    constante_1 = 2*np.pi/(amostragem)
    constante_2 = 2/amostragem
    Cfc = np.zeros((amostragem, 1))
    Cfs = np.zeros((amostragem, 1))
    fftM = np.zeros((len(data)-amostragem, 1))
    fftM_ref = np.zeros((len(data) - amostragem, 1))
    fftA = np.zeros((len(data)-amostragem, 1))
    fftA_ref = np.zeros((len(data) - amostragem, 1))
    fase = np.zeros((len(data) - amostragem, 1))

    for i in range(0, amostragem, 1):
        angle = constante_1*i
        Cfc[i] = np.cos(angle)
        Cfs[i] = - np.sin(angle)

    #ref = np.zeros((len(data), 1))

    ref = referencia(data, frequencia, time)

    for i in range(amostragem, len(data), 1):
        fftM[i-amostragem], fftA[i-amostragem] = fft_mod_angle(data, amostragem, i, Cfc, Cfs, constante_2)
        fftM_ref[i - amostragem], fftA_ref[i - amostragem] = fft_mod_angle(ref, amostragem, i, Cfc, Cfs, constante_2)

    for i in range(0, len(fftA), 1):
        fase[i] = fft_angle_build(fftA, fftA_ref, i)

    return fftM, fase


def fft_angle_build(fftA, fftRef, pv):
    x = fftA[pv] - 90
    if x <= -180:
        x = x + 360

    xRef = fftRef[pv] - 90
    if xRef <= -180:
        xRef = xRef + 360

    while xRef >= 180:
        xRef = xRef - 360

    while xRef <= -180:
        xRef = xRef + 360

    gallas = x - xRef

    if gallas >= 180:
        gallas = gallas - 360
    if gallas <= -180:
        gallas = gallas + 360
    if (gallas >= -0.0001) and (gallas <= 0.0001):
        gallas = 0

    return gallas


def referencia(data, frequencia, time):
    w = 2*np.pi*frequencia
    ref = np.zeros((len(data), 1))

    for i in range(0, len(data), 1):
        ref[i] = np.sin(w*time[i])

    return ref


def fft_mod_angle(data, amostragem, pv, Cfc, Cfs, constante_2):

    fftR = 0
    fftI = 0
    decremento_amostragem = 0
    a = pv - amostragem
    for i in range(a, pv, 1):
        fftR = fftR + data[i]*Cfc[decremento_amostragem]
        fftI = fftI + data[i]*Cfs[decremento_amostragem]
        decremento_amostragem = decremento_amostragem + 1

    fftR = constante_2*fftR
    fftI = constante_2*fftI

    fftA = math.atan2(fftI, fftR)*57.295779
    fftM = np.sqrt(fftR*fftR+(fftI*fftI))

    return fftM, fftA


if __name__ == '__main__':
    print(fft(60, 128))