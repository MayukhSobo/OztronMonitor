import configparser
import os
#  config = configparser.ConfigParser()
#  config.read('monitor.conf')
#  print(config)


class GlobalConfigParse(object):

    def __init__(self, config):
        if not os.path.exists(config):
            raise IOError('Can not find the config file')
        elif config.split('.')[-1].lower() != 'conf':
            raise ValueError('Illegal config file')
        self.config = configparser.ConfigParser()
        self.config.read(config)

    def verify(self):
        for each in self.config['SECURITY']:
            print(each)
gc = GlobalConfigParse('monitor.conf')
gc.verify()
