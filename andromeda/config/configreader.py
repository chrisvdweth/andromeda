import os
import yaml


class ConfigReader:

    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, conf_file_name):
        f = open(conf_file_name)
        # use safe_load instead load
        self.data = yaml.safe_load(f)
        f.close()




if __name__ == '__main__':

    print ConfigReader.CONFIG_DIR
    cr = ConfigReader('/home/christian/google-drive/work/development/pycharm-projects/andromeda/andromeda/config/textpreprocessor.yaml')


    print cr.data
