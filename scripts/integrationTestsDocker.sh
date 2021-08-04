#!/usr/bin/bash
set -eux

BUILDIMAGE=$(docker build -q -f test/Dockerfile .)

docker run -v /var/run/docker.sock:/var/run/docker.sock \
        -v "$(pwd)":"$(pwd)" \
        -p 50001:50001/udp \
        -p 51024:51024/udp \
        "$BUILDIMAGE" \
        /bin/bash -c "pushd $(pwd) && ./scripts/runIntegrationTests.sh"
