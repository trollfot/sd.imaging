# -*- coding: utf-8 -*-

from Acquisition import Explicit
from zope.cachedescriptors.property import Lazy
from zope.app.form.browser.widget import DisplayWidget, SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from sd.common.widgets.file import FileUploadWidget


class ImageWidgetMixin(object):
    scale = "preview"

    @Lazy
    def attributes(self):
        attrs = dict(
            name = self.name,
            file_exists = False,
            required = self.context.required,
            modified_name = getattr(self, '_modified_name', u'')
            )

        if self._data is not self._data_marker:
            attrs['file_exists'] = True
            attrs['filename'] = getattr(self, 'filename', u'')
            attrs['image_url'] = '%s/++thumbnail++%s.%s' % (
                self.request.get("URL1"),
                self.context.__name__,
                self.scale
                )
        return attrs


class ImageUploadWidget(FileUploadWidget, ImageWidgetMixin):
    """This widget renders a file upload widget enhanced by the display
    of the image preview if an image has already been uploaded. It also
    allows you to delete, keep or override the current uploaded image.
    """
    existWidget = ViewPageTemplateFile('templates/exist_widget.pt')
    emptyWidget = ViewPageTemplateFile('templates/empty_widget.pt')

    def __call__(self):
        attrs = self.attributes
        if not attrs['file_exists']:
            return self.emptyWidget(**attrs)
        return self.existWidget(**attrs)

    def _getFormInput(self):
        if not self.chosen_option:
            return None
        return self.request.get(self.name, None) or None

    def hasInput(self):
        return bool(self.chosen_option)

    @Lazy
    def chosen_option(self):
        return int(self.request.get(self._modified_name, 0))


class DisplayImageWidget(Explicit, DisplayWidget, ImageWidgetMixin):
    """Display the image.
    """
    render = ViewPageTemplateFile('templates/display.pt')
    
    def __init__(self, context, request):
        DisplayWidget.__init__(self, context, request)

    def __call__(self):
        return self.render(**self.attributes)
