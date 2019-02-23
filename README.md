# Djaptcha

Djaptcha is a Django plugin that implements the `captcha` python package by `lepture`. It is designed to store user sessions in the database and generate random captcha images based on these sessions.

## Installation

If you haven't already, `pip install captcha` and then use the following to install `djaptcha`:

```bash
$ pip install djaptcha
```

Now add `djaptcha` to the list of installed plugins in your Django app.

```python
INSTALLED_APPS = [
    ...
    'djaptcha',
    ...
]
```

*__Note__: You must have sessions enabled and configured in your django app to use this plugin. You also must have configured a database. End users must have cookies enabled in their browser to be able to generate captcha images.*

Finally, run `python manage.py make_migrations` and `python manage.py migrate` to create the djaptcha database models.

## Settings

It's recommended that you change the following settings to suit your specific project needs:
```python
# These are the default values
DJAPTCHA_MAX_TRIES = 10 # Maximum amount of tries before user can't generate new captchas
DJAPTCHA_LENGTH = 6 # Length of the captcha (example: 'F7W8MG' has a length of 6)
DJAPTCHA_CHARACTERS = 'ABCEFGHJKLMNPRSTUVWXYZ' # Characters allowed in the captcha
DJAPTCHA_URL = STATIC_URL + 'captcha/' # The URL that end users can access captcha images at
DJAPTCHA_DIR = 'static/captcha/' # The local directory your captcha images should be stored in
DJAPTCHA_EXPIRY = 5 # Length in minutes before the captcha and image are deleted
DJAPTCHA_COOKIES_TEMPLATE = 'djaptcha/cookies.html' # The template that tells users to enable cookies
```

## Usage

To add a captcha field to your form you need to follow these steps:

1. Add the `CaptchaMixin` to your View class. *`CaptchaMixin` should be on the far left to ensure it's methods have priority*
```python
from djaptcha.views import CaptchaMixin

class MyView(CaptchaMixin, FormView):
    form_class = MyForm
    # View logic here
```

2. Add the `CaptchaForm` to your Form class. *`CaptchaForm` should be on the far left to ensure the captcha is validated before any other data.*
```python
from djaptcha.forms import CaptchaForm

class MyForm(CaptchaForm, Form)
    # Form fields and logic here.
    pass
```

3. Djaptcha also provides some context variables to use in your views. You can use them like so in your form templates:
```html
<!--
    captcha_refresh_link : a path to the url that will refresh the captcha image
    captcha_retries : the number of retries the user has left
-->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <p><a href="{{ captcha_refresh_link }}">Refresh</a></p>
    <p>{{ captcha_retries }} retries left.</p>
    <button type="submit">Submit</button>
</form>
```
