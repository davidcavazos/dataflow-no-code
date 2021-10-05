#!/bin/bash

set -e

# Start the language servers.
$(cd /app/python && bash run.sh) &

if [ "${ACTION}" == "run" ]; then
    # Run the Apache Beam pipeline.
    python /app/main.py "$@"
else
    # Run the Apache Beam SDK worker launcher.
    /opt/apache/beam/boot "$@"
fi
