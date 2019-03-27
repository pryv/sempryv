# -*- coding: utf-8 -*-
"""Semantic API endpoints."""


# pylint: disable=too-few-public-methods
class SemanticClass:
    """A semantic class."""

    def __init__(self, system, code, names, version=None):
        """Create a semantic class."""
        self.system = system
        self.version = version
        self.code = code
        self.names = names

    def serializable(self):
        """Return a serializable representation of a semantic class."""
        result = {
            "system": self.system.system(),
            "system_name": self.system.name(),
            "code": self.code,
            "display": self.system.preferred_name_for(*self.names),
        }
        if self.version:
            result["version"]: self.version
        return result
