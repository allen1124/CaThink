"""ImageX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from ImageX.views import index, register
from images import views as images_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
	url(r'^register/', register, name='register'),
	url(r'^images/$', images_view.image_home, name='images'),
	url(r'^images/create/$', images_view.image_create),
	url(r'^images/detail/$', images_view.image_detail),
	url(r'^images/update/$', images_view.image_update),
	url(r'^images/delete/$', images_view.image_delete)
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
