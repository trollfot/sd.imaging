# -*- coding: utf-8 -*-

from zope.schema import Dict, TextLine
from zope.interface import Interface, Attribute
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.publisher.interfaces.browser import IBrowserPublisher
from Products.ATContentTypes import ATCTMessageFactory as __
from sd import _
from field import ImageField


class IItemWithImageField(IAttributeAnnotatable):
    """Interface allowing you to store and retrieve thumbnails on the
    object itself using annotations. This means the item must have  a formlib
    image field.
    """
    url = Attribute("The physical path to the storage.")


class IPortletWithImage(IItemWithImageField):
    """This interface represents a portlet containing an image field.
    """    
    image = ImageField(
        title = _(u"Picture"),
        description=_(u"The illustration/picture associated"),
        required = False
        )
    
    caption = TextLine(
        title=__(u'label_image_caption', default=u'Image Caption'),
        default=u"",
        required = False,
        )


class IThumbnailWrapper(IBrowserPublisher):
    """A wrapper around a binary data, representing an image thumbnail
    """
    def __call__():
        """Return the thumbnail raw data with the
        correct HTTP response header.
        """


class IImageUpdatedEvent(IObjectModifiedEvent):
    """Triggered on an image creation or modification
    """
    fieldname = Attribute("The name of the image field being updated.")


class IImageMiniaturizer(Interface):
    """Defines an ImageMiniaturizer, a handy adapter that has
    for mission to generate, store, and retrieve thumbnails on
    a given object.
    """    
    annotation_prefix = TextLine(title=u"Thumbnails size",
                                 description=u"List of thumbnails size",
                                 default=u'thumbnails',
                                 required=True)
    
    thumbnails_scales = Dict(title=u"Prefix of thumbnails",
                             description=u"Prefix of thumbnails",
                             default= {'large'  : (700, 700),
                                       'preview': (400, 400),
                                       'mini'   : (250, 250),
                                       'thumb'  : (150, 150),
                                       'small'  : (128, 128)},
                             required=True)


