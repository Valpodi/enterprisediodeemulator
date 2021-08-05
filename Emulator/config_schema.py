

class ConfigSchema:
    @staticmethod
    def get_schema():
        ethernet_ports = {
            "type": "array",
            "items": {"type": "object"},
            "minItems": 2,
            "maxItems": 2
        }

        interface = {
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
                "ethernetPorts": ethernet_ports
            },
            "required": ["useDHCP", "ping", "mtu"]
        }

        return {
            "properties": {
                "egress": interface,
                "ingress": interface,
                "routingTable": {
                    "type": "array"
                },
            },
            "required": ["egress", "ingress", "routingTable"]
        }
