# -*- coding: utf-8 -*-
"""FHIR import."""

import json

from flask import Response, request

from sempryv.fhir.pryv import _get_events, _get_streams_structure


def fhir_import(server, stream_id):
    """Route for importing FHIR events."""
    # Auth checking
    headers = {}
    token = request.headers.get("Authorization", None)
    if token:
        headers["Authorization"] = token
    if "auth" in request.args:
        headers["Authorization"] = request.args["auth"]
    structure = _get_streams_structure(server, headers)

    # FHIR format checking
    malformatted = False
    fhir = dict()
    try:
        fhir = json.loads(request.data)
    except json.JSONDecodeError:
        malformatted = True
    if "resourceType" not in fhir or fhir["resourceType"].lower() != "bundle":
        malformatted = True
    if "type" not in fhir or fhir["type"].lower() != "collection":
        malformatted = True
    if "type" not in fhir or fhir["type"].lower() != "collection":
        malformatted = True
    if malformatted:
        return Response(
            "The input format is not supported", status=400, mimetype="text/plain"
        )
    return Response(request.data, mimetype="application/json")
