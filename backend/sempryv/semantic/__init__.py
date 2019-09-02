# -*- coding: utf-8 -*-
"""Semantic API endpoints."""

from flask import Blueprint, jsonify, request
from sempryv.semantic import providers, suggestion
import json, requests

# Flask blueprint
BP: Blueprint = Blueprint("api", __name__)


@BP.route("search", methods=["GET"])
def search() -> str:
    """Search a semantic ontology."""
    term = request.args.get("term")
    results = providers.search(term)
    return jsonify([r.serializable() for r in results])


@BP.route("suggest", methods=["GET"])
def suggest() -> str:
    """Suggest semantic ontologies."""
    kind = request.args.get("kind")
    path = request.args.get("path")
    results = suggestion.suggest(kind, path)
    return jsonify([r.serializable() for r in results])


@BP.route("create_annotation_mappings_for_user", methods=["POST"])
def create_annotation_mappings_for_user() -> str:
    data = json.loads(request.data)
    uname = data['uname']
    token = data['token']
    response = json.loads(requests.get(url="https://{}.pryv.me/streams".format(uname), params={"auth": token}).text)
    streams = response['streams']
    suggestion.create_annotation_mappings(streams)
    return ''
