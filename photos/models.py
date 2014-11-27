from __future__ import(
absolute_import, unicode_literals
) 


import re
import math 
import datetime
from django.db import models
from django.db.models import *
from django.contrib import auth
from django.contrib.auth.models import *
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.db.models.query import QuerySet
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.db.models import Manager
from weekly.settings import *

#from follow import utils
from sorl.thumbnail import ImageField



class PhotoManager(models.Manager):
   
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
        
    def most_popular(self):
        return self.all().order_by('-views', '-pub_date')

   
    def by_author(self, user):
        return self.filter(user=user)
        
class Photo(models.Model):
    caption = models.CharField(
       max_length=140
    )
    main_photo = models.ImageField(
       upload_to='funny_photos',
       verbose_name='Photo'
    )
    post = HTMLField(
       max_length=300,
       null=True,blank=True
    )
    slug = models.SlugField(
       max_length=50
    )
    editors_pick = models.BooleanField(
       default=False,verbose_name='Editors Pick'
    )
    is_public = models.BooleanField(
       default=True,verbose_name='Publish?'
    )
    enable_comments = models.BooleanField(
       default=True
    )
    views = models.IntegerField(
       default=0
    )
    ratings_score = models.IntegerField(
       default=0
    )
    pub_date = models.DateTimeField(
       auto_now_add=True
    )
    author = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='photos'
    )
    objects = PhotoManager()
    
    class Meta(object):
        db_table = 'Funny Pic'
        ordering = ['-pub_date']
        verbose_name_plural = 'Funny Pic'
        
    def __unicode__(self):
        return smart_unicode(self.author)

    @models.permalink
    def get_absolute_url(self):
        return ('photos', (), { 'slug': self.slug })

        
    @permalink
    def get_edit_url(self):
        #return ('views.view_something_edit', (), {'slug': self.slug})
        pass
    
    
    def get_next_photo(self):
        """Determines the next live article"""

        if not self._next:
            try:
                qs = Photo.objects.live().exclude(id__exact=self.id)
                article = qs.filter(pub_date__gte=self.pub_date).order_by('pub_date')[0]
            except (Photo.DoesNotExist, IndexError):
                article = None
            self._next = article

        return self._next   
    
    
                         
    def save(self,*args,**kwargs):
        self.slug = slugify(self.caption)
        super(Photo,self).save(*args,**kwargs)
        
        
    
