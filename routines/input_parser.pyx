import yaml
import argparse
import pickle


def yaml_parser():

    parser = argparse.ArgumentParser(prog='xx.py', description='yy')
    parser.add_argument('config_file', type=str, nargs=1, help='config file')
    args = parser.parse_args()
    file_conf = args.config_file[0]

    stream = file(file_conf, 'r')
    config_out = yaml.load(stream)
    config_out['Settings']['Input_yaml'] = file_conf
    return config_out

def pickle_saver(input_dict, append_name):
    pickle.dump(input_dict, open(input_dict['Settings']['output_rad']+append_name, "wb"))


def pickle_parser(append_name):
    parser = argparse.ArgumentParser(prog='xx.py', description='yy')
    parser.add_argument('config_file', type=str, nargs=1, help='config file')
    args = parser.parse_args()
    file_conf = args.config_file[0]

    stream = file(file_conf, 'r')
    conf_temp = yaml.load(stream)

    return pickle.load(open(conf_temp['Settings']['output_rad']+append_name, "rb"))

