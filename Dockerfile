FROM python:3.8-slim-buster

COPY src/Emulator/rootfs_template /
COPY src/Emulator/emulator.py /usr/src/app/emulator.py

RUN pip3 install pysisl

CMD ["python", "-u", "/usr/src/app/emulator.py"]
