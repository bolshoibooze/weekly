from django.forms.util import ValidationError
from django.core import validators

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [ '.gif', '.jpg', '.png','jpeg' ]
    if not ext in valid_extensions:
        raise ValidationError(u'Only images are allowed.')
