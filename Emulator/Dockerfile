FROM python:3.8-slim-buster

RUN pip3 install pysisl

COPY rootfs_template /
COPY openapi/ /usr/src/app/openapi/
COPY verify_config.py /usr/src/app/verify_config.py
COPY verify_bitmap.py /usr/src/app/verify_bitmap.py
COPY emulator.py /usr/src/app/emulator.py
COPY config/diode_type.json /usr/src/app/config/diode_type.json

CMD ["python", "-u", "/usr/src/app/emulator.py"]
