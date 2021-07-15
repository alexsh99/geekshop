import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('user/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('user/read/', adminapp.UsersListView.as_view(), name='users'),
    path('user/update/<int:pk>/', adminapp.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('categories/list/', adminapp.CategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/list/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/create/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
]
