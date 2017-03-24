__author__ = "Mayukh Sarkar"
__date__ = "24th March, 2017"
'''
// TODO Documentation
'''
import sys
import os
import inspect
import json
import socket


class ConfigParse(object):

    def __init__(self, config_file='inverter.json'):
        # ######### Check for proper file name ##########
        if len(config_file.split('.')) == 2:
            config_file_name, config_file_type = config_file.split('.')
        else:
            raise NameError('Error parsing the file name')

        # ######## Check for file presence #########
        currentFile = inspect.getfile(inspect.currentframe())
        currentPath = os.path.dirname(os.path.abspath(currentFile))
        self.config_path = os.path.join(currentPath, '..', 'configs')
        if not os.path.exists(self.config_path):
            raise IOError('Can not find the config files path')

        self.tags = ['device-info',
                     'device-network',
                     'device-registers']
        self.allowed_types = ['meter', 'inverter']
        if config_file_type == 'xml':
            self._parse_xml(config_file)
        elif config_file_type == 'yml':
            self._parse_yml(config_file)
        else:
            self._parse_json(config_file)

    def _parse_json(self, config_file):
        with open(os.path.join(self.config_path, config_file)) as json_data_file:
            self._data = json.load(json_data_file)

    @property
    def data(self):
        return self._data

    def verify(self):
        for each in self.data:
            if each in self.tags:
                if each == 'device-info' and self.data[each]['type'].lower() not in self.allowed_types:
                    raise TypeError('Device type is not supported')
                elif each == 'device-network':
                    self._verify_network(self.data[each])
                elif each == 'device-registers':
                    self._verify_registers(self.data[each])
            else:
                raise KeyError('{}:Illegal tag key in config file'.format(each))

    def _verify_network(self, data):
        if data['host'] == '':
            print('No host info...Falling back to IP address')
            try:
                socket.gethostbyaddr(data['ip'])
            except socket.herror:
                raise socket.herror('Unable to access the remote device')
        else:
            print('Selecting the host address....')
            # // TODO add the fallback when the host name is given

    def _verify_registers(self, data):
        pass


    def _parse_xml(self, config_file):
        pass

    def _parse_yml(self, config_file):
        pass

class DataMap(ConfigParse):
    pass


#############################
def main(configFile):
    config1 = ConfigParse(config_file=configFile)
    config1.verify()

if __name__ == '__main__':
    main(configFile=sys.argv[1])
