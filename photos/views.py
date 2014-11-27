from django.shortcuts import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy,resolve
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from weekly.settings import *
from ua_detector.views import *
from ua_detector.generic_views import *
from ua_detector.model_views import *
from .models import *
from .forms import *
from .utils import *


class PostPhotoView(ModelCreateView):
    form_class = PhotoForm
    mobile_template_name = 'm_photo_form.html'
    template_name = 'photo_form.html'
    success_url = '/photos/posted/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostPhotoView, self).form_valid(form)
        
class PhotoSuccessView(MobileTemplateView):
    mobile_template_name = 'm_photo_posted.html'
    template_name= 'photo_posted.html'
        
class View(ModelListView):
    model = Photo
    mobile_template_name = 'photo_list.html'
    template_name = 'm_photo_list.html'

class PhotoListView(MobileListView):
    model = Photo
    mobile_template_name = 'm_photo_list.html'
    template_name = 'photo_list.html'
    context_object_name = 'photo'
    
    def  get_context_data(self,**kwargs):
         context = super(PhotoListView,self).get_context_data( **kwargs)
         context['photo_list'] = Photo.objects.all()
         return context
                 
        
        
class PhotoDetailView(MobileDetailView):
    mobile_template_name = 'm_photo_detail.html'
    template_name = 'photo_detail.html'
    context_object_name = 'photo'
    queryset = Photo.objects.all()

    def get_context_data(self,**kwargs):
        context=super(PhotoDetailView,self).get_context_data(**kwargs)
        return context
