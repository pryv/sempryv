# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""

import json
import re

from sempryv.semantic.providers.bioportal import look


# class SuggestionsProvider(object):
#     def __init__(self):

def suggest(kind, path):
    """Suggest semantic codes based on a kind and a path."""
    rules = _rules_suggestions(kind, path)
    ml = _ml_suggestions(kind, path)
    return rules + ml


def _rules_suggestions(kind, path):
    """Suggest semantic codes based on rules."""
    return _calculate_rule_suggestions(kind, path, RULES, CODES)


def _ml_suggestions(_kind, _path):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future

    return []


def _calculate_rule_suggestions(kind, path, rules, codes):
    """Find the codes from the rules that are matching path and kind."""
    matchings = []
    for rule in rules.values():
        if "pryv:pathExpression" in rule and re.fullmatch(
                rule["pryv:pathExpression"].lower(), path.lower()
        ):
            matchings += rule["pryv:mapping"]
    results = []
    for matching in matchings:
        rule = rules[matching]
        for notation in rule["skos:notation"]:
            if notation.lower() == kind.lower():
                for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                    if matchtype in rule and rule[matchtype] in codes:
                        results.append(codes[rule[matchtype]])
    return results


def create_annotation_mappings(streams):
    stream_annotations = {}
    for stream in streams:
        name=stream['name']
        annotation_map[name]={}
        children = stream['children']
        sempryv_codes = stream['clientData']['sempryv:codes']
        for type in sempryv_codes:
            stream_annotations[name][type] = sempryv_codes[type]
            pass
        x=1

    return stream_annotations


def _load_rules():
    """Load the rules."""
    print('===================== LOAD RULES =====================\n')
    rules = {}
    codes = {}
    # Open the file
    with open("rules.json", "r") as file_pointer:
        entries = json.load(file_pointer)["@graph"]
    # For each entry
    for entry in entries:
        # If it is a type entry, load its codes
        if "@type" in entry and entry["@type"] == "skos:Concept":
            rules[entry["@id"]] = entry
            for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                if matchtype not in entry:
                    continue
                code_str = entry[matchtype]
                code = _parse_code(code_str)
                if code:
                    codes[code_str] = code
        # If it is a path entry just copy it
        elif "pryv:mapping" in entry:
            rules[entry["@id"]] = entry
    return rules, codes


def _parse_code(code_str):
    """Return the code object of a given text code input."""
    ontology, code = code_str.split(":", maxsplit=1)
    ontology = {"snomed-ct": "SNOMEDCT", "loinc": "LOINC"}[ontology]
    return look(ontology, code)


RULES, CODES = _load_rules()
