import datetime
import json
import math
import re
import subprocess as sp
import time
from binascii import unhexlify
from multiprocessing import Queue
from typing import List

import serial
from loguru import logger
from typing_extensions import Literal

from homesolar.utils import bluetooth

BYTE_ORDER = Literal["little", "big"]


class Parameter:
    def __init__(self, field: str, start_byte: int, stop_byte: int, byte_order: BYTE_ORDER = "big",
                 signed: bool = False, precision: float = 1.0):
        self.field = field
        self.start_byte = start_byte
        self.stop_byte = stop_byte
        self.byte_order = byte_order
        self.signed = signed
        self.precision = precision

    def get_value(self, reading_data):
        data = reading_data[self.start_byte: self.stop_byte]
        value = int.from_bytes(data[self.start_byte: self.stop_byte], byteorder=self.byte_order,
                               signed=self.signed) * self.precision
        if self.precision < 1:
            value = round(value, math.ceil(math.log(1 / self.precision, 10)))

        return value

    def get_bits(self, reading_data):
        string_bytes = reading_data[self.start_byte: self.stop_byte]

        bytes_list = []
        for i in range(len(string_bytes)):
            bytes_list.append(string_bytes[i:i + 1])

        bits = []
        for byte in bytes_list:
            for i in range(8):
                bits.append((ord(byte) >> i) & 1)
        return bits


class BluetoothClient:
    def __init__(self, address: str, baudrate: int = 9600, parity: str = serial.PARITY_NONE,
                 stopbits: int = serial.STOPBITS_ONE, bytesize: int = serial.EIGHTBITS, params: List[Parameter] = None,
                 request_code: str = "", read_size: int = 0, read_period: int = 5):

        self.address = address
        self.baudrate = baudrate
        self.parity = parity
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.params = params
        self.request_code = request_code
        self.read_size = read_size
        self.read_period = read_period

        self._verification = None
        self._calculated_data = None

        self.connection = serial.Serial()
        self.connect()

    @property
    def verification(self):
        return self._verification

    @verification.setter
    def verification(self, func):
        self._verification = func

    @property
    def calculated_data(self):
        return self._calculated_data

    @calculated_data.setter
    def calculated_data(self, func):
        self._calculated_data = func

    def set_params(self, params: list):
        self.params = params

    def set_request_code(self, request_code: str):
        self.request_code = request_code

    def set_read_size(self, read_size: int):
        self.read_size = read_size

    def set_read_period(self, read_period: int):
        self.read_period = read_period

    def set_verification(self, verification: dict):
        self.verification = verification

    def connect(self):
        if not self.is_connected():
            while self.rfcomm_port() == -1:
                if not self.bind_rfcomm():
                    logger.warning(
                        "Cannot bind Bluetooth Device to a RFComm Address. Please make sure that the device is already paired")
                    break

            self.connection = serial.Serial(
                port=f"dev/rfcomm{self.rfcomm_port()}",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize)

            if not self.connection.isOpen():
                self.connection.open()

    def disconnect(self):
        if self.connection.isOpen():
            self.connection.close()

        if not self.release_rfcomm():
            logger.warning(
                "Cannot release Bluetooth Device from the RFComm Address. Might want to manually verify")

    def rfcomm_port(self):
        stdoutdata = sp.getoutput("sudo rfcomm")
        pattern = re.compile(r"rfcomm(\d+): (\S+)")

        # Split the output into lines and search for the target MAC address
        for line in stdoutdata.split('\n'):
            match = pattern.search(line)
            if match:
                port, mac_address = match.groups()
                if mac_address == self.address:
                    return port

        return -1

    def bind_rfcomm(self):
        for port_number in range(0, 30):
            stdoutdata = sp.getoutput(f"sudo rfcomm")
            if self.address in stdoutdata:
                return True
            stdoutdata = sp.getoutput(f"sudo rfcomm bind dev/rfcomm{port_number} {self.address}")
            if "Can't create device" not in stdoutdata.split():
                return True
        return False

    def release_rfcomm(self):
        if self.rfcomm_port() != -1:
            stdoutdata = sp.getoutput(f"sudo rfcomm release dev/rfcomm{self.rfcomm_port()}")

            if "Can't release device" not in stdoutdata.split():
                return True
        return False

    def is_connected(self):
        stdoutdata = sp.getoutput("hcitool con")

        if self.address in stdoutdata.split():
            return True
        return False

    def run(self, task_queue: Queue):
        try:
            if self.read_size == 0 or self.params is None:
                raise Exception("Bluetooth read_size is 0, please make sure to setup the device correctly")

            while True:
                if not self.is_connected():
                    self.connect()

                if not self.connection.isOpen():
                    self.connection.open()
                else:
                    try:
                        if self.request_code != "":
                            self.connection.write(unhexlify(self.request_code))

                        read_data = self.connection.read(self.read_size)

                        fields = {}
                        verified = True
                        for param in self.params:
                            fields[param.field] = param.get_value(read_data)

                            if self.calculated_data is not None:
                                self.calculated_data(param, read_data, fields)

                            if self.verification is not None:
                                if not self.verification(param, read_data):
                                    verified = False
                                    self.connection.close()
                                    time.sleep(1)
                                    break

                        if verified:
                            data = {
                                "name": "Antw33-BMS",
                                "payload": json.dumps(fields),
                                'time': datetime.datetime.now().timestamp()
                            }
                            logger.debug(f"Incoming Sensor Data [{data['name']}]")
                            task = {
                                "name": "write_sensor_data",
                                "data": data
                            }
                            task_queue.put(task)
                            time.sleep(5)

                    except Exception as e:
                        logger.warning(f"Something failing during bluetooth communication, [{e}]")

        except Exception as e:
            logger.exception(f"Something went wrong when dealing with bluetooth connection, [{e}]")
        finally:
            self.disconnect()


