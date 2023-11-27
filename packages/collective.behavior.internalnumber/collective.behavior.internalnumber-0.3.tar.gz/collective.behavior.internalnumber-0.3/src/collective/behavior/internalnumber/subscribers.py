# -*- coding: utf-8 -*-
"""Subscribers."""

from collective.behavior.internalnumber.browser.settings import increment_nb_for


def object_added(obj, event):
    """Increments the registry default_number for the type or globally (if one of both configured)."""
    increment_nb_for(obj)
