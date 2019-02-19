# -*- coding: utf-8 -*-
"""SemPryv semantic backend."""

import os
from flask import Flask
from flask_cors import CORS


from sempryv import semantic, fhir

# Load `.env` file
if not os.environ.get("SEMPRYV_PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()

# Setup Flask
APP = Flask(__name__, subdomain_matching=True)
APP.config["JSON_SORT_KEYS"] = False
CORS(APP)

# Register blueprints
APP.register_blueprint(semantic.BP, url_prefix="/semantic")
APP.register_blueprint(fhir.BP, url_prefix="/<server>/")
