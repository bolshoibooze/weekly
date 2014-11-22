# -*- coding: utf-8 -*-
from django.template import Library
from django.template.base import TemplateSyntaxError
from django.template import Node
from home.models import Notify

register = Library()

@register.assignment_tag(takes_context=True)
def get_unread_count(context):
    if 'user' not in context:
        return ''
    
    user = context['user']
    notifications = Notice.objects.get_unread()
    return notifications
    
