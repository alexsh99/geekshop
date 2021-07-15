from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Пользователи

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'админка/пользователи'
        return context


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'пользователи/создание'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    object = ''
    template_name = 'adminapp/user_update.html'
    # fields = ['username', 'first_name', 'last_name', 'age', 'avatar', 'is_active']
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('adminapp:user_update', args=[self.object.id])


class UserDeleteView(DeleteView):
    model = ShopUser
    object = ''
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user_to_delete'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'пользователи/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Категории

class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'админка/категории'
        return context


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'категории/создание'
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    object = ''
    template_name = 'adminapp/category_update.html'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('adminapp:category_update', args=[self.object.id])


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    object = ''
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'cat_to_delete'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'категории/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# Товары/Продукты

class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'
    category = None

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        self.category = self.kwargs.get('pk')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(category__id=self.category).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'админка/продукт'
        context["category"] = self.category
        return context


class ProductUpdateView(UpdateView):
    model = Product
    object = ''
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        self.object = self.get_object()
        context["category"] = self.object.category
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('adminapp:product_update', args=[self.object.id])


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'продукт/создание'
        context["category"] = {'id': self.kwargs.get('pk')}
        return context

    def get_success_url(self):
        return reverse_lazy('adminapp:products', args=[self.kwargs.get('pk')])


class ProductDeleteView(DeleteView):
    model = Product
    object = ''
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product_to_delete'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'продукт/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('adminapp:products', args=[self.object.category.id])
