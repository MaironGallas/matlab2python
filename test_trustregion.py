import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

def func2(xdata, a, b, w):
    return a*np.sin(np.pi*(xdata-b/w))


if __name__ == '__main__':

    w = 8333.46406

    xdata = np.array([-5612.84560510564, 5625.24223537838, -5644.87683290912, 5675.34436231571, -5691.41421664163])
    y = np.array([1, 8331, 16659, 24984, 33313])

    """np.random.seed(1729)
    y_noise = 0.2 * np.random.normal(size=xdata.size)
    ydata = y + y_noise
    plt.plot(xdata, ydata, 'b-', label='data')

    popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
    plt.plot(xdata, func(xdata, *popt), 'g--', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()"""