FROM python:3.8-slim-buster

COPY rootfs_template /
COPY emulator.py /usr/src/app/emulator.py

RUN pip3 install pysisl

CMD ["python", "-u", "/usr/src/app/emulator.py"]
