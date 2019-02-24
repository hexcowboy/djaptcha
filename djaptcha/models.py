import datetime, os, secrets, uuid

from captcha.image import ImageCaptcha

from hashlib import md5

from django.conf import settings
from django.db import models
from django.dispatch import receiver


class CaptchaManager(models.Manager):

    def all_expired(self):
        """Get all records older than the expiry length."""
        expiry_length = settings.DJAPTCHA_EXPIRY
        expiry_time = datetime.datetime.now() \
                    - datetime.timedelta(minutes=expiry_length)
        return super().get_queryset().filter(created__gte=expiry_time)

    def get_captcha_or_generate(self, request):
        """Get the Captcha object based on the request."""
        key = request.session.session_key

        try:
            captcha = Captcha.objects.get(pk=key)
        except Captcha.DoesNotExist:
            captcha = Captcha(pk=key)

        captcha.generate(refresh=False)
        return captcha


class Captcha(models.Model):
    """
    The Captcha model contains data about the session id,
    the secret, the time it was created, and the amount
    of retries.
    """
    id = models.CharField(
        primary_key=True,
        max_length=32,
        editable=False)
    secret = models.CharField(
        max_length=settings.DJAPTCHA_LENGTH)
    created = models.DateTimeField(
        auto_now=True)
    retries = models.PositiveSmallIntegerField(
        default=settings.DJAPTCHA_MAX_TRIES)

    # Manager class
    objects = CaptchaManager()

    def __str__(self):
        return f'Secret for session {self.id} is {self.secret}.'

    def generate(self, refresh=True):
        """Generate the secret"""
        if self.retries <= 0:
            return False

        # Only generate if it's the first time creating the secret or
        # if the secret needs to be refreshed
        if not self.secret or refresh:
            if refresh:
                self.retries -= 1

            chars = settings.DJAPTCHA_CHARACTERS
            length = settings.DJAPTCHA_LENGTH
            self.secret = ''.join(secrets.choice(chars) for _ in range(length))
            self.generate_image()
            self.save()

    def generate_image(self):
        """Generates image based on secret and stores it in DJAPTCHA_LOCATION"""
        path = self.get_image_url(local=True)
        image = ImageCaptcha()
        image.generate(self.secret)
        image.write(self.secret, path)

    def get_image_url(self, local=False):
        return f'{settings.DJAPTCHA_DIR if local else settings.DJAPTCHA_URL}{self.id}{self.retries}.png'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def verify(self, guess):
        correct = self.secret == guess

        if not correct:
            self.generate(refresh=True)

        return correct


@receiver(models.signals.post_delete, sender=Captcha)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Captcha` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Captcha)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old image from filesystem
    when corresponding `Captcha` object is updated
    with a new image.
    """
    if not instance.pk:
        return False

    try:
        old_image = Captcha.objects.get(pk=instance.pk).get_image_url(local=True)
    except Captcha.DoesNotExist:
        return False

    new_image = instance.get_image_url(local=True)
    if not old_image == new_image:
        if os.path.isfile(old_image):
            os.remove(old_image)
