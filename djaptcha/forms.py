import uuid

from django.forms import Form
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from djaptcha.models import Captcha

from . import fields


class CaptchaForm(Form):
    djaptcha_errors = {
        'invalid_captcha': _("Please try the captcha again."),
    }

    def __init__(self, session_key, *args, **kwargs):
        """Pass the session_key to the widget so it can load the image."""
        super().__init__(*args, **kwargs)
        self.fields['captcha'].widget.set_session(session_key)

    def clean(self):
        """Verify guess is right."""
        guess = self.cleaned_data.get('answer')
        session_id = self.fields['captcha'].widget.session_id
        captcha = Captcha.objects.get(pk=session_id)

        if not captcha.verify(guess):
            raise ValidationError(self.djaptcha_errors['invalid_captcha'])

        return super().clean()
