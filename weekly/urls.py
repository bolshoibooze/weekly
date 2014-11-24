from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.comments.feeds import *


from django.contrib import admin
admin.autodiscover()

from yawdadmin import admin_site
admin_site._registry.update(admin.site._registry)

urlpatterns = patterns('',
    #url(r'^$',IndexRedirectView.as_view()),
    
    url(r'^home/', include('home.urls')),
    
    url(r'^photos/', include('photos.urls')),
    
    #url(r'^articles/',include('articles.urls')),
    
    url(r'^about/', include('about.urls')),
    
    url(r'^users/', include('users.urls')),
    
    url(r'^tinymce/', include('tinymce.urls')),
    
    url(r'^ua_detector/',include('ua_detector.urls')),
    
    url(r'^post/comments/', include('fluent_comments.urls')),
    
    url('^inbox/notifications/', include('notifications.urls')),
    #url(r'^comments/', include('django.contrib.comments.urls')),
    
    #url('', include('social.apps.django_app.urls', namespace='social')),
    
    #url('^', include('follow.urls')),
    
    
    
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
