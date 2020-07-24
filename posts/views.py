from django.contrib.auth.views import LoginView

from .models import Post, Community, Profile

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from .forms import SignUpForm, PostCreateForm

# Create your views here.
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

            return HttpResponseRedirect(reverse('post', args=(post.pk,)))
    else:
        form = PostCreateForm()
    return render(request, 'posts/post_create.html', {'form': form})

class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'posts/post_update_form.html'

class PostDelete(DeleteView):
    model = Post
    success_url = '/'


def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'posts/profile.html', {'user': user})

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['image', 'bio', 'location']
    template_name = 'posts/profile_update_form.html'

    def get_object(self, queryset=None):
        return Profile  .objects.get(user=self.request.user)











