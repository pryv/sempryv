# -*- coding: utf-8 -*-
"""Semantic API endpoints."""

from flask import Blueprint, jsonify, request
from sempryv.semantic import providers, suggestion

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
    stream_id = request.args.get("stream_id")
    results = suggestion.suggest(kind, stream_id)
    return jsonify([r.serializable() for r in results])
