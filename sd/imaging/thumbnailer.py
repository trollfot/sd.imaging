# -*- coding: utf-8 -*-

from PIL import Image
from cStringIO import StringIO
from Acquisition import aq_base
from zope.component import adapts
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.annotation.interfaces import IAnnotations, IAnnotatable
from interfaces import IImageMiniaturizer


class AssignmentThumbnailsHandler(object):
    """This adapter is an implementation of an IImageMiniaturizer.
    Adapting an IItemWithImageField, it will simply generate a set of
    thumbnails and write them on an annotation. The annotation key
    depends on the field name.
    """
    implements(IImageMiniaturizer)
    adapts(IAnnotatable)

    annotation_prefix = FieldProperty(IImageMiniaturizer['annotation_prefix'])
    thumbnails_scales = FieldProperty(IImageMiniaturizer['thumbnails_scales'])

    def __init__(self, context):
        self.context = context

    def generate_thumbnails(self, fieldname='image'):
        """Generates a set of thumbnails from the available
        sizes and stores them in an annotation.
        """
        original = getattr(self.context, fieldname, None)
        if not original:
            return False
        
        an_key = "%s.%s" % (self.annotation_prefix, fieldname)
        thumbs = dict()

        for format, size in self.thumbnails_scales.iteritems():
            data = StringIO(str(original))
            image = Image.open(data)
            image.thumbnail(size, Image.ANTIALIAS)
            tfd = StringIO()
            image.save(tfd, image.format, quality=90)
            thumbs[format] = tfd.getvalue()

        an = IAnnotations(self.context)
        an[an_key] = thumbs
        return True


    def delete_thumbnails(self, fieldname='image'):
        """Deletes the thumbnails of the given field
        """
        an = IAnnotations(self.context)
        an_key = "%s.%s" % (self.annotation_prefix, fieldname)
        an[an_key] = None


    def retrieve_thumbnail(self, scale, fieldname='image'):
        """Grabs the thumb from its scale name
        """
        image = getattr(aq_base(self.context), fieldname, None)
        
        if image:
            an = IAnnotations(self.context)
            an_key = "%s.%s" % (self.annotation_prefix, fieldname)
            thumbnails = an.get(an_key, None)
            if thumbnails is not None and scale in thumbnails:
                return thumbnails[scale]
            
        return None
