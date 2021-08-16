# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import argparse
import asyncio
import pysisl
from pysisl import parser_error
from verify_bitmap import VerifyBitmap


class ProxyEndpoint(asyncio.DatagramProtocol):

    def __init__(self, remote_address):
        self.remote_address = remote_address
        self.remotes = {}
        self.diode_type_filepath = "/usr/src/app/config/diode_type.json"
        self.diode_type = self.get_diode_type()
        super().__init__()

    def get_diode_type(self):
        with open(self.diode_type_filepath) as diode_type_file:
            return json.load(diode_type_file)["f2 type"]

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
            return
        loop = asyncio.get_event_loop()
        if self.diode_type == "import":
            coroutine = loop.create_datagram_endpoint(
                lambda: ImportDestinationEndpoint(self, addr, data), remote_addr=self.remote_address)
        else:
            coroutine = loop.create_datagram_endpoint(
                lambda: DestinationEndpoint(self, addr, data), remote_addr=self.remote_address)
        asyncio.ensure_future(coroutine)


class DestinationEndpoint(asyncio.DatagramProtocol):

    def __init__(self, proxy, addr, data):
        self.proxy = proxy
        self.addr = addr
        self.data = data
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.data)


class ImportDestinationEndpoint(asyncio.DatagramProtocol):

    def __init__(self, proxy, addr, data):
        self.proxy = proxy
        self.addr = addr
        self.data = data

        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        if not self.check_for_valid_control_header(self.data):
            print("Control header invalid, frame dropped")
            return
        header, data = self.extract_control_header(self.data)

        if not VerifyBitmap.validate(data):
            data = self.wrap_non_sisl_data(data)

        if self.check_for_wrapped_data(data):
            to_send = header + data
        else:
            to_send = header + (48 * b"\x00") + data
        self.transport.sendto(to_send)

    @staticmethod
    def check_for_valid_control_header(data):
        if not len(data) >= 112:
            print(f"Failed on size: {len(data)} \n {data}")
            return False
        if data[8] > 1:
            print(f"Failed on EOF: {data[8]}")
            return False
        if not int.from_bytes(data[3:7], byteorder='little') >= 1:
            print("Failed on frame count")
            return False
        if not data[9:112] == (103 * b"\x00"):
            print(f"Failed on padding: {len(data[9:112])}")
            return False
        return True

    def extract_control_header(self, data):
        return data[:64], data[112:]

    def check_for_wrapped_data(self, data):
        return data[:4] == b"\xd1\xdf\x5f\xff"

    def wrap_non_sisl_data(self, data):
        data_string = data.decode('utf-8')
        try:
            pysisl.loads(data_string)
        except parser_error.ParserError:
            data = pysisl.wraps(data)
        return self.encode_to_bytes(data)

    def encode_to_bytes(self, data):
        if type(data) == str:
            data = bytes(data, 'utf-8')
        return data


async def start_proxy(bind, port, remote_host, remote_port):
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: ProxyEndpoint((remote_host, remote_port)), local_addr=(bind, port))


class Emulator:
    def run(self, diode_config):
        loop = asyncio.get_event_loop()
        for route in diode_config["routingTable"]:
            print(f"Mapping input on {route['ingressPort']} to {route['egressIpAddress']}:{route['egressDestPort']}")
            coroutine = start_proxy("0.0.0.0", route['ingressPort'], route['egressIpAddress'], route['egressDestPort'])
            transport, _ = loop.run_until_complete(coroutine)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        transport.close()
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portConfig', help="path to portConfig file")
    port_config_path = parser.parse_args().portConfig or "/usr/src/app/config/port_config.json"
    with open(port_config_path) as file:
        json_map = json.load(file)
    Emulator().run(json_map)
