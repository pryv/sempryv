# -*- coding: utf-8 -*-
"""FHIR import."""

import json

from flask import Response, request

from sempryv.fhir.pryv import get_events, get_streams_structure


def fhir_import(server, stream_id):
    """Route for importing FHIR events."""
    # Auth checking
    headers = {}
    token = request.headers.get("Authorization", None)
    if token:
        headers["Authorization"] = token
    if "auth" in request.args:
        headers["Authorization"] = request.args["auth"]
    structure = get_streams_structure(server, headers)
    if isinstance(structure, Response):
        return structure

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
    try:
        _import(server, headers, stream_id, fhir)
    except RuntimeError:
        return Response("Error while tryint to import the events", 400)
    return Response("OK", 200)
