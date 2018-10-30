# -*- coding: utf-8 -*-
"""LOINC ontology."""


def system():
    """Return the system identifier of the ontology."""
    return "http://loinc.org"


def name():
    """Return the name of the ontology."""
    return "LOINC"


def preferred_name_for(*names):
    """Return the preferred name for a class of this ontology."""
    ordered = sorted(names, key=_count_dot_semicolumn)
    return ordered[0]


def _count_dot_semicolumn(value):
    """Count the number of `.` and `:` in the given string."""
    return sum([1 for c in value if c in [".", ":"]])
