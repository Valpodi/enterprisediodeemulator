# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import argparse
import asyncio
import os
import pysisl
from pysisl import parser_error
from verify_bitmap import VerifyBitmap
from verify_control_header import VerifyControlHeader


class ProxyEndpoint(asyncio.DatagramProtocol):

    def __init__(self, remote_address):
        self.remote_address = remote_address
        self.remotes = {}
        self.is_import_diode = self.get_diode_type()
        super().__init__()

    @staticmethod
    def get_diode_type():
        return os.environ.get("IMPORTDIODE") == "True"

    @staticmethod
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
            return
        loop = asyncio.get_event_loop()
        if self.is_import_diode:
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
        self.frame = data

        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        if not self.check_for_valid_control_header():
            print("Control header invalid, frame dropped")
            return
        header, data = self.extract_control_header()
        to_send = self._construct_payload(data, header)
        self.transport.sendto(to_send)

    def _construct_payload(self, data, header):
        if self._is_bmp(data) or self._is_sisl(data):
            to_send = header + (48 * b"\x00") + data
        else:
            wrapped_data = pysisl.wraps(data)
            to_send = header + wrapped_data
        return to_send

    @staticmethod
    def _is_bmp(data):
        return VerifyBitmap().validate(data)

    @staticmethod
    def _is_sisl(data):
        data_string = data.decode('utf-8')
        try:
            pysisl.loads(data_string)
            return True
        except parser_error.ParserError:
            return False

    def check_for_valid_control_header(self):
        return VerifyControlHeader().validate(self.frame)

    def extract_control_header(self):
        return self.frame[:64], self.frame[112:]


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
