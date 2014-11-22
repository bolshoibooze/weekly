from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *
from .forms import *





class ExtendedUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    
    list_display = ('full_name','can_write',)
    list_filter = ('can_write',)
    search_fields = ('full_name',)
    
    
    
admin.site.register(ExtendedUser,ExtendedUserAdmin)


#admin.site.register(CustomUser)

# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
