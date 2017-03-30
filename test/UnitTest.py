# from pymodbus3.constants import Endian
# from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus3.payload import BinaryPayloadDecoder
# import time
# import numpy as np
#
# NUMBER_OF_REGS = 2
# client = ModbusClient('203.59.95.40', port=502)
# client.connect()
# for _ in range(5):
#         rr1 = client.read_holding_registers(40070, NUMBER_OF_REGS, unit=1)
#         decoder = BinaryPayloadDecoder.from_registers(rr1.registers, endian=Endian.Big).decode_32bit_float()
#         # print(bin(rr1.registers[0]), bin(rr1.registers[1]))
#         print(decoder)

from pymongo import MongoClient
import json


with open('../configs/device.json') as json_data_file:
    data = json.load(json_data_file)

def get_db():
    client = MongoClient('localost:27017', connect=False, serverSelectionTimeoutMS=1)
    client.server_info()
    # db = client.example
    return 1


def add_country(db):
    db.device.insert(data)


def get_country(db):
    return db.device.find_one()


if __name__ == "__main__":
    db = get_db()
    # add_country(db)
    # print(get_country(db))