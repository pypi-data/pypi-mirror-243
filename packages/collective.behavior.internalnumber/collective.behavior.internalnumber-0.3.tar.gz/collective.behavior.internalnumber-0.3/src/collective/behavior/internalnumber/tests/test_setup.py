# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.behavior.internalnumber import PLONE_VERSION
from collective.behavior.internalnumber import TYPE_CONFIG
from collective.behavior.internalnumber.testing import COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING
from plone import api
from zope.schema._bootstrapinterfaces import WrongType

import unittest


class CommonSetup():  # noqa

    def set_installer(self):
        if PLONE_VERSION >= '5.1':
            from Products.CMFPlone.utils import get_installer  # noqa
            self.installer = get_installer(self.portal, self.layer["request"])
            self.ipi = self.installer.is_product_installed
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')  # noqa
            self.ipi = self.installer.isProductInstalled


class TestSetup(unittest.TestCase, CommonSetup):
    """Test that collective.behavior.internalnumber is properly installed."""

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.set_installer()

    def test_product_installed(self):
        """Test if collective.behavior.internalnumber is installed."""
        self.assertTrue(self.ipi('collective.behavior.internalnumber'))

    def test_browserlayer(self):
        """Test that ICollectiveBehaviorInternalnumberLayer is registered."""
        from collective.behavior.internalnumber.interfaces import ICollectiveBehaviorInternalnumberLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveBehaviorInternalnumberLayer, utils.registered_layers())

    def test_registry(self):
        self.assertRaises(api.exc.InvalidParameterError, api.portal.set_registry_record, 'Unexistent key', True)
        self.assertRaises(WrongType, api.portal.set_registry_record, TYPE_CONFIG, 'string')
        api.portal.set_registry_record(TYPE_CONFIG, [])

    def test_catalog(self):
        catalog = api.portal.get_tool('portal_catalog')
        # we have an index
        self.assertTrue('internal_number' in catalog.Indexes)
        # we no more have a metadata
        self.assertFalse('internal_number' in catalog.schema())


class TestUninstall(unittest.TestCase, CommonSetup):

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.set_installer()
        if PLONE_VERSION >= '5.1':
            self.installer.uninstall_product('collective.behavior.internalnumber')
        else:
            self.installer.uninstallProducts(['collective.behavior.internalnumber'])

    def test_product_uninstalled(self):
        """Test if collective.behavior.internalnumber is cleanly uninstalled."""
        self.assertFalse(self.ipi('collective.behavior.internalnumber'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBehaviorInternalnumberLayer is removed."""
        from collective.behavior.internalnumber.interfaces import ICollectiveBehaviorInternalnumberLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveBehaviorInternalnumberLayer, utils.registered_layers())

    def test_catalog_cleaned(self):
        catalog = api.portal.get_tool('portal_catalog')
        # no more catalog index
        self.assertFalse('internal_number' in catalog.Indexes)
        # no more catalog metadata
        self.assertFalse('internal_number' in catalog.schema())
