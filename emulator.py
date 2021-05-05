# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import yaml
import argparse
import asyncio


class ProxyEndpoint(asyncio.DatagramProtocol):

    def __init__(self, remote_address):
        self.remote_address = remote_address
        self.remotes = {}
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
            return
        loop = asyncio.get_event_loop()
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

    def datagram_received(self, data, _):
        self.proxy.transport.sendto(data, self.addr)


async def start_proxy(bind, port, remote_host, remote_port):
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: ProxyEndpoint((remote_host, remote_port)), local_addr=(bind, port))


class Emulator:
    def run(self, port_map):
        loop = asyncio.get_event_loop()
        for i in range(len(port_map)):
            print(f"Mapping input on {port_map[i]['srcPort']} to {port_map[i]['destIP']}:{port_map[i]['destPort']}")
            coroutine = start_proxy("0.0.0.0", port_map[i]['srcPort'], port_map[i]['destIP'], port_map[i]['destPort'])
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
    port_config_path = parser.parse_args().portConfig or "/portConfig.yaml"
    with open(port_config_path) as file:
        yaml_map = yaml.load(file, Loader=yaml.FullLoader)["streamToPortMap"]
    Emulator().run(yaml_map)
