#!/bin/bash

set -e

# Start the language servers.
$(cd python && bash run.sh) &

# Launch the Apache Beam boot file.
${ENTRYPOINT:-/opt/apache/beam/boot} "$@"
