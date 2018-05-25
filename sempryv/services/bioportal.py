# -*- coding: utf-8 -*-
"""Wrapper for the Bioportal API."""

import os
from typing import Any, Dict
from urllib.parse import quote

import requests

BIOPORTAL_API_URL = "http://data.bioontology.org"


def auth() -> Dict:
    """Return the authorization headers for accessing the Bioportal API."""
    token = "apikey token={}"
    return {'Authorization': token.format(os.environ.get('BIOPORTAL_API_KEY'))}


def search(term: str, **parameters: Any) -> Dict:
    """Wrapper for searching a term in the Bioportal API."""
    # Create the base search URL
    search_url = "{}/search?q={}".format(BIOPORTAL_API_URL, quote(term))
    # Append all extra parameters to the search URL
    for k, v in parameters.items():
        # If it is a list, separated values by a comma
        if isinstance(v, list):
            value = ",".join(v)
        # Otherwise use the string representation
        else:
            value = str(v)
        # Append the parameter and its value to the search URL
        search_url += "&{}={}".format(quote(k), quote(value))
    # Do the request
    req = requests.get(search_url, headers={**auth()})
    # Return the result as a dictionary
    return req.json()
