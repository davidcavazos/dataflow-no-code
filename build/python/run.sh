#!/bin/bash

set -e

source env/bin/activate

gunicorn --threads=8 --timeout=0 --bind=localhost:42000 main:app