# -*- coding: utf-8 -*-
"""Semantic concepts."""


# pylint: disable=too-few-public-methods
class SemanticClass:
    """A semantic class."""

    def __init__(self, system, code, title):
        """Create a semantic class."""
        self.system = system
        self.code = code
        self.title = title

    def serializable(self):
        """Return a serializable representation of a semantic class."""
        return self.__dict__
