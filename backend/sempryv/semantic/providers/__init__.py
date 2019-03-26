# -*- coding: utf-8 -*-
"""The external providers for semantic information."""

import os
from importlib import import_module


def _providers():
    """Return all the providers in the current package."""
    providers = []
    for name in os.listdir(os.path.dirname(__file__)):
        if name.endswith(".py") and name != "__init__.py":
            providers.append(_load(name[:-3]))
    return providers


def _load(module):
    """Load a module from its name."""
    return import_module("{}.{}".format(__name__, module))


def suggest(term):
    """Query the providers for suggestions and return them aggregated."""
    results = []
    providers = _providers()
    for provider in providers:
        results += provider.suggest(term)
    return results
