from django import template
from cryptography.fernet import Fernet
from django.conf import settings

register = template.Library()

@register.filter
def replaceBlank(value, stringVal=""):
    """Replaces specified string in value with an empty string"""
    value = str(value).replace(stringVal, '')
    return value

@register.filter
def encryptdata(value):
    """Encrypts the given value using Fernet encryption"""
    fernet = Fernet(settings.ID_ENCRYPTION_KEY)
    encrypted_value = fernet.encrypt(str(value).encode())
    return encrypted_value
  