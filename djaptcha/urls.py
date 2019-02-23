from django.urls import path

from djaptcha import views

app_name = 'djaptcha'
urlpatterns = [
    # Generate should only be accessed from the CaptchaMixin view.
    # Don't link to this from anywhere else unless you're sure.
    # Otherwise, from djaptcha.views import CaptchaMixin,
    # and add it as the first parent of your View,
    # eg. MyView(CaptchaMixin, FormView):
    path('generate', views.generate_captcha, name='generate'),
]
