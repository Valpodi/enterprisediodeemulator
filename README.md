# Oakdoor 10G Enterprise Diode Emulator
The emulator mimics the UDP port forwarding and frame inspection capability of the Oakdoor 10G Enterprise Diode. At present, the Basic Diode and Import Diode variants are supported by the emulator.:
  - Basic: 1 way transfer of UDP traffic with UDP port forwarding.
  - Import: 1 way transfer of UDP traffic with UDP port forwarding and packet inspection. UDP packets must meet the Enterprise Diode frame format (header + SISL/bitmap). Bitmap and SISL inspection have also been implemented by the emulator. Non conformant frames are rendered inert with the Cloaked Dagger wrapping technique.

### Requirements:
In order to launch the emulator you will need to install docker & python3, and the python json module. See section below for build and launch instructions.

To build the docker containers behind a firewall, proxy information can be added to the docker container by adding the appropriate files to the `rootfs_template` folder. For example, to add a PyPI mirror, create a custom pip.conf file and place here: `rootfs_template/etc/pip.conf`.

The Oakdoor Enterprise Diode supports an mtu up to 9000 bytes. To match the Oakdoor Enterprise Diode, you may need to reconfigure the mtu for the docker daemon as follows: 
On your host machine, in `/etc/docker/daemon.json` add:

`{"mtu": 9000}`

You will also have to set the mtu to 9000 on the host's 10G network interface(s):

`ifconfig [INTERFACE_NAME] mtu 9000 up`


### Configuring the UDP port forwarding mapping:
In [port_config.json](Emulator/config/port_config.json) the routingTable block contains the mappings of the source ports to destination IP addresses.

    "routingTable": [{
            "ingressPort": {{ Ingress Port }},
            "egressIpAddress": {{ Egress Destination IP Address }},
            "egressSrcPort": {{ Egress Source Port }},
            "egressDestPort": {{ Egress Destination Port }}
        }]

Please note that while the emulator can use DNS name resolution for the destination IP address,
the diode will only support IP addresses.

### Configuring the diode variant
By default the emulator is configured as the basic diode. 
The emulator can be configured as the import variant by using the import diode flag (`--importDiode` or `-i`) when running the management interface or emulator script.

Note that though the port config is validated when using the emulator directly for ease of use, 
but the enterprise diode itself will not validate the port config, as this is expected to be done by the management interface API.

### Building the emulator
Build the emulator and management interface docker containers with:

`./scripts/buildInterfaceAndEmulator.sh`

### Management interface
The management interface uses a REST API to interact with the diode emulator. 
The management interface server host will be localhost by default.
To launch the management interface, run the script:

`python3 Emulator/launch_management_interface.py -p [INTERFACE_PORT]`

#### Power On ####
Power on the diode emulator

`POST /api/command/diode/power/on`

Example Usage: `curl -X POST http://[INTERFACE_SERVER_HOST]:[INTERFACE_PORT]/api/command/diode/power/on`

#### Power Off ####
Power off the diode emulator

`POST /api/command/diode/power/off` 

Example Usage:`curl -X POST http://[INTERFACE_SERVER_HOST]:[INTERFACE_PORT]/api/command/diode/power/off`

#### Update Diode Config ####
Update the JSON config used by the diode for port configuration. JSON config required in the payload.

`PUT /api/config/diode`

Example Usage:`curl -H "Content-Type:application/json" -T [PATH_TO_CONFIG_FILE] http://[INTERFACE_SERVER_HOST]:[INTERFACE_PORT]/api/config/diode` 

#### Get Diode Config ####
Get the JSON config used by the diode for port configuration

`GET /api/config/diode`

Example Usage:`curl http://[INTERFACE_SERVER_HOST]:[INTERFACE_PORT]/api/config/diode`

#### Get Config Schema ####
Get the JSON schema used to validate the config file used by the diode

`GET /api/config/diode/schema` 

Example Usage:`curl http://[INTERFACE_SERVER_HOST]:[INTERFACE_PORT]/api/config/diode/schema`

### Running the emulator locally
Note: It is not advised to run the emulator directly, but rather through API calls to the management interface. 
In particular, updating the config file should be performed through the appropriate API call, so that it is validated against the config schema.  

To run the emulator on your local machine the egressIpAddress in the config file should be set to the docker bridge network gateway IP address 172.17.0.1.

See [Configuring the diode variant](#configuring-the-diode-variant) for instructions to set the diode variant.

Run the python launch script:

`python3 Emulator/launch_emulator.py -p [PATH_TO_CONFIG_FILE]`

You can test the emulator by listening on a destination ip address and sending udp at the mapped source port.

To listen:
`nc -lvu [EGRESS_IP_ADDRESS] [EGRESS_DEST_PORT]`

To send:
`echo -n "test" | nc -4u localhost [INGRESS_PORT]`

or

`echo -n "test" > /dev/udp/localhost/[INGRESS_PORT]`
