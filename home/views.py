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
from django.db.models import *
from .models import *
from .forms import *
from .utils import *




    

class EditorsPicksListView(MobileListView):
    template_name = 'picks_list.html'
    mobile_template_name = 'picks_list.html'
    queryset = Article.objects.editor_picks()
    paginate_by = 25

class PopularArticles(MobileTemplateView):
    template_name = 'most_read.html' 
    mobile_template_name =  'm_most_read.html'  
     
class MostReadListView(MobileListView):
    template_name = 'most_read_list.html'
    mobile_template_name = 'm_most_read_list.html'
    queryset = Article.objects.most_read()
    paginate_by = 25
    
    def  get_context_data(self,**kwargs):
         context = super(MostReadListView,self).get_context_data(**kwargs)
         context['article_list'] = Article.objects.most_read()
         return context

class ArticleCreateView(ModelCreateView):
    form_class = CreateForm
    mobile_template_name = 'm_create_form.html'
    template_name = 'create_form.html'
    success_url = '/home/stream/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)
        
class UnPublishedArticles(ModelCreateView):
    form_class = ArticleForm
    mobile_template_name = 'm_unpublished_form.html'
    template_name = 'unpublished_form.html'
    success_url = '/home/post_success/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UnPublishedArticles, self).form_valid(form)
        
class UnPublishedListView(MobileListView):
    queryset = Article.objects.filter(is_public=False)
    mobile_template_name = 'm_unpublished_list.html'
    template_name = 'unpublished_list.html'
    context_object_name = 'article'
    paginate_by = 50
    
    def  get_context_data(self,**kwargs):
         context = super(UnPublishedListView,self).get_context_data(**kwargs)
         context['article_list'] = Article.objects.filter(is_public=False)
         return context 
         
class UnPublishedEditView(ModelUpdateView):
    model = Article
    form_class = ArticleForm
    mobile_template_name = 'm_unpublished_form.html'
    template_name = 'unpublished_form.html'
    success_url = '/home/stream/'
    lookup_field = 'slug'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UnPublishedEditView, self).form_valid(form)       
      

class ArticleEditView(ModelUpdateView):
    model = Article
    form_class = ArticleForm
    mobile_template_name = 'm_article_form.html'
    template_name = 'article_form.html'
    success_url = '/home/stream/'
    lookup_field = 'slug'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleEditView, self).form_valid(form)

class PostListView(MobileListView):
    queryset = Article.objects.stream()
    mobile_template_name = 'm_post_list.html'
    template_name = 'post_list.html'
    context_object_name = 'article'
    paginate_by = 25
    
    def  get_context_data(self,**kwargs):
         context = super(PostListView,self).get_context_data(**kwargs)
         context['article_list'] = Article.objects.stream()
         return context
         
class PostDetailView(MobileDetailView):
    mobile_template_name = 'm_post_detail.html'
    template_name = 'post_detail.html'
    context_object_name = 'article'
    queryset = Article.objects.all()

    def get_context_data(self,**kwargs):
        context=super(PostDetailView,self).get_context_data(**kwargs)
        #views = int(self.request.COOKIES.get('views', '0'))
        #views = self.request.session.get('views', 0)
        #self.request.session['views'] = F('views') + 1
        return context
        

class NotificationListView(MobileListView):
    template_name = 'notification_list.html'
    mobile_template_name = 'm_notification_list.html'
    context_object_name = 'notice'
    model = Notice 
    
    def  get_context_data(self,**kwargs):
         context = super(NotificationListView,self).get_context_data( **kwargs)
         context['notice_list'] = Notice.objects.all()
         return context
         
         
def mark_as_read(request):
    #notification = get_object_or_404(Notify,unread=True)
    q_dict = {'unread__exact':'True',}
    notification = Notice.objects.filter(**q_dict).update(unread=False)
    #notification.mark_as_read()
    return redirect('all')
    
def mark_all_as_read(request):
    request.user.home.mark_all_as_read()
    return redirect('all')

    

    
class SectionListView(ModelListView):
    model = Section
    #queryset = Post.objects.all().order_by('section') 
    mobile_template_name = 'm_section_list.html'
    template_name = 'section_list.html'
 

class ArticleSections(ModelListView):
    pass      

    
