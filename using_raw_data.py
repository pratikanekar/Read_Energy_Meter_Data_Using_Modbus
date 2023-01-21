import socket
from time import sleep

relay1_on = ["01050000FF008C3A", "01050001FF00DDFA", "01050002FF002DFA", "01050003FF007C3A", "01050004FF00CDFB", "01050005FF009C3B", "01050006FF006C3B", "01050007FF003DFB"]
relay2_on = ["02050000FF008C09", "02050001FF00DDC9", "02050002FF002DC9", "02050003FF007C09", "02050004FF00CDC8", "02050005FF009C08", "02050006FF006C08", "02050007FF003DC8"]
relay3_on = ["03050000FF008DD8", "03050001FF00DC18", "03050002FF002C18", "03050003FF007DD8", "03050004FF00CC19", "03050005FF009DD9", "03050006FF006DD9", "03050007FF003C19"]
relay4_on = ["04050000FF008C6F", "04050001FF00DDAF", "04050002FF002DAF", "04050003FF007C6F", "04050004FF00CDAE", "04050005FF009C6E", "04050006FF006C6E", "04050007FF003DAE"]

relay1_off = ["010500000000CDCA", "0105000100009C0A", "0105000200006C0A", "0105000300003DCA", "0105000400008C0B", "010500050000DDCB", "0105000600002DCB", "0105000700007C0B"]
relay2_off = ["020500000000CDF9", "0205000100009C39", "0205000200006C39", "0205000300003DF9", "0205000400008C38", "020500050000DDF8", "0205000600002DF8", "0205000700007C38"]
relay3_off = ["030500000000CC28", "0305000100009DE8", "0305000200006DE8", "0305000300003C28", "0305000400008DE9", "030500050000DC29", "0305000600002C29", "0305000700007DE9"]
relay4_off = ["040500000000CD9F", "0405000100009C5F", "0405000200006C5F", "0405000300003D9F", "0405000400008C5E", "040500050000DD9E", "0405000600002D9E", "0405000700007C5E"]

datas = [{"read_slave": f"01020000000879CC", "relay_on_slave": relay1_on, "relay_off_slave": relay1_off}]


IPAddress = '192.168.2.40'
port = 4196  # This is Final Port NOT 5000


def read_data():
    i = 1
    for on_data in datas:
        try:
            socket.send(bytes.fromhex(on_data.get("read_slave")))
            print(f"Send info slave{i} successfully, Now trying to receive Data")
            socket.settimeout(2)
            recv_data = socket.recv(1024).hex().upper()
            print(f"Received Data from Slave_{i}: {recv_data}")
            sleep(0.1)
            j = 1
            for on in on_data.get("relay_on_slave"):
                socket.send(bytes.fromhex(on))
                print(f"Relay_{j} On of Slave_{i}")
                recv_data_1 = socket.recv(1024).hex().upper()
                print(f"Received for Relay ON_{i}: {recv_data_1}")
                sleep(1)
                j = j+1
            if i == 4:
                i = 1
                for off_data in datas:
                    k = 1
                    for off in off_data.get("relay_off_slave"):
                        try:
                            socket.send(bytes.fromhex(off))
                            print(f"Relay_{k} Off of Slave_{i}")
                            recv_data_2 = socket.recv(1024).hex().upper()
                            print(f"Received for Relay OFF_{i}: {recv_data_2}")
                            sleep(1)
                            k = k+1

                        except Exception as e:
                            print(f"Error for slave_{i}: {e}")
                    i = i + 1
        except Exception as e:
            print(f"Error for slave_{i}: {e}")
        finally:
            i = i + 1


if __name__ == '__main__':
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("socket is open waiting for connection")
    socket.connect((IPAddress, port))
    print(f"connected successfully to {IPAddress} and port {port}")
    while True:
        try:
            read_data()
            sleep(0.1)
        except KeyboardInterrupt:
            print(f"Found KeyBoard Interrupt,so EXIT Code")
            break
