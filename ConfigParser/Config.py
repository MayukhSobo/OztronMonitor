__author__ = "Mayukh Sarkar"
__date__ = "24th March, 2017"
'''
// TODO Documentation
'''
import sys
import os
import inspect
import json


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


    def _parse_xml(self, config_file):
        pass

    def _parse_yml(self, config_file):
        pass

class DataMap(ConfigParse):
    pass

def main(configFile):
    config1 = ConfigParse(config_file=configFile)
    # print(config1.data['device-info']['model'])
    for each in config1.data:
        print(each)

if __name__ == '__main__':
    main(configFile=sys.argv[1])
