from django.contrib import admin
from . import views
from django.urls import path

app_name = 'main'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('recos/', views.event_recos, name='recos'),
    path('home/', views.index, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('practice/', views.leetcode, name='practice'),
    path('members/', views.members, name='members'),
    path('profile/', views.profile, name='profile')
]
