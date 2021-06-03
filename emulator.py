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


async def start_proxy(bind, port, remote_host, remote_port):
    loop = asyncio.get_event_loop()
    return await loop.create_datagram_endpoint(
        lambda: ProxyEndpoint((remote_host, remote_port)), local_addr=(bind, port))


class Emulator:
    def run(self, port_map):
        loop = asyncio.get_event_loop()
        ports = []
        for i in range(len(port_map)):
            port = port_map[i].split(":")[0]
            ports.append(port)
        if (int(max(ports)) - int(min(ports)) + 1) > 1024:
            raise ValueError(f"Ingress portspan must be 1024 or smaller. Not {int(max(ports)) - int(min(ports)) + 1}")
        for i in range(len(port_map)):
            mapping = port_map[i].split(":")
            print(f"Mapping input on {mapping[0]} to {mapping[1]}:{mapping[2]}")
            coroutine = start_proxy("0.0.0.0", mapping[0], mapping[1], mapping[2])
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
    port_config_path = parser.parse_args().portConfig or "/usr/src/app/portConfig.yaml"
    with open(port_config_path) as file:
        yaml_map = yaml.load(file, Loader=yaml.FullLoader)["routingTable"]
    Emulator().run(yaml_map)
