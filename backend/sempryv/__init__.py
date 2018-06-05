# -*- coding: utf-8 -*-
"""SemPryv semantic backend."""

from flask import Flask

from dotenv import load_dotenv
from sempryv import api

# Load `.env` file
load_dotenv()

# Setup Flask
APP = Flask(__name__)
APP.register_blueprint(api.BP, url_prefix='/api')
