from django.urls import path
from .views import products, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('<int:pk>', product, name='product'),
    path('category/<int:index>/', products, name='category'),
    path('category/<int:index>/page/<int:page>/', products, name='page'),
]
