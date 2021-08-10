FROM python:3.8-slim-buster

RUN pip3 install pysisl

COPY rootfs_template /
COPY openapi/ /usr/src/app/openapi/
COPY verify_config.py /usr/src/app/verify_config.py
COPY emulator.py /usr/src/app/emulator.py

CMD ["python", "-u", "/usr/src/app/emulator.py"]
