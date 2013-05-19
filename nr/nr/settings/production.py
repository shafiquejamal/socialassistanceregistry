from .base import *
DEBUG = False
ALLOWED_HOSTS = ['.socialassistanceregistry.com']

EMAIL_BACKEND = 'nr.sendmailemailbackend.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "admin@socialassistanceregistry.com"
