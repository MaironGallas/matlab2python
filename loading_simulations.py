from scipy.io import loadmat
import re



def file_pattern(file):
   pattern_no = r'N3819'
   pattern_fase_a = r'_FA_'
   pattern_fase_b = r'_FB_'

   return bool(re.search(pattern_no, file)), bool(re.search(pattern_fase_a, file)), bool(re.search(pattern_fase_b, file))

def print_variables(data):
    lista = []
    for x in data:
        lista.append(x)

    return print(lista)

def loading_variables(file):
    data = loadmat(file)
    flag_N3819, flag_fase_a, flag_fase_b = file_pattern(file)

    if flag_N3819:
        if flag_fase_a:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0123a6181a'], 'Ib': data['iX0123b6181b'], 'Ic': data['iX0123c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0129'], 'Ifalta_carga': data['iLoadXx0124'],
                        'Vfalta_fonte': data['vSo_a'], 'Vfalta_carga': data['vLo_a'], 'time': data['t']}

        elif flag_fase_b:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0123a6181a'], 'Ib': data['iX0123b6181b'], 'Ic': data['iX0123c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0129'], 'Ifalta_carga': data['iLoadXx0124'],
                        'Vfalta_fonte': data['vSo_b'], 'Vfalta_carga': data['vLo_b'], 'time': data['t']}
        else:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0123a6181a'], 'Ib': data['iX0123b6181b'], 'Ic': data['iX0123c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0129'], 'Ifalta_carga': data['iLoadXx0124'],
                        'Vfalta_fonte': data['vSo_c'], 'Vfalta_carga': data['vLo_c'], 'time': data['t']}
    else:
        if flag_fase_a:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0124a6181a'], 'Ib': data['iX0124b6181b'], 'Ic': data['iX0124c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0130'], 'Ifalta_carga': data['iLoadXx0125'],
                        'Vfalta_fonte': data['vSo_a'], 'Vfalta_carga': data['vLo_a'], 'time': data['t']}
        elif flag_fase_b:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0124a6181a'], 'Ib': data['iX0124b6181b'], 'Ic': data['iX0124c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0130'], 'Ifalta_carga': data['iLoadXx0125'],
                        'Vfalta_fonte': data['vSo_b'], 'Vfalta_carga': data['vLo_b'], 'time': data['t']}
        else:
            data_dict = {'Va': data['v6181a'],'Vb': data['v6181b'],'Vc': data['v6181c'],
                        'Ia': data['iX0124a6181a'], 'Ib': data['iX0124b6181b'], 'Ic': data['iX0124c6181c'],
                        'Ineutro': data['iTerraXx0111'], 'Ifalta_fonte': data['iSourcXx0130'], 'Ifalta_carga': data['iLoadXx0125'],
                        'Vfalta_fonte': data['vSo_c'], 'Vfalta_carga': data['vLo_c'], 'time': data['t']}
    return data_dict
