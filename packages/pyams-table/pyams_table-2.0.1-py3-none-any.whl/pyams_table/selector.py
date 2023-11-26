#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_table.selector module

This module provides custom events predicates used to filter tables events.
"""

__docformat__ = 'restructuredtext'


class TableContextSelector:  # pylint: disable=too-few-public-methods
    """Table selector

    This selector can be used as a predicate to define a class or an interface that the event
    *table* attribute must inherit from or implement for the subscriber to be called:

    .. code-block:: python

        from pyams_table.interfaces import ITableUpdatedEvent
        from pyams_sample.zmi.interfaces import IMyTable

        @subscriber(ITableUpdatedEvent, table_selector=IMyTable)
        def table_updated_event_handler(event):
            '''This is an event handler for an IMyTable update event'''
    """

    def __init__(self, ifaces, config):  # pylint: disable=unused-argument
        if not isinstance(ifaces, (list, tuple, set)):
            ifaces = (ifaces,)
        self.interfaces = ifaces

    def text(self):
        """Return selector"""
        return 'table_context_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event):
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.context):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.context, intf):
                    return True
        return False


class TableRowContextSelector:  # pylint: disable=too-few-public-methods
    """Table row context selector

    This selector can be used as a predicate to define a class or an interface that the event
    *item* attribute must inherit from or implement for the subscriber to be called:

    .. code-block:: python

        from pyams_table.interfaces import ITableRowUpdatedEvent
        from pyams_sample.interfaces import IMyContext

        @subscriber(ITableRowUpdatedEvent, row_selector=IMyContext)
        def table_row_updated_event_handler(event):
            '''This is an event handler for an ITableRowUpdatedEvent on a IMyContext object'''
    """

    def __init__(self, ifaces, config):  # pylint: disable=unused-argument
        if not isinstance(ifaces, (list, tuple, set)):
            ifaces = (ifaces,)
        self.interfaces = ifaces

    def text(self):
        """Return selector"""
        return 'row_context_selector = %s' % str(self.interfaces)

    phash = text

    def __call__(self, event):
        for intf in self.interfaces:
            try:
                if intf.providedBy(event.item):
                    return True
            except (AttributeError, TypeError):
                if isinstance(event.item, intf):
                    return True
        return False
