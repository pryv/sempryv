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
    bundle["id"] = "bundle-{}{}".format(server, f"-{stream_id}" if stream_id else "")
    bundle["type"] = "collection"
    bundle["entry"] = [_observation(e, server) for e in events]
    return bundle


def _observation(event, server):
    """Create an observation out of an event."""
    observation = OrderedDict()
    observation["resourceType"] = "Observation"
    observation["status"] = "final"
    observation["code"] = _codes(event)
    observation["issued"] = datetime.datetime.now().isoformat()
    observation["effectiveDateTime"] = datetime.datetime.fromtimestamp(
        event["time"]
    ).isoformat()
    observation["identifier"] = {
        "use": "official",
        "system": "https://pryv.com",
        "value": "{}/events/{}".format(server, event["id"]),
    }
    observation["valueString"] = event["content"]
    return observation


def _codes(event):
    """Return the codes associated to an event."""
    # TODO
    return []
