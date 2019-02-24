from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.forms.fields import CharField, Field
from django.utils.translation import gettext as _

from djaptcha.models import Captcha
from djaptcha.widgets import CaptchaWidget


class CaptchaField(Field):
    captcha_errors = {
        'max_retries': _("You ran out of retries."),
    }

    def __init__(self, **kwargs):
        super().__init__(required=False, disabled=True, widget=CaptchaWidget,
            **kwargs)

    def validate(self, value):
        session_id = self.widget.session_id
        captcha = Captcha.objects.get(pk=session_id)

        if captcha.retries <= 0:
            raise ValidationError(self.captcha_errors['max_retries'])

        super().validate(value)


class CaptchaAnswerField(CharField):
    def __init__(self, **kwargs):
        super().__init__(
            max_length=settings.DJAPTCHA_LENGTH,
            min_length=settings.DJAPTCHA_LENGTH,
            widget=TextInput(),
            **kwargs
        )
