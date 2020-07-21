from . import views

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Login.as_view(), name='login'),
    path('accounts/profile/<username>/', views.profile, name='profile'),
    path('accounts/update-profile/', views.UpdateProfile.as_view(), name='update_profile'),
    path('posts/create/', views.postcreate, name='create_post'),
    path('posts/<int:pk>/', views.PostView.as_view(), name='post'),
#    path('posts/update-post/', views.UpdatePost.as_view(), name='update_post')
    path('posts/update-post/<int:pk>/', views.UpdatePost.as_view(), name='update_post')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

