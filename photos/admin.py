from django.contrib import admin
from .models import *



class PhotoAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Photo',{
      'fields':('caption','main_photo')
    }),
    ('The Story',{
      'fields':('post',)
    }),
    ('Publish or Ban',{
      'fields':('is_public',)
    }),
    )
    list_display = ('caption','main_photo','is_public','pub_date')
    list_filter=( 'is_public',)
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        
admin.site.register(Photo,PhotoAdmin)
