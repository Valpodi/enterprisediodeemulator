#!/usr/bin/bash
set -eux

BUILDIMAGE=$(docker build -q -f src/test/Dockerfile .)

docker run -v /var/run/docker.sock:/var/run/docker.sock \
        -v "$(pwd)":"$(pwd)" \
        "$BUILDIMAGE" \
        /bin/bash -c "pushd $(pwd) && ./scripts/runIntegrationTests.sh"
