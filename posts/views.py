from django.contrib.auth.views import LoginView

from .models import Post, Community, Profile, Comment, Share

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm, PostCreateForm, CommentForm

# Create your views here.
class UploaderRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().uploader != self.request.user:
            return HttpResponseForbidden()
        return super(UploaderRequiredMixin, self).dispatch(request, *args, **kwargs)


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'posts/signup.html', {'form': form})

class Login(LoginView):
    template_name = 'posts/login.html'


class IndexView(ListView):
    context_object_name = 'post_list'
    template_name = 'posts/index.html'

    def get_queryset(self):
        return Post.objects.all()


class CommunityCreate(LoginRequiredMixin, CreateView):
    model = Community
    fields = ['title', 'slug']
    template_name = 'posts/community_create.html'

class CommunityView(DetailView):
    model = Community
    context_object_name = 'community'
    template_name = 'posts/community.html'


@login_required()
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)

        if form.is_valid():
            post = Post()
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.community = Community.objects.get(slug=request.POST['community'])
            post.uploader = request.user

            post.save()

            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = PostCreateForm()
    return render(request, 'posts/post_create.html', {'form': form})

class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = 'posts/post.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)

        try:
            obj = queryset.get(pk=pk, community__slug=slug)
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

class PostUpdate(LoginRequiredMixin, UploaderRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_update_form.html'
    login_url = reverse_lazy('login')

class PostDelete(LoginRequiredMixin, UploaderRequiredMixin, DeleteView):
    model = Post
    success_url = '/'
    login_url = reverse_lazy('login')


def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'posts/profile.html', {'user': user})

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['image', 'bio', 'location']
    template_name = 'posts/profile_update_form.html'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


@require_http_methods(["POST"])
def comment_create(request, pk):
    comment = Comment()
    comment.post = Post.objects.get(pk=pk)
    comment.content = request.POST['content']
    comment.uploader = request.user
    comment.save()

    return redirect('post', pk)

@require_http_methods(["POST"])
def comment_update(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.content = request.POST['content']
    comment.save()

    return redirect('post', pk)


@require_http_methods(["POST"])
def comment_delete(request, pk, comment_pk):
    Comment.objects.get(pk=comment_pk).delete()

    return redirect('post', pk)

class SearchView(ListView):
    model = Post
    context_object_name = 'search_result'
    template_name = 'posts/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        return Post.objects.filter(title__contains=query)

    def get_extra_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')

        return context


def portfolio(request):
    user = request.user
    shares = Share.objects.filter(owner=user)
    context = {
        "shares": shares,
    }
    return render(request, 'posts/portfolio.html', context)









