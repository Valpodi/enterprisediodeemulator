# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

class ConfigSchema:
    @staticmethod
    def get_schema():
        return {
            "properties": {
                "egress": ConfigSchema._interface(),
                "ingress": ConfigSchema._interface(),
                "routingTable": ConfigSchema._route_table(),
            },
            "required": ["egress", "ingress", "routingTable"]
        }

    @staticmethod
    def _interface():
        return {
            "type": "object",
            "properties": {
                "useDHCP": {
                    "type": "boolean"
                },
                "ping": {
                    "type": "boolean"
                },
                "mtu": {
                    "type": "integer",
                    "minimum": 576,
                    "maximum": 9000
                },
                "ethernetPorts": ConfigSchema._ethernet_ports()
            },
            "required": ["useDHCP", "ping", "mtu"],
            "if": {"properties": {"useDHCP": {"const": True}}, "required": ["useDHCP"]},
            "then": {"required": ["ping", "useDHCP", "mtu", "ethernetPorts"]},
            "else": {"required": ["ping", "useDHCP", "mtu"]}}

    @staticmethod
    def _ethernet_ports():
        return {
            "type": "array",
            "items": ConfigSchema._adapter(),
            "minItems": 2,
            "maxItems": 2
        }

    @staticmethod
    def _adapter():
        return {
            "type": "object",
            "properties": {
                "ip": {"type": "string", "format": "ipv4"},
                "nm": {"type": "string", "format": "ipv4"},
                "gw": {"type": "string", "format": "ipv4"},
                "ntp": {"type": "string", "format": "ipv4"},
                "log": {"type": "string", "format": "ipv4"}},
            "required": ["ip", "nm"]
        }

    @staticmethod
    def _route_table():
        return {
            "type": "array",
            "items": ConfigSchema._route(),
            "minItems": 1,
            "maxItems": 1024,
            "additionalItems": False
        }

    @staticmethod
    def _route():
        return {
            "type": "object",
            "properties": {
                "ingressPort": {"type": "integer"},
                "egressIpAddress": {"type": "string"},
                "egressSrcPort": {"type": "integer"},
                "egressDestPort": {"type": "integer"}},
            "required": ["ingressPort", "egressIpAddress", "egressSrcPort", "egressDestPort"]
        }
