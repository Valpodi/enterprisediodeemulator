# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import json
import argparse
import os


def write_diode_type(diode_variant):
    print(os.getcwd())
    with open("Emulator/config/diode_type.json", "w") as diode_type_file:
        diode_type_file.write(json.dumps({"f2 type": diode_variant}))


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--diodeType', help="type of diode to emulate", default="basic")
diode_type = parser.parse_args().diodeType
write_diode_type(diode_type)

