from routines.input_parser import *
from routines.write_TRADES_files import *
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
from scipy import stats

input_dict = pickle_parser("_step_01.p")

input_dict['Planets_Original'] = input_dict['Planets']

print('planet, slope, intercept, r_value, p_value, std_err')
for key in input_dict['Integrator']['planets_list']:
    file_transits = input_dict['Integrator']['output']['system'] + '1_0_NB' + \
          repr(input_dict['Planets'][key]['trades_index']) + '_tra.dat'
    data_0 = np.genfromtxt(file_transits, usecols=(0,1))

    ind = np.where(data_0[:,0]> input_dict['Integrator']['Tref'])[0][0]
    T0_0 = data_0[ind:, 0] + data_0[ind:, 1]
    n_transit = np.arange(0,np.size(T0_0),1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(n_transit,T0_0)
    TTV = T0_0 - (slope*n_transit + intercept)

    print(key, slope, intercept, r_value, p_value, std_err)
    if np.size(data_0) > 5:
        input_dict['Planets'][key]['T'] = intercept
        input_dict['Planets'][key]['P'] = slope


    plt.rc('text', usetex=True)
    fig = plt.figure(figsize=(12, 12))
    plt.xlabel('N transit')
    plt.ylabel('O-C [m]')

    plt.plot(n_transit, TTV*24*60)
    plt.scatter(n_transit, TTV*24*60)
    plt.savefig(input_dict['Settings']['output_rad'] + '_TTV_planet_' + key + '.pdf', bbox_inches='tight', dpi=300)

    plt.close(fig)

print()

bash_script = open('./'+ input_dict['Settings']['output_rad'] + '_exec_trades_step_02.source', 'w')
bash_script.write('export PWD_NOW=$PWD\n')

for key in input_dict['Integrator']['planets_list']:

    input_dict['Integrator']['output'][key] = input_dict['Integrator']['output']['system'] + '/planet_' + key + '/'

    write_TRADES_files(input_dict,
                       input_dict['Integrator']['output'][key],
                       [key])
    bash_script.write('cd ' + input_dict['Integrator']['output'][key] + ' && ' +
                      input_dict['Settings']['trades_command'] + ' > trades_exec.log \n')
    bash_script.write('cd $PWD_NOW\n')

bash_script.write('mkdir -p ' + input_dict['GLS_directory']+ '\n')
bash_script.write('python ' + input_dict['Settings']['code_dir'] + 'step_03.py '
                  + input_dict['Settings']['Input_yaml']+'\n')
bash_script.write('cd ' + input_dict['GLS_directory']+ '\n')
bash_script.write(input_dict['Settings']['GLS_command'] + '\n')
bash_script.write('cd $PWD_NOW\n')

pickle_saver(input_dict, "_step_02.p")
print('Now execute:   source ./'+ input_dict['Settings']['output_rad'] + '_exec_trades_step_02.source ')
