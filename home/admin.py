from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import *

"""
class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False

class AuthorAdmin(UserAdmin):
    inlines=(AuthorInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), AuthorAdmin)

class WriterAdmin(RelatedAdmin):
    fieldsets = (
    ('Bio',{
       'fields':('mug_shot','bio')
    }),
    )
    list_display = ('user__username','user__first_name','user__last_name'
                   'can_write','is_a_fellow','is_editor')
    list_filter = ('can_write','is_editor')
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(Writer,WriterAdmin)
 """   

class SectionAdmin(admin.ModelAdmin):
    fieldsets =(
    ('Details',{
      'fields':('name','about','is_approved')
    }),
   
    
    )
    list_display = ('name','is_approved','date')
    list_filter = ('date',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(Section,SectionAdmin)



class ArticleAdmin(admin.ModelAdmin):
    fieldsets =(
    ('Title',{
      'fields':('title',)
    }),
    ('Section',{
      'fields':('section',)
    }),
    ('Photo',{
      'fields':('main_photo',)
    }),
    ('Overview',{
      'fields':('overview',)
    }),
    ('Post',{
      'fields':('post',)
    }),
    ('Adminstrative',{
      'fields':('editors_pick','is_public',)
    })
    )
    list_display = ('title','reading_time','views','is_public','pub_date')
    list_filter = ('is_public','pub_date')
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        
admin.site.register(Article,ArticleAdmin)

