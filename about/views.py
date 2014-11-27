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
#from .utils import *



class AboutListView(ModelListView):
    model = About
    fields = ('title','image','post')
    mobile_template_name = 'm_about_list.html'
    template_name = 'about_list.html'

class StyleGuideListView(ModelListView):
    model = StyleGuide
    fields = ('title','image','post','date')
    mobile_template_name = 'm_guide_list.html'
    template_name = 'guide_list.html'
    
    
class StyleDetailView(ModelDetailView):
    model = StyleGuide
    fields = ('title','image','post','date')
    mobile_template_name = 'm_guide_detail.html'
    template_name = 'guide_detail.html'
    
class TermsListView(ModelListView):
    model = Terms
    fields = ('title','image','post','date')
    mobile_template_name = 'm_terms_list.html'
    template_name = 'terms_list.html'
    
    
class FaqListView(ModelListView):
    model = Faq
    fields = ('qstn','answer','date')
    mobile_template_name = 'm_faq_list.html'
    template_name = 'faq_list.html'  
    
    
    
      
