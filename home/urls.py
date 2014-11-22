from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse,resolve
from .models import *
from .views import *


urlpatterns = patterns('home.views',

    #url(r'^stream/$', ArticleListView.as_view(), name='stream'),
        
    #url(r'^post/(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='post'),
    
    url(r'^stream/$', PostListView.as_view(), 
        name='stream'),
        
    url(r'^unpublished/$', UnPublishedListView.as_view(), 
        name='unpublished'),
          
    url(r'^article/(?P<slug>[a-zA-Z0-9-]+)/$', PostDetailView.as_view(),
        name='article'),
        
        
    
    url(r'^edit_article/(?P<slug>[a-zA-Z0-9-]+)/$',ArticleEditView.as_view(),
        name='edit_article'),
        
        
    url(r'^review_article/(?P<slug>[a-zA-Z0-9-]+)/$',UnPublishedEditView.as_view(),
        name='review_article'),
               
    url(r'^popular/$', MostReadListView.as_view(), 
        name='popular'),
        
    url(r'^sections/$', SectionListView.as_view(), 
        name='sections'),
        
        
    url(r'^section_articles/$',ArticleSections.as_view(),
        name='section_articles'),
           
    url(r'^create/$', ArticleCreateView.as_view(), 
        name='create'),
        
    url(r'^all/$',NotificationListView.as_view(),
        name='all'),
    
    url(r'^mark_as_read/$','mark_as_read',name='mark_as_read'),        
    #Human-Friendly URLs 
    
    url(r'^authors/$', AuthorListView.as_view(), 
        name='authors'),
        
    url(r'^/$', AuthorDetailView.as_view(), 
        name='author_profile'),
        
    url(r'^quick/$',QuickListView.as_view()),
    
    url(r'^get_sections/$','list_sections',
        name='get_sections'),
    
    url(r'^my_bookmarks/$',UserBookmarks.as_view(),
        name='my_bookmarks'),
        
    url(r'^$','user_bookmarks',name='article_user_bookmarks'),
        
    #url(r'^add/(?P<article_id>)/$','add_bookmark',name='bookmark_add'),
    url(r'^add/(?P<slug>[a-zA-Z0-9-]+)/$','add_bookmark',name='bookmark_add'),
       
    url(r'^delete/(?P<slug>[a-zA-Z0-9-]+)/$','delete_bookmark',name='bookmark_delete'),
        
   
    
    
)
