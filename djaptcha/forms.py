import uuid

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from djaptcha.widgets import CaptchaWidget
from djaptcha.models import Captcha


class CaptchaForm(forms.Form):
    djaptcha_errors = {
        'invalid_captcha': _("Please try the captcha again."),
        'max_retries': _("You ran out of retries."),
    }

    captcha = forms.Field(
        required=False,
        widget=CaptchaWidget,
    )
    answer = forms.CharField(
        required=True,
        max_length=settings.DJAPTCHA_LENGTH,
        min_length=settings.DJAPTCHA_LENGTH,
        widget=forms.TextInput()
    )

    def __init__(self, session_key, *args, **kwargs):
        """Pass the session_key to the widget so it can load the image."""
        super().__init__(*args, **kwargs)
        self.fields['captcha'].widget.set_session(session_key)

    def clean(self):
        """Verify guess is right."""
        guess = self.cleaned_data.get('answer')
        session_id = self.fields['captcha'].widget.session_id
        captcha = Captcha.objects.get(pk=session_id)

        if captcha.retries <= 0:
            raise ValidationError(self.djaptcha_errors['max_retries'])

        if not captcha.verify(guess):
            raise ValidationError(self.djaptcha_errors['invalid_captcha'])

        return super().clean()
