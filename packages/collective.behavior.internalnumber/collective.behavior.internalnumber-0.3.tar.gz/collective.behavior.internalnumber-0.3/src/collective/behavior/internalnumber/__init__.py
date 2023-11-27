# -*- coding: utf-8 -*-
"""Init and utils."""
from plone import api
from zope.i18nmessageid import MessageFactory

import logging


logger = logging.getLogger('collective.behavior.internalnumber')
_ = MessageFactory('collective.behavior.internalnumber')

REGISTRY_KEY = 'collective.behavior.internalnumber.browser.settings.IInternalNumberConfig'
TYPE_CONFIG = '%s.portal_type_config' % REGISTRY_KEY

PLONE_VERSION = api.env.plone_version()[:3]
