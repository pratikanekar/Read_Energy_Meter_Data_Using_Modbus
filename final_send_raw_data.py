import socket
from time import sleep

IPAddress = '192.168.2.40'
port = 4196  # This is Final Port NOT 5000

# following fuction is used to calculate the CRC16 for relay OFF of slaves
def find_relay_off_crc(slave_id, on_change_data):
    function_code = f"05"
    if slave_id <= 9:
        read_input_data = f"000{on_change_data}0000"
        checksum = crc16(f"0{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"0{slave_id}{function_code}{read_input_data}{checksum}"
    elif slave_id == 10:
        read_input_data = f"000{on_change_data}0000"
        checksum = crc16(f"{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"{slave_id}{function_code}{read_input_data}{checksum}"
    else:
        read_input_data = f"00{on_change_data}0000"
        checksum = crc16(f"{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"{slave_id}{function_code}{read_input_data}{checksum}"


# following fuction is used to calculate the CRC16 for relay ON of slaves
def find_relay_on_crc(slave_id, on_change_data):
    function_code = f"05"
    if slave_id <= 9:
        read_input_data = f"000{on_change_data}FF00"
        checksum = crc16(f"0{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"0{slave_id}{function_code}{read_input_data}{checksum}"
    elif slave_id == 10:
        read_input_data = f"000{on_change_data}FF00"
        checksum = crc16(f"{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"{slave_id}{function_code}{read_input_data}{checksum}"
    else:
        read_input_data = f"00{on_change_data}FF00"
        checksum = crc16(f"{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"{slave_id}{function_code}{read_input_data}{checksum}"


# following fuction is used to calculate the CRC16 for slaves
def find_slave_crc(slave_id):
    function_code = f"02"
    read_input_data = f"00000008"
    if slave_id <= 9:
        checksum = crc16(f"0{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"0{slave_id}{function_code}{read_input_data}{checksum}"
    else:
        checksum = crc16(f"{slave_id}{function_code}{read_input_data}").replace(" ", "0")
        return f"{slave_id}{function_code}{read_input_data}{checksum}"


# following function is used to calculate the CRC16 (cheksum) for modbus
def crc16(data, bits=8):
    crc = 0xFFFF
    for op, code in zip(data[0::2], data[1::2]):
        crc = crc ^ int(op+code, 16)
        for bit in range(0, bits):
            if (crc & 0x0001) == 0x0001:
                crc = ((crc >> 1) ^ 0xA001)
            else:
                crc = crc >> 1
    msb = crc >> 8
    lsb = crc & 0x00FF
    return '{:2X}{:2X}'.format(lsb, msb)


# following fuction is used to READ data on slaves
def read_slaves(send_read_salve, slave_id):
    try:
        socket.send(bytes.fromhex(send_read_salve))
        print(f"Send info slave{slave_id} successfully, Now trying to receive Data")
        socket.settimeout(2)
        recv_data = socket.recv(1024).hex().upper()
        print(f"Received Data from Slave_{slave_id}: {recv_data}")
        sleep(0.1)
    except Exception as e:
        pass


# following fuction is used to ON relay on slaves
def relay_on(send_on_relay, slave_id, on_change_data):
    try:
        socket.send(bytes.fromhex(send_on_relay))
        print(f"Relay_{on_change_data + 1} On of Slave_{slave_id}")
        socket.settimeout(2)
        recv_data = socket.recv(1024).hex().upper()
        print(f"Received for Relay ON_{on_change_data + 1}: {recv_data}")
        sleep(0.1)
    except Exception as e:
        pass


# following fuction is used to OFF relay on slaves
def relay_off(send_off_relay, slave_id, on_change_data):
    try:
        socket.send(bytes.fromhex(send_off_relay))
        print(f"Relay_{on_change_data + 1} OFF of Slave_{slave_id}")
        socket.settimeout(2)
        recv_data = socket.recv(1024).hex().upper()
        print(f"Received for Relay OFF_{on_change_data + 1}: {recv_data}")
        sleep(0.1)
    except Exception as e:
        pass


if __name__ == '__main__':
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("socket is open waiting for connection")
    socket.connect((IPAddress, port))
    print(f"connected successfully to {IPAddress} and port {port}")
    connected_slaves = 4
    relay = 8
    slave_id = 1
    while True:
        try:
            for slave_id in range(1, connected_slaves + 1):
                send_read_salve = find_slave_crc(slave_id) # calculate crc16 for slaves
                read_slaves(send_read_salve, slave_id) # it is used to read data on slaves
                for on_change_data in range(0, relay):
                    send_on_relay = find_relay_on_crc(slave_id, on_change_data) # calculate crc16 for relay on
                    relay_on(send_on_relay, slave_id, on_change_data) # it is used to on relays on slaves
                    sleep(1)
            if slave_id == 4:
                slave_id = 1
                for slave_id in range(1, connected_slaves + 1):
                    for on_change_data in range(0, relay):
                        send_off_relay = find_relay_off_crc(slave_id, on_change_data) # calculate crc16 for relay ooff
                        relay_off(send_off_relay, slave_id, on_change_data) # it is used to off relays on slaves
                        sleep(1)
                    slave_id = slave_id + 1
        except KeyboardInterrupt:
            print(f"Found KeyBoard Interrupt,so EXIT Code")
            break
        finally:
            slave_id = slave_id + 1
