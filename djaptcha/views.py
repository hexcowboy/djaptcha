from django import views
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from djaptcha.models import Captcha

def generate_captcha(request):
    if request.session.test_cookie_worked():
        captcha = Captcha.objects.get_captcha_or_generate(request)
        if request.GET.get('refresh', False) == 'True':
            captcha.generate(refresh=True)
    else:
        # Returns a redirect to the 'enable cookies' page.
        return render(request, settings.DJAPTCHA_COOKIES_TEMPLATE)

    return redirect(request.GET.get('next', None))


class CaptchaMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.session.test_cookie_worked():
            # Initialize the captcha
            self.get_captcha()
        else:
            # Set test cookie and redirect to captcha generate view
            request.session.set_test_cookie()
            return redirect(self.get_captcha_generate_url())

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['session_key'] = self.request.session.session_key
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_refresh_link'] = self.get_captcha_generate_url(refresh=True)
        context['captcha_retries'] = self.get_captcha().retries
        return context

    def get_captcha_generate_url(self, refresh=False):
        generate_url = reverse_lazy('djaptcha:generate')
        next_page = self.request.path
        return f"{generate_url}?next={next_page}&refresh={refresh}"

    def get_captcha(self):
        return Captcha.objects.get_captcha_or_generate(self.request)