class AuthorListView(ModelListView):
    #queryset = Author.objects.all().order_by('-is_editor','-is_a_fellow')
    mobile_template_name = 'm_author_list.html'
    template_name = 'author_list.html'
    
class AuthorDetailView(ModelDetailView):
    model = None
    mobile_template_name = 'm_author_detail.html'
    template_name = 'author_detail.html'
 
class CreateProfile(ModelCreateView):
    model = None
    fields = ('bio','mug_shot')
    mobile_template_name = 'm_author_form.html'
    template_name = 'author_form.html'
    success_url = '/home/authors/' 
      
class EditView(ModelUpdateView):
    model = None
    fields = ('bio','mug_shot')
    mobile_template_name = 'm_author_form.html'
    template_name = 'author_form.html'
    
"""   
def list_sections(request,pk,template= 'section_articles.html'):
   
    section = get_object_or_404(Section,pk__iexact=pk)
    data = {'object': section,}

    variables = RequestContext(request, context)
    response = render_to_response(template, variables)

    return response
"""   

def _sections(request,template = 'section_articles_list.html'):
    
    sections = Section.objects.all()
    post = Post.objects.filter(section__in=sections)
    #data = {'object_list': post.object_list,}
    return render_to_response(template,  RequestContext(request))
    
    """
    return object_list(
    request,template,data,
    queryset = post.order_by('-section','-pub_date','-title'),
    
    )
    """
    
def list_sections(request,template="sections.html"):
    """Listing of articles in a section."""
    posts = Post.objects.all()
    name = Section.objects.all()
    data = {'posts':posts,'name':name}
    variables = RequestContext(request)
    response = render_to_response(template, variables)
    return response

class QuickListView(ModelListView):
    queryset = Article.objects.all().order_by('-section') #doesn't work 
    mobile_template_name = 'm_quick_list.html'
    template_name = 'quick_list.html'
    

class UserBookmarks(MobileListView):
    model = Bookmark
    mobile_template_name = 'user_bookmarks_list.html'
    template_name = 'm_user_bookmarks_list.html'
    context_object_name = 'bookmark'
    
    def  get_context_data(self,**kwargs):
         context = super(UserBookmarks,self).get_context_data( **kwargs)
         context['bookmark_list'] = Bookmark.objects.filter(user__pk=self.request.user.id)
         return context
         
         
class UserBookmarksView(MobileTemplateView):
    mobile_template_name = 'user_bookmarks_list.html'
    template_name = 'm_user_bookmarks_list.html'
      
@login_required
def user_bookmarks(request):
    return object_list(
        request,
        queryset=Bookmark.objects.filter(user__pk=request.user.id),
        template_name='user_bookmarks.html',
        paginate_by=20)
            
@login_required
def add_bookmark(request, slug):
    # TODO: this should probably be a POST action
    article = get_object_or_404(Article, slug=slug)
    try:
        Bookmark.objects.get(user=request.user,article=article)
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(user=request.user,article=article)
    return redirect('/home/stream/')
    


@login_required
def delete_bookmark(request, slug):
    bookmark = get_object_or_404(
    Bookmark,article__pk=slug,user=request.user
    )
    if request.method == 'POST':
        bookmark.delete()
        return redirect('article_user_bookmarks')
    else:
        return render(request, 'confirm_bookmark_delete.html',
                      {'article': bookmark.article})
        




"""
install Haystack
_____________________
def search(request):
    query = request.GET.get('q')
    article_qs = Article.objects.none()
    if query:
        article_qs = Article.objects.filter(
            Q(title__icontains=query) |
            Q(post__in=[query]) | 
            Q(author__username__iexact=query)
        ).distinct().order_by( '-pub_date')

    return snippet_list(
        request,
        queryset=article_qs,
        template_name='search.html',
        extra_context={'query': query},
    )
    
def autocomplete(request):
    q = request.GET.get('q', '')
    results = []
    if len(q) > 2:
        sqs = SearchQuerySet()
        result_set = sqs.filter(title=q)[:10]
        for obj in result_set:
            results.append({
                'title': obj.title,
                'author': obj.author,
                'url': obj.url
            })
    return HttpResponse(json.dumps(results), mimetype='application/json')
"""
