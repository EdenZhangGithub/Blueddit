from . import views

from django.urls import include, path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='post')
]