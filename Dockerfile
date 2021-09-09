FROM python:3.8-slim

WORKDIR /pipeline

ARG BEAM_VERSION=2.31.0

COPY python python

RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ \
    && rm -rf /var/lib/apt/lists/* \
    # Python language server.
    && python -m venv python/env \
    && python/env/bin/pip install --no-cache-dir -r python/requirements.txt \
    # Main Apache Beam pipeline setup.
    && pip install --no-cache-dir apache-beam[gcp]==${BEAM_VERSION} \
    && pip check

COPY main.py .
COPY run.sh .

COPY --from=apache/beam_python3.8_sdk:2.31.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "bash", "run.sh" ]