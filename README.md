# Beam/Dataflow no-code proof of concept

This is a proof of concept on making a no-code / low-code experience for Apache Beam and Dataflow.

_tl;dr_: We grab a declarative (JSON/YAML) representation of an Apache Beam pipeline, and we generate a Dockerfile with everything needed to run the pipeline.

## Overview

The JSON/YAML representation (low-code) can be easily generated via a graphical UI interface (no-code).

### Core functions

All the core Apache Beam transforms would be supported out-of-the-box in the JSON/YAML representation.
This includes element-wise transforms, aggregation transforms, windowing, triggers, as well as I/O transforms.
This also includes a transform to call used-defined functions, described below.

### User-defined functions

Custom functions are supported in one or more languages.

For this prototype, we support custom functions in Python only, but any language could easily be supported by creating a local web server.

All the language servers must have a well defined input and output format:

* Each function processes exactly one element.
* Additional arguments can be optionally added.
* Requests and responses are JSON encoded.
* The response is either a value or an error.

When a custom function is used in a pipeline, it uses a custom `DoFn` to call the custom function.
Each custom function has a URL through which it's accessible (local or remote).
Each element is encoded into JSON, passed to the custom function server, and the response is JSON decoded.

### Pipeline file

The JSON/YAML pipeline file would contain all the necessary information to build the image, except for the user-defined functions' code itself.
It would include:

* All the steps in the pipeline.
  * User-defined function calls need the language, function name, and any additional arguments.
* A list of requirements for each language used in user-defined functions.

## Generation workflow

The user files would be:

* The JSON/YAML pipeline file.
* All the user-defined functions in their respective language, with one (public) function per file.

The language server files could be provided in Beam released images, one image per language.

The Dockerfile would be a [multi-stage build](https://docs.docker.com/develop/develop-images/multistage-build) like this:

1. Pipeline builder stage
    1. Copy or install the pipeline generator and any other requirements.
    1. Copy the JSON/YAML pipeline file from the local filesystem.
    1. Run the generator, which would create the following files:
        * The `main` pipeline file, with all user-defined functions registered.
        * A `run` script, which would start all the language servers and then run the Beam worker boot file.
1. For each language used in user-defined functions, create a builder stage
    1. These could base from different base images if needed
    1. Install any required build tools, if any
    1. Copy the user-defined function files from the local filesystem.
    1. Copy the language server files from the language server image.
    1. Compile any source files for languages that require it.
    1. Package the language server with all the user-defiend functions
1. Main image
    1. Update/install any packages needed, including:
        * Tools/programs needed to run the pipeline itself.
        * Tools/programs needed to run each language server used.
    1. Copy the Beam worker boot files from the Beam image.
    1. Copy the `main` pipeline file(s) from the pipeline builder stage.
    1. Copy the `run` script from the pipeline builder stage.
    1. For each language builder stage, copy the packaged language servers.
    1. Set the entry point to the `run` script.

## Generating the pipeline

```sh
# TODO
```

## Building the container image

```sh
export PROJECT=$(gcloud config get-value project)
export IMAGE="gcr.io/$PROJECT/dataflow-no-code"

gcloud builds submit -t $IMAGE build/
```

## Running locally

```sh
docker run --rm -e ENTRYPOINT=python $IMAGE main.py
```

## Running in Dataflow

```sh
export BUCKET="your-cloud-storage-bucket"
export REGION="us-central1"

# TODO: make this into a `gcloud builds submit --config run.yaml` for service account credentials.
docker run --rm -e ENTRYPOINT=python $IMAGE main.py \
    --runner "DataflowRunner" \
    --project "$PROJECT" \
    --region "$REGION" \
    --temp_location "gs://$BUCKET/temp" \
    --sdk_container_image "$IMAGE"
```
