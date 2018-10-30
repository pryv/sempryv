# -*- coding: utf-8 -*-
"""SemPryv semantic backend."""

import os
from flask import Flask
from flask_cors import CORS


from sempryv import semantic, converter

# Load `.env` file
if not os.environ.get("SEMPRYV_PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()

# Setup Flask
APP = Flask(__name__, subdomain_matching=True)
APP.config["SERVER_NAME"] = os.environ["SERVER_NAME"]
CORS(APP)

# Register blueprints
APP.register_blueprint(semantic.BP, url_prefix="/semantic", subdomain=None)
APP.register_blueprint(converter.BP, url_prefix="/", subdomain="<username>")
