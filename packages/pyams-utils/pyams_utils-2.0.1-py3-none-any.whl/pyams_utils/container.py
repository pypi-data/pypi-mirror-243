#
# Copyright (c) 2008-2015 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
# pylint: disable=no-name-in-module

"""PyAMS_utils.container module

This module provides several classes, adapters and functions about containers.
"""

from typing import Callable, Iterable

from BTrees.OOBTree import OOBTree  # pylint: disable=import-error
from persistent.interfaces import IPersistent
from persistent.list import PersistentList
from pyramid.threadlocal import get_current_registry
from zope.container.interfaces import IContainer
from zope.container.ordered import OrderedContainer
from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectMovedEvent
from zope.location.interfaces import IContained, ISublocations

from pyams_utils.adapter import ContextAdapter, adapter_config


__docformat__ = 'restructuredtext'


class SimpleContainerMixin:
    """Simple container mixin class"""

    next_id = 1

    def append(self, obj: IPersistent):
        """Append object to container"""
        key = str(self.next_id)
        self[key] = obj
        self.next_id += 1
        return obj.__name__


class BTreeOrderedContainer(OrderedContainer):
    """BTree based ordered container

    This container maintain a manual order of it's contents
    """

    def __init__(self):
        # pylint: disable=super-init-not-called
        self._data = OOBTree()
        self._order = PersistentList()


class ParentSelector:
    """Interface based parent selector

    This selector can be used as a subscriber predicate on IObjectAddedEvent to define
    an interface that the new parent must support for the event to be applied:

    .. code-block:: python

        from pyams_utils.interfaces.site import ISiteRoot

        @subscriber(IObjectAddedEvent, parent_selector=ISiteRoot)
        def siteroot_object_added_event_handler(event):
            '''This is an event handler for an ISiteRoot object added event'''
    """

    def __init__(self, interfaces: Iterable[Interface], config):  # pylint: disable=unused-argument
        if not isinstance(interfaces, (list, tuple, set)):
            interfaces = (interfaces,)
        self.interfaces = interfaces

    def text(self):
        """Predicate string output"""
        return 'parent_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event: IObjectMovedEvent):
        if not IObjectMovedEvent.providedBy(event):  # pylint: disable=no-value-for-parameter
            return False
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.newParent):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.newParent, intf):
                    return True
        return False


@adapter_config(required=IContained,
                provides=ISublocations)
class ContainerSublocationsAdapter(ContextAdapter):
    """Contained object sub-locations adapter

    This adapter checks for custom ISublocations interface adapters which can
    be defined by any component to get access to inner locations, defined for
    example via annotations.
    """

    def sublocations(self):
        """See `zope.location.interfaces.ISublocations` interface"""
        context = self.context
        # Check for adapted sub-locations first...
        registry = get_current_registry()
        for name, adapter in registry.getAdapters((context,), ISublocations):
            if not name:  # don't reuse default adapter!!
                continue
            yield from adapter.sublocations()
        # then yield container items
        if IContainer.providedBy(context):
            yield from context.values()


def find_objects_matching(root: IPersistent,
                          condition: Callable,
                          ignore_root: bool = False,
                          with_depth: bool = False,
                          initial_depth: int = 0):
    """Find all objects in root that match the condition

    The condition is a Python callable object that takes an object as
    argument and must return a boolean result.

    All sub-objects of the root will also be searched recursively.

    :param object root: the parent object from which search is started
    :param callable condition: a callable object which may return true for a given
        object to be selected
    :param boolean ignore_root: if *True*, the root object will not be returned, even if it
        matches the given condition
    :param boolean with_depth: if *True*, iterator elements will be made of tuples made of
        found elements and their respective depth
    :param int initial_depth: initial depth of the root element; this argument is mainly used
        when function is called recursively
    :return: an iterator for all root's sub-objects matching condition
    """
    if (not ignore_root) and condition(root):
        yield (root, initial_depth) if with_depth else root
    locations = ISublocations(root, None)
    if locations is not None:
        for location in locations.sublocations():  # pylint: disable=too-many-function-args
            if condition(location):
                yield (location, initial_depth+1) if with_depth else location
            yield from find_objects_matching(location, condition,
                                             ignore_root=True,
                                             with_depth=with_depth,
                                             initial_depth=initial_depth+1)


def find_objects_providing(root: IPersistent,
                           interface: Interface,
                           ignore_root: bool = False,
                           with_depth: bool = False):
    """Find all objects in root that provide the specified interface

    All sub-objects of the root will also be searched recursively.

    :param object root: object; the parent object from which search is started
    :param Interface interface: interface; an interface that sub-objects should provide
    :param boolean ignore_root: if *True*, the root object will not be returned, even if it
        provides the given interface
    :param boolean with_depth: if *True*, iterator elements will be made of tuples made of
        found elements and their respective depth
    :return: an iterator for all root's sub-objects that provide the given interface
    """
    yield from find_objects_matching(root, interface.providedBy, ignore_root, with_depth)
