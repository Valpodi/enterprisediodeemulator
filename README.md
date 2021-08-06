# Oakdoor 10G Enterprise Diode Emulator
The emulator mimics the UDP port forwarding and frame inspection capability of the Oakdoor 10G Enterprise Diode. At present, the Basic Diode and Import Diode variants are supported by the emulator.:
  - Basic: 1 way transfer of UDP traffic with UDP port forwarding.
  - Import: 1 way transfer of UDP traffic with UDP port forwarding and packet inspection. UDP packets must meet the Enterprise Diode frame format (header + SISL. Note bitmap inspection has not yet been implemented by the emulator). Non conformant frames are rendered inert with the Cloaked Dagger wrapping technique.

### Requirements:
In order to launch the emulator you will need to install docker & python3, and the python json module. See section below for build and launch instructions.

To build the docker containers behind a firewall, proxy information can be added to the docker container by adding the appropriate files to the `rootfs_template` folder. For example, to add a PyPI mirror, create a custom pip.conf file and place here: `rootfs_template/etc/pip.conf`.

The Oakdoor Enterprise Diode supports an mtu up to 9000 bytes. To match the Oakdoor Enterprise Diode, you may need to reconfigure the mtu for the docker daemon as follows: 
On your host machine, in `/etc/docker/daemon.json` add:

`{"mtu": 9000}`

You will also have to set the mtu to 9000 on the host's 10G network interface(s):

`ifconfig [INTERFACE_NAME] mtu 9000 up`


### Configuring the UDP port forwarding mapping:
Inside the config folder you will find a file named [portConfig.json](Emulator/config/portConfig.json). In this file, in the routingTable block,
are the mappings of the source ports to destination IP addresses.

    "routingTable": [{
            "ingressPort": {{ Ingress Port }},
            "egressIpAddress": {{ Egress Destination IP Address }},
            "egressSrcPort": {{ Egress Source Port }},
            "egressDestPort": {{ Egress Destination Port }}
        }]

Please note that while the emulator can use DNS name resolution for the destination IP address,
the diode will only support IP addresses.

### Building the emulator
Build the emulator and interface docker containers with:

`./scripts/buildInterfaceAndEmulator.sh`

### Management interface
The management interface uses a REST API to interact with the diode emulator. 
To launch the interface, run the script:

`python3 Emulator/launch_emulator_interface.py -p [INTERFACE_PORT]`

#### Management interface endpoints ####
The /api/command/diode/power/on and /api/command/diode/power/off endpoints can be used to control the diode emulator power.

The /api/config/diode endpoint can be used with GET and PUT requests to retrieve or update the portConfig the emulator uses. 

### Running the emulator locally
To run the emulator on your local machine the egressIpAddress in the config file should be set to the docker bridge network gateway IP address 172.17.0.1.

#### Basic Diode ####
Run the python launch script:

`python3 launch_emulator.py -p [PATH_TO_CONFIG_FILE]`

#### Import Diode ####
Run the python launch script:

`python3 launch_emulator.py -p [PATH_TO_CONFIG_FILE] --importDiode`

You can test the emulator by listening on a destination ip address and sending udp at the mapped source port.

To listen:
`nc -lvu [egressIpAddress] [egressDestPort]`

To send:
`echo -n "test" | nc -4u localhost [ingressPort]`

or

`echo -n "test" > /dev/udp/localhost/[ingressPort]`
