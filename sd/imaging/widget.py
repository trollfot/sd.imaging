# -*- coding: utf-8 -*-

from OFS.Image import File
from zope.cachedescriptors.property import Lazy
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from sd.common.widgets.file import FileUploadWidget


class ImageUploadWidget(FileUploadWidget):
    """This widget renders a file upload widget enhanced by the display
    of the image preview if an image has already been uploaded. It also
    allows you to delete, keep or override the current uploaded image.
    """
    existWidget = ViewPageTemplateFile('templates/exist_widget.pt')
    emptyWidget = ViewPageTemplateFile('templates/empty_widget.pt')

    def __call__(self):
        kwargs = dict(
            name = self.name,
            required = self.context.required,
            modified_name = self._modified_name
            )
        
        if not self._data or not isinstance(self._data, File):
            return self.emptyWidget(**kwargs)
            
        kwargs['filename'] = self.filename
        kwargs['image_url'] = ('%s/++thumbnail++%s.preview' %
                               (self.request.get("URL1"), self._data.__name__))
        return self.existWidget(**kwargs)

    def _getFormInput(self):
        if not self.chosen_option:
            return None
        return self.request.get(self.name, None) or None

    def hasInput(self):
        return bool(self.chosen_option)

    @Lazy
    def chosen_option(self):
        return int(self.request.get(self._modified_name, 0))
