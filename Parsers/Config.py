__author__ = "Mayukh Sarkar"
__date__ = "24th March, 2017"

# // TODO Documentation

import sys
import os
import inspect
import json
import socket
from termcolor import colored
# import time
import Helpers
from abc import ABC, abstractmethod


class ConfigParse(ABC):
    """
    The config parser used for parsing the configuration
    of the remote device, validate the configuration, and
    store it into a local data base. The data base and other
    configurations can be loaded from the global rc files.

    The supported device configurations are JSON, XML and YML.
    The basic verifications are performed here. The DataMap class
    must inherit the configurations that are parsed from the config
    files and then store it into the database. It calls the required
    database class which performs the required operations.

    This class is an Abstract Base Class and Object of the DataMap had to
    be created.
    """

    def __init__(self, config_file='device.json'):
        # ######### Check for proper file name ##########
        self._data = None
        ConfigParse.parse(self, config_file=config_file)
        self.tags = ['device-info',
                     'device-network',
                     'device-registers']
        self.allowed_device_types = ['meter', 'inverter']
        ConfigParse.verify(self)

    @property
    def data(self):
        return self._data

    @staticmethod
    def parse(self, config_file):
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

    @staticmethod
    def verify(self):
        for each in self.data:
            if each in self.tags:
                if each == 'device-info' and self.data[each]['type'].lower() not in self.allowed_device_types:
                    raise TypeError('Device type is not supported')
                elif each == 'device-network':
                    self._verify_network(self.data[each])
                elif each == 'device-registers':
                    self._verify_registers(self.data[each])
            else:
                raise KeyError('{}:Illegal tag key in config file'.format(each))

    # ######### Low level calls ##########
    # ### Shouldn't be tampered ######
    def _verify_network(self, data):
        if data['host'] == '':
            if Helpers.__VERBOSE__:
                print(colored("[**WARNING**]", "yellow", attrs=['bold']) + " No host info...Falling back to IP address")
            # time.sleep(1)
            try:
                socket.gethostbyaddr(data['ip'])
            except socket.herror:
                raise socket.herror('Unable to access the remote device')
        else:
            print('Selecting the host address....')
            # // TODO add the fallback when the host name is given
        if Helpers.__VERBOSE__:
            print(colored("[OKAY✓]", "green", attrs=['bold']) + " Device Network Verification")
        # time.sleep(1)

    def _verify_registers(self, data):
        if Helpers.__VERBOSE__:
            print(colored("[OKAY✓]", "green", attrs=['bold']) + " Device Register Verification")
        # time.sleep(1)
        pass

    def _parse_xml(self, config_file):
        pass

    def _parse_yml(self, config_file):
        pass

    def _parse_json(self, config_file):
        with open(os.path.join(self.config_path, config_file)) as json_data_file:
            self._data = json.load(json_data_file)
        if Helpers.__VERBOSE__:
            print(colored("[OKAY✓]", "green", attrs=['bold']) + " JSON Syntax Verification")
        # time.sleep(1)
    ######################################

    @abstractmethod
    def mapIt(self):
        pass


class DataMap(ConfigParse):
    def __init__(self, config_file):
        super(self.__class__, self).__init__(config_file=config_file)

    def mapIt(self):
        pass

    if Helpers.__DEBUG__:
        def __str__(self):
            return json.dumps(self.data, indent=4, sort_keys=True)

#############################
def main(configFile):
    dm = DataMap(config_file=configFile)
    if Helpers.__DEBUG__:
        print(dm)
    # dm.mapIt()
if __name__ == '__main__':
    main(configFile=sys.argv[1])