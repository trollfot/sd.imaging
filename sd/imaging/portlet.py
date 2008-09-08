# -*- coding: utf-8 -*-

# Zope
from zope.formlib import form
from zope.event import notify
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectModifiedEvent
from zope.cachedescriptors.property import Lazy

# Plone, ATCT
from plone.app.portlets.portlets import base
from Products.CMFPlone import PloneMessageFactory as __
from Products.ATContentTypes.interface.image import IImageContent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# sd.common
from sd import _
from sd.common.fields.file import FileProperty
from sd.common.portlets.base import BasePortletRenderer

# sd.imaging
from field import ImageField, IImageField
from events import ImageUpdatedEvent
from widget import ImageUploadWidget
from interfaces import IPortletWithImage


class AssignmentWithImage(base.Assignment):
    """A basic portlet assignement handling a captioned image.
    """
    implements(IPortletWithImage)
    image = FileProperty(IPortletWithImage['image'])
    url = ""

    def __init__(self, name, url, caption=u"", image=None):
        self.name = name
        self.url = url
        self.caption = caption
        if image:
            self.image = image
            notify(ImageUpdatedEvent(self, 'image'))

    @Lazy
    def title(self):
        return self.name


class AddFormWithImage(base.AddForm):
    """An add form with an image field
    """
    form_fields = form.Fields(IPortletWithImage)
    
    def __init__(self,  *args, **kwargs):
        super(AddFormWithImage, self).__init__(*args, **kwargs)
        self.form_fields['image'].custom_widget = ImageUploadWidget

    def create(self, data):
        return AssignmentWithImage(**data)

    def createAndAdd(self, data):
        data['url'] = '/'.join(self.context.__parent__.getPhysicalPath())
        return base.AddForm.createAndAdd(self, data)
    

class EditFormWithImage(base.EditForm):
    """A form with a save action triggering an event if an image
    has been uploaded.
    """
    form_fields = form.Fields(IPortletWithImage)
    
    def __init__(self,  *args, **kwargs):
        super(EditFormWithImage, self).__init__(*args, **kwargs)
        self.form_fields['image'].custom_widget = ImageUploadWidget

    
    @form.action(__(u"label_save", default=u"Save"), name=u'save',
                 condition=form.haveInputWidgets)
    def handle_save_action(self, action, data):
        if form.applyChanges(self.context, self.form_fields,
                             data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            for field in [f.field for f in self.form_fields]:
                if IImageField.providedBy(field) and field.__name__ in data:
                    notify(ImageUpdatedEvent(self.context, field.__name__))
            self.status = "Changes saved"
        else:
            self.status = "No changes"
            
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


class ImagePortletRenderer(BasePortletRenderer):
    """Base renderer for portlets containing an image
    """
    implements(IImageContent)

    render = ViewPageTemplateFile('templates/image.pt')

    def caption(self):
        """Returns the image caption text.
        """
        return self.data.caption

    
    def getImage(self, **kwargs):
        """Returns the original image
        """
        return self.data.image


    def setImage(self, value, **kwargs):
        """Present to respect the interface contract.
        """
        raise NotImplementedError


    def getImageUrl(self, scale="original"):
        base = '%s/%s' % (self.data.url, self.data.__name__)
        if scale is 'original':
            return base + '/image'
        return '%s/++thumbnail++image.%s' % (base, scale)


    def tag(self, scale=u"thumb", base=u"", cssClass=u"", **kwargs):
        """Returns a valid XHTML image tag.
        """
        if not self.data.image:
            return u""

        return (u'<img src="%(url)s" alt="%(alt)s" title="%(title)s"'
                    u'class="%(cssClass)s" />') % (
            {'url': self.getImageUrl(scale = scale),
             'title': self.data.name,
             'alt': self.data.name,
             'cssClass': cssClass or 'portlet-image'}
            )
