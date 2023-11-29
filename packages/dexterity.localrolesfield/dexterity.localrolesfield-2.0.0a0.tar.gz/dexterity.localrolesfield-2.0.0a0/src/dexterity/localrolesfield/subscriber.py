# encoding: utf-8
from dexterity.localroles.subscriber import configuration_change_analysis
from dexterity.localroles.subscriber import related_role_addition as lr_related_role_addition
from dexterity.localroles.subscriber import related_role_removal as lr_related_role_removal
from dexterity.localroles.utility import runRelatedSearch
from dexterity.localroles.utils import add_related_roles
from dexterity.localroles.utils import del_related_roles
from dexterity.localroles.utils import del_related_uid
from dexterity.localroles.utils import fti_configuration
from dexterity.localroles.utils import get_state
from dexterity.localrolesfield import logger
from dexterity.localrolesfield.utils import get_localrole_fields
from OFS.interfaces import IObjectWillBeAddedEvent
from OFS.interfaces import IObjectWillBeRemovedEvent
from plone import api
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityFTI
from plone.memoize.interfaces import ICacheChooser
from zope.component import getUtility
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


try:
    from zope.component.interfaces import ComponentLookupError  # noqa
except ImportError:
    from zope.interface.interfaces import ComponentLookupError


def fti_modified(obj, event):
    """
        When an FTI is modified, invalidate localrole fields list cache.
    """
    return  # cache is no more used because not necessary following timecall
    if not IDexterityFTI.providedBy(event.object):
        return
    cache_chooser = getUtility(ICacheChooser)
    thecache = cache_chooser('dexterity.localrolesfield.utils.get_localrole_fields')
    thecache.ramcache.invalidate('dexterity.localrolesfield.utils.get_localrole_fields')


def _check_modified_fieldname(obj, event):
    try:
        names = [f[0] for f in get_localrole_fields(getUtility(IDexterityFTI, name=obj.portal_type))]
    except ComponentLookupError:
        return False, []
    for at in event.descriptions:
        for name in getattr(at, 'attributes', []):
            if '.' in name:
                name = name.split('.')[-1]
            if name in names:
                return True, names
    return False, []


def get_field_values(obj, name):
    values = getattr(obj, name) or []
    if not isinstance(values, (list, tuple)):
        values = [values]
    return values


def related_role_removal(obj, state, field_config, name):
    if state in field_config:
        dic = field_config[state]
        uid = obj.UID()
        for suffix in dic:
            if dic[suffix].get('rel', ''):
                related = eval(dic[suffix]['rel'])
                for utility in related:
                    if not related[utility]:
                        continue
                    for val in get_field_values(obj, name):
                        princ = suffix and '%s_%s' % (val, suffix) or val
                        for rel in runRelatedSearch(utility, obj):
                            if del_related_roles(rel, uid, princ, related[utility]):
                                rel.reindexObjectSecurity()


def related_role_addition(obj, state, field_config, name):
    if state in field_config:
        dic = field_config[state]
        uid = obj.UID()
        for suffix in dic:
            if dic[suffix].get('rel', ''):
                related = eval(dic[suffix]['rel'])
                for utility in related:
                    if not related[utility]:
                        continue
                    for val in get_field_values(obj, name):
                        princ = suffix and '%s_%s' % (val, suffix) or val
                        for rel in runRelatedSearch(utility, obj):
                            add_related_roles(rel, uid, princ, related[utility])
                            rel.reindexObjectSecurity()


def related_annot_removal(obj, state, field_config):
    if state in field_config:
        dic = field_config[state]
        uid = obj.UID()
        for suffix in dic:
            if dic[suffix].get('rel', ''):
                related = eval(dic[suffix]['rel'])
                for utility in related:
                    if not related[utility]:
                        continue
                    for rel in runRelatedSearch(utility, obj):
                        del_related_uid(rel, uid)


