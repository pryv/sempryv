# -*- coding: utf-8 -*-
"""The external services used for providing semantic information."""

import os
from importlib import import_module


def _services():
    """List all services in the current package."""
    services = []
    for name in os.listdir(os.path.dirname(__file__)):
        if name.endswith(".py") and name != "__init__.py":
            services.append(_load(name[:-3]))
    return services


def _load(module):
    """Load a module from its name."""
    print(module)
    return import_module("{}.{}".format(__name__, module))


def suggest(term):
    """Query the services for suggestions and return them aggregated."""
    results = []
    services = _services()
    for service in services:
        results += service.suggest(term)
    return results
