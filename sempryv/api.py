# -*- coding: utf-8 -*-
"""Semantic API endpoints."""

from flask import Blueprint, jsonify, request
from sempryv.services import bioportal

# Flask blueprint
BP = Blueprint('sempryv', __name__)


@BP.route('search', methods=['GET'])
def search():
    """Search a semantic ontology."""
    term = request.args.get('term')
    result = bioportal.search(term)
    return jsonify(result['collection'])
