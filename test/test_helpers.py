# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file
import copy
import subprocess
import time
import json
import socket


class TestSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data, ip, port):
        self.sock.sendto(data, (ip, port))

    def close(self):
        self.sock.close()


class TestReceiver:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(1)

    def recv(self):
        data, addr = self.sock.recvfrom(9000)
        return data

    def close(self):
        self.sock.close()


class TestHelpers:

    @staticmethod
    def read_udp_msg(server_sock,
                     expected_output=b""):
        rx_msg = server_sock.recvfrom(1024)[0]
        print(f"received {rx_msg}")
        return expected_output in rx_msg, rx_msg

    @staticmethod
    def wait_for_action(action, message, delay=2, attempts=5):
        for i in range(attempts):
            success, msg = action()
            if not success:
                print("waiting for action..")
                if i == attempts - 1:
                    raise TimeoutError("Failed waiting for: " + message)
                time.sleep(delay)
            else:
                return msg

    @staticmethod
    def wait_for_open_comms_ports(address, port, options, attempts=5):
        return TestHelpers.wait_for_action(lambda: TestHelpers.ping_port(address, port, options),
                                           f"port {port} should be open", attempts=attempts)

    @staticmethod
    def wait_for_closed_comms_ports(address, port, options, attempts=5):
        return TestHelpers.wait_for_action(lambda: TestHelpers.ping_port(address, port, options, 1),
                                           f"port {port} should be closed", attempts=attempts)

    @staticmethod
    def ping_port(addr, port, options, expected_outcome=0):
        return (subprocess.call(f"nc -{options} {addr} {port} -w 1".split()) == expected_outcome), 0

    @staticmethod
    def control_header_dict():
        return dict(Session_Id=b'\x01\x00\x00\x00',
                    Frame_Count=b'\x01\x00\x00\x00',
                    EOF=b'\x00',
                    Padding=103*b'\x00'
                    )

    @staticmethod
    def get_valid_control_header():
        return b"".join(TestHelpers.control_header_dict().values())

    @staticmethod
    def get_invalid_control_header():
        invalid_control_header = copy.deepcopy(TestHelpers.control_header_dict())
        invalid_control_header["Frame_Count"] = b'\x00\x00\x00\x00'
        return b"".join(invalid_control_header.values())

    @staticmethod
    def read_port_config():
        with open('Emulator/config/port_config.json', 'r') as config_file:
            return json.loads(config_file.read())

    @staticmethod
    def reset_port_config_file(valid_port_config):
        with open('Emulator/config/port_config.json', 'w') as config_file:
            json.dump(valid_port_config, config_file, indent=4)
