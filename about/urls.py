from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from .models import *
from .views import *


urlpatterns = patterns('places.views',

    url(r'^about/$', AboutListView.as_view(), 
        name='about'),
        
    url(r'^detail/(?P<pk>\d+)/$', StyleDetailView.as_view(), 
        name='detail'),
        
        
    url(r'^start_writing/$',StyleGuideListView.as_view(),
        name='start_writing'), 
        
    url(r'^terms/$',TermsListView.as_view(),
        name='terms'),
        
              
    url(r'^faqs/$',FaqListView.as_view(),
        name='faqs'),
        
    #url(r'^/$',.as_view(),name=''),
        
        
    #url(r'^/$',.as_view(),name=''),
        
    #url(r'^/$',.as_view(),name='')         
                        
            
)
