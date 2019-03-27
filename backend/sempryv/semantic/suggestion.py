# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""

import json
import re

from sempryv.semantic.providers.bioportal import look


def suggest(kind, path):
    """Suggest semantic codes based on a kind and a path."""
    rules = _suggest_rules(kind, path)
    ml = _suggest_ml(kind, path)
    return rules + ml


def _suggest_rules(kind, path):
    """Suggest semantic codes based on rules."""
    rules, codes = _load_rules()
    return _find_matching_codes(kind, path, rules, codes)


def _suggest_ml(_kind, _path):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    return []


def _find_matching_codes(kind, path, rules, codes):
    """Find the codes from the rules that are matching path and kind."""
    matchings = []
    for rule in rules.values():
        if "pryv:pathExpression" in rule and re.match(
            rule["pryv:pathExpression"], path
        ):
            matchings += rule["pryv:mapping"]
    results = []
    for matching in matchings:
        rule = rules[matching]
        if rule["skos:notation"] == kind:
            for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                if matchtype in rule:
                    results.append(codes[rule[matchtype]])
    return results


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
                    codes[code_str] = code
        # If it is a path entry:
        elif "pryv:mapping" in entry:
            rules[entry["@id"]] = entry
    return rules, codes


def _parse_code(code_str):
    """Return the code object of a given text code input."""
    ontology, code = code_str.split(":", maxsplit=1)
    ontology = {"snomed-ct": "SNOMEDCT", "loinc": "LOINC"}[ontology]
    print(ontology)
    print(code)
    val = look(ontology, code)
    if val:
        print(val.serializable())
    return val
