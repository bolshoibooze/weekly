from __future__ import(
absolute_import, unicode_literals
) 



from django.db import models
from django.db.models import *
from django.contrib import auth
from django.dispatch import receiver
from django.db.models.signals import *
from django.contrib.auth.models import *
from django.contrib.auth.signals import *

from django.db.models.manager import EmptyManager
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

GENDER_CHOICES = (
   ('Male','Male'),
   ('Female','Female'),
)



        
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = CustomUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_admin = True
        u.save(using=self._db)
        return u
        
class ExtendedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
       verbose_name='email address',
       max_length=255,unique=True,
       db_index=True,
    )
    full_name = models.CharField(
       max_length=50,
       blank=True,null=True
    )
    gender = models.CharField(
       max_length=10,blank=True,null=True,
       choices=GENDER_CHOICES, 
       verbose_name='Gender'
    )
    photo = ImageField(
       upload_to='images/writers',
       blank=True,null=True
    )
    birthday = models.DateField(
       auto_now_add=False,
       blank=True,null=True
    )
    bio = models.CharField(
       max_length=300,
       blank=True,null=True
    )
    can_write = models.BooleanField(
       default=False
    )
    is_editor = models.BooleanField(
       default=False
    )
    is_fellow = models.BooleanField(
       default=False
    )
    is_active = models.BooleanField(
       default=True
    )
    is_admin = models.BooleanField(
       default=False
    )
    date_joined = models.DateTimeField(
       auto_now_add=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','gender']
    
    objects = CustomUserManager()
    
    class Meta(object):
        db_table = 'User Data'
        ordering = ['-can_write']
        unique_together = ('email', )
        verbose_name_plural = 'Users Data'
        
    def __unicode__(self):
        return self.full_name
        
    def get_full_name(self):
        pass 
        
    def get_short_name(self):
        #return self.full_name
        pass 
             
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)
        
    def can_edit(self):
        return ExtendedUser.objects.filter(is_editor=True)
     
    def is_a_writer(self):
        return ExtendedUser.objects.filter(can_write=True) 
             
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    #@property
    def is_staff(self):
        return self.is_admin
        
    def set_priveleges(self):
        objs = ExtendedUser.objects.all()  
        for obj in objs:
            
            if obj.is_staff==True:
               self.is_editor=True
               self.save()
          
    def save(self,*args,**kwargs):
        super(ExtendedUser,self).save(*args,**kwargs)


