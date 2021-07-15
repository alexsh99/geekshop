from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from .models import ShopUser


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {'title': title, 'login_form': login_form}
    return render(request, 'login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    title = 'редактирование'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('authapp:login'))
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {'title': title, 'edit_form': edit_form, 'profile_form': profile_form}
    return render(request, 'edit.html', context=context)


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_link(user):
                return render(request, 'reg_complete.html',
                              {'message': 'На ваш электронный адрес отправлена ссылка для активации'})
            else:
                return render(request, 'reg_complete.html',
                              {'message': 'Не удалось отправить ссылку для активации'})
    else:
        register_form = ShopUserRegisterForm()
    content = {'title': title, 'register_form': register_form}
    return render(request, 'register.html', context=content)


def send_verify_link(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    message = f'You link for account activation: {settings.DOMAIN_NAME}{verify_link}'
    subject = 'Account verify'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.activation_key = ''
        user.is_active = True
        user.activation_key_created = None
        user.save()
        auth.login(request, user)
    return render(request, 'verify.html')
