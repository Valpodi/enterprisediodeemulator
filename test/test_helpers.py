import subprocess
import time
import json


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
    def wait_for_open_comms_ports(address, port, options):
        return TestHelpers.wait_for_action(lambda: TestHelpers.ping_port(address, port, options),
                                           f"port {port} should be open")

    @staticmethod
    def ping_port(addr, port, options):
        return (subprocess.call(f"nc -{options} {addr} {port} -w 1".split()) == 0), 0

    @staticmethod
    def get_example_control_header():
        return b'\xd6\xb7\x79\x3e\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    @staticmethod
    def get_bad_example_control_header():
        return b'\xd6\xb7\x79\x3e\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    @staticmethod
    def save_port_config():
        with open('Emulator/config/portConfig.json', 'r') as config_file:
            return json.loads(config_file.read())

    @staticmethod
    def reset_port_config_file(valid_port_config):
        with open('Emulator/config/portConfig.json', 'w') as config_file:
            json.dump(valid_port_config, config_file, indent=4)
