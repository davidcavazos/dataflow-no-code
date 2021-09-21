#!/bin/bash

set -e

cd python

python -m venv env
source env/bin/activate

pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt
pip check