# -*- coding: utf-8 -*-

from collective.behavior.internalnumber import _
from collective.behavior.internalnumber import TYPE_CONFIG
from collective.behavior.talcondition.utils import _evaluateExpression
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform.directives import widget
from plone.dexterity.interfaces import IDexterityFTI
from plone.z3cform import layout
from Products.CMFPlone.utils import base_hasattr
from z3c.form import form
from zope import schema
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class IPortalTypeConfigSchema(Interface):
    portal_type = schema.Choice(
        title=_("Portal type"),
        vocabulary=u'collective.internalnumber.portaltypevocabulary',
        required=True)
    uniqueness = schema.Bool(
        title=_("Uniqueness"),
        required=False)
    default_number = schema.Int(
        title=_(u'Number of next content item'),
        description=_(u"This value can be used as 'number' variable in tal expression"),
        default=1)
    default_expression = schema.TextLine(
        title=_("Default value tal expression"),
        description=_("Elements 'number', 'member', 'context' and 'portal' are available."),
        default=u"number",
        required=False)


class IInternalNumberConfig(Interface):
    """
    Configuration of internalnumber
    """

    portal_type_config = schema.List(
        title=_(u'By type configuration'),
        value_type=DictRow(title=_("Portal type conf"),
                           schema=IPortalTypeConfigSchema))

    widget('portal_type_config', DataGridFieldFactory)


class SettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    form.extends(RegistryEditForm)
    schema = IInternalNumberConfig
    label = _("Internal number behavior configuration")


SettingsView = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)


def get_settings():
    ptc = api.portal.get_registry_record(TYPE_CONFIG)
    settings = {}
    if ptc is None:
        return settings
    for row in ptc:
        expr = row['default_expression'] and row['default_expression'] or u''
        settings[row['portal_type']] = {'u': row['uniqueness'], 'nb': row['default_number'], 'expr': expr}
    return settings


def get_pt_settings(pt):
    settings = get_settings()
    if pt in settings:
        return settings[pt]
    elif 'glo_bal' in settings:
        return settings['glo_bal']
    return {}


def set_settings(settings):
    config = []
    for pt in sorted(settings.keys()):
        config.append({'portal_type': pt, 'uniqueness': settings[pt]['u'],
                       'default_number': settings[pt]['nb'],
                       'default_expression': settings[pt]['expr']})
    api.portal.set_registry_record(TYPE_CONFIG, config)


def _internal_number_is_used(obj):
    """ """
    return base_hasattr(obj, 'internal_number') and obj.internal_number


def increment_nb_for(obj, bypass_attr_check=False):
    # internal_number is unknown or empty => no need to increment
    if not bypass_attr_check and not _internal_number_is_used(obj):
        return

    settings = get_settings()
    pt = obj.portal_type
    updated = False
    nb = None
    if pt in settings:
        updated = True
        settings[pt]['nb'] += 1
        nb = settings[pt]['nb']
    elif 'glo_bal' in settings:
        updated = True
        settings['glo_bal']['nb'] += 1
        nb = settings['glo_bal']['nb']
    if updated:
        set_settings(settings)
    return nb


def decrement_nb_for(obj):
    # internal_number is unknown or empty => no need to decrement
    if not _internal_number_is_used(obj):
        return

    settings = get_settings()
    pt = obj.portal_type
    updated = False
    nb = None
    if pt in settings:
        updated = True
        settings[pt]['nb'] -= 1
        nb = settings[pt]['nb']
    elif 'glo_bal' in settings:
        updated = True
        settings['glo_bal']['nb'] -= 1
        nb = settings['glo_bal']['nb']
    if updated:
        set_settings(settings)
    return nb


def decrement_if_last_nb(obj):
    # internal_number is unknown or empty => no need to decrement
    if not _internal_number_is_used(obj):
        return

    internal_number = getattr(obj, "internal_number")
    settings = get_settings()
    pt = obj.portal_type
    updated = False
    nb = None

    def _compute_expr(obj, pt_settings):
        return _evaluateExpression(
            obj,
            pt_settings['expr'],
            extra_expr_ctx={'number': pt_settings['nb'] - 1},
            empty_expr_is_true='')

    if pt in settings and internal_number == _compute_expr(obj, settings[pt]):
        updated = True
        settings[pt]['nb'] -= 1
        nb = settings[pt]['nb']
    elif 'glo_bal' in settings and \
            internal_number == _compute_expr(obj, settings['glo_bal']):
        updated = True
        settings['glo_bal']['nb'] -= 1
        nb = settings['glo_bal']['nb']
    if updated:
        set_settings(settings)
    return nb


@implementer(IVocabularyFactory)
class DxPortalTypesVocabulary(object):
    """ Active mail types vocabulary """

    def __call__(self, context):
        terms = [SimpleTerm('glo_bal', 'glo_bal', _(u'Global configuration'))]
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        portal = api.portal.get()
        for fti in ftis:
            translation_domain = getUtility(ITranslationDomain, fti.i18n_domain)
            terms.append(SimpleTerm(fti.id, fti.id, translation_domain.translate(
                fti.title, context=portal.REQUEST)))
        return SimpleVocabulary(terms)
