"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from mainapp import urls
from . import settings
from .views import main, contact

app_name = 'geekshop'

urlpatterns = [
    path('', main, name='index'),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contacts'),
    path('products/', include(urls)),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin_staff/', include('adminapp.urls', namespace='admin_staff')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)