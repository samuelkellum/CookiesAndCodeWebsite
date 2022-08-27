from django.contrib import admin
from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

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
    path('profile/', views.profile, name='profile'),
    #path('change-password/', auth_views.PasswordChangeView.as_view(template_name='main/change_password.html', success_url = '/'), name='change_password'),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='main/password_reset_form.html',
             subject_template_name='main/password_reset_subject.txt',
             email_template_name='main/password_reset_email.html',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='main/password_reset_done.html',

         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
