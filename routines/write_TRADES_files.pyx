import os
import numpy as np


def write_TRADES_files(input_dict, directory, planets_list):

    os.system('rm -r ./' + directory)
    os.system('mkdir -p ./' + directory + '/')
    os.system('cp ' + input_dict['Settings']['code_dir'] + 'files_repo/*.* ./' + directory + '/')

    fileout = open('./' + directory + '/obsRV.dat', 'w')

    fileout.write('# BJD_TDB RVobs eRVobs RVsetID\n')
    for b_file in input_dict['Integrator']['BJD'][:]:
        fileout.write('{0:f} 0.00 1.00 1 \n'.format(b_file))

    fileout.close()

    fileout = open('./' + directory + '/arg.in', 'w')
    #### writing TRADES files
    fileout.write('progtype = 2 \n')
    fileout.write('nboot = 0 \n')
    fileout.write('bootstrap_scaling = T \n')
    fileout.write('tepoch = {0:f} \n'.format(input_dict['Integrator']['Tref']))
    fileout.write('tstart = {0:f} \n'.format(input_dict['Integrator']['Tref']+input_dict['Integrator']['BJD_range'][0]))
    fileout.write('tint = {0:f} \n'.format(input_dict['Integrator']['BJD_range'][1]-input_dict['Integrator']['BJD_range'][0]))
    fileout.write('step = 1.e-3 \n')
    fileout.write('wrttime = 0.020835 \n')
    fileout.write('NB = {0:d} \n'.format(np.size(planets_list)+1))
    fileout.write('idtra = 1 \n')
    fileout.write('durcheck = 0 \n')
    fileout.write('tol_int = 1.e-13 \n')
    fileout.write('wrtorb = 0 \n')
    fileout.write('wrtconst = 0 \n')
    fileout.write('wrtel = 1 \n')
    fileout.write('rvcheck = 1 \n')
    fileout.write('idpert = 3 \n')
    fileout.write('lmon = 0 \n')
    fileout.write('weight_chi_square = 1. \n')
    fileout.write('secondary_parameters = 0 \n')
    fileout.close()

    fileout = open('./' + directory + '/bodies.lst', 'w')
    fileout.write('star.dat 0 0          #filename Mass Radius [1=to fit, 0=fixed]\n')
    for key in planets_list:
        fileout.write(key+'.dat 1 0 1 1 1 1 0 0   #filename Mass Radius Period eccentricity Arg.ofPericenter MeanAnomaly inclination Long.ofNodes \n')
    fileout.close()

    fileout = open('./' + directory + '/star.dat', 'w')
    fileout.write('{0:f} # Mstar [Msun] \n'.format(input_dict['Star']['M']))
    fileout.write('{0:f} # Rstar [Rsun] \n'.format(input_dict['Star']['R']))
    fileout.close()

    for key in planets_list:
        planet = input_dict['Planets'][key]
        fileout = open('./' + directory + '/'+ key +'.dat', 'w')
        fileout.write('{0:f} {1:f} {2:f} ss # [Mjup]\n'.format(planet['M_jup'], planet['M_jup']*0.80, planet['M_jup']*1.20))
        fileout.write('{0:f} {1:f} {2:f} ss # Radius of Planet [Rjup]\n'.format(planet['R_jup'], planet['R_jup']*0.80, planet['R_jup']*1.20))
        fileout.write('{0:f} {1:f} {2:f} rn # Period [day]\n'.format(planet['P'], planet['P']*0.80,planet['P']*1.20))
        fileout.write('999.   0. 0.   rn  # semi major axis [AU]\n')
        fileout.write('{0:f}  0. 1.   rn  # eccentricity\n'.format(planet['e']))
        fileout.write('{0:f}  0. 360. rn  # argument of the pericenter [deg]\n'.format(planet['o']*(180/np.pi)))
        fileout.write('{0:f}  0. 360. rn  # mean anomaly [deg]\n'.format(planet['mA']*(180.0/np.pi)))
        fileout.write('9.e8   0. 0.   rn  # time of pericenter passage [JD]\n')
        fileout.write('{0:f}  0. 180. rn  # orbit inclination [deg]\n'.format(planet['i']))
        fileout.write('0.     0. 0.   rn  # longitude of the ascending node [deg]\n')
        fileout.close()
