#!/usr/bin/env bash
# temporary container, completely deleted when exited
docker run --rm -it \
--entrypoint bash \
--mount type=bind,source="$(pwd)",target=/code,readonly \
--env-file=.env \
ks-tha
