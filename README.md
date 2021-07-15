# 10G Diode Emulator
The emulator includes 2 variants of the 10G diode:
  - Basic: provides 1 way transfer
  - Import: provides 1 way transfer, any data that is not valid SISL or a bitmap will be wrapped and given a Cloaked Dagger header
### Requirements:
In order to launch the emulator you will need to install docker & python3, and pip install json.

You will need to build emulator docker image, which uses the public python:3.8-slim-buster image
and needs to pip install json.

To enable such installs using repository mirrors the `rootfs_template` folder is copied onto the root folder.

For example, to add a PyPI mirror, place your pip.conf file here: `rootfs_template/etc/pip.conf`.

To match the Oakdoor Enterprise Diode, you will need to reconfigure the mtu for the docker daemon as follows:
In `/etc/docker/daemon.json` add:

`{"mtu": 9000}`

You will also have to set the mtu to 9000 on the host's 10G network interface(s):

`ifconfig [INTERFACE_NAME] mtu 9000 up`


### Configuring the port-destination mapping:
Inside the config folder you will find a file named [portConfig.json](config/portConfig.json). In this file, in the routingTable block,
are the mappings of the source ports to destination IP addresses.

    "routingTable": [{
            "ingressPort": {{ Ingress Port }},
            "egressIpAddress": {{ Egress Destination IP Address }},
            "egressSrcPort": {{ Egress Source Port }},
            "egressDestPort": {{ Egress Destination Port }}
        }]

Please note that while the emulator can use DNS name resolution for the destination IP address,
the diode will only support IP addresses.

### Running the emulator
Build the emulator docker container with:

`docker build -f Dockerfile -t emulator .`

#### Basic Diode ####
Run the python launch script:

`python3 launchEmulator.py -p [PATH_TO_CONFIG_FILE]`

#### Import Diode ####
Run the python launch script:

`python3 launchEmulator.py -p [PATH_TO_CONFIG_FILE] --importDiode`


You can test the emulator by listening on a destination ip address and sending udp at the mapped source port:

`echo -n "test" | nc -4u localhost [MAPPED_PORT]`

or

`echo -n "test" > /dev/udp/localhost/[MAPPED_PORT]`