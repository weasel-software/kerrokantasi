
from kerrokantasi.settings import *

# Get whitenoise for serving static files

if 'MIDDLEWARE' in locals():
    try:
        place = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    except ValueError:
        place = 0
    
    MIDDLEWARE.insert(place, 'whitenoise.middleware.WhiteNoiseMiddleware')

elif 'MIDDLEWARE_CLASSES' in locals():
    try:
        place = MIDDLEWARE_CLASSES.index('django.middleware.security.SecurityMiddleware')
    except ValueError:
        place = 0
    
    MIDDLEWARE_CLASSES.insert(place, 'whitenoise.middleware.WhiteNoiseMiddleware')    
else:
    MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware']

import environ

deploy_env = environ.Env(
    USE_X_FORWARDED_HOST = (bool, False),
    SECURE_PROXY = (bool, False)
)

USE_X_FORWARDED_HOST = deploy_env('USE_X_FORWARDED_HOST')

if deploy_env('SECURE_PROXY'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

