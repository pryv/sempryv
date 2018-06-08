# -*- coding: utf-8 -*-
"""Wrapper for the Bioportal API."""

import os
from typing import Any, Dict, List
from urllib.parse import quote

import requests
from sempryv.ontologies import loinc, snomedct
from sempryv.semantic import SemanticClass

BIOPORTAL_API_URL = "http://data.bioontology.org"


def _auth() -> Dict:
    """Return the authorization headers for accessing the Bioportal API."""
    token = "apikey token={}"
    return {"Authorization": token.format(os.environ.get("BIOPORTAL_API_KEY"))}


def _search(term: str, **parameters: Any) -> Dict:
    """Wrapper for searching a term in the Bioportal API."""
    # Create the base search URL
    search_url = "{}/search?q={}".format(BIOPORTAL_API_URL, quote(term))
    # Append all extra parameters to the search URL
    for k, v in parameters.items():
        # If it is a list, separated values by a comma
        if isinstance(v, list):
            value = ",".join(v)
        # If it is a bool, put it lowercase
        elif isinstance(v, bool):
            value = str(v).lower()
        # Otherwise use the string representation
        else:
            value = str(v)
        # Append the parameter and its value to the search URL
        search_url += "&{}={}".format(quote(k), quote(value))
    # Do the request
    req = requests.get(search_url, headers={**_auth()})
    # Return the result as a dictionary
    return req.json()


def _system_from_id(uri):
    """Extract and return a semantic system from its uri."""
    parts = uri.split("/")
    if parts[-2] == "LNC":
        return loinc
    if parts[-2] == "SNOMEDCT":
        return snomedct
    raise ValueError("Unknown system")


def _to_semantic(entry):
    """Transform a bioportal entry to a semantic class."""
    result = SemanticClass(
        system=_system_from_id(entry["@id"]),
        code=entry["notation"],
        names=[entry["prefLabel"], *entry["synonym"]],
    )
    return result


def suggest(term: str) -> List[SemanticClass]:
    """Suggest semantic classes from a given term."""
    responses = _search(
        term,
        ontologies=["SNOMEDCT", "LOINC"],
        include=["notation", "prefLabel", "synonym"],
        pagesize=50,
        display_context=False,
        display_links=False,
    )
    results = [r for r in responses["collection"] if "synonym" in r]
    return [_to_semantic(v) for v in results]
