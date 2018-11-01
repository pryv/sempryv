#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for running SemPryv semantic backend."""

import os

import ptvsd
from sempryv import APP


def main():
    """Entry point for running the SemPryv semantic backend."""
    # Debug is enabled by default, can be disabled by environment variable
    debug = not os.environ.get("NO_DEBUG", False)
    if debug:
        # Workaround for the werkzeug reloader removing the current directory from
        # the path. It's nasty, but it works! Inspired by:
        # https://github.com/mitsuhiko/flask/issues/1246
        os.environ["PYTHONPATH"] = os.getcwd()
        # Enable PTVSD in werkzeug watched processes only
        if "WERKZEUG_RUN_MAIN" in os.environ:
            ptvsd.enable_attach()
    # Run the Flask app
    APP.run(host="0.0.0.0", port=8000, debug=debug)


if __name__ == "__main__":
    main()
