from loading_simulations import loading_variables
import os
import matplotlib.pyplot as plt

def run_all_simulations(path):
    data_dict_array = []
    for p, _, files in os.walk(os.path.abspath(path)):
        for file in files:
            data_dict = loading_variables(os.path.join(p, file))
            data_dict_array.append(data_dict)
    return data_dict_array

if __name__ == '__main__':
    path = r'C:\Users\Mairon\Desktop\Mairon\Algoritimo Localizador de Falta\Simulacoes_Python'
    simulations = run_all_simulations(path)
    plt.plot(simulations[1]["time"], simulations[1]["Ifalta_fonte"], simulations[50]["time"], simulations[50]["Ifalta_fonte"])
    plt.show()

