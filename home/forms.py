
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from form_utils.widgets import *
from form_utils.fields import *
from weekly.settings import *
from .widgets import *
from .models import *

        
class ArticleForm(forms.ModelForm):
    post = forms.CharField(
        max_length=5000,label='Post',
        widget=forms.Textarea(attrs={'rows':60,'cols':20}),
        initial = mark_safe(
        "Title: <h1> My Title</h1> | Quotes: <blockquote> My Quote </blockquote>"
        )
        
    )
    main_photo = forms.ImageField(widget=ImageWidget())
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['section'].widget.attrs['class'] = 'alt-choices'
        self.fields['main_photo'].widget.attrs['class'] = 'fileUpoad'
        
        
    class Meta(object):
        model = Article
        fields = (
        'title','section',
        'main_photo','post','overview',
        'is_public','editors_pick'
        )
       
        
        
class CreateForm(forms.ModelForm):
    post = forms.CharField(
        max_length=5000,label='Post',
        #widget=forms.Textarea(attrs={'rows':60,'cols':20}),
        widget=AutoResizeTextarea(attrs={'rows':30,'cols':20}),
        initial = mark_safe("Title: <h1> My Title</h1>")
        
    )
    main_photo = forms.ImageField(widget=ImageWidget())
    
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['section'].widget.attrs['class'] = 'alt-choices'
        self.fields['main_photo'].widget.attrs['class'] = 'fileUpoad'
        
        
        
    class Meta(object):
        model = Article
        fields = (
        'title','section',
        'main_photo','post','overview',
        'is_public'
        
        )
       
        
        

