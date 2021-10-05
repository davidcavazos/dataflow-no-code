FROM python:3.8-slim

WORKDIR /app

COPY . ./

RUN bash python/setup.sh \
    && pip install --no-cache-dir apache-beam[gcp]==2.32.0 \
    && pip check

COPY --from=apache/beam_python3.8_sdk:2.32.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "bash", "/app/entrypoint.sh" ]
