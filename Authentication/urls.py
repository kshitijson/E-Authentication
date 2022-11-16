"""Authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eauth import views

link = views.usrname

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eauth.urls')),
    path('Home', include('eauth.urls')),
    path('Login', include('eauth.urls')),
    path('Sign-up', include('eauth.urls')),
    path('Contact_Us', include('eauth.urls')),
    path('Login/2-Factor-Authentication', include('eauth.urls')),
    path('Profile', include('eauth.urls')),
    path('logout', include('eauth.urls')),
    path('Profile/Change_password', include("eauth.urls")),
    path('Change-password', include("eauth.urls"))
]
