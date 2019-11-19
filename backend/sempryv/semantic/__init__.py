# -*- coding: utf-8 -*-
"""Semantic API endpoints."""

import json

from flask import Blueprint, jsonify, request

from sempryv.semantic import providers, suggestion
from semantic.providers.data_provider import SempryvDataProvider
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


@BP.route("start_sempryv_ml_component", methods=["POST"])
def start_sempryv_ml_component() -> str:
    req_data = json.loads(request.data)
    # TODO: persist new user in DB
    username = req_data['username']
    token = req_data['token']
    provider = SempryvDataProvider()
    if not provider.exists_user(username=username):
        print('Insert new user in DB')
        provider.insert_new_user(username=username, token=token)

    print('Train users model... ')
    suggestion.sempryv_ml_train()
    print('users model done ')
    return ''

