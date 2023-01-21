from using_modbus_tcp import read_mod_data_using_pyModTCPClient

IPAddress = '192.168.2.41'
mod_port = 5000 #it is default port

if __name__ == "__main__":
    read_mod_data_using_pyModTCPClient(IPAddress, mod_port)
