from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from .models import *
from .views import *


urlpatterns = patterns('photos.views',

    
    url(r'^all/$', PhotoListView.as_view(), 
        name='all'),
        
    
    url(r'^post_photo/$', PostPhotoView.as_view(), 
        name='post_photo'),
             
    url(r'^photo/(?P<slug>[a-zA-Z0-9-]+)/$', PhotoDetailView.as_view(),
        name='photo'),
   
)
