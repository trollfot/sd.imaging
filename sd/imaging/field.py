# -*- coding: utf-8 -*-

from zope.interface import Interface, implements
from sd.common.fields.file import FileField


class IImageField(Interface):
    """Marker interface for fields storing images.
    """

class ImageField(FileField):
    """A field for representing an image.
    """
    implements(IImageField)
    
    def __init__(self, preferred_dimensions=None, **kw):
        super(ImageField, self).__init__(**kw)
        self.preferred_dimensions = preferred_dimensions
    
