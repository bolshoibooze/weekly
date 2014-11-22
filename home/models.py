from __future__ import(
absolute_import, unicode_literals
) 


import re
import math 
from django.db import models
from datetime import datetime
from django.db.models import *
from django.contrib import auth
from django.contrib.auth.models import *
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.utils.encoding import smart_unicode
from django.db.models.query import QuerySet
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.db.models import Manager
from weekly.settings import *

#from follow import utils
from sorl.thumbnail import ImageField
from django.contrib import comments
from django.contrib.comments import Comment
from notifications import notify

class Section(models.Model):
    name = models.CharField(
       max_length=50,db_index=True
    )
    about = HTMLField(
       max_length=350,null=True,
       blank=True
    )
    is_approved = models.BooleanField(
       default=False
    )
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    date = models.DateTimeField(
       auto_now_add=True
    )
    class Meta(object):
        db_table = 'Section'
        ordering = ['name','is_approved']
        verbose_name_plural = 'Sections'
        
    def  __unicode__(self):
         return self.name
         
    @property     
    def posts(self):
        return self.post_set.all()
        
         
    def get_post_set(self):
        return self.posts 
           
    def num_posts(self):
        return self.posts.count() 
         
    def last_post(self):
        if self.num_posts:
            return self.posts.order_by("pub_date")   
            
    def save(self,*args,**kwargs):
        super(Section,self).save(*args,**kwargs)
        



        

        
class ArticleManager(models.Manager):
    def stream(self):
        return self.filter(is_public=True)
        
    def live(self, user=None):
        """Retrieves all live articles"""

        qs = self.stream()

        if user is not None and user.is_superuser or user.is_staff:
            # superusers get to see all articles
            return self.filter(is_public=False)
        else:
            # only show live articles to regular users
            return self.filter(is_public=False)  
              
    def editor_picks(self):
        return self.filter(editors_pick=True)
        
    def most_read(self):
        return self.filter(editors_pick=True).order_by('-pub_date')
        

    def most_bookmarked(self):
        return self.all().order_by('-bookmark_count', '-pub_date')
        
    def next_article(self, user=None):
        """Retrieves all live articles"""
        return self.all().order_by('is_public','-pub_date')
        
    def posts(self):
        sections = Section.objects.filter(name=self.name)
        posts = Post.objects.filter(section__in=sections)
        return self.filter(section__in=sections)
        
    def by_section(self,section):
        return self.filter(section=section) 
           
    def by_author(self, user):
        return self.filter(user=user)
        
class Article(models.Model):
    title = models.CharField(
       max_length=50,db_index=True,
       verbose_name='Title'
    )
    section = models.ForeignKey(
       Section,related_name='sections',
       verbose_name='Section'
    )
    main_photo = ImageField(
       upload_to='article_photos',
       verbose_name='Main Photo'
    )
    overview = HTMLField(
       max_length=140
    )
    post = HTMLField(
        max_length=1000,
        verbose_name='Post'
    )
    slug = models.SlugField(
       max_length=50
    )
    editors_pick = models.BooleanField(
       default=False,verbose_name='Editors Pick'
    )
    is_public = models.BooleanField(
       default=False,verbose_name='Publish?'
    )
    enable_comments = models.BooleanField(
       default=True
    )
    views = models.PositiveIntegerField(default=0)
    reading_time = models.FloatField(
       default=0.00
    )
    bookmark_count = models.IntegerField(
       default=0
    ) 
    ratings_score = models.IntegerField(
       default=0
    )
    pub_date = models.DateTimeField(
       default=datetime.datetime.now()
    )
    author = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='articles'
    )
    objects = ArticleManager()
    class Meta(object):
        db_table = 'Story'
        ordering = ['-pub_date']
        verbose_name_plural = 'Stories'
        
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('article', (), {'author':self.author.full_name, 'slug': self.slug })

        
    @permalink
    def get_edit_url(self):
        #return ('views.view_something_edit', (), {'slug': self.slug})
        pass
    
    @property        
    def authorized_writers(self):
        today = datetime.date.today() 
        objs = Article.objects.filter(pub_date__gte=today) 
        for obj in objs:
            if obj.author.can_write == True:
               self.is_public=True
               self.save()
    
    def get_next_article(self):
        """Determines the next live article"""

        if not self._next:
            try:
                qs = Article.objects.live().exclude(id__exact=self.id)
                article = qs.filter(pub_date__gte=self.pub_date).order_by('pub_date')[0]
            except (Article.DoesNotExist, IndexError):
                article = None
            self._next = article

        return self._next   
    
    def update_bookmark_count(self):
        self.bookmark_count = self.bookmarks.count() or 0
        self.save()
                         
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        #if not self.created:self.views = F('views') + 1self.save()
        super(Article,self).save(*args,**kwargs)
  
        
class Bookmark(models.Model):
    article = models.ForeignKey(
       Article, related_name='bookmarks'
    )
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    date = models.DateTimeField(
       auto_now_add=True
    )

    class Meta:
        db_table = 'Bookmark'
        ordering = ('-date',)
        verbose_name_plural='Bookmarks'

    def __unicode__(self):
        return "%s bookmarked by %s" % (self.article, self.user)

    def save(self, *args, **kwargs):
        super(Bookmark, self).save(*args, **kwargs)
        self.article.update_bookmark_count()

    def delete(self, *args, **kwargs):
        super(Bookmark, self).delete(*args, **kwargs)
        self.article.update_bookmark_count()   
        
        
        
class NotificationsManager(models.Manager):
    def unread(self):
        "Return only unread items in the current queryset"
        return self.filter(unread=True)
    
    def update_or_create(self, **kwargs):
        #https://code.djangoproject.com/attachment/ticket/20429/upsert.py
        obj, created = self.get_or_create(**kwargs)
        if not created and "defaults" in kwargs:
            for k, v in kwargs.get("defaults", {}).items():
                if k not in dir(obj):
                    raise AttributeError("Invalid attribute %s provided for update on %s (%d)" % (k, type(obj), obj.pk))

                setattr(obj, k, v)
            obj.save()

        return obj, created
            
    def get_unread(self):
        return self.unread().count()
        
    def read(self):
        "Return only read items in the current queryset"
        return self.filter(unread=False)
        
    def mark_all_as_read(self, recipient=None):
        """Mark as read any unread messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        # We want to filter out read ones, as later we will store 
        # the time they were marked as read.
        qs = self.unread()
        if recipient:
            qs = qs.filter(recipient=recipient)
        
        qs.update(unread=False)
    
    def mark_all_as_unread(self, recipient=None):
        """Mark as unread any read messages in the current queryset.
        
        Optionally, filter these by recipient first.
        """
        qs = self.read()
        
        if recipient:
            qs = qs.filter(recipient=recipient)
            
        qs.update(unread=True)
                          
class Notice(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL, 
       related_name='notice'
    )
    unread = models.BooleanField(
       default=True
    )
    title = models.CharField(
       max_length=50
    )
    description = models.TextField(
       max_length=200,
       blank=True, null=True
    )
    unfollow = models.BooleanField(
       default =False
    )
    timestamp = models.DateTimeField(
       auto_now_add=True
    )
    
    objects = NotificationsManager()
    
    class Meta(object):
        db_table = 'Notification'
        ordering = ['-timestamp']
        verbose_name_plural = 'Notifications'
        
    def __unicode__(self):
        return unicode(self.user)
        
        
    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()
  
                    
    def save(self,*args,**kwargs):
        super(Notice,self).save(*args,**kwargs)
        
   
