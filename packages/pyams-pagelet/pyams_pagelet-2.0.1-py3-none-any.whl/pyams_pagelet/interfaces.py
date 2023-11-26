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

"""PyAMS_pagelet.interfaces module

"""

from pyramid.interfaces import IView
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent


__docformat__ = 'restructuredtext'


class IPagelet(IView):
    """Pagelet interface"""

    def update(self):
        """Update the pagelet data."""

    def render(self):
        """Render the pagelet content w/o o-wrap."""


class IPageletRenderer(IContentProvider):
    """Render a pagelet by calling it's 'render' method"""


class IBasePageletEvent(IObjectEvent):
    """Base pagelet event interface"""

    context = Attribute('The context object')
    request = Attribute('The request object')


class IPageletCreatedEvent(IBasePageletEvent):
    """Pagelet creation event interface"""


class IPageletUpdatedEvent(IBasePageletEvent):
    """Pagelet updated event interface"""


class BasePageletEvent(ObjectEvent):
    """Base pagelet event"""

    def __init__(self, obj):
        super().__init__(obj)
        self.context = obj.context
        self.request = obj.request


@implementer(IPageletCreatedEvent)
class PageletCreatedEvent(BasePageletEvent):
    """Pagelet created event"""


@implementer(IPageletUpdatedEvent)
class PageletUpdatedEvent(BasePageletEvent):
    """Pagelet updated event"""
