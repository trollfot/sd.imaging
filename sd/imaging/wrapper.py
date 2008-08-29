# -*- coding: utf-8 -*-

from Acquisition import Explicit
from zope.interface import implements
from interfaces import IThumbnailWrapper


class ThumbnailWrapper(Explicit):
    """A class that masquarades an image, in order to access
    thumbnails of a given context.
    """
    implements(IThumbnailWrapper)

    def __init__(self, context, request, data, fieldname='image'):
        self.context = context
        self.request = request

        # internal data
        self._data = data
        self._fieldname = fieldname
        
        # contextual positionning
        self.__parent__ = context


    def browserDefault(self, request):
        return self, ()


    def __call__(self):
        response = self.request.response
        image = getattr(self.context, self._fieldname, None)
        if not image:
            raise NotFound(self.context, self._fieldname, self.request)
        content_type = image.get('content_type', 'image/jpeg')
        response.setHeader('Content-Type', content_type)
        return self._data
