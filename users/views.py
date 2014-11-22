
import urlparse
from django.shortcuts import *
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth import  *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
#from django.contrib.auth.utils import UNUSABLE_PASSWORD
from django.contrib.auth.forms import *
from django.contrib.formtools.preview import FormPreview
from django.core.urlresolvers import *
from django.views.generic.edit import(
FormView,DeleteView,CreateView,UpdateView
)

from django.views.generic.base import(
TemplateView,RedirectView
)
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages

from .forms import *
from .models import *
from .utils import *
from .models import *
from weekly.settings import *
from ua_detector.views import *
from ua_detector.generic_views import *
from ua_detector.model_views import *



class LoginView(MobileFormView):
    template_name = 'login_form.html'
    mobile_template_name = 'm_login_form.html'
    form_class = MyAuthForm
    success_url = '/home/stream/' 
    #success_url = '/accounts/home/' 
    redirect_field_name = REDIRECT_FIELD_NAME
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)
            
            
def logout_view(request):

    logout(request)
    request.session.flush()
    request.user = AnonymousUser

    return HttpResponseRedirect('/users/login/') 
                
class MyLogoutView(RedirectView):
    permanent = False
    url = '/users/login/'
    query_string = False 
            
            
class LogoutView(MobileTemplateView):
    template_name= 'login_form.html'
    mobile_template_name='m_login_form.html'
    redirect_url = '/users/login/'
    redirect_field_name = "next"
    
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        context = kwargs
        redirect_field_name = self.get_redirect_field_name()
        context.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.REQUEST.get(redirect_field_name),
            })
        return context

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.LOGIN_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)
        


        

        

class StepOneView(MobileFormView):
    #model = CustomUser
    template_name = 'reg_form.html'
    mobile_template_name = 'm_reg_form.html'
    form_class = UserCreationForm
    #success_url = '/wallet/activate/'
    success_url = '/users/welcome/'
    
    def form_valid(self, form):
        form.save()
        return super(StepOneView, self).form_valid(form)
        

        
class RegistrationView(CustomCreateView):
    model = ExtendedUser
    form_class = UserCreationForm
    template_name = 'reg_form.html'
    mobile_template_name = 'm_reg_form.html'
    success_url = reverse_lazy('redirect')
    
    def form_valid(self, form):
        form.save()
        return super(RegistrationView, self).form_valid(form)
    
 


        
        
class RegSuccessView(MobileTemplateView):
    template_name = 'reg_success.html'
    mobile_template_name='reg_m_success.html'
    
    
class ChangePasswordFormView(MobileFormView):
    template_name = 'password_form.html'
    mobile_template_name = 'password_m_form.html'
    form_class = MyPasswordChangeForm
    success_url = ''
    
    def form_valid(self, form):
        self.instance.user = request.user
        form.save()
        messages.info(self.request,
            ("Password successfully changed.")
            )
        return super(ChangePasswordFormView, self).form_valid(form)
        
class PinChangeSuccessView(MobileTemplateView):
    template_name ='pin_change_success.html'
    mobile_template_name= 'pin_change_m_success.html'
        
 
#this should be an edit view on User model       
class FreezeAccountFormView(MobileFormView):
    template_name = 'freeze_form.html'
    mobile_template_name = 'freeze_form.xhtml'
    form_class = FreezeAccountForm
    get_success_url = ''
    
    def get_object(self):
        return get_object_or_404(User, pk=request.session['user_id'])
        
    def form_valid(self, form):
        form.save()
        return super(FreezeAccountFormView, self).form_valid(form)
        
        
class FreezeAccountView(ModelUpdateView):
    model = User
    fields = ('password','is_active')
    template_name = 'freeze_form.html'
    mobile_template_name = 'freeze_m_form.html'
    get_success_url = reverse_lazy('login')      
        

        
        
class ProfileTemplateView(MobileTemplateView):
    template_name = 'profile.html'
    mobile_template_name = 'm_profile.html'
    
    def get_object(self):
        """Return the User object

        NoOp, here, we set the self.object alread during dispatch"""
        return self.object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """override dispatch with a csrf_excempt decorator"""
        #check authentication. TODO factor out:
        #raise Exception(str(dir(request.user)))
        self.object = request.user
        if kwargs.has_key('username') and \
                self.object.username != kwargs['username']:
            messages.warning(request, "You can only view your own profile "
                             "pages!")
            profile_page = '/users/myprofile/'
            return redirect(profile_page)
        return super(ProfileTemplateView, self).dispatch(request, *args, **kwargs)
    
class UserProfileDetailView(ModelDetailView):
    model = User
    slug_field = "username"
    template_name = 'profile_detail.html'
    mobile_template_name = 'm_profile_detail.html'
    context_object_name="u"

    def get_object(self):
        """Return the User object

        NoOp, here, we set the self.object alread during dispatch"""
        return self.object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """override dispatch with a csrf_excempt decorator"""
        #check authentication. TODO factor out:
        #raise Exception(str(dir(request.user)))
        self.object = request.user
        if kwargs.has_key('username') and \
                self.object.username != kwargs['username']:
            messages.warning(request, "You can only view your own profile "
                             "pages!")
            profile_page = self.object.get_profile().get_absolute_url()
            return redirect(profile_page)
        return super(UserProfileDetailView, self).dispatch(
            request, *args, **kwargs)
    
    
class EditProfileView(ModelUpdateView):
    model = ExtendedUser
    form_class = EditProfileForm
    #fields = ('photo','bio','username')
    template_name = 'profile_edit_form.html'
    mobile_template_name = 'profile_edit_m_form.html'
    success_url = reverse_lazy('myprofile')
 
