from datetime import datetime, timedelta

from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid Token')
        if (hasattr(token.user, 'is_active')) and (not token.user.is_active):
            raise AuthenticationFailed('Inactive User')
        (now, expiry) = (datetime.now(), settings.AUTHENTICATION_TOKEN_EXPIRY)
        if not isinstance(expiry, timedelta):
            raise ValueError(
                "TOKEN_EXPIRY variable must be a timedelta instance")
        if (token.created + expiry) > now:
            raise AuthenticationFailed('Token Expired')
        return super().authenticate_credentials(key)
