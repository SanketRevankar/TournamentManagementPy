import configparser
import os


class ConfigHelper:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_conf = os.path.join(os.getcwd(), 'config', 'config.conf')
        self.config.read(self.config_conf)

        print('{} - Initialized'.format(__name__))

    def get_config(self):
        return self.config

    def save_config(self):
        with open(self.config_conf, 'w') as configfile:
            self.config.write(configfile)
