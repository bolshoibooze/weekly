from django.dispatch import receiver
from django.contrib import comments
from django.dispatch import receiver
from django.contrib.comments import Comment

from home.models import Notice

# https://djangosnippets.org/snippets/1539/raw/

def new_comment_notifier(sender, comment, request, *args, **kwargs):
    """
    Signal to notify new saved comments.

    Example:
        from django.contrib.comment import models, signals
        signals.comment_was_posted.connect(new_comment_notifier,
            sender=models.Comment)
    """

    # get the new comment url
    site = Site.objects.get_current()
    content_object = comment.content_object
    url = 'http://%s?c=%d' % (site.domain + content_object.get_absolute_url(),
        comment.id)

    # send the mail message
    subject = "New comment posted on '%s'" % str(content_object)
    message = "%s:\n%s" % (subject, url)
    mail_admins(subject, message)
    
    
    
