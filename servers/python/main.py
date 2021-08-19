# Static file.

import importlib
import logging
import os

import flask

app = flask.Flask(__name__)


@app.route("/<function>", methods=["POST"])
def call(function):
    request = flask.request.get_json()
    element = request["x"]
    args = request.get("args", {})
    try:
        module = importlib.import_module(f"functions.{function}")
        f = module.__dict__[function]
        return {"ok": f(element, **args)}
    except Exception as e:
        logging.error(e, stack_info=True)
        return {"error": f"{type(e).__name__}: {e}"}


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PYTHON_SERVER_PORT", 42000)),
    )
