from routines.input_parser import *
import numpy as np
import matplotlib.pyplot as plt

input_dict = pickle_parser("_step_02.p")

data_system = np.genfromtxt(input_dict['Integrator']['output']['system']+'/1_0_simRV.dat',
                            usecols=(0, 3), skip_header=1)


input_dict['Results'] = {'BJD': data_system[:, 0], 'RV_dyn': data_system[:, 1]}

data_planet = np.zeros(np.size(data_system, axis=0), dtype=np.double)

for key in input_dict['Integrator']['planets_list']:
    data_planet += np.genfromtxt(input_dict['Integrator']['output'][key]+'/1_0_simRV.dat',
                                usecols=3, skip_header=1)
input_dict['Results']['RV_kep'] = data_planet

input_dict['Results']['RV_dif'] = data_system[:, 1]-data_planet
input_dict['Results']['RV_std'] = np.std(input_dict['Results']['RV_dif'])

fileout = open(input_dict['GLS_directory']+ '/RV_diff.dat', 'w')
fileout.write('descriptor bjd rv,+- \n')
for bb, rr in zip(input_dict['Results']['BJD'], input_dict['Results']['RV_dif']):
    fileout.write('{0:f} {1:f} 1.00 \n'.format(bb, rr))
fileout.close()

plt.rc('text', usetex=True)
fig = plt.figure(figsize=(12, 12))
plt.xlabel('BJD-2450000 [d]')
plt.ylabel('RV$_{Dyn}$-RV$_{Kep}$ [ms$^{-1}$]')

plt.plot(input_dict['Results']['BJD'],input_dict['Results']['RV_dif'])
plt.savefig(input_dict['Settings']['output_rad'] + '_Dyn_vs_Kep.pdf', bbox_inches='tight', dpi=300)
plt.close(fig)

pickle_saver(input_dict, "_output.p")
