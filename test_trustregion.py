import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def func2(xdata, a, b):
    return a*np.sin(np.pi*(xdata-b/8333.46406))


if __name__ == '__main__':

    ydata = np.array([-4591.41822694435, 4592.68041950579, -4590.11184811078, 4591.39307701415, -4592.68325154941])
    xdata = np.array([1, 8334, 16668, 25001, 33334])

    popt, pcov = curve_fit(func2, xdata, ydata, bounds=([10335, 1407], [11000, 2000]), method='trf')
    print(popt)
    print(pcov)