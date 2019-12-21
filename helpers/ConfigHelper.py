import configparser
import os


class ConfigHelper:
    def __init__(self):
        """
        Initialize the Config Helper
        This Class contains Config Functions

        """

        self.config = configparser.ConfigParser()
        self.config_conf = os.path.join(os.getcwd(), 'config', 'config_prod.conf')
        self.config.read(self.config_conf)

        print('{} - Initialized'.format(__name__))

    def get_config(self):
        """
        Return the config object

        :return: Config object
        """

        return self.config

    def save_config(self):
        """
        Save the config back to the config file

        """

        with open(self.config_conf, 'w') as configfile:
            self.config.write(configfile)
