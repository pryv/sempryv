# -*- coding: utf-8 -*-
"""SemPryv semantic backend."""

import os
from flask import Flask

from sempryv import api

# Load `.env` file
if not os.environ.get("SEMPRYV_PRODUCTION"):
    from dotenv import load_dotenv

    load_dotenv()

# Setup Flask
APP = Flask(__name__)
APP.register_blueprint(api.BP, url_prefix="/api")
