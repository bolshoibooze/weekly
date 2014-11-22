from django.contrib import admin
from .models import *



class AboutAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Title',{
      'fields':('title',)
    }),
    ('Background Image',{
      'fields':('image',)
    }),
    ('About',{
      'fields':('post',)
    }),
    )
    list_display = ('title','date')
    
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(About,AboutAdmin)



class StyleGuideAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Title',{
      'fields':('title',)
    }),
    ('Background Image',{
      'fields':('image',)
    }),
    ('Style Guide',{
      'fields':('post',)
    }),
    )
    list_display = ('title','date')
    list_filter = ('date',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(StyleGuide,StyleGuideAdmin)
    
    
    
    
class TermsAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Title',{
      'fields':('title',)
    }),
    ('Background Image',{
      'fields':('image',)
    }),
    ('Terms',{
      'fields':('post',)
    }),
    )
    list_display = ('title','date')
    list_filter = ('date',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(Terms,TermsAdmin)
    
    
class FaqAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Question',{
      'fields':('qstn',)
    }),
    
    ('Answer',{
      'fields':('answer',)
    }),
    )
    list_display = ('qstn','date',)
    list_filter = ('date',)
    exclude = ('user',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()
        
admin.site.register(Faq,FaqAdmin)
            

    
