#!/bin/bash

export PYTHON_SERVER=localhost:42000

# Start the Python server.
$(cd python && ./env/bin/gunicorn --threads=8 --timeout=0 --bind=$PYTHON_SERVER server:app) &

# Launch the Apache Beam boot file.
# python main.py hello=http://$PYTHON_SERVER/hello
/opt/apache/beam/boot hello=http://$PYTHON_SERVER/hello "$@"
