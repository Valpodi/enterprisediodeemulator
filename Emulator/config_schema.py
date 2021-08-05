class ConfigSchema:
    @staticmethod
    def get_schema():
        return {
            "properties": {
                "egress": ConfigSchema._interface(),
                "ingress": ConfigSchema._interface(),
                "routingTable": {
                    "type": "array"
                },
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
                    "type": "integer"
                },
                "ethernetPorts": ConfigSchema._ethernet_ports()
            },
            "required": ["useDHCP", "ping", "mtu"]
        }

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