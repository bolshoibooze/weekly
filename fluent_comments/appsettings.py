from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


USE_THREADEDCOMMENTS = 'threadedcomments' in settings.INSTALLED_APPS

FLUENT_COMMENTS_REPLACE_ADMIN = getattr(settings, "FLUENT_COMMENTS_REPLACE_ADMIN", True)


FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION = getattr(settings, 'FLUENT_COMMENTS_USE_EMAIL_NOTIFICATION', True)  # enable by default
FLUENT_COMMENTS_CLOSE_AFTER_DAYS = getattr(settings, 'FLUENT_COMMENTS_CLOSE_AFTER_DAYS', None)
FLUENT_COMMENTS_MODERATE_AFTER_DAYS = getattr(settings, 'FLUENT_COMMENTS_MODERATE_AFTER_DAYS', None)

FLUENT_COMMENTS_EXCLUDE_FIELDS = getattr(settings, 'FLUENT_COMMENTS_EXCLUDE_FIELDS', ()) or ()


if FLUENT_COMMENTS_EXCLUDE_FIELDS:
    # The exclude option only works when our form is used.
    # Allow derived packages to inherit our form class too.
    if not hasattr(settings, 'COMMENTS_APP') or settings.COMMENTS_APP == 'comments':
        raise ImproperlyConfigured("To use 'FLUENT_COMMENTS_EXCLUDE_FIELDS', also specify: COMMENTS_APP = 'fluent_comments'")
