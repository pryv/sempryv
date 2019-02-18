# -*- coding: utf-8 -*-
"""SemPryv FHIR backend."""


from collections import OrderedDict
import json
import datetime

import requests
from flask import Blueprint, Response, request, jsonify

# Flask blueprint
BP: Blueprint = Blueprint("fhir", __name__)


@BP.route("events")
def streams_route(server):
    """Route for exporting and converting streams."""
    headers = {}
    token = request.headers.get("Authorization", None)
    if token:
        headers["Authorization"] = token
    if "token" in request.args:
        headers["Authorization"] = request.args["token"]
    structure = _get_streams_structure(server, headers)
    events = _get_events(server, headers, request.args)
    if isinstance(events, Response):
        return events
    content = _bundle(events, structure, server)
    return jsonify(content)


def _get_streams_structure(server, headers):
    """Get streams structure associated with a request."""
    response = requests.get("https://{}/streams".format(server), headers=headers)
    if response.status_code != 200:
        return Response(
            response.content, status=response.status_code, mimetype="text/plain"
        )
    raw_streams = json.loads(response.content)["streams"]
    flat_streams = _flaten_streams_structure(raw_streams)
    return {v["id"]: v for v in flat_streams}


def _flaten_streams_structure(structure):
    """Flatten the streams structure."""
    streams = list()
    for stream in structure:
        streams.append(stream)
        if "children" in stream:
            streams += _flaten_streams_structure(stream["children"])
    return streams


def _get_events(server, headers, params):
    """Get events associated with a request parameters."""
    response = requests.get(
        "https://{}/events".format(server), headers=headers, params=params
    )
    if response.status_code != 200:
        return Response(
            response.content, status=response.status_code, mimetype="text/plain"
        )
    events = json.loads(response.content)["events"]
    return events


def _bundle(events, structure, server):
    """Create the bundle for the given stream ID."""
    bundle = OrderedDict()
    bundle["resourceType"] = "Bundle"
    bundle["type"] = "collection"
    bundle["entry"] = [_observation(e, structure, server) for e in events]
    return bundle


def _observation(event, structure, server):
    """Create an observation out of an event."""
    observation = OrderedDict()
    observation["resourceType"] = "Observation"
    observation["status"] = "final"
    observation["code"] = dict()
    observation["code"]["coding"] = _codes(event, structure)
    observation["issued"] = datetime.datetime.fromtimestamp(
        event["modified"]
    ).isoformat()
    observation["effectiveDateTime"] = datetime.datetime.fromtimestamp(
        event["time"]
    ).isoformat()
    observation["identifier"] = {
        "use": "official",
        "system": "https://pryv.com",
        "value": "{}/events/{}".format(server, event["id"]),
    }
    key, value = _encode_value(event)
    observation[key] = value
    return observation


def _encode_value(event):
    """Encode a Pryv content in the related FHIR format."""
    # Load the Pryv's "flat.json" file as dict
    with open("flat.json", "r") as file_pointer:
        structure = json.load(file_pointer)
    # Get the event type
    event_type = event["type"]
    # Look for event type in the structure
    flat_type = structure["types"].get(event_type, None)
    # If not existing, just skip the rest and return as String
    if not flat_type:
        return "valueString", event["content"]
    # Get the associated value type
    value_type = flat_type.get("type", None)
    # Return value encoded regarding its type
    if value_type == "number":
        value = {"value": event["content"], "unit": event_type}
        return "valueQuantity", value
    # If the value is a string, return it as such
    if isinstance(event["content"], str):
        return "valueString", event["content"]
    # Otherwise assume it's an object
    return "valueObject", event["content"]


def _codes(event, structure):
    """Return the codes associated to an event."""
    # List to store resulting codes
    coding = list()
    # Terminology
    etype = event["type"]
    namespace = "sempryv"
    key_codes = namespace + ":codes"
    key_rec = namespace + ":recursive"
    # Codes associated to the event
    if (
        "clientData" in event
        and key_codes in event["clientData"]
        and etype in event["clientData"][key_codes]
    ):
        coding += event["clientData"][key_codes][etype]
    # Codes associated with direct parent
    parent_id = event["streamId"]
    parent = structure[parent_id]
    if (
        "clientData" in parent
        and key_codes in parent["clientData"]
        and etype in parent["clientData"][key_codes]
    ):
        coding += parent["clientData"][key_codes][etype]
    # Codes associated to the hierarchy
    parent_id = structure[parent_id].get("parentId", None)
    while parent_id:
        parent = structure[parent_id]
        if (
            "clientData" in parent
            and key_rec in parent["clientData"]
            and parent["clientData"][key_rec]
            and key_codes in parent["clientData"]
            and etype in parent["clientData"][key_codes]
        ):
            coding += parent["clientData"][key_codes][etype]
        parent_id = parent.get("parentId", None)
    # Remove system_name from codes
    for code in coding:
        if "system_name" in code:
            del code["system_name"]
    return coding
