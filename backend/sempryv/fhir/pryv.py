# -*- coding: utf-8 -*-
"""Pryv interfacing."""

import json
import requests

from flask import Response


def get_streams_structure(server, headers):
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


def get_events(server, headers, params):
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


def batch_call(server, headers, batch):
    """Do a batch call on a server."""
    response = requests.post("https://{}/".format(server), headers=headers, json=batch)
    print(response.text)
    print(response.content)
    return response.status_code == 200
