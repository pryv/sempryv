# -*- coding: utf-8 -*-
"""Semantic API endpoints."""

from flask import Blueprint, jsonify, request
from sempryv import services

# Flask blueprint
BP: Blueprint = Blueprint("sempryv", __name__)


@BP.route("search", methods=["GET"])
def search() -> str:
    """Search a semantic ontology."""
    term = request.args.get("term")
    results = services.suggest(term)
    return jsonify([r.serializable() for r in results])
