from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """
    Authenticates users by email address instead of username.

    Django's default backend looks up by username; this one performs a
    case-insensitive email lookup first, then delegates password checking
    and active-status verification to the parent class.

    Register in settings.py:
        AUTHENTICATION_BACKENDS = [
            "nexusApp.backends.EmailBackend",
            "django.contrib.auth.backends.ModelBackend",  # fallback for admin
        ]
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # `username` holds the email address when called from EmailLoginForm
        email = (username or kwargs.get("email", "")).strip().lower()

        if not email or not password:
            return None

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Run the default password hasher to mitigate timing attacks
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Defensive: if duplicate emails somehow exist, deny access
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
