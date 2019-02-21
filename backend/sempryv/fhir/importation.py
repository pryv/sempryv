# -*- coding: utf-8 -*-
"""FHIR import."""

import json
import datetime

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


def _import(server, headers, stream_id, fhir):
    """Import the given FHIR bundle into the stream_id."""
    events = [_to_event(entry, stream_id) for entry in fhir["entry"]]
    _store_event(server, headers, events)


def _to_event(observation, stream_id):
    """Create a Pryv event out of a FHIR observation."""
    event = dict()
    event["streamId"] = stream_id
    event["modified"] = datetime.datetime.fromisoformat(
        observation["issued"]
    ).timestamp()
    event["time"] = datetime.datetime.fromisoformat(
        observation["effectiveDateTime"]
    ).timestamp()
    typ, content = _decode_value(observation)
    event["type"] = typ
    event["content"] = content
    return event


def _decode_value(observation):
    """Decode a FHIR observation in the related Pryv format."""
    if "valueString" in observation:
        return "note/txt", observation["valueString"]
    elif "valueQuantity" in observation:
        return (
            observation["valueQuantity"]["unit"],
            observation["valueQuantity"]["value"],
        )
    if "valueObject" in observation:
        return "unknown/object", observation["valueObject"]
    print(observation)


def _store_event(server, headers, events):
    """Store events into Pryv."""
    batch = list()
    for event in events:
        batch.append({"method": "events.create", "params": event})
    batch_call(server, headers, batch)