def initialize(main_task_queue: Queue):
    params = [
        Parameter("Voltage", 4, 6, signed=True, precision=0.1),
        Parameter("Current", 70, 74, signed=True, precision=0.1),
        Parameter("Power", 111, 115, signed=True),
        Parameter("Capacity", 75, 79, signed=False, precision=0.000001),
        Parameter("ChargeStatus", 103, 104),
        Parameter("DischargeStatus", 104, 105),
        Parameter("BalanceStatus", 105, 106),
        Parameter("BalanceCells", 133, 136),
        Parameter("Temp1", 91, 93),
        Parameter("Temp2", 93, 95),
        Parameter("Temp3", 95, 97),
        Parameter("Temp4", 97, 99),
        Parameter("Temp5", 99, 101),
        Parameter("Temp6", 101, 103),
        Parameter("MinCell", 118, 119),
        Parameter("MaxCell", 115, 116),
        Parameter("MinVolt", 119, 121, signed=False, precision=0.001),
        Parameter("MaxVolt", 116, 118, signed=False, precision=0.001),
        Parameter("AvgVolt", 121, 123, precision=0.001),
        Parameter("Cell1", 6, 8, signed=False, precision=0.001),
        Parameter("Cell2", 8, 10, signed=False, precision=0.001),
        Parameter("Cell3", 10, 12, signed=False, precision=0.001),
        Parameter("Cell4", 12, 14, signed=False, precision=0.001),
        Parameter("Cell5", 14, 16, signed=False, precision=0.001),
        Parameter("Cell6", 16, 18, signed=False, precision=0.001),
        Parameter("Cell7", 18, 20, signed=False, precision=0.001),
        Parameter("Cell8", 20, 22, signed=False, precision=0.001),
        Parameter("Cell9", 22, 24, signed=False, precision=0.001),
        Parameter("Cell10", 24, 26, signed=False, precision=0.001),
        Parameter("Cell11", 26, 28, signed=False, precision=0.001),
        Parameter("Cell12", 28, 30, signed=False, precision=0.001),
        Parameter("Cell13", 30, 32, signed=False, precision=0.001),
        Parameter("Cell14", 32, 34, signed=False, precision=0.001),
        Parameter("Cell15", 34, 36, signed=False, precision=0.001),
        Parameter("Cell16", 36, 38, signed=False, precision=0.001),
        Parameter("Cell17", 38, 40, signed=False, precision=0.001),
        Parameter("Cell18", 40, 42, signed=False, precision=0.001),
        Parameter("Cell19", 42, 44, signed=False, precision=0.001),
        Parameter("Cell20", 44, 46, signed=False, precision=0.001),
        Parameter("Cell21", 46, 48, signed=False, precision=0.001),
        Parameter("Cell22", 48, 50, signed=False, precision=0.001),
        Parameter("Cell23", 50, 52, signed=False, precision=0.001),
        Parameter("Cell24", 52, 54, signed=False, precision=0.001)
    ]

    ant_bms = BluetoothClient("AA:BB:CC:91:23:45")
    ant_bms.set_params(params)
    ant_bms.set_read_size(140)
    ant_bms.set_request_code("DBDB00000000")

    def verification(param: Parameter, reading_data):
        if param.field == "AvgVolt":
            if param.get_value(reading_data) == 0:
                return False
        return True

    def calculated_data(param: Parameter, reading_data, fields: dict):
        if param.field == 'BalanceCells':
            for index, bal in enumerate(param.get_bits(reading_data)):
                fields[f"Bal{index}"] = bal

        if param.field == 'AvgVolt':
            fields['SoC'] = bluetooth.ManualSoC().get_soc(param.get_value(reading_data))

    ant_bms.verification = verification
    ant_bms.calculated_data = calculated_data
    ant_bms.run(main_task_queue)
    # try:
    #     ser = serial.Serial(
    #         port=config.homesolar_config['BLUETOOTH']['port'],
    #         baudrate=9600,
    #         parity=serial.PARITY_NONE,
    #         stopbits=serial.STOPBITS_ONE,
    #         bytesize=serial.EIGHTBITS)
    #
    #     try:
    #         ser.open()
    #         time.sleep(1)
    #     except Exception as e:
    #         ser.close()
    #         ser.open()
    #         logger.warning(f"Something went wrong when trying to open Bluetooth as a Serial Connection [{e}]")
    #
    #     first_boot = True
    #     while True:
    #         try:
    #             ser.write(unhexlify(config.homesolar_config['BLUETOOTH']['request_code']))
    #             if first_boot:
    #                 time.sleep(1)
    #                 first_boot = False
    #
    #             antw33 = ser.read(140)
    #
    #             voltage = 0
    #             fields = {}
    #             for data in params:
    #                 fields[data.field] = data.value
    #
    #                 if data.field == 'AvgVolt':
    #                     voltage = data.value
    #
    #                 if data.field == 'BalanceCells':
    #                     for index, bal in enumerate(data.get_bits()):
    #                         fields[f"Bal{index}"] = bal
    #
    #                 if data.field == 'AvgVolt':
    #                     fields['SoC'] = bluetooth.ManualSoC().get_soc(data.value)
    #
    #             if voltage == 0:
    #                 ser.close()
    #                 time.sleep(1)
    #                 ser.open()
    #                 time.sleep(1)
    #
    #             data = {
    #                 "name": "Antw33-BMS",
    #                 "payload": json.dumps(fields),
    #                 'time': datetime.datetime.now().timestamp()
    #             }
    #             logger.debug(f"Incoming Sensor Data [{data['name']}]")
    #             task = {
    #                 "name": "write_sensor_data",
    #                 "data": data
    #             }
    #             main_task_queue.put(task)
    #             time.sleep(5)
    #         except:
    #             ser.close()
    #             time.sleep(1)
    #             ser.open()
    #             time.sleep(1)
    #
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     try:
    #         ser.close()
    #     except Exception as e:
    #         logger.warning(f"Something went wrong when trying to close Bluetooth as Serial Connection [{e}]")