def object_modified(obj, event):
    (modif, names) = _check_modified_fieldname(obj, event)
    if not modif:
        return
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return

    # We have to reindex sub objects security when a localrolefield is modified
    if IDexterityContainer.providedBy(obj):
        obj.reindexObjectSecurity(skip_self=True)

    # We have to update related objects
    state = get_state(obj)
    # First we remove previous rel annotation for this uid
    if 'static_config' in fti_config:
        related_annot_removal(obj, state, fti_config['static_config'])
    for name in names:
        if name not in fti_config:
            continue
        related_annot_removal(obj, state, fti_config[name])
    # Second we add related roles annotations
    if 'static_config' in fti_config:
        lr_related_role_addition(obj, state, fti_config)
    for name in names:
        if name not in fti_config:
            continue
        related_role_addition(obj, state, fti_config[name], name)


def related_change_on_transition(obj, event):
    """ Set local roles on related objects after transition """
    if event.old_state.id == event.new_state.id:  # escape creation
        return
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        # We have to remove the configuration linked to old state
        related_role_removal(obj, event.old_state.id, fti_config[name], name)
        # We have to add the configuration linked to new state
        related_role_addition(obj, event.new_state.id, fti_config[name], name)


def related_change_on_addition(obj, event):
    """ Set local roles on related objects after addition """
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        related_role_addition(obj, get_state(obj), fti_config[name], name)


def related_change_on_removal(obj, event):
    """ Set local roles on related objects after removal """
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        # We have to remove the configuration linked to deleted object
        # There is a problem in Plone 4.3. The event is notified before the confirmation and after too.
        # The action could be cancelled: we can't know this !! Resolved in Plone 5...
        # We choose to update related objects anyway !!
        related_annot_removal(obj, get_state(obj), fti_config[name])


def related_change_on_moving(obj, event):
    """ Set local roles on related objects before moving """
    if IObjectWillBeAddedEvent.providedBy(event) or IObjectWillBeRemovedEvent.providedBy(event):  # not move
        return
    if event.oldParent and event.newParent and event.oldParent == event.newParent:  # rename
        return
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        related_role_removal(obj, get_state(obj), fti_config[name], name)


def related_change_on_moved(obj, event):
    """ Set local roles on related objects after moving """
    if IObjectAddedEvent.providedBy(event) or IObjectRemovedEvent.providedBy(event):  # not move
        return
    if event.oldParent and event.newParent and event.oldParent == event.newParent:  # rename
        return
    (fti_config, fti) = fti_configuration(obj)
    if not fti_config:
        return
    for (name, f) in get_localrole_fields(fti):
        if name not in fti_config:
            continue
        related_role_addition(obj, get_state(obj), fti_config[name], name)


def local_role_related_configuration_updated(event):
    """Local roles configuration modification: we have to compare old and new values.

    event.old_value is like : {'private': {'raptor': {'rel': "{'dexterity.localroles.related_parent': ['Editor']}",
                                                      'roles': ('Reader',)}}}
    """
    only_reindex, rem_rel_roles, add_rel_roles = configuration_change_analysis(event)
    portal = api.portal.getSite()
    if only_reindex:
        logger.info('Objects security update')
        for brain in portal.portal_catalog(portal_type=event.fti.__name__, review_state=list(only_reindex)):
            obj = brain.getObject()
            obj.reindexObjectSecurity()
    if rem_rel_roles:
        logger.info("Removing related roles: %s" % rem_rel_roles)
        for st in rem_rel_roles:
            for brain in portal.portal_catalog(portal_type=event.fti.__name__, review_state=st):
                if event.field == 'static_config':
                    lr_related_role_removal(brain.getObject(), brain.review_state, {event.field: rem_rel_roles})
                else:
                    related_role_removal(brain.getObject(), brain.review_state, rem_rel_roles, event.field)
    if add_rel_roles:
        logger.info('Adding related roles: %s' % add_rel_roles)
        for st in add_rel_roles:
            for brain in portal.portal_catalog(portal_type=event.fti.__name__, review_state=st):
                if event.field == 'static_config':
                    lr_related_role_addition(brain.getObject(), brain.review_state, {event.field: add_rel_roles})
                else:
                    related_role_addition(brain.getObject(), brain.review_state, add_rel_roles, event.field)
