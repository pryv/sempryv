# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""


def suggest(kind, stream_id):
    """Suggest semantic codes based on a kind and a stream_id."""
    rules = _suggest_rules(kind, stream_id)
    ml = _suggest_ml(kind, stream_id)
    return rules + ml


def _suggest_rules(kind, stream_id):
    """Suggest semantic codes based on rules."""
    return []


def _suggest_ml(_kind, _stream_id):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    return []
