# -*- coding: utf-8 -*-
"""SemPryv FHIR backend."""


from collections import OrderedDict
import json
import datetime

import requests
from flask import Blueprint, Response, request, jsonify

# Flask blueprint
BP: Blueprint = Blueprint("fhir", __name__)


@BP.route("streams")
@BP.route("streams.<ext>")
@BP.route("streams/<stream_id>")
@BP.route("streams/<stream_id>.<ext>")
def get_streams(server, stream_id=None, ext=None):
    """TODO."""
    token = request.headers.get("Authorization", None)
    # streams = _get_streams(server, token)
    events = _get_events(
        server, token, streams=[stream_id] if stream_id else None, recursive=True
    )
    if not ext or ext.lower() == "json":
        content = events
    elif ext.lower() == "fhir":
        content = _bundle(events, server, stream_id)
    else:
        return Response(
            'File format "{}" not supported'.format(ext),
            status=400,
            mimetype="text/plain",
        )
    return jsonify(content)


def _get_streams(server, token):
    """Get streams associated with a token."""
    response = requests.get(
        "https://{}/streams".format(server), headers={"Authorization": token}
    )
    if response.status_code != 200:
        return None
    return json.loads(response.content)["streams"]


def _get_events(server, token, streams=None, limit=0, recursive=True):
    """Get events associated with a token."""
    query = f"?limit={limit}"
    if streams:
        sep = "&streams[]="
        query += sep + sep.join(streams)
    response = requests.get(
        "https://{}/events{}".format(server, query), headers={"Authorization": token}
    )
    if response.status_code != 200:
        return None
    events = json.loads(response.content)["events"]
    if not recursive:
        events = [e for e in events if e["streamId"] in streams]
    return events


def _bundle(events, server, stream_id=None):
    """Create a bundle out of an id and observations."""
    bundle = OrderedDict()
    bundle["resourceType"] = "Bundle"
    bundle["id"] = "{}/streams/{}".format(server, stream_id)
    bundle["type"] = "collection"
    bundle["entry"] = [_observation(e, server) for e in events]
    return bundle


def _observation(event, server):
    """Create an observation out of an event."""
    observation = OrderedDict()
    observation["resourceType"] = "Observation"
    observation["status"] = "final"
    observation["code"] = _codes(event)
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
    key, value = _encode_value(event, server)
    observation[key] = value
    return observation


def _encode_value(event, server):
    """Encode a value in the FHIR format."""
    # Load the Pryv's "flat.json" file as dict
    with open("flat.json", "r") as fp:
        structure = json.load(fp)
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
        value = {"value": event["content"], "unit": flat_type.get("description", None)}
        return "valueQuantity", value
    # In all other cases return only String types
    return "valueString", event["content"]


def _codes(event):
    """Return the codes associated to an event."""
    # TODO
    return []
