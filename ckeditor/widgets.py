import re

try:
    import simplejson as json
except ImportError:
    import json

from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets


FILEBROWSER_PRESENT = 'filebrowser' in getattr(settings, 'INSTALLED_APPS', [])
GRAPPELLI_PRESENT = 'grappelli' in getattr(settings, 'INSTALLED_APPS', [])

MEDIA = getattr(settings, 'CKEDITOR_MEDIA_URL',
                '%s' % settings.STATIC_URL.rstrip('/')).rstrip('/')

_CSS_FILE = 'grappelli.css' if GRAPPELLI_PRESENT else 'standard.css'
_CONFIG_FILE = '/ckeditor/js/config.js' if getattr(settings, 'CKEDITOR_CONFIG_FILE', '') == '' else settings.CKEDITOR_CONFIG_FILE

class CKEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.get('attrs', {})
        attrs['class'] = 'django-ckeditor'
        kwargs['attrs'] = attrs

        self.ckeditor_config = kwargs.pop('ckeditor_config', 'default')
        
        kwargs['attrs']['data-config'] = self.ckeditor_config

        super(CKEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        rendered = super(CKEditor, self).render(name, value, attrs)

        return rendered

    def value_from_datadict(self, data, files, name):
        val = data.get(name, u'')
        r = re.compile(r"""(.*?)(\s*<br\s*/?>\s*)*\Z""", re.MULTILINE | re.DOTALL)
        m = r.match(val)
        return m.groups()[0].strip()

    class Media:
        js = (
            MEDIA + '/ckeditor/js/underscore.js',
            _CONFIG_FILE,
            MEDIA + '/ckeditor/ckeditor/ckeditor.js',
            MEDIA + '/ckeditor/js/init.js',
        )
        css = {
            'screen': (
                MEDIA + '/ckeditor/css/' + _CSS_FILE,
            ),
        }

class AdminCKEditor(admin_widgets.AdminTextareaWidget, CKEditor):
    pass

