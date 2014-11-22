from __future__ import absolute_import
from django.contrib.auth.decorators import login_required 
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from .models import *
from .views import *


urlpatterns = patterns('accounts.views',

    url(r'^login/$',LoginView.as_view(),
        name = 'login'),
    
    
    url(r'^logout/$',MyLogoutView.as_view(),
        name = 'logout'),
    
      
    #url(r'^signup/$',StepOneView.as_view(),name = 'signup'),
    
    url(r'^register/$',TestView.as_view()),
        
    url(r'^signup/$',RegistrationView.as_view(),name = 'signup'),
    
        
    url(r'^redirect/$',RegSuccessView.as_view(),
        name = 'redirect'),
    
    url(r'^change_pin/(?P<pk>\d+)/$',ChangePasswordFormView.as_view(),
        name='change_pin'),
        
    url(r'^freeze/(?P<pk>\d+)/$',FreezeAccountView.as_view(),
        name='freeze'),
    
    url(r'^myprofile/$',ProfileTemplateView.as_view(),
        name='myprofile'),
        
    url(r'^edit_profile/(?P<pk>\d+)/$',EditProfileView.as_view(),
        name='edit_profile'),
        
   url(r'^profilepage/(?P<username>.*[^/])/$', UserProfileDetailView.as_view(),
        name='profilepage'),
        
    
        
    #url(r'^edit_idnum/(?P<pk>\d+)/$',ChangeIdNumberView.as_view(),name='edit_idnum'),


)
