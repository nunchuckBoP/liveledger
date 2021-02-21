from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_user(value):
    # check if value is a username or if it is a valid
    # email address
    if not(User.objects.filter(username=value).exists() or \
        User.objects.filter(email=value)):
            raise ValidationError(
            _('%(value)s is not a valid user'),
            params={'value': value},
        )