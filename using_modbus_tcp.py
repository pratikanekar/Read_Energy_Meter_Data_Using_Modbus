from time import sleep
import pymodbus.client.sync_diag
# from datetime import datetime, time
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from loguru import logger

# following variable is used to find received val is little endian or big endian
order = [['little', 'little', Endian.Little, Endian.Little], ['little', 'big', Endian.Little, Endian.Big],
         ['big', 'little', Endian.Big, Endian.Little], ['big', 'big', Endian.Big, Endian.Big]]

# def current_time():
#     today = datetime.now().isoformat()
#     return today

"""this following function is used to read energy meter data using modbusTCPclient"""
def read_mod_data_using_pyModTCPClient(IPAddress, mod_port):
    try:
        client = pymodbus.client.sync_diag.ModbusTcpClient(host=IPAddress, port=mod_port)  #it is used for connecting using ip address and port
        client.connect()
        sleep(1)
        decode_type = "int" #it is hard coded decode_type will be int or float
        size_bits = 32  #it is hard coded size_bits will be 16 or 32
        read_register = client.read_input_registers(address=0, count=2, unit=1)  #it is used for reading input registers
        mod_read_list = read_register.registers  #it is used to store input register values
        logger.info(f"Connected Registers {mod_read_list}")
        decoded = []
        for orders in order:
            decoder = BinaryPayloadDecoder.fromRegisters(mod_read_list, byteorder=orders[2], wordorder=orders[3])  #it is used for to find values are little endian or big endian
            try:
                receive_val = None
                bits_size = size_bits
                if decode_type == "int":
                    if bits_size == 16:
                        receive_val = decoder.decode_16bit_int()  #here receive actual value
                    elif bits_size == 32:
                        receive_val = decoder.decode_32bit_int()
                final_dict = {}
                final_dict.update({"word_order": orders[1], "byte_order": orders[0], "value": receive_val})
                decoded.append(final_dict)
            except Exception:
                continue
            logger.info(f"Receive Data {final_dict}")
        # client.close()
    except ValueError:
        logger.error(f"Error with host or port")
    except KeyboardInterrupt:
        logger.error(f"Found KeyBoard Interrupt,so EXIT Code")

