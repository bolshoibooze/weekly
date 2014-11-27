from django import forms
from django.forms import *
from django import template
from django.forms.fields import *
from django.forms.widgets import *
from django.forms import ModelForm
from django.template import loader



from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.forms.util import ValidationError
from django.contrib.auth.forms import *
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db.models.fields.files import *
from django.db.models import *

from django.contrib.auth.models import *
from form_utils.widgets import *
from form_utils.fields import *
from weekly.settings import *
from .models import *
from .date_widget import *
from .models import *


GENDER = (
   ('Male','Male'),
   ('Female','Female'),   
)   

# : AuthenticationForm utilizes value set in USER_NAME_FIELD.

#<https://djangosnippets.org/snippets/1228/>
def clean_unique(form, field, exclude_initial=True, 
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value
    

attrs_dict = {'class': 'required'}

GENDER_CHOICES = (
   ('Female','Female'),
   ('Male','Male'),
   
)

class MyUserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("That email already exists."),
        'password_mismatch': _("Passwords don't match'."),
    }
    email = forms.CharField(
       label=_("email"), max_length=30
    )
    password1 = forms.CharField(
       max_length=50,
       label=_("Set Password"),
       widget=forms.PasswordInput
    )
    birthday = forms.DateField(
       initial='Format:day-month-Year',
       input_formats=['%d-%m-%Y',], 
       label=_('Date of Birth')
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class':'choices'}),
        label=_('Gender')
    )
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'fileUpoad'
        
    class Meta(object):
        model = ExtendedUser
        fields = (
        'email','full_name',
        'photo','birthday','gender'
        ) 
       
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) == 0:
            raise forms.ValidationError('Please enter a password')
        return password1
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        
        if len(full_name) > 50:
            raise ValidationError(_('Your name should not exceed 50 characters'))
        return full_name
            
    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email': _("That email already exists."),
        'password_mismatch': _("Passwords don't match'."),
    }
    email = forms.CharField(
       label=_("email"), max_length=30
    )
    password1 = forms.CharField(
       max_length=50,
       label=_("Set Password"),
       widget=forms.PasswordInput
    )
    birthday = forms.DateField(
       initial='Format:day-month-Year',
       input_formats=['%d-%m-%Y',], 
       label=_('Date of Birth')
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class':'choices'}),
        label=_('Gender')
    )
    bio = forms.CharField(
        max_length=500,label='Bio',
        widget=forms.Textarea(attrs={'rows':60,'cols':20}),
        initial = 'Optional,you can skip this'
        
    )
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'fileUpoad'
       
        
        
    class Meta:
        model = ExtendedUser
        
        fields = (
        "full_name","gender","email",
        "photo","birthday","bio"
    
        )
        
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        #validate content type
        main, sub = photo.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')
        
        
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1", "")
        if len(password1) == 0:
            raise forms.ValidationError('Please enter a password')
        return password1
        
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        
        if len(full_name) > 50:
            raise ValidationError(_('Your name should not exceed 50 characters'))
        return full_name
        
          
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class EditProfileForm(forms.ModelForm):
    email = forms.CharField(
       label=_("email"), max_length=30
    )
    bio = forms.CharField(
       max_length=250,label='About me',
       #widget=forms.Textarea(attrs={'rows':15,'cols':20}),
       widget=AutoResizeTextarea()
    )
    photo = forms.ImageField(
       widget=ImageWidget()
    )
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs['class'] = 'fileUpoad'
        
    class Meta(object):
        model = ExtendedUser
        fields = (
        'bio','photo','email'
        )
        
    def clean_photo(self):
        photo = self.cleaned_data['photo']
        #validate content type
        main, sub = photo.content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')
    

        
class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = ExtendedUser
      
                           

        
    
               
class MyAuthForm(AuthenticationForm):
    pass 
    
    error_messages = {
        'invalid_login': _("Please enter your registred email. "
                           ),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(MyAuthForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if not self.fields['username'].label:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'] % {
                        'username': self.username_field.verbose_name
                    })
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    #throws errors:to be deleted
    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


               
class FreezeAccountForm(forms.ModelForm):
    """set account to inactive"""
    
    password = forms.CharField(
       max_length=4,
       widget=forms.PasswordInput,
       label=_('Current PIN')
    )
    #is_active = forms.BooleanField(label=('Active Status'))
    class Meta:
        model = User
        fields = ['password','is_active']
        
    #def save(self):
        #obj = UserAccount.objects.update(
          #is_active = self.cleaned_data['is_active']
        #)
        #obj.user = request.user
        #obj.save()
    
    
class MyPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two PINs  didn't match."),
    }
    old_password = forms.CharField(
       label=_("Current PIN"),
       widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
       label=_("New PIN"),
       widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
       label=_("Confirm PIN"),
       widget=forms.PasswordInput
    )
    
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
   
    def clean_old_password(self):
        UserModel = get_user_model()
        old_password = self.cleaned_data["old_password"]
        self.users_cache = UserModel._default_manager.filter(
        password__iexact=password
        )
        if not len(self.users_cache):
            raise forms.ValidationError(
                self.error_messages['pin_incorrect']
                )
    """  
    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
                raise forms.ValidationError(
                self.error_messages['pin_incorrect'])
        #if self.old_password:
            #self.user_cache = authenticate(old_password)
            #if self.user_cache is None:
                raise forms.ValidationError(
                self.error_messages['pin_incorrect'])
        return old_password
    """ 
        
    def clean_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return new_password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
        
            

