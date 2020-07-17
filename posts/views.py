from django.contrib.auth.views import LoginView

from .models import Post, Profile

from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from .forms import SignUpForm

# Create your views here.
def signup(request):
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

class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'posts/profile.html', {'user': user})
