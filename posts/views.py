from .models import Post

from django.views.generic import ListView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
def signup(request):
    return render(request, 'index.html')

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
        form = UserCreationForm()
    return render(request, 'posts/signup.html', {'form': form})

class IndexView(ListView):
    context_object_name = 'post_list'
    template_name = 'posts/index.html'

    def get_queryset(self):
        return Post.objects.all()

class PostView(DetailView):
    model = Post
    template_name = 'posts/post.html'

