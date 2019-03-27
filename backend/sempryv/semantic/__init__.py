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
    path = request.args.get("path")
    results = suggestion.suggest(kind, path)
    return jsonify([r.serializable() for r in results])
