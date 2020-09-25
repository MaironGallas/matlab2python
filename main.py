from loading_simulations import loading_variables
import os

def run_all_simulations(path):
    for p, _, files in os.walk(os.path.abspath(path)):
        for file in files:
            data_dict = loading_variables(os.path.join(p, file))

if __name__ == '__main__':
    path = r'C:\Users\Mairon\Desktop\Simulacoes_Python\SI_FAIResistencia_N3819_S0_FA_T2'
    run_all_simulations(path)
