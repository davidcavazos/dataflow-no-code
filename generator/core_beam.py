# Static file.

import logging
import requests
from typing import Any, Dict, Iterable

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

logging.getLogger().setLevel(logging.INFO)

# Aliases for core Beam transforms and other utilities.
Create = beam.Create
Map = beam.Map
FlatMap = beam.FlatMap

AsIter = beam.pvalue.AsIter
AsList = beam.pvalue.AsList
AsSingleton = beam.pvalue.AsSingleton
AsDict = beam.pvalue.AsDict


@beam.ptransform_fn
def Call(pcollection, url: str, **args: Any):
    def json_encodable(name, value):
        # https://docs.python.org/3/library/json.html#json.JSONEncoder
        if isinstance(value, (dict, list, tuple, str, int, float, bool, type(None))):
            return value
        elif isinstance(value, Iterable):
            # Handle `beam.pvalue.AsIter` side inputs.
            # As a very temporary workaround, simply convert the iterable into a list.
            # TODO: find a way to "paginate" elements for PCollections that don't fit into memory.
            return list(value)
        raise TypeError(
            f"Type {type(value)} in argument {name} from function {url} is not supported"
        )

    def call(element, **args: Dict[str, Any]):
        request_args = {
            name: json_encodable(name, value) for name, value in args.items()
        }
        response = requests.post(url, json={"x": element, "args": request_args})
        result = response.json()
        if "error" in result:
            raise RuntimeError(
                "I got the following error during the call: "
                f"{url} (element={element}, args={args})\n"
                f"{result['error']}"
            )
        return result["ok"]

    return pcollection | f"Call {url}" >> beam.Map(call, **args)


@beam.ptransform_fn
def Log(pcollection, level=logging.INFO):
    def log(element):
        logging.log(level, element)
        return element

    return pcollection | f"Log {logging.getLevelName(level)}" >> beam.Map(log)


def identity(x):
    return x


def Pipeline(beam_args, **beam_options: Any):
    return beam.Pipeline(options=PipelineOptions(beam_args, **beam_options))
