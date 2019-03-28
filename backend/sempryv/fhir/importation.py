# -*- coding: utf-8 -*-
"""FHIR import."""

import json
import datetime

from flask import Response, request

from sempryv.fhir import pryv


def fhir_import(server, stream_id):
    """Route for importing FHIR events."""
    # Auth checking
    headers = {}
    token = request.headers.get("Authorization", None)
    if token:
        headers["Authorization"] = token
    if "auth" in request.args:
        headers["Authorization"] = request.args["auth"]
    structure = pryv.get_streams_structure(server, headers)
    if isinstance(structure, Response):
        return structure

    # FHIR formatting checking
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

    # Semantic codes preparation
    try:
        codes = _prepare_codes(server, headers, stream_id, fhir)
    except ValueError:
        return Response(
            "Semantic codes not consistant or already existing",
            status=400,
            mimetype="text/plain",
        )

    # Finally import data
    try:
        events = [_to_event(entry, stream_id) for entry in fhir["entry"]]
        _store_event(server, headers, events)
        _store_codes(server, headers, stream_id, codes)
    except RuntimeError:
        return Response("Error while tryint to import the events", 400)
    return Response("OK", 200)


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


def _store_event(server, headers, events):
    """Store events into Pryv."""
    batch = list()
    for event in events:
        batch.append({"method": "events.create", "params": event})
    pryv.batch_call(server, headers, batch)


def _prepare_codes(server, headers, stream_id, fhir):
    """Prepare semantic codes to be stored."""
    # Get existing codes
    stream = pryv.get_stream(server, headers, stream_id)
    oldcodes = {}
    if stream and "clientData" in stream and "sempryv:codes" in stream["clientData"]:
        oldcodes = stream["clientData"]["sempryv:codes"]
    # Get new codes
    newcodes = {}
    for entry in fhir["entry"]:
        kind = _decode_value(entry)[0]
        if kind in newcodes:
            continue
        if "code" in entry and "coding" in entry["code"]:
            coding = entry["code"]["coding"]
            for code in coding:
                code["system_name"] = {
                    "http://snomed.info/sct": "SNOMEDCT",
                    "http://loinc.org": "LOINC",
                }.get(code["system"], "Unknown")
            newcodes[kind] = coding
    # Check for overlapping:
    for newcode in newcodes:
        if newcode in oldcodes:
            raise ValueError
    codes = {**newcodes, **oldcodes}
    return codes


def _store_codes(server, headers, stream_id, codes):
    """Store semantic codes in the stream."""
    stream = pryv.get_stream(server, headers, stream_id)
    client_data = {}
    if stream and "clientData" in stream:
        client_data = stream["clientData"]
    client_data["sempryv:codes"] = codes
    update = {"clientData": client_data}
    pryv.update_stream(server, headers, stream_id, update)
