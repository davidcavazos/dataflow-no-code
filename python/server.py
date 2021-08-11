# Static file, copy from build stage with cloned repo.

import os
import logging

import flask

import functions

app = flask.Flask(__name__)


@app.route("/<function>", methods=["POST"])
def call(function):
    request = flask.request.get_json()
    element = request["x"]
    args = request.get("args", {})
    try:
        f = functions.__dict__[function]
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
