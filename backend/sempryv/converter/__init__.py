# -*- coding: utf-8 -*-
"""SemPryv FHIR backend."""


from flask import Blueprint, request

# Flask blueprint
BP: Blueprint = Blueprint("fhir", __name__)


@BP.route("streams/<stream_id>.<ext>", methods=["GET"])
# pylint: disable=unused-argument
def streams(username, stream_id, ext) -> str:
    """TODO."""
    return request.headers.get("Authorization", "NONE")
