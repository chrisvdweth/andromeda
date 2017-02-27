import os
import yaml


class ConfigReader:

    CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, conf_file_name):
        f = open(os.path.expanduser(conf_file_name))
        # use safe_load instead load
        self.data = yaml.safe_load(f)
        f.close()



