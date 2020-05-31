from . import views

from django.urls import include, path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='post')
]