# -*- coding: utf-8 -*-
from collective.behavior.internalnumber import PLONE_VERSION
from collective.behavior.internalnumber import TYPE_CONFIG
from collective.behavior.internalnumber.browser.settings import decrement_if_last_nb
from collective.behavior.internalnumber.browser.settings import decrement_nb_for
from collective.behavior.internalnumber.browser.settings import DxPortalTypesVocabulary
from collective.behavior.internalnumber.browser.settings import get_pt_settings
from collective.behavior.internalnumber.browser.settings import get_settings
from collective.behavior.internalnumber.browser.settings import increment_nb_for
from collective.behavior.internalnumber.browser.settings import set_settings
from collective.behavior.internalnumber.testing import COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING  # noqa
from operator import itemgetter
from plone import api

import unittest


class TestSettings(unittest.TestCase):
    """Test settings."""

    layer = COLLECTIVE_BEHAVIOR_INTERNALNUMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.tt1 = self.portal['tt1']
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'glo_bal', u'uniqueness': False,
                                                      u'default_number': 1, u'default_expression': u'number'},
                                                     {u'portal_type': u'testtype', u'uniqueness': True,
                                                      u'default_number': 1, u'default_expression': u'number'}])

    def test_get_settings(self):
        self.assertDictEqual(get_settings(), {u'glo_bal': {u'u': False, u'nb': 1, 'expr': u'number'},
                                              u'testtype': {u'u': True, u'nb': 1, 'expr': u'number'}})

    def test_get_pt_settings(self):
        self.assertDictEqual(get_pt_settings('testtype'), {u'u': True, u'nb': 1, 'expr': u'number'})
        self.assertDictEqual(get_pt_settings('unknown'), {u'u': False, u'nb': 1, 'expr': u'number'})
        api.portal.set_registry_record(TYPE_CONFIG, [{u'portal_type': u'glo_bal', u'uniqueness': False,
                                                      u'default_number': 1, u'default_expression': u'number'}])
        self.assertDictEqual(get_pt_settings('testtype'), {u'u': False, u'nb': 1, 'expr': u'number'})

    def test_DxPortalTypesVocabulary(self):
        voc_inst = DxPortalTypesVocabulary()
        voc_list = sorted([(t.value, t.title) for t in voc_inst(self.portal)], key=itemgetter(1))
        if PLONE_VERSION == '4.3':
            res = [('glo_bal', u'Global configuration'), ('testtype', u'Test type')]
        elif PLONE_VERSION == '5.2':
            res = [('Collection', 'Collection'), ('Event', 'Event'), ('File', 'File'), ('Folder', 'Folder'),
                   ('glo_bal', 'Global configuration'), ('Image', 'Image'), ('Link', 'Link'),
                   ('News Item', 'News Item'), ('Document', 'Page'), ('testtype', 'Test type')]
        elif PLONE_VERSION > '5.2':
            res = [('Collection', 'Collection'), ('Event', 'Event'), ('File', 'File'), ('Folder', 'Folder'),
                   ('glo_bal', 'Global configuration'), ('Image', 'Image'), ('Link', 'Link'),
                   ('News Item', 'News Item'), ('Document', 'Page'), ('Plone Site', 'Plone Site'),
                   ('testtype', 'Test type')]
        self.assertEqual(voc_list, res)

    def test_increment_nb_for(self):
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 1, 'u': True})
        self.assertEqual(increment_nb_for(self.tt1), 2)
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 2, 'u': True})
        # glo_bal
        settings = get_settings()
        settings.pop(self.tt1.portal_type)
        set_settings(settings)
        self.assertEqual(increment_nb_for(self.tt1), 2)

    def test_decrement_nb_for(self):
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 1, 'u': True})
        self.assertEqual(increment_nb_for(self.tt1), 2)
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 2, 'u': True})
        self.assertEqual(decrement_nb_for(self.tt1), 1)
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 1, 'u': True})
        # glo_bal
        settings = get_settings()
        settings.pop(self.tt1.portal_type)
        settings['glo_bal']['nb'] = 5
        set_settings(settings)
        self.assertEqual(decrement_nb_for(self.tt1), 4)
        # internal_number attr not used
        self.assertIsNone(decrement_nb_for(self.portal))

    def test_decrement_if_last_nb(self):
        self.tt1.internal_number = 1
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 1, 'u': True})
        self.assertEqual(increment_nb_for(self.tt1), 2)
        self.assertEqual(get_pt_settings(self.tt1.portal_type), {'expr': u'number', 'nb': 2, 'u': True})
        # change tt1 internal_number is not the last, not decremented
        self.tt1.internal_number = 3
        self.assertIsNone(decrement_if_last_nb(self.tt1))
        # set internal_number as last nb
        self.tt1.internal_number = 1
        self.assertEqual(decrement_if_last_nb(self.tt1), 1)
        # internal_number attr not used
        self.assertIsNone(decrement_if_last_nb(self.portal))

    def test_decrement_if_last_nb_complex_internal_number(self):
        self.assertEqual(self.tt1.internal_number, 'AA123')
        settings = get_settings()
        settings[self.tt1.portal_type]['nb'] = 124
        settings[self.tt1.portal_type]['expr'] = u"string:AA${number}"
        set_settings(settings)
        self.assertEqual(decrement_if_last_nb(self.tt1), 123)
        # glo_bal
        settings.pop(self.tt1.portal_type)
        settings['glo_bal']['nb'] = 111
        settings['glo_bal']['expr'] = u"string:AA${number}"
        set_settings(settings)
        self.tt1.internal_number = 'AA110'
        self.assertEqual(decrement_if_last_nb(self.tt1), 110)
