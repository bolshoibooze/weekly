
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from form_utils.widgets import *
from form_utils.fields import *
from weekly.settings import *
from .models import *



class PhotoForm(forms.ModelForm):
    caption = forms.CharField(
        max_length=140,label='Caption',
        widget=forms.Textarea(attrs={'rows':1,'cols':20}),
    )
    main_photo = forms.ImageField(widget=ImageWidget())
    post = forms.CharField(
        initial='Optional,you can skip this',
        max_length=140,label='Post',
        widget=forms.Textarea(attrs={'rows':6,'cols':20}),
    )
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['main_photo'].widget.attrs['class'] = 'fileUpoad'
        
        
    class Meta(object):
        model = Photo 
        fields = (
        'caption','main_photo'
        )
        
        
        

