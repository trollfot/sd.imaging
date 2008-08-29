# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.lifecycleevent import ObjectModifiedEvent
from interfaces import IImageMiniaturizer, IImageUpdatedEvent


class ImageUpdatedEvent(ObjectModifiedEvent):
    """A portlet has been added or modified
    """
    implements(IImageUpdatedEvent)

    def __init__(self, obj, fieldname):
        self.object = obj
        self.fieldname = fieldname


def ThumbnailsGeneration(obj, event):
    """Event handler triggering the thumbnail generation
    """
    original = getattr(obj, event.fieldname, None)
    handler = IImageMiniaturizer(obj)
    
    # The image has been deleted if 'original' is None
    if original is None:
        # We delete the thumbnails.
        handler.delete_thumbnails(fieldname = event.fieldname)
    else:
        # We generate the thumbnails.
        handler.generate_thumbnails(fieldname = event.fieldname)
