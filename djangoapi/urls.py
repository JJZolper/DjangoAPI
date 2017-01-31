"""djangoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from djangoapi import views as djapi_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', djapi_views.schema_view, name='schema'),

    url(r'^register/$', djapi_views.register, name='register'),
    url(r'^login/$', djapi_views.login, name='login'),
    url(r'^reddit/$', djapi_views.reddit, name='reddit'),
    url(r'^favorite/$', djapi_views.favorite, name='favorite'),
    url(r'^favorites/$', djapi_views.favorites, name='favorites'),
]