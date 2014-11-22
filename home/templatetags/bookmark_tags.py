from django import template

from home.models import Bookmark
register = template.Library()


@register.filter
def is_bookmarked(article, user):
    """
    {% if article|is_bookmarked:request.user %}
        already bookmarked
    {% else %}
        not bookmarked yet
    {% endif %}
    """
    if not user.is_authenticated():
        return False
    return Bookmark.objects.filter(article=article, user=user).exists()



