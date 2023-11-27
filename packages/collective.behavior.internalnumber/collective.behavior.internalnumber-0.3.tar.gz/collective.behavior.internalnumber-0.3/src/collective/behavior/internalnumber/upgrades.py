# -*- coding: utf-8 -*-

from plone import api


def upgrade_to_1001(context):
    """Upgrade to 1001, remove the "internal_number" catalog metadata."""

    catalog = api.portal.get_tool('portal_catalog')
    catalog.delColumn('internal_number')
