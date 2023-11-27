# -*- coding: utf-8 -*-

from collective.behavior.internalnumber import logger
from collective.behavior.internalnumber import TYPE_CONFIG
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import INonInstallable
from ZODB.POSException import ConnectionStateError
from zope.component import getUtility
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.behavior.internalnumber:uninstall',
        ]


def post_install(context):
    """Post install script"""
    registry = getUtility(IRegistry)
    # Initialize the registry content if nothing is stored
    if registry[TYPE_CONFIG] is None:
        # may fail in tests because a datagridfield is stored, just pass in this case
        try:
            registry[TYPE_CONFIG] = []
        except ConnectionStateError:
            logger.warn('!!!Failed to set registry config to []!!!')
            registry.records[TYPE_CONFIG].field.value_type = None


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
