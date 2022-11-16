from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from eauth import views

link = views.usrname

urlpatterns = [
    path('', views.home, name='Home'),
    path('Home', views.home, name='Home'),
    path('Sign-up', views.signup, name='Sign-up'),
    path('Login', views.login, name='Login'),
    path('Contact_Us', views.contact_us, name='Contact Us'),
    path('Login/2-Factor-Authentication', views.two_factor, name='two_factor'),
    path('Profile', views.profile, name='index'),
    path('logout', views.logoutusr, name='logout'),
    path('Profile/Change_Password', views.ch_pass, name='Change_pass'),
    path('Change-password', views.ch_pass_unauthenticated, name='Change-pass')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)