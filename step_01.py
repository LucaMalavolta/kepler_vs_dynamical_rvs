from routines.input_parser import *
from routines.constants import *
from routines.planets import compute_phase
from routines.miscellanea import *
from routines.write_TRADES_files import *

input_dict = yaml_parser()
clean_directory(input_dict)

input_dict['Settings']['trades_command'] = input_dict['Settings']['trades_dir'] + 'bin/trades_o_int_lm_bootstrap'
input_dict['Settings']['GLS_command'] ='python ' + input_dict['Settings']['GLSmod_dir'] + 'gls_mod.py RV_diff.dat -fbeg 0.0001 -fend 0.500 -nfreq 20000 -ofile RV_diff -skipr 1 '

for key in input_dict['Planets'].iterkeys():
    planet = input_dict['Planets'][key]

    if 'R' not in planet: planet['R'] = 2.6
    if 'e' not in planet: planet['e'] = 0.00000
    if 'o' not in planet: planet['o'] = np.asarray(np.pi/2.)
    if 'i' not in planet: planet['i'] = 90.000

    planet['M_sun'] = planet['M'] / Msear
    planet['M_jup'] = planet['M'] * Mejup
    planet['R_jup'] = planet['R'] * Rejup
    planet['T0'] = planet['T'] - input_dict['Integrator']['Tref']

input_dict = compute_phase(input_dict)

P_min = get_P_min(input_dict)

input_dict['Integrator']['BJD_step'] = P_min/25.
input_dict['Integrator']['BJD0'] = np.arange(input_dict['Integrator']['BJD_range'][0],
                                             input_dict['Integrator']['BJD_range'][1],
                                             input_dict['Integrator']['BJD_step'], dtype=np.double)
input_dict['Integrator']['BJD'] = input_dict['Integrator']['BJD0']+input_dict['Integrator']['Tref']

bash_script = open('./'+ input_dict['Settings']['output_rad'] + '_exec_trades_step_01.source', 'w')
bash_script.write('export PWD_NOW=$PWD\n')

input_dict = get_planets_list(input_dict)
input_dict = add_trades_index(input_dict)

input_dict['Integrator']['output'] = {'system': './'+ input_dict['Settings']['output_rad'] + '_trades/'}
input_dict['GLS_directory'] = './'+ input_dict['Settings']['output_rad'] + '_GLS/'

write_TRADES_files(input_dict,
                   input_dict['Integrator']['output']['system'],
                   input_dict['Integrator']['planets_list'])

bash_script.write('cd ' + input_dict['Integrator']['output']['system'] + ' && ' +
                  input_dict['Settings']['trades_command'] + ' > trades_exec.log \n')
bash_script.write('cd $PWD_NOW\n')

pickle_saver(input_dict, "_step_01.p")

print
print 'Now execute:   source ./' + input_dict['Settings']['output_rad'] +  '_exec_trades_step_01.source '
