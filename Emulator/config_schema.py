

class ConfigSchema:
    @staticmethod
    def get_schema():
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
                }
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
