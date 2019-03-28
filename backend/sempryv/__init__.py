# -*- coding: utf-8 -*-
# pylint: disable=wrong-import-position
# flake8: noqa
"""SemPryv semantic backend."""

import os

# Load `.env` file first to avoid missing env variable on import
if not os.environ.get("SEMPRYV_PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()

from flask import Flask
from flask_cors import CORS

from sempryv import semantic, fhir

# Setup Flask
APP = Flask(__name__, subdomain_matching=True)
CORS(APP)

# Register blueprints
APP.register_blueprint(semantic.BP, url_prefix="/semantic")
APP.register_blueprint(fhir.BP, url_prefix="/<server>/")
