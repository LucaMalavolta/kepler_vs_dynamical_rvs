import numpy as np
from scipy.optimize import leastsq
import routines.kepler_exo as kp

def phase_calc(p, t_obs, period, e, omega):
    t_mod = kp.kepler_Tcent_T0P(period, p, e, omega)
    return t_obs-t_mod


def compute_phase(input_dict):
    for key, key_val in input_dict['Planets'].items():
        planet = input_dict['Planets'][key]
        planet['T0'] = planet['T0'] % planet['P']
        planet['f'] = 0.0
        if planet['T0'] != 0.0:
            p0 = 0.000
            plsq = leastsq(phase_calc, p0, args=(planet['T0'], planet['P'], planet['e'], planet['o']))
            planet['f'] = plsq[0][0]
            if planet['f'] < 0.00:
                planet['f'] += 2*np.pi
        planet['K'] = kp.kepler_K1(input_dict['Star']['M'], planet['M_sun'], planet['P'], planet['i'], planet['e'])
        planet['mA'] = planet['f'] - planet['o']


    return input_dict
