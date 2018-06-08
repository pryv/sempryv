# -*- coding: utf-8 -*-
"""SNOMEDCT ontology."""


def system():
    """Return the system identifier of the ontology."""
    return "http://snomed.info/sct"


def name():
    """Return the name of the ontology."""
    return "SNOMEDCT"


def preferred_name_for(*names):
    """Return the preferred name for a class of this ontology."""
    ordered = sorted(names, key=_count_parenthesis, reverse=True)
    return ordered[0]


def _count_parenthesis(value):
    """Count the number of `.` and `:` in the given string."""
    return sum([i for i, c in enumerate(value) if c in ["(", ")"]])
