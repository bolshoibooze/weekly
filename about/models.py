from __future__ import(
absolute_import, unicode_literals
) 



import datetime
from django.db import models
from django.db.models import *
from django.contrib import auth
from django.contrib.auth.models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.db.models.query import QuerySet
from tinymce.models import HTMLField
from django.db.models import Manager
from sorl.thumbnail import ImageField
from weekly.settings import *
#from follow import utils






class About(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    title = models.CharField(
       max_length=50,
       verbose_name='Title'
    )
    image = ImageField(
       upload_to='images/about',
       verbose_name='Photo'
    )
    post = HTMLField(
       max_length=350
    )
    date = models.DateTimeField(
       auto_now_add=True
    )
    class Meta(object):
        db_table = 'About'
        verbose_name_plural='About'
        
    def __unicode__(self):
        return smart_unicode(self.user)
        
    def save(self,*args,**kwargs):
        super(About,self).save(*args,**kwargs)
        
#class Writer(models.Model):
        
class StyleGuide(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    title = models.CharField(
       max_length=50,
       verbose_name='Title'
    )
    image = ImageField(
       upload_to='images/style',
       verbose_name='Photo'
    )
    post = HTMLField(
       max_length=500,
       verbose_name='Style Guide'
    )
    date = models.DateTimeField(
       auto_now_add=True
    )
    class Meta(object):
        ordering = ['-date']
        db_table = 'Style Guide'
        verbose_name_plural='Style Guide'
        
    def __unicode__(self):
        return smart_unicode(self.user)
        
    def save(self,*args,**kwargs):
        super(StyleGuide,self).save(*args,**kwargs)
        
        
class Terms(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    title = models.CharField(
       max_length=50,
       verbose_name='Title'
    )
    image = ImageField(
       upload_to='images/terms',
       verbose_name='Photo'
    )
    post = HTMLField(
       max_length=500,
       verbose_name='Terms'
    )
    date = models.DateTimeField(
       auto_now_add=True
    )
    class Meta(object):
        ordering = ['-date']
        db_table = 'Term'
        verbose_name_plural='Terms'
        
    def __unicode__(self):
        return smart_unicode(self.user)
        
    def save(self,*args,**kwargs):
        super(Terms,self).save(*args,**kwargs)
    
    
class Faq(models.Model):
    user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='+'
    )
    qstn = models.TextField(
       max_length=150,
       verbose_name='Question'
    )
    answer = models.TextField(
       max_length=500,
       verbose_name='Answer'
    )
    date = models.DateTimeField(
       auto_now_add=True
    )
    class Meta(object):
        ordering = ['-date']
        db_table = 'Faq'
        verbose_name_plural='Faqs'
        
    def __unicode__(self):
        return smart_unicode(self.user)
        
    def save(self,*args,**kwargs):
        super(Faq,self).save(*args,**kwargs)
    
    
               
