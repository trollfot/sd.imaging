# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.http import IHTTPRequest
from wrapper import ThumbnailWrapper
from interfaces import IItemWithImageField, IImageMiniaturizer


class PortletThumbnailsTraverser(object):
    """A traverser that is involved while traversing an object implementing
    IItemWithImageField. It's merely a namespace traverser, retrieving and
    instanciating an image thanks to an IImageMiniaturizer.
    """
    implements(ITraversable)
    adapts(IItemWithImageField, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def traverse(self, name, ignore):
        
        handler = IImageMiniaturizer(self.context, None)

        try:
            fieldname, scale = name.split('.')
        except ValueError:
            raise NotFound(self.context, name, self.request)
            
        scale = handler.retrieve_thumbnail(scale, fieldname=fieldname)
        if scale is not None:
            return ThumbnailWrapper(self.context,
                                    self.request,
                                    scale,
                                    fieldname).__of__(self.context)
        
        raise NotFound(self.context, name, self.request)
