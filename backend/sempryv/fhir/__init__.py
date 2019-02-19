# -*- coding: utf-8 -*-
"""SemPryv FHIR backend."""

import json
import requests

from flask import Blueprint

from sempryv.fhir.exportation import fhir_export
from sempryv.fhir.importation import fhir_import


# Flask blueprint
BP: Blueprint = Blueprint("fhir", __name__)

BP.add_url_rule("/events", "fhir_export", fhir_export, methods=["GET"])
BP.add_url_rule("/events/<stream_id>", "fhir_import", fhir_import, methods=["POST"])
