# -*- coding: utf-8 -*-

from collective.behavior.internalnumber import PLONE_VERSION
from collective.behavior.internalnumber.behavior import IInternalNumberBehavior
from plone.indexer import indexer
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapts
from zope.interface import implementer


try:
    from Products.PluginIndexes.common.UnIndex import _marker as common_marker  # noqa
except ImportError:
    from Products.PluginIndexes.unindex import _marker as common_marker  # noqa

if PLONE_VERSION < '6.0':
    from collective.dexteritytextindexer.interfaces import IDynamicTextIndexExtender
else:
    from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender


@indexer(IContentish)
def internal_number_index(obj):
    """ Index method escaping acquisition and ready for ZCatalog 3 """
    if base_hasattr(obj, 'internal_number') and obj.internal_number:
        return obj.internal_number
    return common_marker


@implementer(IDynamicTextIndexExtender)
class InternalNumberSearchableExtender(object):
    """
        Extends SearchableText of IInternalNumberBehavior objects.
    """
    adapts(IInternalNumberBehavior)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return safe_unicode(self.context.internal_number)
