import numpy as np
import os

def get_P_min(input_dict):
    P_list = []
    for key, key_val in input_dict['Planets'].items():
        P_list.extend([input_dict['Planets'][key]['P']])
    return np.amin(P_list)


def get_planets_list(input_dict):
    planets_list = []
    P_list = []
    N_ind = 2
    for key, key_val in input_dict['Planets'].items():
        planets_list.extend([key])
        P_list.extend([input_dict['Planets'][key]['P']])
        N_ind += 1
    planet_sorted = np.argsort(P_list)

    input_dict['Integrator']['planets_list'] = np.asarray(planets_list)[planet_sorted]
    return input_dict


def add_trades_index(input_dict):
    trades_index = 2
    for key in input_dict['Integrator']['planets_list']:
        input_dict['Planets'][key]['trades_index'] = trades_index
        trades_index += 1
    return input_dict


def clean_directory(input_dict):
    os.system('rm -r ./trades')
    os.system('rm -r ./*.p')
    os.system('rm -r ./*.source')
