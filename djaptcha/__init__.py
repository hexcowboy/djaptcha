from django.conf import settings

djaptcha_settings = {
    "DJAPTCHA_MAX_TRIES": 10, # Maximum amount of tries before user can't generate new captchas
    "DJAPTCHA_LENGTH": 6, # Length of the captcha (example: 'F7W8MG' has a length of 6)
    "DJAPTCHA_CHARACTERS": 'ABCEFGHJKLMNPRSTUVWXYZ', # Characters allowed in the captcha
    "DJAPTCHA_URL": f'{settings.STATIC_URL}captcha/', # The URL that end users can access captcha images at
    "DJAPTCHA_DIR": 'static/captcha/', # The local directory your captcha images should be stored in
    "DJAPTCHA_EXPIRY": 5, # Length in minutes before the captcha and image are deleted
    "DJAPTCHA_COOKIES_TEMPLATE": 'djaptcha/cookies.html', # The template that tells users to enable cookies
}

for setting, value in djaptcha_settings.items():
    setattr(settings, setting, value)
