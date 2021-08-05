

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
            "items": {"type": "object"},
            "minItems": 2,
            "maxItems": 2
        }
