import os.path

from django.conf import settings
from django.forms import widgets

from djaptcha.models import Captcha


class CaptchaWidget(widgets.Widget):
    input_type = None
    template_name = 'djaptcha/forms/widgets/captcha.html'

    def __init__(self, attrs=None):
        self.session_id = None
        super().__init__(attrs)

    def set_session(self, session_id):
        """The session is set to get the image_path context"""
        self.session_id = session_id

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        captcha_object = Captcha.objects.get(pk=self.session_id)
        context['widget']['image_url'] = captcha_object.get_image_url()
        return context
