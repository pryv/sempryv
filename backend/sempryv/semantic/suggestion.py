# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""

import json

from sempryv.semantic.providers.bioportal import look


def suggest(kind, stream_id):
    """Suggest semantic codes based on a kind and a stream_id."""
    rules = _suggest_rules(kind, stream_id)
    ml = _suggest_ml(kind, stream_id)
    return {**rules, **ml}


def _suggest_rules(kind, stream_id):
    """Suggest semantic codes based on rules."""
    rules, codes = _load_rules()
    print(rules)
    print(codes)
    return codes


def _suggest_ml(_kind, _stream_id):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    return {}


def _load_rules():
    """Load the rules."""
    rules = {}
    codes = {}
    # Open the file
    with open("rules.json", "r") as file_pointer:
        entries = json.load(file_pointer)["@graph"]
    # For each entry
    for entry in entries:
        # If it is a type entry:
        if "@type" in entry and entry["@type"] == "skos:Concept":
            rules[entry["@id"]] = entry
            for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                if matchtype not in entry:
                    continue
                code_str = entry[matchtype]
                code = _parse_code(code_str)
                if code:
                    codes[code] = code
        # If it is a path entry:
        elif "pryv:mapping" in entry:
            rules[entry["@id"]] = entry
    return rules, codes


def _parse_code(code_str):
    """Return the code object of a given text code input."""
    ontology, code = code_str.split(":", maxsplit=1)
    ontology = {"snomed-ct": "SNOMEDCT", "loinc": "LOINC"}[ontology]
    return look(ontology, code)
